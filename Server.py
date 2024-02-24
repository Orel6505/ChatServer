import socket

IP = "127.0.0.1"
PORT = 8081
def main():
    try: 
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP
        server.bind((IP,PORT))
        server.listen(2)
            
    except Exception as e:
        print("The Error is: " + e)
    finally:
        server.close()
        
    

if __name__ == "__main__":
    main()