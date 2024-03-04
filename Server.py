import socket, Log, threading

class Server:
    def __init__(self, ip: str, port: int, logName: str="Server") -> None:
        self.ip = ip
        self.port = port
        self.status = True
        self.clients = []
        self.log: Log.Log = self.__createLog(logName)
        self.server: socket.socket = self.createServer()
    
    ## Manage Clients
    def getCLients(self) -> list:
        return self.clients
    
    def addClient(self, client: tuple) -> None:
        self.clients.append(client)
        self.log.writeInfo(f'New Client connected: {client[1]} ')
        print(f'New Client connected: {client[1]} ')
    
    def removeClient(self, client: tuple) -> None:
        self.clients.remove(client)
        self.log.writeInfo(f'Client disconnected {client[1]}')
        print(f'Client disconnected')
        client[0].close()
        
    def clearClients(self):
        for client in self.clients:
            self.removeClient(client)
    
    ## Manage Status
    def getStatus(self) -> bool:
        return self.status

    def setStatus(self, boolean: bool) -> None:
        self.status = boolean
    
    ## Manage Log class
    def __createLog(self, logName: str) -> Log.Log:
        return Log.Log(logName, newFileLog=False)

    def __closeLog(self) -> None:
        self.log.closeLog()
        self.log = None
    
    ## Manage Server
    def createServer(self) -> socket.socket:
        try: 
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.bind((self.ip,self.port))
            server.listen(10)
            server.settimeout(10)
            self.log.writeInfo("Server Created Successfully")
            return server
        except Exception:
            self.log.writeFatal()
            
    def closeServer(self) -> None:
        self.setStatus(False)
        if self.clients:
            self.clearClients()
        if self.server:
            self.log.writeInfo("Server Closed")
            self.server.close()
        if self.log:
            self.__closeLog()
        
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
                except OSError:
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
                conn: socket.socket = client[0]
                try: 
                    data = conn.recv(1024)
                except ConnectionAbortedError:
                    break
                if data == b'':
                    self.removeClient(client)
                    break
                else:
                    print(f'{data}')
                    self.log.writeInfo(f'Server Received {data} from {client[1]}')
        except Exception:
            self.log.writeFatal()
            
    def sendMessage(self) -> None:
        try:
            while self.getStatus():
                message = input("")
                if message == "close":
                    self.log.writeInfo("Server is closing the server")
                    self.closeServer()
                else:
                    for client in self.clients:
                        client[0].send(message.encode())
                        self.log.writeInfo(f'Sent message "{message}" to address: {client[1]} ')
        except Exception as e:
            self.log.writeFatal()

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
            print("Server failed")
    except KeyboardInterrupt:
        print('Server interrupted')
    except Exception as e:
        if server.getStatus():
            server.log.writeFatal()
        else:
            print(e)
    finally:
        print("Server Finished")
        if server.getStatus():
            server.closeServer()

if __name__ == "__main__":
    main()