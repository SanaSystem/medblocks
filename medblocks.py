import click
from click import echo, secho
from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
import base64
import os
import json
import web3
import requests

w3 = web3.Web3(web3.HTTPProvider('https://ropsten.infura.io/JpLB58GjoxPYInfTNHf0')) 
credentials_path = os.path.expanduser('~/.medblocks')

@click.group()
@click.version_option('0.01', message="MedBlocks v0.01")
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
    
def encrypt_rsa(data, public_key):
    handler = PKCS1_OAEP.new(public_key)
    return base64.encodebytes(handler.encrypt(data))
def decrypt_rsa(data, private_key):
    handler = PKCS1_OAEP.new(private_key)
    return handler.decrypt(base64.decodebytes(data))

def pad(s):
    return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

def encrypt(message, key, key_size=256):
    message = pad(message)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return iv + cipher.encrypt(message)

def decrypt(ciphertext, key):
    iv = ciphertext[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext[AES.block_size:])
    return plaintext.rstrip(b"\0")

def encrypt_file(file_name, key):
    with open(file_name, 'rb') as fo:
        plaintext = fo.read()
    enc = encrypt(plaintext, key)
    with open(file_name + ".enc", 'wb') as fo:
        fo.write(enc)

def decrypt_file(file_name, key):
    with open(file_name, 'rb') as fo:
        ciphertext = fo.read()
    dec = decrypt(ciphertext, key)
    with open(file_name[:-4], 'wb') as fo:
        fo.write(dec)

def generate_random_aes_key():
    return os.urandom(32)

def dump_user(user):
    #Serialize ethereum account
    ethereum_keys = user['ethereum']
    user['ethereum'] = {'private_key':ethereum_keys.privateKey.hex(), 'public_key':ethereum_keys.address}
    # Serialize rsa 
    rsa_key = user['rsa']
    user['rsa'] = {'private_key':rsa_key.exportKey().decode('utf-8'),'public_key':rsa_key.publickey().exportKey().decode('utf-8')}
    echo("[+] Serializing to JSON")
    user = json.dumps(user)
    return user

def load_user(string):
    user = json.loads(string)
    user['rsa'] = RSA.importKey(user['rsa']['private_key'])
    user['ethereum'] = w3.eth.account.privateKeyToAccount(user['ethereum']['private_key'])
    return user

def load(file=credentials_path):
    try:
        with open(file, 'r') as f:
            user = load_user(f.read())
    except FileNotFoundError:
        echo("[-] No user logged in. Please login.")
        click.secho("Hint: Use 'createuser' to create a user json file", fg='green')
        exit(1)
    return user

def register_on_blockchain(user):
    rsa_public_key = user['rsa']['public_key']
    ethereum_address = user['ethereum']['public_key']
    # mobile => address, rsa_key
    # address => [{ ipfs hash, cipher, emergency_cipher}]


def write_medblock(data, schema, mobile, is_emergency=False):
    # Get ethereum address for mobile number

    # Get rsa public key for ethereum address

    # Generate random aes cipher

    # Encrypt data with aes cipher

    # Encrypt cipher with rsa key

    # if is_emergency:
        # Encrypt cipher with rsa key of emregency key

    # write {'data':encrypted data, 'schema':schema} to ipfs and return hash

    # return ipfs hash, encrypted cipher
    pass
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
    echo("[+] Generating Ethereum keypair")
    ethereum_keys = w3.eth.account.create()
    user['ethereum'] = ethereum_keys
    random_generator = Random.new().read
    rsa_key = RSA.generate(1024, random_generator)
    echo("[+] Generating RSA keypair")
    user['rsa'] = rsa_key
    st = dump_user(user)
    click.secho("Writing private key data to a json file. Please be sure to save it securely. You will need it to log in later.", fg='red')
    click.pause()
    echo("[+] Writing file to disk as: {}".format(output))
    with open(output,'w') as f:
        f.write(st)

@main.command()
def register():
    """Register current user on the blockchain"""
    user = load()
    

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

def get_ether_balance(address):
    return w3.eth.getBalance(address)/1000000000000000000

def check_ether():
    """Sends 1 Ropsten test ether if account has 0 ETH"""
    address = load()['ethereum'].address
    balance = get_ether_balance(address)
    if balance < 1:
        secho("[o] No Ether in account. Automatically requesting test ether...", fg='yellow')
        base = 'http://faucet.ropsten.be:3001/donate/{address}'
        echo('[+] Requesting test ether for {}'.format(address))
        requests.get(base.format(address=address))
        echo("[+] Request sent. Check back after a while...")
    else:
        secho("[+] Got test ether! Ready to create some medblocks!", fg='green')
    return

@main.command()
def info():
    """Get info about current user"""
    echo("[+] Loading user from .medblocks")
    user = load()
    echo('Name: {}'.format(user['name']))
    echo('Phone: {}'.format(user['phone']))
    echo('RSA public key: ')
    click.secho(user['rsa'].publickey().exportKey().decode(), fg='green')
    echo('Ethereum address: {}'.format(user['ethereum'].address))
    balance = get_ether_balance(user['ethereum'].address)
    echo('Test Ether balance: {} ETH'.format(balance))
    check_ether()

if __name__ == "__main__":
    main()

