import socket, Log, threading

class Client:
    def __init__(self, ip: str, port: int, logName: str="Client") -> None:
        self.ip = ip
        self.port = port
        self.status = True
        self.log: Log.Log = self.__createLog(logName)
        self.client: socket.socket = self.createClient()
    
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
    
    ## Manage Client
    def createClient(self) -> socket.socket:
        try: 
            client: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.settimeout(60)
            self.log.writeInfo(f'Client Created')
            return client
        except Exception:
            self.log.writeFatal()
            
    def closeClient(self) -> None:
        self.setStatus(False)
        if self.client:
            self.log.writeInfo("Client is closed")
            self.client.close()
        if self.log:
            self.__closeLog()
            
    def connectToServer(self) -> None:
        self.client.connect((self.ip,self.port))
        self.log.writeInfo(f'Client Connected to {self.ip}:{self.port}')
        
    def sendData(self) -> None:
        try:
            while self.getStatus():
                message = input("")
                self.client.send(message.encode())
                self.log.writeInfo(f'Client send {message} to {self.ip}:{self.port}')
        except ConnectionResetError:
            self.log.writeWarning("Server Closed Connection")

    def recvData(self) -> None:
        try:
            while self.getStatus():
                message = self.client.recv(1024)
                if message == "close":
                        self.log.writeInfo("Server is closing the server")
                        self.closeServer()
                else:
                    self.log.writeInfo("Server: " + message.decode('utf-8'))
                    print("Server: " + message.decode('utf-8'))
        except ConnectionResetError:
            self.log.writeWarning("Server Closed Connection")

IP = "127.0.0.1"
PORT = 8081

def main():
    try:
        client = Client(IP,PORT)
        log = client.log
        client.connectToServer()
        t1 = threading.Thread(target=client.sendData, args=())
        t2 = threading.Thread(target=client.recvData, args=())
        t1.start()
        t2.start()
        t2.join()
        t1.join()
    except Exception as e:
        log.writeFatal()
    finally:
        client.closeClient()

if __name__ == "__main__":
    main()