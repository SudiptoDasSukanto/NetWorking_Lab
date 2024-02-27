
import socket             

def isPalindrome(s):
    return s == s[::-1]
s = socket.socket()         
print ("Socket successfully created")
 
port = 2947          
 

s.bind(('', port))         
print ("socket binded to %s" %(port)) 
 
# put the socket into listening mode 
s.listen(5)     
print ("socket is listening")            
 
# a forever loop until we interrupt it or 
# an error occurs 
c, addr = s.accept()     
print ('Got connection from', addr )
error = 0 
for i in range(100): 
    recevRand=c.recv(1024).decode()
    recevRand = int(recevRand)
    if(recevRand<=30) :
        error+=1
error_str = str(error)
c.send(error_str.encode())     
print("In server site error percentage : " + error_str + "%")


    
    
    
    # ans = isPalindrome(mass)
    
    # if ans:
    #     print("Yes")
    #     c.send("yes".encode())
        
    # else:
    #     print("No")
    #     c.send("no".encode())
    # print(c.recv(1024).decode())
    
    # num = int(mass)
    # if num > 1:
    #     for i in range(2, int(num/2)+1):
    #         if (num % i) == 0:
    #             print(num, "is not a prime number")
    #             c.send("no".encode())
    #             break
    #     else:
    #         print(num, "is a prime number")
    #         c.send("yes".encode())
            
    # else:
    #     print(num, "is not a prime number")
    #     c.send("no".encode())
    
    # print(c.recv(1024).decode())
    
    
    # if mass=='D':
    #     c.send("give me a ammount".encode())
    #     amm=c.recv(1024).decode()
    #     yoo=int(amm)
    #     ammount=ammount+yoo
    #     jj=str(ammount)
    #     c.send(jj.encode())
    
    # elif mass=='W':
    #     c.send("give me a ammount".encode())
    #     amm=c.recv(1024).decode()
    #     yoo=int(amm)
    #     ammount=ammount-yoo
    #     jj=str(ammount)
    #     c.send(jj.encode())

    
