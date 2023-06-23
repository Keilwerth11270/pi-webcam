import socket
import cv2
import struct
import numpy as np

# Set up the socket for communication
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Create a socket object with AF_INET (IPv4) address family and SOCK_STREAM (TCP) type

# In the case of a webcam server, where real-time video streaming is involved, using UDP (User Datagram Protocol) could be an alternative. 
# UDP is a connectionless and unreliable protocol that does not guarantee data delivery or order. 
# It is often used in situations where real-time data transmission is more important than reliability, 
# such as video streaming or online gaming. UDP can be faster than TCP due to its lower overhead, but it may 
# result in packet loss or out-of-order delivery.

# server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


host = '0.0.0.0'
# host = '0.0.0.0' allows the server to listen on all available network interfaces, 
# making it reachable from both the local machine and other devices on the network.
# host = '' restricts the server to listen only on the local loopback address, making it accessible only from the local machine itself.

port = 2099  # Server port number

# Bind the socket to a specific host and port
server_socket.bind((host, port))
# Bind the socket to the specified host and port number
# Binding associates the socket with a specific network address (host and port) on the Raspberry Pi

# Start listening for incoming connections
server_socket.listen(1)
# Start listening for incoming connections with a backlog of 1
# The backlog parameter specifies the maximum number of queued connections allowed

print("Waiting for incoming connection...")

# Accept a client connection
client_socket, addr = server_socket.accept()
print("Connected to client:", addr)
# Accept a client connection when it arrives and get the client socket and address
# The accept() method blocks until a connection is made

# Function to capture and send frames
def send_frame():
    # Open the webcam
    video_capture = cv2.VideoCapture(0)

    while True:
        # Capture frame from the webcam
        ret, frame = video_capture.read()
        # video_capture.read() reads the next frame from the webcam. 
        # It returns a tuple (ret, frame) where ret is a boolean indicating if the frame was successfully read and frame is the captured frame itself.
        # ret is True if a frame is read successfully, and False if there are no more frames to read or an error occurred.

        # Encode the frame as JPEG
        encoded_frame = cv2.imencode('.jpg', frame)[1]
        # cv2.imencode() encodes the frame as an image in the specified format (JPEG in this case).
        # It returns a tuple (retval, encoded_image) where retval is a boolean indicating if 
        # the encoding was successful and encoded_image is the encoded frame as a numpy array.
        # [1] is used to access the encoded frame, as the encoded image is returned as the second element of the tuple.

        # Calculate the size of the frame
        frame_size = len(encoded_frame)
        # len(encoded_frame) returns the number of bytes in the encoded frame, representing its size.

        try:
            # Send the frame size to the client
            client_socket.send(struct.pack('>I', frame_size))
            # struct.pack() packs the frame size into a binary format specified by the format string '>I'.
            # '>I' represents a big-endian unsigned integer of size 4 bytes (32 bits).
            # struct.pack('>I', frame_size) converts the frame size to a 4-byte binary representation according to the specified format.
            # The resulting binary data is then sent to the client via client_socket.

            # Send the frame data to the client
            client_socket.sendall(encoded_frame)
            # client_socket.sendall() sends the entire encoded frame data to the client.
            # It ensures that all the data is sent, even if it requires multiple send operations.

            # print("Frame size:", frame_size)
            # print("Frame sent")

        except Exception as e:
            print("Error sending frame:", str(e))
            break

    # Release the webcam and resources
    video_capture.release()
    # video_capture.release() releases the webcam resources.
    # It is necessary to release the webcam when you are done using it to free up system resources.

    client_socket.close()
    # client_socket.close() closes the client socket connection.
    # Closing the socket is important to release system resources and properly terminate the connection.

    cv2.destroyAllWindows()
    # cv2.destroyAllWindows() closes any active OpenCV windows.
    # It is useful to clean up any remaining windows after the program finishes execution.


# Call the function to start capturing and sending frames
send_frame()
