import socket, Log, threading
from status import ServerStatus

status = True
IP = "127.0.0.1"
PORT = 8081
def main():
    try:
        clients = []
        log = Log.Log("Server", newFileLog=False)
        status: ServerStatus = ServerStatus()
        server = Create_Server(log)
        if server:
            t1= threading.Thread(target=Add_Client, args=((server,clients,log, status)))
            t1.start()
            t1.join()
        else:
            print("server failed")
        print("server finished")
        log.writeInfo("Server Closed")
    except Exception:
        log.writeFatal()
    finally:
        if server:
            Close_Server(server, clients)
        log.closeLog()
        
def Create_Server(log: Log.Log) -> socket.socket:
    try: 
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((IP,PORT))
        server.listen(10)
        server.settimeout(10)
        log.writeInfo("Server Created Successfully")
        return server
    except Exception as e:
        log.writeFatal()

def Close_Server(server: socket.socket, clients: list):
    for client in clients:
        clients.remove(client)
        client[0].close()
    server.close()
        
def Add_Client(server: socket.socket, clients: list, log: Log.Log, status: ServerStatus) -> None:
    try:
        while status.GetServerStatus():
            try:
                conn: tuple = server.accept()
                clients.append(conn)
                log.writeInfo(f'New Client connected: {conn[1]} ')
                t = threading.Thread(target=Receive_Data, args=(server, clients, conn, log, status))
                t.start()
                print(f'New Client connected: {conn[1]} ')
            except TimeoutError:
                log.writeWarning("Server Timeout")
                if not status.GetServerStatus():
                    break
            except OSError:
                log.writeWarning("Server Interrupted")
                break
        t.join()
    except KeyboardInterrupt:
        print('Server interrupted')
    except Exception:
        log.writeFatal()

def Receive_Data(server: socket.socket, clients: list, client: tuple, log: Log.Log, status: ServerStatus) -> None:
    try: 
        while status.GetServerStatus():
            conn: socket.socket = client[0]
            try: 
                data = conn.recv(1024)
            except ConnectionAbortedError:
                break
            if data == b'':
                log.writeInfo(f'Client disconnected {client[1]}')
                print(f'Client disconnected')
                clients.remove(client)
                conn.close()
                break
            elif data == b'close':
                log.writeInfo("client is closing the server")
                Close_Server(server, clients)
                status.SetServerStatus(False)
                break
            else:
                print(f'{data}')
                log.writeInfo(f'Server Received {data} from {client[1]}')
    except Exception:
        log.writeFatal()
        
#async def Send_Messages(server: socket.socket, clients: list, log: Log.Log):
#    try:
#        while server:
#            message = input("")
#            for client in clients:
#                conn, addr = client
#                conn.send(message.encode())
#                log.writeInfo(f'Sent message "{message}" to address: {addr} ')
#    except Exception as e:
#        log.writeFatal()

if __name__ == "__main__":
    main()