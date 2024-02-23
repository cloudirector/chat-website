import socket
import threading

serverhost, serverport = "0.0.0.0", 1337

def handle_client(client_socket):
    while True:
        # Receive data from the client
        data = client_socket.recv(1024)
        if not data:
            break

        # Process the received data (you can modify this part as needed)
        processed_data = data.upper()

        # Send the processed data back to the client
        client_socket.send(processed_data)

    # Close the connection with the client
    client_socket.close()

def start_server():
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a specific address and port
    server_socket.bind((serverhost, serverport))

    # Listen for incoming connections
    server_socket.listen(5)
    print(f"[*] Listening on {serverhost}:{serverport}")

    while True:
        # Accept a connection from a client
        client_socket, addr = server_socket.accept()
        print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")

        # Create a new thread to handle the client
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

start_server()
