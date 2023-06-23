import socket

def main():
    # Server information
    server_ip = "X"
    server_port = 2088

    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # AF_INET indicates the socket will use IPv4 addressing
    # SOCK_STREAM indicates the socket will use TCP protocol for reliable, ordered communication

    # Bind the socket to a specific IP address and port
    server_socket.bind((server_ip, server_port))

    # Listen for incoming connections
    server_socket.listen()

    print("Server started. Waiting for client connections...")

    while True:
        # Accept a client connection
        client_socket, client_address = server_socket.accept()
        print("Client connected:", client_address)

        # Receive data from the client
        received_data = client_socket.recv(1024).decode()
        print("Received data from the client:", received_data)

        # Send data to the client
        message = "Hello, client!"
        client_socket.sendall(message.encode())
        print("Sent data to the client:", message)

        # Close the client socket
        client_socket.close()
        print("Client socket closed.")

if __name__ == "__main__":
    main()
