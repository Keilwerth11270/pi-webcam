import cv2

# Create a VideoCapture object to access the webcam
capture = cv2.VideoCapture(0)  # 0 represents the default webcam, change if necessary

# Check if the webcam is opened successfully
if not capture.isOpened():
    print("Failed to open webcam")
    exit()

# Read and display video frames from the webcam
while True:
    ret, frame = capture.read()
    # Read a frame from the camera
    # The capture.read() method returns two values: ret (a boolean indicating if the frame was successfully read)
    # and frame (the captured frame itself)

    if not ret:
        break
    # If the frame could not be read (ret is False), exit the loop

    # Display the frame in a window with the title "Webcam"
    cv2.imshow("Webcam", frame)

    # Wait for a key press for 1 millisecond, and check if the 'q' key is pressed
    if cv2.waitKey(1) == ord('q'):
        break

# Release the VideoCapture object to free up resources
capture.release()

# Close all OpenCV windows
cv2.destroyAllWindows()