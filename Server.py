import socket, Log

IP = "127.0.0.1"
PORT = 8081
def main():
    try: 
        log = Log.Log("Server", newFileLog=False)
        server = Create_Server(log)
        conn, addr = []
        conn.append(server.accept())
        with conn:
            while True:
                log.writeInfo(f"Server is connected to {addr}")
                data = conn.recv(1024)
                log.writeInfo(f'Server Received {data}')
                if not data:
                    raise ValueError("Data Is Null")
                conn.sendall(data)
    except Exception:
        log.writeFatal()
    finally:
        log.closeLog()
        server.close()
        
def Create_Server(log: Log) -> socket:
    try: 
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((IP,PORT))
        server.settimeout(60)
        server.listen(2)
        log.writeInfo("Server Created Successfully")
        return server
    except Exception as e:
        log.writeFatal()

if __name__ == "__main__":
    main()