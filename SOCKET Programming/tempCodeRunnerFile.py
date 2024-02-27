import socket			 

# Create a socket object 
s = socket.socket()		 

# Define the port on which you want to connect 
port = 2947			

# connect to the server on local computer 
s.connect(('192.168.232.71', port)) 

# receive data from the server and decoding to get the string.
while True:
    message = input()
    
    s.send(message.encode())
    print (s.recv(1024).decode())
    # reply = input()
    # s.send(reply.encode())
    
s.close()	 
	
