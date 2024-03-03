import socket, Log

IP = "127.0.0.1"
PORT = 8081

def main():
    try:
        log = Log.Log("Client", newFileLog=False)
        client: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(60)
        log.writeInfo(f'Client Created')
        client.connect((IP,PORT))
        log.writeInfo(f'Client Connected to {IP}:{PORT}')
        msg="1"
        while msg != "-1":
            msg = input("")
            client.send(msg.encode())
            log.writeInfo(f'Client send {msg} to {IP}:{PORT}')
        #threading.Thread(target=send_data, args=(client)).start()
        #threading.Thread(target=recv_data, args=(client)).start()
    except Exception as e:
        log.writeFatal()
    finally:
        client.close()
        if not client:
            log.closeLog()
        
def send_data(client: socket.socket):
    while True:
        msg = input("")
        client.send(msg.encode())

def recv_data(client: socket.socket):
    while True:
        msg = client.recv(1024)
        print("[SERVER] " + msg.decode('utf-8'))

if __name__ == "__main__":
    main()