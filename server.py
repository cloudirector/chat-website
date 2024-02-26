import socket
import threading
import signal
import sys
import json
from hashing import *

serverhost, serverport = "0.0.0.0", 1338

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

def handle_client(client_socket):
    # main loop
    while True:
        # set data var and break if empty, process if not
        data = client_socket.recv(1024)
        if not data:
            break
        else:
            print(f"[*] Received data: {data}")
            # logic for block requests
            if data.decode().lower() == "getblock":
                client_socket.send(test_block_json.encode())
            # logic for verifying a hash
            elif data.decode().lower().startswith("verifyhash "):
                # splitting request and create temp block to inject hashnonce
                command, blockname, hashnonce = data.decode().split()
                tempblock = test_block
                tempblock["header"]["nonce"] = int(hashnonce)
                tempblockhash = sha256(json.dumps(tempblock))
                print(f"verify (server)({tempblockhash})[{hashnonce}]")
                print(f"verify (miners)({blockname})[{hashnonce}]")
                if tempblockhash == blockname:
                    if tempblockhash.startswith("0"*test_difficulty):
                        print(f"Solved! ({tempblockhash})")
                        client_socket.send("valid, good job!".encode())
                    else:
                        print(f"invalid difficulty")
                else:
                    print(f"invalid hash")
            elif data.decode().lower() == "ping":
                client_socket.send("pong".encode())
            else:
                client_socket.send(data.encode())
    client_socket.close()

def start_server(serverhost, serverport):
    # init socket, bind, then start listening
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((serverhost, serverport))
    server_socket.listen(5)
    print(f"[*] Listening on {serverhost}:{serverport}")

    try:
        # check for clients and start threads
        miners = []
        while True:
            client_socket, addr = server_socket.accept()
            miners.append([client_socket, addr])
            print(f"[*] Miner {miners.index([client_socket, addr])} connected ({addr[0]}:{addr[1]})")
            client_handler = threading.Thread(target=handle_client, args=(client_socket,))
            client_handler.start()
    # process keyboard interrupt for exit
    except KeyboardInterrupt:
        print("\n[*] Server is shutting down...")
        server_socket.close()
        sys.exit(0)

# start server with signal processing
signal.signal(signal.SIGINT, lambda signal, frame: sys.exit(0))
start_server(serverhost, serverport)
