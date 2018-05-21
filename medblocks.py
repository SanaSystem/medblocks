import click
from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
import base64
import os
from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import CryptoKeypair, generate_keypair
import json

tokens = {}
tokens['app_id'] = 'd5596f54'
tokens['app_key'] = '6f108c571fcb25c4d34056bede9d246f'
bdb = BigchainDB('https://test.bigchaindb.com', headers=tokens)

@click.group()
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

def dump_user(dict):
    
    click.echo("[+] Serializing to JSON")
    user = json.dumps(user)
    return user

def load_user(string):
    user = json.loads(string)
    user['rsa']['private_key'] = RSA.importKey(user['rsa']['private_key'])
    user['rsa']['public_key'] = RSA.importKey(user['rsa']['public_key'])
    return user

def register_on_blockchain(user):
    rsa_public_key = user['rsa']['public_key']
    ethereum_address = user['blockchain']['public_key']
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
def give_permission(address, medblock_index):
    pass

@main.command()
@click.option('--output','-o', help="Output file with credentials", default='patient.json')
@click.option('--name','-n',prompt="Name of patient")
@click.option('--phone','-p',prompt="Phone number")
def createuser(name, phone, output):
    """Generates a random key pairs and writes the user to a file"""
    user = {
        'name':name,
        'phone':phone
    }
    click.echo("[+] Writing Name and Phone")
    # Generate ethereum keys
    ethereum_keys = {'private_key':'1234', 'public_key':'0xsdfsdfs'}
    # TK
    click.echo("[+] Generating bigchainDB keypair")
    random_generator = Random.new().read
    rsa_key = RSA.generate(1024, random_generator)
    click.echo("[+] Generating RSA keypair")
    user['blockchain'] = ethereum_keys
    user['rsa'] = {'private_key':rsa_key.exportKey().decode('utf-8'),'public_key':rsa_key.publickey().exportKey().decode('utf-8')}
    st = dump_user(user)
    click.secho("Writing private key data to file. Please be sure to save it securely.", fg='red')
    click.pause()
    #click.echo(st)
    click.echo("[+] Writing file to disk as: {}".format(output))
    with open(output,'w') as f:
        f.write(st)
    click.echo("[o] Writing public key data to blockchain....")
    
    # Write to Ethereum blockchain using web3
    
    click.echo("[+] Done")

if __name__ == "__main__":
    main()

