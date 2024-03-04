import socket, threading
from Common import Common

class Server(Common):
    def __init__(self, ip: str, port: int, logName: str="Server") -> None:
        super().__init__(ip, port, logName)
        self.clients = []
        self.server: socket.socket = self.createServer()
    
    ## Manage Clients
    def getCLients(self) -> list:
        return self.clients
    
    def addClient(self, client: tuple) -> None:
        self.clients.append(client)
        self.logAndPrintInfo(f'New Client connected: {client[1]}')
    
    def removeClient(self, client: tuple) -> None:
        if client in self.clients:
            self.clients.remove(client)
            self.logAndPrintInfo(f'Client {client[1]} disconnected')
            client[0].close()
        else:
            self.log.writeWarning(f'Client {client[1]} already disconnected')
        
    def clearClients(self):
        for client in self.clients:
            self.removeClient(client)
    
    ## Manage Server
    def createServer(self) -> socket.socket:
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.bind((self.ip,self.port))
            server.listen(10)
            server.settimeout(10)
            self.logAndPrintInfo("Server Created Successfully")
            return server
        except Exception:
            self.log.writeFatal()
            
    def closeServer(self) -> None:
        self.setStatus(False)
        if self.clients:
            self.clearClients()
        if self.server:
            self.logAndPrintInfo("Server Closed")
            self.server.close()
        
    def acceptClient(self) -> None:
        try:
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
                t = threading.Thread(target=Server.receiveData, args=(self,client))
                t.start()
            t.join()
        except Exception:
            self.log.writeFatal()

    def receiveData(self, client: tuple) -> None:
        try: 
            while self.getStatus():
                try:
                    message = client[0].recv(1024)
                except socket.error:
                    self.log.writeWarning("Connection Interrupted")
                    break
                if message == b'':
                    break
                else:
                    print(f'{message}')
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
                    self.logAndPrintInfo("Server is closing the server")
                    self.closeServer()
        except Exception:
            self.log.writeFatal()
            
    def broadcastMessage(self, message: str) -> None:
        for client in self.clients:
            try:
                client[0].send(message.encode())
                self.log.writeInfo(f'Sent message "{message}" to address: {client[1]} ')
            except socket.error:
                self.removeClient(client)

IP = "127.0.0.1"
PORT = 8081

def main():
    try:
        server = Server(IP,PORT)
        if server.getStatus():
            t1= threading.Thread(target=server.acceptClient, args=())
            t1.start()
            server.sendMessage()
            t1.join()
        else:
            server.logAndPrintError("Server failed, Check Logs")
    except Exception:
        server.log.writeFatal()
    finally:
        server.logAndPrintInfo("Server Finished")
        server.closeLog()
        if server.getStatus():
            server.closeServer()

if __name__ == "__main__":
    main()