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
            Echo_Client_Connected(log, addr)
    except Exception as e:
        print("The Error is: " + e)
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
        
def Echo_Client_Connected(log: Log, addr: str):
    log.Write_Logfile("I", f"Server is connected to {addr}")
        
if __name__ == "__main__":
    main()