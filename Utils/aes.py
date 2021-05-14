import string, random, json
from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

BLOCK_SIZE = 16

def unpad(data):
    return data[:-data[-1]]

class AES_CBC:
    @staticmethod
    def generateKey(size_key):
        aes_key = random.choice(string.ascii_letters)
        for i in range (size_key-1):
            aes_key += random.choice(string.ascii_letters)
        return bytes(aes_key,'utf-8')

    @staticmethod
    def encrypt(message, key):
        cipher = AES.new(key, AES.MODE_CBC)
        ct_bytes = cipher.encrypt(pad(bytes(message,'utf-8'), AES.block_size))
        iv = b64encode(cipher.iv).decode('utf-8')
        cipherText = b64encode(ct_bytes).decode('utf-8')
        result = {'iv':iv, 'ct':cipherText}
        return result

    @staticmethod
    def decrypt(encrypted, key):
        encrypted = b64decode(encrypted)
        IV = encrypted[:BLOCK_SIZE]
        aes = AES.new(key, AES.MODE_CBC, IV)
        return unpad(aes.decrypt(encrypted[BLOCK_SIZE:]))