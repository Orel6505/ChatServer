import socket, threading
from Common import Common

#
# Copyright (C) 2024 Orel6505
#
# SPDX-License-Identifier: GNU General Public License v3.0
#

class Client(Common):
    def __init__(self, ip: str, port: int, logName: str="Client") -> None:
        super().__init__(ip, port, logName)
        self.client: socket.socket = self.createClient()
        
    ## My own implementation of TLS
    def ClientHello(self, cert):
        self.cert = cert
        #checking certificate is missing
        return self.pubKey
    
    def ClientHelloDone(self):
        pass
    
    def ClientKeyExchange(self, key: bytes):
        self.serverKey = key
    ## Manage Client
    def createClient(self) -> socket.socket:
        try: 
            client: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.settimeout(10)
            self.logAndPrintInfo(f'Client Created Successfully')
            client.connect((self.ip,self.port))
            self.logAndPrintInfo(f'Client Connected to {self.ip}:{self.port}')
            return client
        except Exception:
            self.log.writeFatal()
            
    def closeClient(self) -> None:
        self.setStatus(False)
        if self.client:
            self.logAndPrintInfo("Closing connection")
            self.client.close()
    
    def receiveMessage(self) -> None:
        try:
            while self.getStatus():
                try:
                    message = self.client.recv(1024)
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
                    self.logAndPrintInfo(f'Server closed connection, closing client...')
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
        t = threading.Thread(target=client.receiveMessage, args=())
        t.start()
        client.sendMessage()
        t.join()
    except Exception:
        client.log.writeFatal()
    finally:
        print("Client Finished")
        client.closeLog()
        if client.getStatus():
            client.closeClient()

if __name__ == "__main__":
    main()