import click
from click import echo, secho
import os
import json
from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair, CryptoKeypair
import requests
import ipfsapi
from encryption import *
bdb = BigchainDB(
    'https://test.bigchaindb.com',
    headers={'app_id': 'd5596f54',
             'app_key': '6f108c571fcb25c4d34056bede9d246f'})
credentials_path = os.path.expanduser('~/.medblocks')
version = '0.01'

@click.group()
@click.version_option(version, message="MedBlocks v0.01")
def main():
    """
    \b
    ███╗   ███╗███████╗██████╗ ██████╗ ██╗      ██████╗  ██████╗██╗  ██╗███████╗
    ████╗ ████║██╔════╝██╔══██╗██╔══██╗██║     ██╔═══██╗██╔════╝██║ ██╔╝██╔════╝
    ██╔████╔██║█████╗  ██║  ██║██████╔╝██║     ██║   ██║██║     █████╔╝ ███████╗
    ██║╚██╔╝██║██╔══╝  ██║  ██║██╔══██╗██║     ██║   ██║██║     ██╔═██╗ ╚════██║
    ██║ ╚═╝ ██║███████╗██████╔╝██████╔╝███████╗╚██████╔╝╚██████╗██║  ██╗███████║
    ╚═╝     ╚═╝╚══════╝╚═════╝ ╚═════╝ ╚══════╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝╚══════╝ 
    Store your medical records securely                                         
    """
    


def dump_user(user):
    """Converts user dictionary to json string"""
    bigchain_keys = user['bigchain']
    user['bigchain'] = {'private_key':bigchain_keys.private_key, 'public_key':bigchain_keys.public_key}
    # Serialize rsa 
    rsa_key = user['rsa']
    user['rsa'] = {'private_key':rsa_key.exportKey().decode('utf-8'),'public_key':rsa_key.publickey().exportKey().decode('utf-8')}
    echo("[+] Serializing to JSON")
    user = json.dumps(user)
    return user

def load_user(string):
    """Loads json string into user dictionary"""
    user = json.loads(string)
    user['rsa'] = RSA.importKey(user['rsa']['private_key'])
    user['bigchain'] = CryptoKeypair(user['bigchain']['private_key'],user['bigchain']['public_key'])
    return user

def load(file=credentials_path):
    """Loads user dictionary from credentials_path"""
    try:
        with open(file, 'r') as f:
            user = load_user(f.read())
    except FileNotFoundError:
        echo("[-] No user logged in. Please login.")
        click.secho("Hint: Use 'createuser' to create a user json file", fg='green')
        exit(1)
    return user

def register_on_blockchain(string):
    user_dict = json.loads(string)
    data = {
        'schema':'medblocks.user',
        'version':'v0.01',
        'rsa':user_dict['rsa']['public_key'],
        'bigchain':user_dict['bigchain']['public_key'],
        'phone':user_dict['phone'],
        'name':user_dict['name']
    }
    echo("[+] Preparing CREATE transaction with {}...".format(str(data)[:10]))
    tx = bdb.transactions.prepare(
    operation='CREATE',
    signers=user_dict['bigchain']['public_key'],
    asset={'data': data})

    echo("[+] Signing with private key")
    signed_tx = bdb.transactions.fulfill(
    tx,
    private_keys=user_dict['bigchain']['private_key']
    )
    echo("[+] Sending to the Blockchain")
    sent = bdb.transactions.send(signed_tx)
    echo("[+] Sent transaction {}".format(sent))
    return sent
    # mobile => address, rsa_key
    # address => [{ ipfs hash, cipher, emergency_cipher}]

current_user = load()


def filter(l, key, value):
    new_list = []
    for instance in l:
        data = instance.get('data')
        if data.get(key) == value:
            new_list.append(instance)
    return new_list

def version_filter(l):
    return filter(l, 'version','v'+version)
    
    
class Patient(object):
    def __init__(self, mobile=None, public_key=None):
        self.registered = None
        self.records = None
        if mobile is not None:
            self.bio = self.get_bio_from_mobile(mobile)
        if public_key is not None:
            self.bio = self.get_bio_from_public_key(public_key)
        self.medblocks = []
        self.get_medblocks()
        
    def get_bio_from_mobile(self, mobile):
        records = bdb.assets.get(search=mobile)
        records = filter(records, 'schema','medblocks.user')
        if len(records) == 1:
            echo("[+] Found user with mobile number!")
            self.registered = True
            return records[0]['data']
        if len(records) > 1:
            secho("[o] Got more than one record for the same version. Last registery will be taken",fg='yellow')
            self.registered = True
            return records[-1]['data']
        
        secho("[-] No user with that phone number registered", fg='red')
        self.registered = False
        return

    def get_bio_from_public_key(self, public_key):
        self.records = bdb.assets.get(search=public_key)
        registers = filter(self.records, 'schema','medblocks.user')

        if len(registers) == 1:
            self.registered = True
            return registers[0].get('data')

        if len(registers) > 1:
            secho("[o] Got more than one record for the same version. Last registery will be taken",fg='yellow')
            self.registered = True
            return registers[-1].get('data')
        
        secho("[-] No user with that public key registered", fg='red')
        self.registered = False
        return

    def get_medblocks(self):
        if self.records is None:
            self.records = bdb.assets.get(search=self.bio['bigchain'])
    
        for record in self.records:
            if record.get('data').get('schema') == 'medblocks.medblock':
                self.medblocks.append(record)

        self.medblocks = version_filter(self.medblocks)
    
    def write_medblock(self, ipfs_hash, encrypted_key, type=None):
        data = {
        'schema':'medblocks.medblock',
        'version':'v0.01',
        'type': type,
        'ipfs_hash': ipfs_hash,
        'patient': self.bio['bigchain']
        }
        echo("[+] Preparing CREATE transaction with {}...".format(str(data)[:10]))
        tx = bdb.transactions.prepare(
        operation='CREATE',
        signers=current_user['bigchain'].public_key,
        asset={'data': data})
        
        echo("[+] Signing with private key")
        signed_tx = bdb.transactions.fulfill(
        tx,
        private_keys=current_user['bigchain'].private_key
        )
        echo("[+] Creating MedBlock on the Blockchain")
        sent = bdb.transactions.send(signed_tx)
        echo("[+] Created! {}".format(sent))
        self.transfer_medblock(sent, encrypted_key)
    
    def transfer_medblock(self, tx, encrypted_key):
        
        echo("[+] Transfering MedBlock to patient: {}".format(self.bio['bigchain']))
        metadata = {
            self.bio['bigchain']: encrypted_key
        }
        output = tx['outputs'][0]
        transfer_input = {
            'fulfillment': output['condition']['details'],
            'fulfills': {
                'output_index': 0,
                'transaction_id': tx['id'],},
            'owners_before': output['public_keys'],}
        transfer_asset = {
            'id':tx['id'],
        }
        echo("[+] Preparing TRANSFER transaction with encrypted key")
        prepared_tx = bdb.transaction.prepare(
            operation='TRANSFER',
            asset=transfer_asset,
            inputs=transfer_input,
            recipients=self.bio['bigchain'],
            metadata=metadata
        )
        echo("[+] Signing transaction")
        signed = bdb.transaction.fulfill(
            prepared_tx,
            private_keys=current_user['bigchain'].private_key
        )
        echo("[+] Sending on the blockchain")
        tx = bdb.transactions.send(signed)
        echo(tx)
        secho("[+] Transaction sent!", fg='green')


def ipfs_connect():
    try:
        api = ipfsapi.connect('127.0.0.1', 5001)
        secho("[+] Connected to local IPFS node", fg='green')
    except ipfsapi.exceptions.ConnectionError:
        secho("[o] Local IPFS daemon not running. Connecting to ipfs.infura.io node...", fg='yellow')
        api = ipfsapi.connect('https://ipfs.infura.io', 5001)
    return api

def give_permission(address, medblock_index):
    pass

@main.command()
@click.option('--output','-o', help="Output file with credentials", default='user.json')
@click.option('--name','-n',prompt="Name of patient")
@click.option('--phone','-p',prompt="Phone number")
def createuser(name, phone, output):
    """Generate a user file data"""
    user = {
        'name':name,
        'phone':phone
    }
    echo("[+] Writing Name and Phone")
    echo("[+] Generating BigChainDB keypair")
    bigchain_keys = generate_keypair()
    user['bigchain'] = bigchain_keys
    random_generator = Random.new().read
    rsa_key = RSA.generate(1024, random_generator)
    echo("[+] Generating RSA keypair")
    user['rsa'] = rsa_key
    st = dump_user(user)
    click.secho("Writing private key data to a json file. Please be sure to save it securely. You will need it to log in later.", fg='yellow')
    click.pause()
    echo("[+] Writing file to disk as: {}".format(output))
    with open(output,'w') as f:
        f.write(st)

@main.command()
def register():
    """Register current user on the blockchain"""
    user = load()
    register_on_blockchain(dump_user(user))

@main.command()
@click.argument('login', type=click.Path(exists=True))
@click.pass_context
def login(ctx, login):
    """Log in with a user file"""
    user = load(login)
    if click.confirm(text="This will overwrite all previous user data. Are you sure?"):
        echo("[+] Writing to .medblocks")
        with open(credentials_path,'w') as f:
            f.write(dump_user(user))
    ctx.invoke(info)

@main.command()
def info():
    """Get info about current user"""
    echo("[+] Loading user from .medblocks")
    user = load()
    echo('Name: {}'.format(user['name']))
    echo('Phone: {}'.format(user['phone']))
    echo('RSA public key: ')
    secho(user['rsa'].publickey().exportKey().decode(), fg='green')
    echo('Bigchain public key: {}'.format(user['bigchain'].public_key))
    # Check registered on BigChainDB
    
    echo("[+] Loading all records of user on the blockchain")
    publicpatient = Patient(public_key=user['bigchain'].public_key)
    if publicpatient.registered:
        secho('Registered on the Blockchain!', fg='green')
    else:
        secho("Not yet registered on the Blockchain. Register with the 'register' command",fg='yellow')
    echo("MedBlocks: {}".format(len(publicpatient.medblocks)))

@main.command()

@click.option('--to','-t', help="Mobile number of the patient")
@click.option('--emergency','-e', help="IS EMERGENCY DATA", is_flag=True)
@click.argument('file',type=click.Path(exists=True))
def add(file, to, emergency):
    echo("[+] Fetching user data from the blockchain")
    patient = Patient(mobile=to)
    public_rsa = patient.bio['rsa']
    echo("[+] Got Public RSA key")
    secho(public_rsa, fg='green')
    public_rsa = RSA.importKey(public_rsa)
    echo("[+] Generating random AES key")
    key = generate_random_aes_key()
    echo("[+] Encrypting data...")
    enc = encrypt_file(file, key)
    secho("[+] Writing encrypted data to IPFS", fg='yellow')
    api = ipfs_connect()
    ipfs_hash = api.add_bytes(enc)
    secho("[+] Data written to IPFS: {}".format(ipfs_hash), fg='green')
    echo("[+] Encrypting AES key with RSA public key")
    encrypted_key = encrypt_rsa(key, public_rsa)
    # Create MedBlock
    click.echo([ipfs_hash, encrypted_key, patient.bio['bigchain'], 'schema'])

if __name__ == "__main__":
    main()

