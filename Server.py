import socket, threading, os
from BaseChat import BaseChat
from CertificateManager import CertificateManager
from CryptoHelper import CryptoHelper

#
# Copyright (C) 2024 Orel6505
#
# SPDX-License-Identifier: GNU General Public License v3.0
#

class Server(BaseChat):
    def __init__(self, ip: str, port: int, cHelper: CryptoHelper, logName: str="Server",clientCert: bool=True) -> None:
        super().__init__(ip, port, logName, cHelper)
        self.clients = []
        self.threads = []
        self.clientCert = clientCert
        self.server: socket.socket = self.createServer()
    
    ## Manage Clients
    def getCLients(self) -> list:
        return self.clients
    
    def addClient(self, client: tuple) -> None:
        self.clients.append(client)
        t = threading.Thread(target=Server.receiveMessage, args=(self,client))
        self.threads.append(t)
        t.start()
        self.log.writePrintInfo(f'New Client connected: {client[1]}')
    
    def removeClient(self, client: tuple) -> None:
        if client in self.clients:
            self.clients.remove(client)
            self.log.writePrintInfo(f'Client {client[1]} disconnected')
            client[0].close()
        else:
            self.log.writeWarning(f'Client {client[1]} already disconnected')
        
    def clearClients(self):
        for client in self.clients:
            self.removeClient(client)
    
    def ServerHello(self):
        return self.cert
    
    def ServerKeyExchange(self, key):
        self.clientKey = key
        return self.pubKey

    def ServerSecureConnection(self, client: tuple) -> None:
        try:
            ServerHello = {}
            
            ClientHello = client[0].recv(self.buffer)
            ClientHello = self.DeserializeJson(ClientHello)
            self.writePrintInfo(ClientHello)

            ClientRandom = ClientHello["ClientRandom"]
            
            #Select Hash
            ChosenHash = self.ChooseHashType(ClientHello["SupportedHashes"])
            if ChosenHash:
                ServerHello["ChosenHashCipher"] = ChosenHash
            
            #Select Hash
            ChosenKey = self.ChooseKeyType(ClientHello["SupportedKeys"])
            if ChosenKey:
                ServerHello["ChosenKeyCipher"] = ChosenKey
            
            #Generate Server Random
            ServerRandom = os.urandom(32)
            ServerHello["ServerRandom"] = ServerRandom
            
            #Add the certificate
            ServerHello["ServerCert"] = self.cert.decode()
            
            self.writePrintInfo(ServerHello)
            #Send
            client[0].send(self.SerializeJson(ServerHello))
            ServerHello.clear()

            #Receive
            ClientHello = self.DeserializeJson(client[0].recv(self.buffer))
                            
            #Gets Pre-master secret and decrypt it using it's certificate private key
            ClientSecret = self.cHelper.DecryptData(self.key, ClientHello["ClientSecret"])
            
            #Generate Server Secret
            ServerSecret = os.urandom(42)
            
            #Client Certificate is required?
            ServerHello["ClientCSR"] = self.clientCert
            client[0].send(self.SerializeJson(ServerHello))
            ServerHello.clear()
            ClientHello = self.DeserializeJson(client[0].recv(self.buffer))
            if self.clientCert:
                cert = CertificateManager.LoadCertificate(ClientHello["ClientCert"])
            
                #Validate CSR
                if not CertificateManager.ValidateCSR(cert):
                    return None
                
                #Encrypt the Server Secret
                ServerHello["ServerSecret"] = self.cHelper.EncryptData(cert.public_key(), ServerSecret)
            else:
                #Load Client Public key
                #ClientPubKey = self.cHelper.LoadPublicKey(ClientHello["ClientPubKey"])
                self.closeServer()
                #Encrypt the Server Secret
                #ServerHello["ServerSecret"] = self.cHelper.EncryptData(ClientPubKey, ServerSecret)
            client[0].send(self.SerializeJson(ServerHello))
            ServerHello.clear()
            
            MasterKey = self.GenerateMasterKey(ServerRandom,ClientRandom,ServerSecret,ClientSecret)
            
            #ServerHello["FirstMessage"] = self.cHelper.EncryptData(ClientPubKey, "ReadyToSwitch")
            #client[0].send(self.SerializeJson(ServerHello))
            #ServerHello.clear()
                        
            #if self.cHelper.DecryptData(self.key, ClientHello["FirstMessage"]) == "ReadyToSwitch":
            print("Worked")
        except Exception:
            self.log.writeFatal()
    
    ## Manage Server
    def createServer(self) -> socket.socket:
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.bind((self.ip,self.port))
            server.listen(10)
            server.settimeout(10)
            self.log.writePrintInfo("Server Created Successfully")
            return server
        except Exception:
            self.log.writeFatal()
            
    def closeServer(self) -> None:
        self.setStatus(False)
        if self.clients:
            self.clearClients()
        if self.server:
            self.log.writePrintInfo("Server Closed")
            self.server.close()
        
    def acceptClient(self) -> None:
        try:
            threads = []
            while self.getStatus():
                try:
                    client: tuple = self.server.accept()
                except TimeoutError:
                    self.log.writeInfo("Server Timeout")
                    if not self.getStatus():
                        break
                    continue
                except socket.error:
                    self.log.writeWarning("Server Interrupted")
                    break
                self.addClient(client)
            for t in threads:
                t.join()
        except Exception:
            self.log.writeFatal()
        finally:
            if self.getStatus():
                self.closeServer()

    def receiveMessage(self, client: tuple) -> None:
        try: 
            while self.getStatus():
                try:
                    message = client[0].recv(self.buffer)
                except socket.error:
                    self.log.writeWarning("Connection Interrupted")
                    break
                if message == b'':
                    self.log.writeWarning("Client disconnected")
                    break
                else:
                    print(f'{message}')
                    self.broadcastMessage(message,client)
                    self.log.writeInfo(f'Server Received {message} from {client[1]}')
        except Exception:
            self.log.writeFatal()
        finally:
            self.removeClient(client)

    def sendMessage(self) -> None:
        try:
            while self.getStatus():
                message = input("")
                self.broadcastMessage(message)
                if message == "close":
                    self.log.writePrintInfo("Server is shutting down")
                    self.closeServer()
        except Exception:
            self.log.writeFatal()
    
    def broadcastMessage(self, message: str, sender: tuple=None) -> None:
        for client in self.clients:
            try:
                if sender != client:
                    client[0].send(f'Server: {message}'.encode())
                    self.log.writeInfo(f'Sent message "{message}" to address: {client[1]}')
            except socket.error:
                self.removeClient(client)

IP = "127.0.0.1"
PORT = 8081

SIP = "127.0.0.1"
SPORT = 8082

def main():
    try:
        cHelper = CryptoHelper("safe")
        try:
            cert = CertificateManager.ReadCertificateFromSafe("cert")
            key = cHelper.ReadFromSafe("PrivCert")
            certKey = cHelper.LoadPrivateKey(key)
        except FileNotFoundError:
            certKey = CertificateManager()
            cHelper.WriteToSafe(certKey, "PrivCert")
            cert = certKey.GenerateCertificate(certKey, "IL", "Haifa", "Ramla", "Orel6505", "Orel Yosupov")
            certKey.WriteCertToSafe(cert, "cert")
            cert = certKey.ReadCertificateFromSafe("cert")
        server = Server(IP,PORT)
        server.AddSecrets(cert, certKey)
        t = threading.Thread(target=server.acceptClient, args=())
        t.start()
        server.sendMessage()
        t.join()
    except Exception:
        server.log.writeFatal()
    finally:
        server.log.writePrintInfo("Server Finished")
        server.closeLog()
        if server.getStatus():
            server.closeServer()

if __name__ == "__main__":
    main()