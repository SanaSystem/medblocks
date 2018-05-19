import click
from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
import base64
import os
from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import CryptoKeypair, generate_keypair
import json

@click.group()
def main():
    
    art = """
███╗   ███╗███████╗██████╗ ██████╗ ██╗      ██████╗  ██████╗██╗  ██╗███████╗
████╗ ████║██╔════╝██╔══██╗██╔══██╗██║     ██╔═══██╗██╔════╝██║ ██╔╝██╔════╝
██╔████╔██║█████╗  ██║  ██║██████╔╝██║     ██║   ██║██║     █████╔╝ ███████╗
██║╚██╔╝██║██╔══╝  ██║  ██║██╔══██╗██║     ██║   ██║██║     ██╔═██╗ ╚════██║
██║ ╚═╝ ██║███████╗██████╔╝██████╔╝███████╗╚██████╔╝╚██████╗██║  ██╗███████║
╚═╝     ╚═╝╚══════╝╚═════╝ ╚═════╝ ╚══════╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝╚══════╝                                          
"""
    click.secho(art,fg='green')
    click.secho("Store your records securely",fg='green')

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

def dump_new_user(name,phone):
    user = {
        'name':name,
        'phone':phone
    }
    click.echo("[+] Writing Name and Phone")
    bigchain_keys = generate_keypair()
    click.echo("[+] Generating bigchainDB blockchain keypair")
    random_generator = Random.new().read
    rsa_key = RSA.generate(1024, random_generator)
    click.echo("[+] Generating RSA keypair")
    user['blockchain'] = {'private_key':bigchain_keys.private_key,'public_key':bigchain_keys.public_key}
    user['rsa'] = {'private_key':rsa_key.exportKey().decode('utf-8'),'public_key':rsa_key.publickey().exportKey().decode('utf-8')}
    click.echo("[+] Serializing to JSON")
    user = json.dumps(user)
    return user

def load_user(string):
    user = json.loads(string)
    user['rsa']['private_key'] = RSA.importKey(user['rsa']['private_key'])
    user['rsa']['public_key'] = RSA.importKey(user['rsa']['public_key'])
    user['blockchain'] = CryptoKeypair(**user['blockchain'])
    return user

@main.command()
@click.option('--output','-o', help="Output file with credentials", default='patient.json')
@click.option('--name','-n',prompt="Name of patient")
@click.option('--phone','-p',prompt="Phone number")
def createuser(name, phone, output):
    """Generates a random key pairs and writes the user to a file"""
    st = dump_new_user(name,phone)
    click.secho("Writing private key data to file. Please be sure to save it securely.", fg='red')
    click.pause()
    #click.echo(st)
    click.echo("[+] Writing file to disk as: {}".format(output))
    with open(output,'w') as f:
        f.write(st)
    click.echo("[+] Done")

if __name__ == "__main__":
    main()

