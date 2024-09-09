import socket
import json
import time
from hashing import *
import sys

serverhost, serverport = "0.0.0.0", int(sys.argv[1])

# something like hash verify for messages and users

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((serverhost, serverport))
    while True:
        message = input("Enter a message (or 'exit' to quit): ")
        if message.lower() == "exit":
            client_socket.send(message.encode())
            break
        else:
            client_socket.send(message.encode())
            data = client_socket.recv(1024)
            print(f"Received message from server: {data.decode()}")
    # disconnect after processing
    client_socket.close()

start_client()