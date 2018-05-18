from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
import base64
import os

random_generator = Random.new().read
rsa_key = RSA.generate(1024, random_generator)

#Import export
#public = RSA.import_key(key.publickey().export_key())

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

aes_key = os.urandom(32)

with open('encrypted.jpg','wb') as f:
    f.write(encrypt(a,key))

decrypt_file('encrypted.jpg',key)

cipher_text = encrypt(b"Whatever the fuck",key.publickey())

decrypt(cipher_text, key)

cipher_text

key.publickey().export_key()