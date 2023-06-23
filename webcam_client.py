import socket
import cv2
import struct
import numpy as np
import os

# Set up the socket for communication
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Create a socket object with AF_INET (IPv4) address family and SOCK_STREAM (TCP) type

# In the case of a webcam server, where real-time video streaming is involved, using UDP (User Datagram Protocol) could be an alternative. 
# UDP is a connectionless and unreliable protocol that does not guarantee data delivery or order. 
# It is often used in situations where real-time data transmission is more important than reliability, 
# such as video streaming or online gaming. UDP can be faster than TCP due to its lower overhead, but it may 
# result in packet loss or out-of-order delivery.

# server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_ip = 'X'  # Server IP address
server_port = 2099  # Server port number

# Connect to the server
client_socket.connect((server_ip, server_port))

# Function to receive and display framesq
def receive_frame():
    screenshot_dir = 'screenshots'
    # Set the directory name for storing screenshots.

    screenshot_counter = 1  
    # Initialize the screenshot counter

    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)
    # If the screenshot directory doesn't exist, create it.
    # os.path.exists() checks if the specified directory path exists.
    # os.makedirs() creates the directory if it doesn't exist.

    while True:
        try:
            # Receive frame size
            size_bytes = client_socket.recv(4)
            # Receive 4 bytes (32 bits) of data from the client socket.
            # client_socket.recv(4) receives data from the socket.
            # The received data is stored in the size_bytes variable.

            if not size_bytes:
                break
            # If size_bytes is empty (no data received), break the loop.

            frame_size = struct.unpack('>I', size_bytes)[0]
            # Unpack the received binary data (size_bytes) using the '>I' format.
            # struct.unpack() interprets the packed binary data according to the specified format.
            # '>I' represents a big-endian unsigned integer of size 4 bytes (32 bits).
            # [0] is used to access the first element of the unpacked data, which represents the frame size.

            frame_data = b''
            # Initialize an empty byte string to store the received frame data.

            while len(frame_data) < frame_size:
                data = client_socket.recv(frame_size - len(frame_data))
                # Receive the remaining frame data by subtracting the length of the received frame data from the expected frame size.
                # The received data is stored in the data variable.

                if not data:
                    break
                # If no data is received, break the loop.

                frame_data += data
                # Append the received data to the frame_data byte string.

            if len(frame_data) == 0:
                break
            # If the received frame data is empty, break the loop.

            frame_np = np.frombuffer(frame_data, dtype=np.uint8)
            # Convert the frame data byte string to a NumPy array of type uint8.
            # np.frombuffer() creates a NumPy array from the provided buffer object (frame_data).
            # dtype=np.uint8 specifies that the array elements should be of unsigned 8-bit integer type.

            frame = cv2.imdecode(frame_np, cv2.IMREAD_COLOR)
            # Decode the NumPy array (frame_np) as an image using OpenCV's imdecode() function.
            # cv2.imdecode() reads the image data from a buffer and returns it as an image.
            # The second argument, cv2.IMREAD_COLOR, indicates that the image should be loaded in color format.

            if frame is not None:
                cv2.imshow('Video', frame)
            # Display the received frame in a window titled 'Video'.
            # cv2.imshow() is used to display an image in a window.
            # The 'Video' window shows the frame if it is not None.

            # Check if the key 'p' is pressed
            if cv2.waitKey(1) & 0xFF == ord('p'):
                # Generate the screenshot file name with an incremented counter
                screenshot_name = os.path.join(screenshot_dir, f'screenshot{str(screenshot_counter)}.png')
                
                # Save the current frame as a screenshot
                cv2.imwrite(screenshot_name, frame)
                
                # Print a message indicating the successful saving of the screenshot
                print("Screenshot saved:", screenshot_name)
            
                # Increment the screenshot counter for the next screenshot
                screenshot_counter += 1


            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            # If the 'q' key is pressed, break the loop and exit the program.
            # cv2.waitKey(1) waits for a key event for 1 millisecond and returns the key value.
            # If the returned key value is equal to the ASCII value of 'q' (ord('q')), break the loop.

        except Exception as e:
            print("Error receiving frame:", str(e))
            break
            # If an exception occurs during the frame receiving process, print the error message and break the loop.

    client_socket.close()
    # Close the client socket connection.
    # client_socket.close() is used to terminate the socket connection.

    cv2.destroyAllWindows()
    # Close any active OpenCV windows.
    # cv2.destroyAllWindows() destroys all the created windows.


# Call the function to start receiving and displaying frames
receive_frame()
