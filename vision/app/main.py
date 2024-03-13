import cv2

##### Variables

camera_feed = "" # example: http://192.168.0.10:5000

#####

# Open the video stream
cap = cv2.VideoCapture(camera_feed)

# If the video stream is successfully opened
try:
    # Loop to continuously read frames from the video stream
    while True:
        # Read a frame from the video stream
        ret, frame = cap.read()

        # Check if the frame is successfully read
        if not ret:
            print("--(!)Error reading frame")
            break

        # Display the frame
        cv2.imshow("Frame", frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
# if the user presses CTRL+C,
except KeyboardInterrupt:
    pass
# release the video stream and close all OpenCV windows
finally:
    print("==> Releasing the video stream and closing all OpenCV windows")
    # Release the video stream and close all OpenCV windows when CTRL+C is pressed
    cap.release()
    cv2.destroyAllWindows()
