import socket, threading, os
from BaseChat import BaseChat
from CryptoHelper import CryptoHelper
from CertificateManager import CertificateManager

#
# Copyright (C) 2024 Orel6505
#
# SPDX-License-Identifier: GNU General Public License v3.0
#

class Client(BaseChat):
    def __init__(self, ip: str, port: int, cHelper: CryptoHelper, logName: str="Client") -> None:
        super().__init__(ip, port, logName, cHelper)
        self.client: socket.socket = self.createClient()
    
    ## Manage Client
    def createClient(self) -> socket.socket:
        try: 
            client: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.settimeout(10)
            self.log.writePrintInfo(f'Client Created Successfully')
            client.connect((self.ip,self.port))
            self.log.writePrintInfo(f'Client Connected to {self.ip}:{self.port}')
            return client
        except Exception:
            self.log.writeFatal()
            
    def closeClient(self) -> None:
        self.setStatus(False)
        if self.client:
            self.log.writePrintInfo("Closing connection")
            self.client.close()
            
    def ClientSecureConnection(self) -> None:
        try:
            ClientHello = {}

            #List of supported keys and hashes
            ClientHello["SupportedKeys"]= ['RSA',]
            ClientHello["SupportedHashes"]= ['SHA-256',]
            
            #Generate Client Random
            ClientRandom = os.urandom(32)
            ClientHello["ClientRandom"] = ClientRandom

            #Send
            self.log.writePrintInfo(ClientHello)
            if not self.SerializeJson(ClientHello).encode('utf-8'):
                return -1
            self.client.send(self.SerializeJson(ClientHello).encode('utf-8'))
            
            ClientHello.clear()
            
            #Receive
            ServerHello = self.DeserializeJson(self.client.recv(self.buffer))
            self.log.writePrintInfo(ServerHello)
            ServerRandom = ServerHello["ServerRandom"] 
            
            #Load the certificate
            self.log.writePrintInfo(ServerHello["ServerCert"])
            cert = CertificateManager.LoadCertificate(ServerHello["ServerCert"].encode())
            
            #Validate Certificate
            if not CertificateManager.ValidateCertificate(cert):
                return None
                     
            #Generate Client Secret
            ClientSecret = os.urandom(42)
            
            #Encrypt the Client Secret with the Certificate public key
            ClientHello["ClientSecret"] = self.cHelper.EncryptAsymmetricData(cert.public_key(), ClientSecret)
            
            #Send
            self.client.send(self.SerializeJson(ClientHello))
            
            ClientHello.clear()
            
            ServerHello = self.DeserializeJson(self.client.recv(self.buffer))
            clientCert = ServerHello["ClientCSR"]
            if clientCert:
                ClientHello["ClientCSR"] = self.cert
            else:
                return 0
                #Not Implemented
            
            self.client.send(self.SerializeJson(ClientHello))
            ClientHello.clear()
            ServerHello = self.DeserializeJson(self.client.recv(self.buffer))
            if clientCert:
                ServerSecret = self.cHelper.DecryptAsymmetricData(self.key, ClientHello["ClientSecret"])
            else:
                #ServerSecret = self.cHelper.DecryptAsymmetricData(key, ClientHello["ClientSecret"])
                print("Not Implemented")
            
            MasterKey = self.GenerateMasterKey(ServerRandom,ClientRandom,ServerSecret,ClientSecret)

            #if self.cHelper.DecryptAsymmetricData(self.key, ServerHello["FirstMessage"]) == "ReadyToSwitch":
            print("Worked")
        except Exception:
            self.log.writeFatal()
    
    def receiveMessage(self) -> None:
        try:
            while self.getStatus():
                try:
                    message = self.client.recv(self.buffer)
                except TimeoutError:
                    self.log.writeInfo("Server Timeout")
                    if not self.getStatus():
                        break
                    continue
                except socket.error:
                    self.log.writeError("Server Connection was lost, closing connection")
                    break
                self.log.writeInfo(f'Received message from server: {message.decode('utf-8')}')
                print(message.decode('utf-8'))
                if message == b'close':
                    self.log.writePrintInfo(f'Server closed connection, closing client...')
                    break
                elif message == b'':
                    self.log.writePrintInfo("Server Connection was lost, closing connection")
                    break
        except Exception:
            self.log.writeFatal()
        finally:
            if self.getStatus():
                self.closeClient()
            
    def sendMessage(self) -> None:
        try:
            while self.getStatus():
                message = input("")
                if self.getStatus:
                    try:
                        self.client.send(message.encode())
                        self.log.writeInfo(f'Client send {message} to {self.ip}:{self.port}')
                    except socket.error:
                        self.log.writeError("Server connection was lost, closing client")
                        break
                    if message == "close":
                        self.log.writeError("Server closed connection, closing client...")
                        break
        except Exception:
            self.log.writeFatal()
        finally:
            if self.getStatus():
                self.closeClient()

IP = "127.0.0.1"
PORT = 8081

def main():
    try:
        client = Client(IP,PORT)
        #t = threading.Thread(target=client.receiveMessage, args=())
        #t.start()
        #client.sendMessage()
        #t.join()
    except Exception:
        client.log.writeFatal()
    finally:
        print("Client Finished")
        client.closeLog()
        if client.getStatus():
            client.closeClient()

if __name__ == "__main__":
    main()