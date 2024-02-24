import socket

IP = "127.0.0.1"
PORT = 8081
def main():
    try: 
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server: #TCP
            server.bind((IP,PORT))
            server.listen(2)
            conn, addr = server.accept()
            with conn:
                print(f"Connected by {addr}")
    except Exception as e:
        print("The Error is: " + e)
        
    

if __name__ == "__main__":
    main()