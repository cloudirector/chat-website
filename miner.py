import socket
import json
from hashing import *

serverhost, serverport = "0.0.0.0", 1337

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((serverhost, serverport))
    while True:
        message = input("Enter a message (or 'exit' to quit): ")
        if message.lower() == "exit":
            client_socket.send(message.encode())
            break
        elif message.lower() == "solveblock":
            client_socket.send("getblock".encode())
            block_json = client_socket.recv(1024).decode()
            print(f"[*] Recived block! ({len(block_json)})")
            block = json.loads(block_json)
            print(f"solving with difficulty: {block['header']['difficulty']}")
            input()
            while True:
                block['header']["nonce"] = block['header']["nonce"] + 1
                hash = sha256(json.dumps(block))
                print(f"({hash})[{block['header']['nonce']}]")
                if hash.startswith("0000"):
                    print(f"Solved! ({hash})")
                    input()
                    break
        else:        
            client_socket.send("getblock".encode())
            data = client_socket.recv(1024)
            print(f"Received from server: {data.decode()}")
    client_socket.close()

start_client()