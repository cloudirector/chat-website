import socket
import json
import time
import sys
from hashing import *

serverHost, serverPort = "0.0.0.0", int(sys.argv[1])

# something like hash verify for messages and users

def verify(serverSocket, socketType):
    verifyMessage = serverSocket.recv(1024).decode()
    serverSocket.send(socketType.encode())
    serverResponse = serverSocket.recv(1024).decode()
    print(f'Server: "{serverResponse}"')
    if serverResponse.startswith("Connected as"):
        return True
    elif serverResponse == "Invalid socketType":
        print("invaid client type")
        return False
    else:
        print("huh")
        return False

def startClient():
    print(f"Attempting to connect to ({serverHost})[{serverPort}]")
    try:
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSocket.connect((serverHost, serverPort))
        if verify(serverSocket, "client"):
            connected = True
        else:
            connected = False
    except Exception as error:
        print(f"Failed to Connect:\n {error}")
        connected = False
    while connected:
        message = input("Enter a message (or 'exit' to quit): ")
        if message.lower() == "exit":
            serverSocket.send(message.encode())
            break
        else:
            serverSocket.send(message.encode())
            data = serverSocket.recv(1024)
            print(f"Received message from server: {data.decode()}")
    else:
        print("Disconected :P")
        serverSocket.close()
    # disconnect after processing
    serverSocket.close()

startClient()