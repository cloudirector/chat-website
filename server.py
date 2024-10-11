import socket
import threading
import signal
import sys
import json
from hashing import *
import sys

serverHost, serverPort = "0.0.0.0", int(sys.argv[1])

# fake block array and difficulty for testing aswell as dumping to json
test_difficulty = 2
test_block = {
    "header": {
        "nonce": 0,
        "difficulty": test_difficulty,
        "prevhash":
        "fe976ece5bdd1bc27958bca70345018da1d37cd9d2ff0b02458c90884dfe99fa",
        "hash": "",
        "timestamp": 1120602139
    },
    "body": {
        "messages": {
            "announcements": [{
                "timestamp": 1120602139,
                "username": "admin",
                "message": "testing"
            }],
            "general": [{
                "timestamp": 1120602139,
                "username": "admin",
                "message": "hello god"
            }, {
                "timestamp": 1120602139,
                "username": "god",
                "message": "what the fuck do you want"
            }]
        }
    }
}
test_block_json = json.dumps(test_block)


def errorPrint(error):
    print(f"[?] What the sigma!\n {error}")


def handleMiner(minerSocket, addr):
    # main loop
    minerSocket.send("Connected as miner".encode())
    while True:
        # set data var and break if empty, process if not
        data = minerSocket.recv(1024).decode()
        if not data:
            minerSocket.send("no data provided".encode())
        else:
            print(f"[+] Received data: {data}")
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
                print(f"[#] verifyhash (server)({tempblockhash})[{hashnonce}]")
                print(f"[#] verifyhash (miners)({blockname})[{hashnonce}]")
                if tempblockhash == blockname:
                    if tempblockhash.startswith("0" * test_difficulty):
                        print(f"Solved! ({tempblockhash})")
                        minerSocket.send("valid, good job!".encode())
                    else:
                        print(f"invalid difficulty")
                else:
                    print(f"invalid hash")
            elif data.lower() == "ping":
                minerSocket.send("pong".encode())
            elif data.lower() == "exit":
                minerIndex = miners.index([minerSocket, addr])
                print(
                    f"[x] Miner {minerIndex} disconnected ({addr[0]}:{addr[1]})"
                )
                miners.pop(minerIndex)
                minerSocket.close()
                break
            else:
                try:
                    minerSocket.send("None".encode())
                except Exception as error:
                    errorPrint(error)


def handleClient(clientSocket, addr):
    clientSocket.send("Connected as client".encode())
    try:
        while True:
            # set data var and break if empty, process if not
            data = clientSocket.recv(1024).decode()
            if not data:
                clientSocket.send("no data provided".encode())
            else:
                print(f"[+] Received data: {data}")
                if data.lower() == "getblock":
                    clientSocket.send(test_block_json.encode())
                elif data.lower().startswith("message":
                    # process this shit bruh
                    pass
                elif data.lower() == "ping":
                    clientSocket.send("pong".encode())
                elif data.lower() == "exit":
                    clientIndex = clients.index([clientSocket, addr])
                    print(
                        f"[x] Client {clientIndex} disconnected ({addr[0]}:{addr[1]})"
                    )
                    clients.pop(clientIndex)
                    clientSocket.close()
                    break
                else:
                    try:
                        clientSocket.send("None".encode())
                    except Exception as error:
                        errorPrint(error)
    except Exception as error:
        errorPrint(error)


def startServer(serverhost, serverport):
    # init socket, bind, then start listening
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((serverhost, serverport))
    server_socket.listen(5)
    print(f"[*] Listening on {serverhost}:{serverport}")

    try:
        # check for clients and start threads
        global miners
        global clients
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
                    print(
                        f"[+] Miner {miners.index([socketStart, addr])} connected ({addr[0]}:{addr[1]})"
                    )
                    minerHandler = threading.Thread(target=handleMiner,
                                                    args=(socketStart, addr))
                    minerHandler.start()
                    break
                elif socketType.startswith("client"):
                    # add check for append
                    clients.append([socketStart, addr])
                    print(
                        f"[+] Client {clients.index([socketStart, addr])} connected ({addr[0]}:{addr[1]})"
                    )
                    clientHandler = threading.Thread(target=handleClient,
                                                     args=(socketStart, addr))
                    clientHandler.start()
                    break
                else:
                    socketStart.send("Invalid socketType".encode())
                    socketStart.close()
                    break
    # process keyboard interrupt for exit
    except KeyboardInterrupt:
        print("\n[*] Server is shutting down...")
        serverSocket.close()
        sys.exit(0)


# start server with signal processing
signal.signal(signal.SIGINT, lambda signal, frame: sys.exit(0))
startServer(serverHost, serverPort)
