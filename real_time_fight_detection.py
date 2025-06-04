import cv2
import numpy as np
import mediapipe as mp
import joblib
from collections import deque
import datetime
import os
import time
from app import insert_video_to_db  # Flask app function for DB insert

# Setup folder for saving videos
foldername = "static/campusRecordedFight"
os.makedirs(foldername, exist_ok=True)

# Load trained model
model = joblib.load('fight_detector_model.pkl')

# MediaPipe pose setup
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False)

# Constants
SEQUENCE_LENGTH = 30
KEYPOINTS_PER_FRAME = 66
sequence = deque(maxlen=SEQUENCE_LENGTH)

# Video capture setup
cap = cv2.VideoCapture(0)
fps = int(cap.get(cv2.CAP_PROP_FPS)) or 30
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

# Variables for recording and detection
recording = False
video_writer = None
record_start_time = None
fight_detected_start = None
consecutive_fight_secs = 4

def extract_keypoints(frame):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(frame_rgb)
    if results.pose_landmarks:
        keypoints = [val for lm in results.pose_landmarks.landmark for val in (lm.x, lm.y)]
        if len(keypoints) == KEYPOINTS_PER_FRAME:
            return keypoints
    # fallback if no landmarks or wrong length
    return [0.0] * KEYPOINTS_PER_FRAME

while True:
    ret, frame = cap.read()
    if not ret:
        break

    keypoints = extract_keypoints(frame)
    sequence.append(keypoints)
    label = "Analyzing..."

    if len(sequence) == SEQUENCE_LENGTH:
        input_data = np.array(sequence).flatten().reshape(1, -1)
        prediction = model.predict(input_data)[0]
        label = "FIGHT" if prediction == 1 else "NON-FIGHT"

        current_time = time.time()

        if label == "FIGHT":
            if fight_detected_start is None:
                fight_detected_start = current_time
            elif current_time - fight_detected_start >= consecutive_fight_secs and not recording:
                # Start recording
                recording = True
                record_start_time = current_time
                timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
                filename = f'FightDetected_{timestamp}.mp4'
                path = os.path.join(foldername, filename)
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                video_writer = cv2.VideoWriter(path, fourcc, fps, (frame_width, frame_height))
                print(f"[INFO] Recording started: {filename}")
        else:
            fight_detected_start = None

    # Record video if currently recording
    if recording:
        video_writer.write(frame)
        if time.time() - record_start_time >= 20:
            recording = False
            video_writer.release()
            video_writer = None
            print("[INFO] Recording stopped after 20 seconds.")
            # Insert filename into DB using Flask app function
            insert_video_to_db(filename)

    # Show prediction label on frame
    color = (0, 0, 255) if label == "FIGHT" else (0, 255, 0)
    cv2.putText(frame, f"Prediction: {label}", (30, 50), cv2.FONT_HERSHEY_SIMPLEX,
                1.2, color, 3)

    cv2.imshow("Real-time Fight Detection", frame)

    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        break

# Cleanup on exit
if video_writer:
    video_writer.release()
    insert_video_to_db(filename)

cap.release()
cv2.destroyAllWindows()
