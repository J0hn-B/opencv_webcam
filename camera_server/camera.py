import cv2
from flask import Flask, Response
import socket

# A Flask-based application enabling real-time sharing of laptop camera feed over HTTP for development purposes.

##### Variables

camera_feed = 0  # 0 for built-in camera, 1 for usb/external camera
local_port = 5000  # Port to run the server on

#####

# Create a Flask app
app = Flask(__name__)

# Create a video capture object
camera = cv2.VideoCapture(camera_feed)

if not camera.isOpened():
    print("Error: Could not open video.")
    exit()

# Get the ip address of the machine
hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)
print("Local IP: ", local_ip)


# Function to check if a port is in use: true || false
def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("localhost", port)) == 0


# Check if port is in use
if is_port_in_use(local_port):
    print(
        "Port %s is in use. Please close the application that is using the port."
        % local_port,
    )
    exit()
else:
    available_port = local_port


def generate_frames():
    while True:
        # Read a frame from the video stream
        ret, frame = camera.read()

        # Resize the frame
        frame = cv2.resize(frame, (640, 480))  # Change to desired dimensions if needed

        # Check if the frame is successfully read
        if not ret:
            print("--(!)Error reading frame")
            break

        # Convert the frame to JPEG format (necessary for streaming the video over HTTP)
        ret, buffer = cv2.imencode(".jpg", frame)
        if not ret:
            break

        # Yield the JPEG-encoded frame
        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" + buffer.tobytes() + b"\r\n"
        )


# The route that returns the video stream
@app.route(
    "/"
)  # to access the video stream from a different route (e.g. /video), change the route to "/"
def video_feed():
    return Response(
        generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame"
    )


# Clean up when the server is stopped
def cleanup(exception=None):
    print("Releasing the camera")
    camera.release()
    cv2.destroyAllWindows()


# Start the server
print("Starting the server")
if __name__ == "__main__":
    try:
        app.run(host=local_ip, port=available_port, debug=False)
    except KeyboardInterrupt:
        cleanup()  # Clean up when Ctrl-C is pressed
