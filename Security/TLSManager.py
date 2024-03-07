from RSAKeyGenerator import RSAKeyGenerator
from CertificateGenerator import CertificateGenerator

class TLSManager(RSAKeyGenerator):
    def __init__(self) -> None:
        super().__init__()
        try:
            self.cert = RSAKeyGenerator.readFromSafe("certification")
        except FileNotFoundError:
            CertificateGenerator().generateCSR()
            self.cert = RSAKeyGenerator.readFromSafe("certification")
        
    def ServerHello(self):
        return self.cert
    
    def ClientHello(self, cert):
        cert = cert
        if not CertificateGenerator.checkCSR(cert): return None
        return self.pubKey
        
    def ServerKeyExchange(self, key):
        self.clientKey = key
        return self.pubKey
        
    def ClientKeyExchange(self, key: bytes):
        self.serverKey = key
        #return RSAKeyGenerator.encrypt(self.serverKey, self.pubKey)
    
    def ChangeChiperSpec(self):
        #self.clientKey = self.decrypt(data)
        pass
    
def main():
    TLSServer = TLSManager()
    TLSClient = TLSManager()
    serverresp = TLSServer.ServerHello()
    clientresp = TLSClient.ClientHello(serverresp)
    serverresp = TLSServer.ServerKeyExchange(clientresp)
    clientresp = TLSClient.ClientKeyExchange(serverresp)
    if TLSClient.pubKey == TLSServer.clientKey:
        print("Yay")
    if TLSServer.pubKey == TLSClient.serverKey:
        print("Yay")

if __name__ ==  '__main__':
    main()