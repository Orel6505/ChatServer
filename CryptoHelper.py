from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

class CryptoHelper():
    
    def __init__(self, SafeLocation: str, Encoding: str) -> None:
        self.backend = default_backend()
        self.SafeLocation = SafeLocation
        self.SetEncoding(Encoding)
    
    def SetEncoding(self, Encoding: str):
        match(Encoding):
            case("pem"):
                self.Encoding = serialization.Encoding.PEM
                self.EncodingFile = "pem"
            case("der"):
                self.Encoding = serialization.Encoding.DER
                self.EncodingFile = "der"
            case("ssh"):
                self.Encoding = serialization.Encoding.OpenSSH
                self.EncodingFile = "ssh"
            case _:
                raise ValueError(f"Unsupported format: {Encoding}")
            
    def SelectCipherSuite(self, Ciphers: list) -> set:
        OldCipherSuites: dict[str,set] = {
            'ECDHE_ECDSA_WITH_AES_128_GCM_SHA256': ('TLSv1.2', 'AES', '128', 'GCM', 'SHA256'),
            'ECDHE_ECDSA_WITH_AES_256_GCM_SHA384': ('TLSv1.2', 'AES', '256', 'GCM', 'SHA384'),
            'ECDHE_ECDSA_WITH_AES_256_CBC_SHA384': ('TLSv1.2', 'AES', '256', 'CBC', 'SHA384'),
            'ECDHE_ECDSA_WITH_AES_128_CBC_SHA256': ('TLSv1.2', 'AES', '128', 'CBC', 'SHA256'),
            'ECDHE_RSA_WITH_AES_128_GCM_SHA256': ('TLSv1.2', 'AES', '128', 'GCM', 'SHA256'),
            'ECDHE_RSA_WITH_AES_256_GCM_SHA384': ('TLSv1.2', 'AES', '256', 'GCM', 'SHA384'),
            'ECDHE_RSA_WITH_AES_128_CBC_SHA256': ('TLSv1.2', 'AES', '128', 'CBC', 'SHA256'),
            'ECDHE_RSA_WITH_AES_256_CBC_SHA384': ('TLSv1.2', 'AES', '256', 'CBC', 'SHA384'),
            'DHE_RSA_WITH_AES_128_GCM_SHA256': ('TLSv1.2', 'AES', '128', 'GCM', 'SHA256'),
            'DHE_RSA_WITH_AES_256_GCM_SHA384': ('TLSv1.2', 'AES', '256', 'GCM', 'SHA384'),
            'DHE_RSA_WITH_AES_128_CBC_SHA256': ('TLSv1.2', 'AES', '128', 'CBC', 'SHA256'),
            'DHE_RSA_WITH_AES_256_CBC_SHA256': ('TLSv1.2', 'AES', '256', 'CBC', 'SHA256'),
        }
        
        NewCipherSuites: dict[str,set] = {
            'ECDHE_AES_128_CCM_8_SHA256': ('TLSv1.3', 'AES', '128', 'CCM_8', 'SHA256'),
            'ECDHE_AES_128_CCM_SHA256': ('TLSv1.3', 'AES', '128', 'CCM', 'SHA256')
        }
        
        for Cipher in Ciphers:
            if Cipher in NewCipherSuites.keys:
                return NewCipherSuites[Cipher]
        
        for Cipher in Ciphers:
            if Cipher in OldCipherSuites.keys:
                return OldCipherSuites[Cipher]
        
        return None
    
    def SetCipherProperties(self, Ciphers: list, pad, label: bytes=b'') -> None:
        self.label = label
        self.padding = pad   
        self.mgf = padding.MGF1(algorithm=self.hash)
        self.OAEP = padding.OAEP(mgf=self.mgf, algorithm=self.hash, label=self.label)
        self.HKDF = HKDF(algorithm=self.hash, length=self.KeyLen, backend=self.backend)
        self.SelectedCipher = self.SelectCipherSuite(Ciphers)
        if not self.SelectedCipher:
            raise ValueError("Ciphers is invalid")
        self.TLSVer = Cipher[0]
        if self.SelectedCipher[1]+self.SelectedCipher[2] == "AES256":
            self.algorithm = algorithms.AES256
        elif self.SelectedCipher[1]+self.SelectedCipher[2] == "AES128":
            self.algorithm = algorithms.AES128
        self.KeyLen = self.SelectedCipher[2]
        self.KeyMode = self.SelectedCipher[3]
        if self.SelectedCipher[1]+self.SelectedCipher[2] == "SHA256":
            self.hash = hashes.SHA256
        elif self.SelectedCipher[1]+self.SelectedCipher[2] == "SHA384":
            self.hash = hashes.SHA384

    def WriteToSafe(self, Key: bytes, FileName: str):
        with open(f'{self.SafeLocation}/{FileName}.{self.EncodingFile}', "wb") as f:
            f.write(Key)
    
    def ReadFromSafe(self, FileName: str):
        with open(f'{self.SafeLocation}/{FileName}.{self.EncodingFile}', "rb") as f:
            return f.read()
    
    def LoadPublicKey(self, Key: bytes):
        match(self.EncodingFile):
            case("pem"):
                return serialization.load_pem_public_key(Key, backend=self.backend)
            case("der"):
                return serialization.load_der_public_key(Key, backend=self.backend)
            case("ssh"):
                return serialization.load_ssh_public_key(Key, backend=self.backend)
        
    
    def LoadPrivateKey(self, Key: bytes):
        match(self.EncodingFile):
            case("pem"):
                return serialization.load_pem_private_key(Key, backend=self.backend)
            case("der"):
                return serialization.load_der_private_key(Key, backend=self.backend)
            case("ssh"):
                return serialization.load_ssh_private_key(Key, backend=self.backend)
    
    def LoadSymmetricKey(self, Key: bytes):
        return Cipher(self.algorithm(Key), backend=self.backend)

    def EncryptAsymmetricData(self, key: bytes, data: bytes):
        with self.LoadPublicKey(key) as key:
            return key.encrypt(data, self.OAEP)
    
    def DecryptAsymmetricData(self, key: bytes, data: bytes):
        with self.LoadPrivateKey(key) as key:
            return key.decrypt(data, self.OAEP)
    
    def EncryptSymmetricData(self, key: bytes, data: bytes):
        with self.LoadSymmetricKey(key).encryptor() as encryptor:
            return encryptor.update(data) + encryptor.finalize()

    def DecryptSymmetricData(self, key: bytes, data: bytes):
        with self.LoadSymmetricKey(key).decryptor() as decryptor:
            return decryptor.update(data) + decryptor.finalize()
    
    def GenerateMasterKey(self, ServerRandom: bytes, ClientRandom: bytes, ServerSecret: bytes, ClientSecret: bytes):
        Secret = ServerRandom + ClientRandom + ServerSecret + ClientSecret
        return self.HKDF.derive(Secret)