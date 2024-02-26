import socket
import json
from hashing import *

serverhost, serverport = "0.0.0.0", 1338

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((serverhost, serverport))
    while True:
        message = input("Enter a message (or 'exit' to quit): ")
        if message.lower() == "exit":
            client_socket.send(message.encode())
            break
        elif message.lower() == "solveblock":
            # get block from server
            client_socket.send("getblock".encode())
            block_json = client_socket.recv(1024).decode()
            print(f"[*] Received block! ({len(block_json)})")
            # load dict from json and get block data
            block = json.loads(block_json)
            blockDifficulty = block['header']['difficulty']
            print(f"Solving with difficulty: {blockDifficulty} ({'0'*blockDifficulty})")
            input()
            # init nonce and start main loop
            nonce = 0
            while True:
                # hash block after incrementing nonce and changing block header
                nonce = nonce + 1
                block['header']["nonce"] = nonce
                hash = sha256(json.dumps(block))
                print(f"({hash})[{nonce}]")
                # check if hash matches set difficulty
                if hash.startswith("0"*blockDifficulty):
                    # if solved validate it on the server
                    print(f"Solved! ({hash})")
                    client_socket.send(f"verifyhash {hash} {nonce}".encode())
                    response = client_socket.recv(1024).decode()
                    input()
                    break
        else:        
            # get block by default
            client_socket.send("getblock".encode())
            data = client_socket.recv(1024)
            print(f"Received block from server: {data.decode()}")
    # disconnect after processing
    client_socket.close()

start_client()