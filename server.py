import socket
import threading
import signal
import sys
import json
from hashing import *
import sys

serverhost, serverport = "0.0.0.0", int(sys.argv[1])

# fake block array and difficulty for testing aswell as dumping to json
test_difficulty = 2
test_block = {
    "header": {
        "nonce": 0,
        "difficulty": test_difficulty,
        "prevhash": "fe976ece5bdd1bc27958bca70345018da1d37cd9d2ff0b02458c90884dfe99fa",
        "hash": "",
        "timestamp": 1120602139
    },
    "body": {
        "messages": {
            "announcements": [
                {"timestamp": 1120602139, "username": "admin", "message": "testing"}
            ],
            "general": [
                {"timestamp": 1120602139, "username": "admin", "message": "hello god"},
                {"timestamp": 1120602139, "username": "god", "message": "what the fuck do you want"}
            ]
        }
    }
}
test_block_json = json.dumps(test_block)

def handleMiner(minerSocket):
    # main loop
    while True:
        # set data var and break if empty, process if not
        data = minerSocket.recv(1024).decode()
        if not data:
            minerSocket.send("no data provided".encode())
        else:
            print(f"[*] Received data: {data}")
            # logic for block requests
            if data.lower() == "getblock":
                minerSocket.send(test_block_json.encode())
            # logic for verifying a hash
            elif data.lower().startswith("verifyhash "):
                # splitting request and create temp block to inject hashnonce
                command, blockname, hashnonce = data.split()
                tempblock = test_block
                tempblock["header"]["nonce"] = int(hashnonce)
                tempblockhash = sha256(json.dumps(tempblock))
                print(f"verify (server)({tempblockhash})[{hashnonce}]")
                print(f"verify (miners)({blockname})[{hashnonce}]")
                if tempblockhash == blockname:
                    if tempblockhash.startswith("0"*test_difficulty):
                        print(f"Solved! ({tempblockhash})")
                        minerSocket.send("valid, good job!".encode())
                    else:
                        print(f"invalid difficulty")
                else:
                    print(f"invalid hash")
            elif data.lower() == "ping":
                minerSocket.send("pong".encode())
            elif data.startswith("changeDiff"):
                if len(data.split(" ")) == 2:
                    nonceDiff = data.split(" ")[1]
                    test_difficulty = nonceDiff
                    print(f"[*] Updated diff to {test_difficulty})")
                    minerSocket.send(f"Updated Diff to {test_difficulty}".encode())
                else:
                    minerSocket.send("Invalid change request".encode())
            elif data.lower() == "exit":
                minerSocket.close()
                print(f"[x] Miner {miners.index([minerSocket, addr])} disconnected ({addr[0]}:{addr[1]})")
            else:
                try:
                    minerSocket.send("None".encode())
                except Exception as error:
                    print(f"what the sigma:\n {error}")
    minerSocket.close()

def handleClient(clientSocket):
    print("incomplete")
    
def start_server(serverhost, serverport):
    # init socket, bind, then start listening
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((serverhost, serverport))
    server_socket.listen(5)
    print(f"[*] Listening on {serverhost}:{serverport}")

    try:
        # check for clients and start threads
        miners = []
        clients = []
        while True:
            socketStart, addr = server_socket.accept()
            socketStart.send("Who are you?".encode())
            # add timer and verify
            while True:
                socketType = socketStart.recv(1024).decode()
                if socketType.startswith("miner"):
                    # add checks for append
                    miners.append([socketStart, addr])
                    print(f"[*] Miner {miners.index([socketStart, addr])} connected ({addr[0]}:{addr[1]})")
                    minerHandler = threading.Thread(target=handleMiner, args=(startSocket,))
                    minerHandler.start()
                elif socketType.startswith("client"):
                    # add check for append
                    clients.append([socketStart, addr])
                    print(f"[*] Client {miners.index([socketStart, addr])} connected ({addr[0]}:{addr[1]})")
                else:
                    socketStart.send("Invalid".encode())
                    socketStart.close()
    # process keyboard interrupt for exit
    except KeyboardInterrupt:
        print("\n[*] Server is shutting down...")
        server_socket.close()
        sys.exit(0)

# start server with signal processing
signal.signal(signal.SIGINT, lambda signal, frame: sys.exit(0))
start_server(serverhost, serverport)