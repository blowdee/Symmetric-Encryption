from binascii import unhexlify
from hashlib import pbkdf2_hmac
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding


class AES_Decryptor:
    def __init__(self, key, IV):
        self.key = pbkdf2_hmac('sha256', key.encode(), b'', 100000)
        self.IV = unhexlify(IV)

    def decrypt(self, message):
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(self.IV), backend=default_backend())
        decryptor = cipher.decryptor()
        result = decryptor.update(unhexlify(message)) + decryptor.finalize()

        unpadder = padding.PKCS7(256).unpadder()
        unpadded_msg = unpadder.update(result) + unpadder.finalize()

        print('The message is: ', unpadded_msg.decode())


file_name = input('Name of file: ')
passphrase = input('Your passphrase: ')

with open(file_name, 'r') as f:
    data = f.readline().split()
    msg, IV = data[0].encode(), data[1].encode()

decr = AES_Decryptor(passphrase, IV)
decr.decrypt(msg)
