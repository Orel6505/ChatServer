from RSAKeyManager import RSAKeyManager
from CertificateManager import CertificateManager

class TLSManager(RSAKeyManager):      
    def __init__(self, cert: bytes=None) -> None:
        super().__init__()
        self.cert = cert
        
    def ServerHello(self):
        return self.cert
    
    def ServerHelloDone(self):
        pass
    
    def ClientHello(self, cert):
        self.cert = cert
        #if not CertificateManager.CheckCertificate(cert): return None
        return self.pubKey
    
    def ClientHelloDone(self):
        pass
        
    def ServerKeyExchange(self, key):
        self.clientKey = key
        return self.pubKey
        
    def ClientKeyExchange(self, key: bytes):
        self.serverKey = key
        #return RSAKeyGenerator.encrypt(self.serverKey, self.pubKey)
    
    def ChangeChiperSpec(self):
        #self.clientKey = self.decrypt(data)
        pass
    
def test():
    safePath = "safe"
    certFileName = "cert"
    try:
        cert = CertificateManager.ReadCertificateFromSafe(safePath, certFileName)
    except FileNotFoundError:
        certKey = RSAKeyManager()
        RSAKeyManager.WritePrivateKeyToSafe(certKey, safePath, "PrivCert")
        CertificateManager.GenerateCertificate(certKey, "IL", "Haifa", "Ramla", "Orel6505", "Orel Yosupov")
        CertificateManager.WriteCertToSafe(cert, safePath, certFileName)
        cert = CertificateManager.ReadCertificateFromSafe(safePath, certFileName)
    TLSServer = TLSManager(cert)
    TLSClient = TLSManager()
    sResponse = TLSServer.ServerHello()
    cResponse = TLSClient.ClientHello(sResponse)
    sResponse = TLSServer.ServerKeyExchange(cResponse)
    cResponse = TLSClient.ClientKeyExchange(sResponse)
    if TLSClient.pubKey == TLSServer.clientKey:
        print("Yay")
    if TLSServer.pubKey == TLSClient.serverKey:
        print("Yay")

if __name__ ==  '__main__':
    test()