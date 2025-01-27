from flask import Flask, render_template, Response, request, jsonify
import cv2
import threading
from pose2 import process_pose  # Import the pose processing function

app = Flask(__name__)

# Global variables for video handling
video_running = False
cap = None
processed_frame = None  # To store the processed frame
lock = threading.Lock()  # For thread-safe access to `processed_frame`

def video_processing():
    """
    Continuously capture video frames, process them with the pose detection logic,
    and store the processed frames in a global variable.
    """
    global cap, video_running, processed_frame

    while video_running:
        if cap and cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                continue

            # Process the frame using pose detection logic
            processed_frame_local = process_pose(frame)

            # Store the processed frame
            with lock:
                processed_frame = processed_frame_local
        else:
            break

def generate_frames():
    """
    Generate video frames for Flask endpoint.
    """
    global processed_frame

    while video_running:
        with lock:
            if processed_frame is None:
                continue
            frame = processed_frame.copy()

        # Encode the frame as JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue
        frame = buffer.tobytes()

        # Yield the frame as a response
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route("/")
def welcome():
    TITLE = "Exercise Pose Detection"
    return render_template("index.html", TITLE=TITLE)

@app.route('/about')
def about():
    return render_template('about.html')  

@app.route('/contact')
def contact():
    return render_template('contact.html')  

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html') 

@app.route('/home')
def home():
    return render_template('home.html')  

@app.route('/product')
def product():
    return render_template('product.html')  

@app.route('/checkout')
def checkout():
    return render_template('checkout.html') 

@app.route('/workout')
def workout():
    return render_template('workout.html')  

@app.route('/video_feed')
def video_feed():
    """
    Video streaming route.
    """
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/start_video_feed', methods=['POST'])
def start_video_feed():
    """
    Start the video feed and processing.
    """
    global video_running, cap

    if not video_running:
        video_running = True
        cap = cv2.VideoCapture(0)  # Start capturing video

        # Verify that the camera was successfully opened
        if not cap.isOpened():
            video_running = False
            return jsonify({'status': 'error', 'message': 'Could not access the webcam'})

        threading.Thread(target=video_processing, daemon=True).start()  # Start processing in a separate thread

    return jsonify({'status': 'started'})

@app.route('/stop_video_feed', methods=['POST'])
def stop_video_feed():
    """
    Stop the video feed and processing.
    """
    global video_running, cap

    if video_running:
        video_running = False
        if cap:
            cap.release()
            cap = None

    return jsonify({'status': 'stopped'})

if __name__ == "__main__":
    try:
        print("Starting Flask app...")
        app.run(debug=True)
    except Exception as e:
        print(f"Error starting Flask app: {e}")
