import socket

def request_for_file(server_address,port,file_name):
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect((server_address,port))    
    client.send(file_name.encode())
    with open(file_name,'wb') as file:
        data = client.recv(1024)
        while data:
            file.write(data)
            data = client.recv(1024)
    print(f"File {file_name} received successfully.")
    client.close()

if __name__ == "__main__":
    server_address = "192.168.137.144"
    port = 2947
    file_name = input("Enter file name which you want to download : ")
    request_for_file(server_address,port,file_name)