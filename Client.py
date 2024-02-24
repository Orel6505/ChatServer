import socket, Log

IP = "127.0.0.1"
PORT = 8081

def main():
    try:
        log = Log.Log("Client.txt")
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(60)
        log.Write_Logfile('I',f'Client Created')
        client.connect((IP,PORT))
        client.sendall(b'Hello, world')
        data = client.recv(1024)
        log.Write_Logfile('I',f'Client sent server {data}')
    except Exception as e:
        log.Write_Logfile("E", f'The Error is: {e}')
    finally:
        log.Close_Logfile()
        client.close()

if __name__ == "__main__":
    main()