from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

class KeysAndHashes:
    @staticmethod
    def WriteToSafe(Key: bytes, FilePath: str, FileName: str):
        with open(f'{FilePath}/{FileName}.pem', "wb") as f:
            f.write(Key)
    
    @staticmethod
    def ReadFromSafe(FilePath: str, FileName: str):
        with open(f'{FilePath}/{FileName}.pem', "rb") as f:
            return f.read()
    
    @staticmethod
    def LoadPublicKey(pemBytes: bytes):
        return serialization.load_pem_public_key(pemBytes, backend=default_backend())
    
    @staticmethod
    def LoadPrivateKey(pemBytes: bytes):
        return serialization.load_pem_private_key(pemBytes, backend=default_backend(), password=None)
    
    @staticmethod
    def WritePublicKeyToSafe(pubKey, FilePath: str, FileName: str):
        KeysAndHashes.WriteToSafe(pubKey.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.PKCS1), FilePath, FileName)
    
    @staticmethod
    def WritePrivateKeyToSafe(privKey, FilePath: str, FileName: str):
        KeysAndHashes.WriteToSafe(privKey.private_bytes(encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.PKCS8, encryption_algorithm=serialization.NoEncryption()), FilePath, FileName)

    @staticmethod
    def EncryptData(key, data: bytes):
        key = KeysAndHashes.LoadPublicKey(key)
        return key.encrypt(data,padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None))
    
    @staticmethod
    def DecryptData(key, data: bytes):
        return key.decrypt(data, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(),label=None))
