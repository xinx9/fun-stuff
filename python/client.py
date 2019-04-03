##############################################
##############################################
##                                          ##
##  Name: Brandon Burke                     ##
##                                          ##
##  Project Name: client.py                 ##
##                                          ##
##  Description: this program uses smtp     ##
##  over TCP to send an email to another    ##
##  authenticated user on the server        ##
##  this program also uses HTTP over UDP    ##
##  to read the users email                 ##
##                                          ##
##  Features:                               ##
##      login                               ##
##      write to server (TCP)               ##
##      read from server (UDP)              ##
##                                          ##
##############################################
##############################################
from socket import *
from threading import *
from select import select
import sys
import os
import datetime
import time
import _thread

MAX = 1024
if(len(sys.argv) != 3):
    print("\n> python3 server.py <HOST NAME> <PORT NUMBER>")
    sys.exit(1)


TCP_ServerAddr, UDP_ServerAddr = (sys.argv[1], int(sys.argv[2]))

######################################
##  Initialize Server Connection    ##
######################################
print("Would you like to send or recieve?")
sendOrRecieve = input().upper()
if(sendOrRecieve.find("SEND") == 0):
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect(TCP_ServerAddr)
    ##################
    #TCP interaction
    ##################
    while 1:
        #--------------------------------------------#
        cmsg = input(">")
        clientSocket.send(cmsg.encode())
        smsg = clientSocket.recv(MAX).decode()
        if(smsg.find("221 Bye") == 0):
            print(smsg)
            sys.exit()
        elif(smsg.find("334 username:") == 0):
            print(smsg)
            user = input()
            Euser = AuthenticateEncode(user)
            clientSocket.send(Euser.decode())
        elif(smsg.find("330") == 0):
            print("your password is: " + AuthenticateDecode(smsg.split()[1]))
            time.sleep(5)
        elif(smsg.find("334 password:") == 0 or smsg.find("535 re-enter password:") == 0):
            print(smsg)
            password = input()
            Epassword = AuthenticateEncode(password)
            clientSocket.send(Epassword)
        elif(smsg.find("354 Send message content; End with <CLRF>.<CLRF>") == 0):
            print(smsg)
            datamsg = []
            i = 0
            while True:
                data = input()
                if data == '.':
                    datamessage = "\n".join(datamsg)
                    clientSocket.send(datamessage.encode())
                    break
                else:
                    datamsg.append(data)
        else:
            print(smsg)
        #--------------------------------------------#    
    clientSocket.close()
    sys.exit()
#########################################
elif(sendOrRecieve.find("RECIEVE") == 0):
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    init = "200 Ready"
    clientSocket.sendto(init.encode(), UDP_ServerAddr)
    auth = clientSocket.recvfrom(MAX)
    
    if(auth.decode() == "200"):
        username = input("username: ")
        password = input("password: ")
        Eusername = AuthenticateEncode(username)
        clientSocket.sendto(Eusername.encode(), UDP_ServerAddr)
        Epassword = AuthenticateEncode(password)
        clientSocket.sendto(Epassword.encode(), UDP_ServerAddr)
        valid = clientSocket.recvfrom(MAX)
        if(valid.decode() == "250 OK")
            Print(valid.decode())
        elif(valid.decode() == "535"):
            while(valid.decode() != "250 OK"):
                print("Invalid Credentials please Re-enter:\n")
                username = input("username: ")
                password = input("password: ")
                Eusername = AuthenticateEncode(username)
                clientSocket.sendto(Eusername.encode(), UDP_ServerAddr)
                Epassword = AuthenticateEncode(password)
                clientSocket.sendto(Epassword.encode(), UDP_ServerAddr)
                valid = clientSocket.recvfrom(MAX)
            print(valid.decode())
    data = clientSocket.recvfrom(MAX)
    data = data.decode()
    if(data == "250 Download")
        lines = []
        while True:
            line = input()
            if line:
                lines.append(line)
            else:
                break
        message = "\n".join(lines)
        print(message)
        clientSocket.sendto(message.encode(),UDP_ServerAddr)
        modifiedMessage = clientSocket.recvfrom(MAX)
        print(modifiedMessage.decode())
        sys.exit()
    elif(data == "404: directory not found")
else:
    print("invalid selection")
    sys.exit()

##############################################
##  Encode/Decode text input with base64    ##
##  Cin = clear text input                  ## 
##  Sin = salted input                      ##   
##  Ein = encoded input                     ##  
##  Bin = binary input                      ##   
##############################################
def AuthenticateEncode(Cin):
    salt = "447"
    Sin = Cin + salt
    Bin = Sin.decode("utf-8")
    Ein = base64.b64encode(Bin)
    return Ein

def AuthenticateDecode(Ein):
    salt = "447"
    Ein = Ein[2:-1]
    Sin = base64.b64decode(Ein)
    Sin = Sin.decode("utf-8")
    Cin = Sin[:len(Sin)-3]
    return Cin
