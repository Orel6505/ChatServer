from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa

class RSAKeyGenerator:
    def __init__(self) -> None:
        self.key = rsa.generate_private_key(public_exponent=65537, key_size=2048,)
        RSAKeyGenerator.writeToSafe(self.key.private_bytes(encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.PKCS8, encryption_algorithm=serialization.NoEncryption()), 'privKey')
        self.pubKey = self.key.public_key().public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)
        
    def writeToSafe(object: bytes, fileName: str):
        with open(f'safe/{fileName}.pem', "wb") as f:
            f.write(object)
            
    def readFromSafe(fileName):
        with open(f'safe/{fileName}.pem', "rb") as f:
            return f.read()
        
    def loadPublicKey(pem_bytes):
        return serialization.load_pem_public_key(pem_bytes, backend=default_backend())

    def encrypt(key, data: bytes):
        key = RSAKeyGenerator.loadPublicKey(key)
        return key.encrypt(data,padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None))
    
    def decrypt(self, data: bytes):
        return self.key.decrypt(data, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(),label=None))