import socket, Log

IP = "127.0.0.1"
PORT = 8081
def main():
    try: 
        log = Log.Log("Server.txt")
        server = Create_Server(log)
        server.listen(2)
        conn, addr = server.accept()
        with conn:
            log.Write_Logfile("I", f"Server is connected to {addr}")
            data = conn.recv(1024)
            log.Write_Logfile("I", f'Server Received {data}')
            if not data:
                raise ValueError("Data Is Null")
            conn.sendall(data)
    except Exception as e:
        log.Write_Logfile("E", f'The Error is: {e}')
    finally:
        log.Close_Logfile()
        server.close()
        
def Create_Server(log: Log) -> socket:
    try: 
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((IP,PORT))
        server.settimeout(60)
        log.Write_Logfile("I","Server Created")
        return server
    except Exception as e:
        log.Write_Logfile("E",f'Server Crashed with Error {e}')
        print(f'The Error is: {e}')

if __name__ == "__main__":
    main()