import hashlib

print("MD5")
hashmd5 = hashlib.md5(b"Criptografia")
print("Hash: "+hashmd5.hexdigest())
print("Length: "+str(len(hashmd5.hexdigest())))

print("\nSHA1")
hashsha1 = hashlib.sha1(b"Criptografia")
print("Hash: "+hashsha1.hexdigest())
print("Length: "+str(len(hashsha1.hexdigest())))

print("\nSHA224")
hashsha224 = hashlib.sha224(b"Criptografia")
print("Hash: "+hashsha224.hexdigest())
print("Length: "+str(len(hashsha224.hexdigest())))

print("\nSHA256")
hashsha256 = hashlib.sha256(b"Criptografia")
print("Hash: "+hashsha256.hexdigest())
print("Length: "+str(len(hashsha256.hexdigest())))

print("\nSHA512")
hashsha512 = hashlib.sha512(b"Criptografia")
print("Hash: "+hashsha512.hexdigest())
print("Length: "+str(len(hashsha512.hexdigest())))

print("\nSHA3-224")
hashsha3224 = hashlib.sha3_224(b"Criptografia")
print("Hash: "+hashsha3224.hexdigest())
print("Length: "+str(len(hashsha3224.hexdigest())))

print("\nSHA3-256")
hashsha3256 = hashlib.sha3_256(b"Criptografia")
print("Hash: "+hashsha3256.hexdigest())
print("Length: "+str(len(hashsha3256.hexdigest())))

print("\nSHA3-384")
hashsha3384 = hashlib.sha3_384(b"Criptografia")
print("Hash: "+hashsha3384.hexdigest())
print("Length: "+str(len(hashsha3384.hexdigest())))

print("\nSHA3-512")
hashsha3512 = hashlib.sha3_512(b"Criptografia")
print("Hash: "+hashsha3512.hexdigest())
print("Length: "+str(len(hashsha3512.hexdigest())))