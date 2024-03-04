import socket, threading
from Common import Common

class Client(Common):
    def __init__(self, ip: str, port: int, logName: str="Client") -> None:
        super().__init__(ip, port, logName)
        self.client: socket.socket = self.createClient()
    
    ## Manage Client
    def createClient(self) -> socket.socket:
        try: 
            client: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.settimeout(10)
            self.log.writeInfo(f'Client Created Successfully')
            return client
        except Exception:
            self.log.writeFatal()
            
    def closeClient(self) -> None:
        self.setStatus(False)
        if self.client:
            self.log.writeInfo("Client is closed")
            self.client.close()
            
    def connectToServer(self) -> None:
        self.client.connect((self.ip,self.port))
        self.log.writeInfo(f'Client Connected to {self.ip}:{self.port}')

    def receiveData(self) -> None:
        try:
            while self.getStatus():
                try:
                    message = self.client.recv(1024)
                except ConnectionAbortedError:
                    break
                except TimeoutError:
                    self.log.writeInfo("Server Timeout")
                    if not self.getStatus():
                        break
                    continue
                self.log.writeInfo(f'Server sent: {message.decode('utf-8')}')
                print("Server: " + message.decode('utf-8'))
                if message == b'close':
                    self.log.writeInfo("Server closed this connection")
                    self.closeClient()
        except socket.error:
            self.log.writeWarning("Server Closed Connection")
        except Exception:
            self.log.writeFatal()
            
    def sendMessage(self) -> None:
        try:
            while self.getStatus():
                message = input("")
                if self.getStatus:
                    self.client.send(message.encode())
                    self.log.writeInfo(f'Client send {message} to {self.ip}:{self.port}')
                    if message == "close":
                        self.log.writeInfo("Closing connection")
                        self.closeClient()
        except socket.error:
            self.log.writeWarning("Closing connection")
        except Exception:
            self.log.writeFatal()

IP = "127.0.0.1"
PORT = 8081

def main():
    try:
        client = Client(IP,PORT)
        client.connectToServer()
        t = threading.Thread(target=client.receiveData, args=())
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