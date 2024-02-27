import socket
import threading


def fileTrans(client_socket):
    file_name = client_socket.recv(1024).decode()
    try:
        with open(file_name,'rb') as file:
            data = file.read(1024)
            while data:
                client_socket.send(data)
                data = file.read(1024)
    except FileNotFoundError:
        print(f"File {file_name} is not exist")
    finally:
        client_socket.close()


def start_server(port):
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind(('',port))
    server.listen(5)
    print(f"Server listing in port : {port}")
    while True:
        connection,address = server.accept()
        print(f"Connection built with the Client : {address}")
        multi_client = threading.Thread(target=fileTrans,args=(connection,))
        multi_client.start()

if __name__ == "__main__":
    port = 2947
    start_server(port)