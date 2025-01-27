import cv2
import mediapipe as mp
import numpy as np

# Mediapipe Pose Detection Setup
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.4, min_tracking_confidence=0.4)
drawing_utils = mp.solutions.drawing_utils

# Curl counter variables
counter = 0
stage = None

def calculate_angle(a, b, c):
    """
    Calculate the angle between three points.
    """
    a = np.array(a)  # First point
    b = np.array(b)  # Midpoint
    c = np.array(c)  # End point

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle

def process_pose(frame):
    """
    Process a single video frame for pose detection, drawing, and counting reps.
    """
    global counter, stage

    # Convert BGR to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_rgb.flags.writeable = False

    # Perform pose detection
    results = pose.process(frame_rgb)

    # Convert back to BGR
    frame_rgb.flags.writeable = True
    frame = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

    if results.pose_landmarks:  # Check if landmarks are detected
        try:
            # Extract pose landmarks
            landmarks = results.pose_landmarks.landmark

            # Get coordinates of key points
            shoulder = [
                landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y,
            ]
            elbow = [
                landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y,
            ]
            wrist = [
                landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y,
            ]

            # Calculate the angle
            angle = calculate_angle(shoulder, elbow, wrist)

            # Display the angle
            cv2.putText(
                frame,
                str(int(angle)),
                tuple(np.multiply(elbow, [640, 480]).astype(int)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 255),
                2,
                cv2.LINE_AA,
            )

            # Curl counter logic
            if angle > 140:
                stage = "down"
            if angle < 50 and stage == "down":
                stage = "up"
                counter += 1
                print(f"Counter: {counter}")

        except Exception as e:
            print(f"Error in processing pose landmarks: {e}")

    else:
        print("No landmarks detected in the frame.")

    # Render curl counter box
    cv2.rectangle(frame, (0, 0), (225, 73), (245, 117, 16), -1)
    cv2.putText(frame, 'REPS', (15, 12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
    cv2.putText(frame, str(counter), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, 'STAGE', (120, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), 1, cv2.LINE_AA)
    cv2.putText(frame, stage if stage else '-', (100, 70), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2, cv2.LINE_AA)

    # Draw pose landmarks
    if results.pose_landmarks:
        drawing_utils.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    return frame
