import socket

IP = "127.0.0.1"
PORT = 8081

def main():
    try: 
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(60)
        client.connect((IP,PORT))
    except Exception as e:
        print("The Error is: " + e)
    finally:
        client.close()

if __name__ == "__main__":
    main()