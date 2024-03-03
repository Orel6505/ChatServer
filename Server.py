import socket, Log, threading

IP = "127.0.0.1"
PORT = 8081
def main():
    try:
        clients = []
        log = Log.Log("Server", newFileLog=False)
        server = Create_Server(log)
        if server:
            t1= threading.Thread(target=Add_Client, args=((server,clients,log)))
            t2= threading.Thread(target=Receive_Data, args=((server,clients,log)))
            t1.start()
            t2.start()
            inpu = input("")
            t1.stop()
            t2.stop()
            t2.join()
            t1.join()
        else:
            print("server failed")
        print("server finished")
    except Exception:
        log.writeFatal()
    finally:
        server.close()
        if not server:
            log.closeLog()
        
def Create_Server(log: Log.Log) -> socket.socket:
    try: 
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((IP,PORT))
        server.listen(2)
        log.writeInfo("Server Created Successfully")
        return server
    except Exception as e:
        log.writeFatal()
        
def Add_Client(server: socket.socket, clients: list, log: Log.Log):
    try:
        while True:
            conn, addr = server.accept()
            clients.append((conn, addr))
            log.writeInfo(f'New Client connected: {addr} ')
            print(f'New Client connected: {addr} ')
    except Exception as e:
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
        
def Receive_Data(server: socket.socket, clients: list, log: Log.Log):
    while True:
        for client in clients:
            print(clients)
            conn = client[0]
            data = conn.recv(1024)
            print(f'{data}')
            if data == b'':
                log.writeInfo(f'Client disconnected {client[1]}')
                print(f'Client disconnected')
                clients.remove(client)
            else:
                log.writeInfo(f'Server Received {data} from')
            #except socket.error:
            #    clients.remove(client)
            #    log.writeInfo(f'Server Removed {client}')
            #    print(f'Client disconnected')
            #    break
            #except Exception as e:
            #    log.writeFatal()

if __name__ == "__main__":
    main()