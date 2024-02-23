import socket

serverhost, serverport = "0.0.0.0", 1337

def start_client():
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    client_socket.connect((serverhost, serverport))

    while True:
        # Send data to the server
        message = input("Enter a message (or 'exit' to quit): ")
        client_socket.send(message.encode())

        if message.lower() == 'exit':
            break

        # Receive and print the response from the server
        data = client_socket.recv(1024)
        print(f"Received from server: {data.decode()}")

    # Close the connection
    client_socket.close()

start_client()