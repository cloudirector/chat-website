import socket
import threading
import signal
import sys
import json
from hashing import *

serverhost, serverport = "0.0.0.0", 1338

test_difficulty = 1
test_block = {
    "header": {
        "nonce": 0,
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
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        else:
            print(f"[*] Recived data: {data}")
        client_socket.send("OK".encode())
    client_socket.close()

def start_server(serverhost, serverport):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((serverhost, serverport))
    server_socket.listen(5)
    print(f"[*] Listening on {serverhost}:{serverport}")

    try:
        while True:
            client_socket, addr = server_socket.accept()
            print(f"[*] Started connection from {addr[0]}:{addr[1]}")
            client_handler = threading.Thread(target=handle_client, args=(client_socket,))
            client_handler.start()
    except KeyboardInterrupt:
        print("\n[*] Server is shutting down...")
        server_socket.close()
        sys.exit(0)

signal.signal(signal.SIGINT, lambda signal, frame: sys.exit(0))
start_server(serverhost, serverport)
