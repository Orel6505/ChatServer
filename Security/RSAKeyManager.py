from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding

class RSAKeyManager:
    def __init__(self) -> None:
        self.privKey: rsa.RSAPrivateKey = rsa.generate_private_key(public_exponent=65537, key_size=2048,)
        self.pubKey: rsa.RSAPublicKey = self.privKey.public_key()
    
    @staticmethod
    def WriteToSafe(Key: bytes, FilePath: str, FileName: str):
        with open(f'{FilePath}/{FileName}.pem', "wb") as f:
            f.Write(Key)
    
    @staticmethod
    def ReadFromSafe(FilePath: str, FileName: str):
        with open(f'{FilePath}/{FileName}.pem', "rb") as f:
            return f.read()
    
    @staticmethod
    def LoadPublicKey(pemBytes: bytes):
        return serialization.load_pem_public_key(pemBytes, backend=default_backend())
    
    @staticmethod
    def loadPrivateKey(pemBytes: bytes):
        return serialization.load_pem_private_key(pemBytes, backend=default_backend())

    @staticmethod
    def EncryptData(key, data: bytes):
        key = RSAKeyManager.loadPublicKey(key)
        return key.encrypt(data,padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None))
    
    @staticmethod
    def DecryptData(key, data: bytes):
        return key.decrypt(data, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(),label=None))
    
    def WritePublicKeyToSafe(self, FilePath: str, FileName: str):
        RSAKeyManager.WriteToSafe(self.pubKey.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.PKCS1), FilePath, FileName)
    
    def WritePrivateKeyToSafe(self, FilePath: str, FileName: str):
        RSAKeyManager.WriteToSafe(self.privKey.private_bytes(encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.PKCS8, encryption_algorithm=serialization.NoEncryption()), FilePath, FileName)
