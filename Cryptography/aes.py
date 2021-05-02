import string, random, json
from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

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
    def decrypt(result, key):
        iv = b64decode(result['iv'])
        cipherText = b64decode(result['ct'])
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plainText = unpad(cipher.decrypt(cipherText), AES.block_size)
        return plainText.decode()

aes_mode_cbc = AES_CBC()
key = aes_mode_cbc.generateKey(16)
result = aes_mode_cbc.encrypt('HOLA MUNDO', key)
plainText = aes_mode_cbc.decrypt(result,key)
print(plainText)