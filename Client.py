import socket, Log

IP = "127.0.0.1"
PORT = 8081

def main():
    try:
        log = Log.Log("Client", newFileLog=False)
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(60)
        log.writeInfo(f'Client Created')
        client.connect((IP,PORT))
        client.sendall(b'Hello, world')
        data = client.recv(1024)
        log.writeInfo(f'Client sent server {data}')
    except Exception as e:
        log.writeFatal()
    finally:
        log.closeLog()
        client.close()

if __name__ == "__main__":
    main()