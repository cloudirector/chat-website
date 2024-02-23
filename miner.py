import socket
from hashing import *

serverhost, serverport = "0.0.0.0", 1338

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((serverhost, serverport))
    while True:
        message = input("Enter a message (or 'exit' to quit): ")
        client_socket.send(message.encode())
        if message.lower() == 'exit':
            break
        data = client_socket.recv(1024)
        print(f"Received from server: {data.decode()}")
    client_socket.close()

start_client()