import socket
import json
import time
import sys
from hashing import *

serverHost, serverPort = "0.0.0.0", int(sys.argv[1])

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

def startMiner():
    try:
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSocket.connect((serverHost, serverPort))
        if verify(serverSocket, "miner"):
            connected = True
    except Exception as error:
        print(f"Failed to Connect:\n {error}")
        connected = False

    while connected:
        message = input("Enter a message (or 'exit' to quit): ")
        if message.lower() == "exit":
            serverSocket.send(message.encode())
            connected = False
            break
        elif message.lower() == "solveblock":
            # get block from server
            serverSocket.send("getblock".encode())
            block_json = serverSocket.recv(1024).decode()
            print(f"[*] Received block! ({len(block_json)})")
            # load dict from json and get block data
            block = json.loads(block_json)
            blockDifficulty = block['header']['difficulty']
            print(f"Solving with difficulty: {blockDifficulty} ({'0'*blockDifficulty})")
            input("Awaiting Input...")
            # init nonce and start main loop
            nonce = 0
            hashCount = 0
            startTime = time.time()
            while True:
                # hash block after incrementing nonce and changing block header
                nonce = nonce + 1
                block['header']["nonce"] = nonce
                hash = sha256(json.dumps(block))
                hashCount = hashCount + 1
                if hashCount % 100 == 0:
                    print(f"Calcuated {hashCount} hashes")
                # print(f"({hash})[{nonce}]")
                # check if hash matches set difficulty
                if hash.startswith("0"*blockDifficulty):
                    # if solved validate it on the server
                    endTime = time.time()
                    elapsedTime = endTime - startTime
                    print(f"[*] Solved: ({hash}) ({elapsedTime}s)")
                    serverSocket.send(f"verifyhash {hash} {nonce}".encode())
                    response = serverSocket.recv(1024).decode()
                    break
        else:
            # get block by default
            serverSocket.send(message.encode())
            data = serverSocket.recv(1024).decode()
            print(f"Received block from server: {data}")
        # disconnect after processing
    else:
        serverSocket.close()
        print("Disconnected :P")
    serverSocket.close()

startMiner()