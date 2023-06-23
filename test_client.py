import socket

def main():
    # Server information
    server_ip = "X"
    server_port = 2088

    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # AF_INET indicates the socket will use IPv4 addressing
    # SOCK_STREAM indicates the socket will use TCP protocol
    
    try:
        # Connect to the server
        client_socket.connect((server_ip, server_port))
        print("Connected to the server.")

        # Send data to the server
        message = "Hello, server!"
        client_socket.sendall(message.encode())
        # The message string is encoded into bytes using the UTF-8 encoding before sending
        print("Sent data to the server:", message)

        # Receive data from the server
        received_data = client_socket.recv(1024).decode()
        # The recv() method receives data from the server with a buffer size of 1024 bytes
        # The received bytes are decoded using the UTF-8 encoding to convert them back into a string
        print("Received data from the server:", received_data)

    except ConnectionRefusedError:
        print("Connection refused. Make sure the server is running.")

    finally:
        # Close the socket
        client_socket.close()
        print("Socket closed.")

if __name__ == "__main__":
    main()
