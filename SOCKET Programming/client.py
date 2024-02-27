import socket		
import random
import time	 

# Create a socket object 
s = socket.socket()		 

# Define the port on which you want to connect 
port = 2947	

# connect to the server on partner computer 
s.connect(('127.0.0.1', port)) 
client_error = 0
start_time = time.time()
for i in range(100):
    random_number = random.randint(1, 100)
    print(str(i) + "th number " + str(random_number))
    if(random_number<=30):
        client_error+=1
    random_number_str = str(random_number)
    s.send(random_number_str.encode())
end_time = time.time()
    
elapsed_time = end_time - start_time
server_error = s.recv(1024).decode()
client_error = str(client_error)
print("From server site error percentage : " + server_error + "%")
print("In client site error percentage : " + client_error + "%")

elapsed_time = str(elapsed_time)

print("Needed time for calculating error : " + elapsed_time)
    


s.close()	 
	
