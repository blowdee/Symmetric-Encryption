import os
from _hashlib import pbkdf2_hmac
from binascii import hexlify
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, modes
from cryptography.hazmat.primitives.ciphers.algorithms import AES
from cryptography.hazmat.primitives import padding


class AES_Encryptor:
    def __init__(self, key):
        self.key = pbkdf2_hmac('sha256', key.encode(), b'', 100000)

    def encrypt(self, msg):
        IV = os.urandom(16)

        padder = padding.PKCS7(256).padder()
        padded = padder.update(msg.encode()) + padder.finalize()

        cipher = Cipher(AES(key=self.key), modes.CBC(initialization_vector=IV), backend=default_backend())
        encryptor = cipher.encryptor()

        result = encryptor.update(padded) + encryptor.finalize()

        file_name = input('Save to file: ')
        self.toFile(file_name, result, IV)

    def toFile(self, file_name, msg, IV):
        with open(file_name, 'w') as f:
            hex_msg, hex_IV = hexlify(msg), hexlify(IV)
            f.write(hex_msg.decode() + ' ' + hex_IV.decode())


AES_key = input('Your passphrase: ')
encr = AES_Encryptor(AES_key)
message = input('Message you want to encrypt: ')
encr.encrypt(message)
