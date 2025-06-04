import cv2
import numpy as np
import mediapipe as mp
import joblib
from collections import deque
import datetime
dateSave = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
foldername = "campusRecordedFight"
# Load the trained model
model = joblib.load('fight_detector_model.pkl')

# MediaPipe pose setup
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False)

# Constants
SEQUENCE_LENGTH = 30
KEYPOINTS_PER_FRAME = 66

# Initialize sequence buffer
sequence = deque(maxlen=SEQUENCE_LENGTH)

# Start webcam
cap = cv2.VideoCapture(0)  # Use 0 or 1 for external webcam

def extract_keypoints(frame):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(frame_rgb)

    if results.pose_landmarks:
        keypoints = []
        for lm in results.pose_landmarks.landmark:
            keypoints.extend([lm.x, lm.y])
        if len(keypoints) != KEYPOINTS_PER_FRAME:
            keypoints = [0.0] * KEYPOINTS_PER_FRAME
    else:
        keypoints = [0.0] * KEYPOINTS_PER_FRAME

    return keypoints

while True:
    ret, frame = cap.read()
    if not ret:
        break

    keypoints = extract_keypoints(frame)
    sequence.append(keypoints)

    if len(sequence) == SEQUENCE_LENGTH:
        input_data = np.array(sequence).flatten().reshape(1, -1)
        prediction = model.predict(input_data)[0]
        label = "FIGHT" if prediction == 1 else "NON-FIGHT"

        # Draw label
        cv2.putText(frame, f"Prediction: {label}", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                    1.2, (0, 0, 255) if label == "FIGHT" else (0, 255, 0), 3)

    cv2.imshow("Real-time Fight Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('s'):
        cv2.imwrite(f'{foldername}/CampusFightSaved_{dateSave}.jpg', frame)
    elif cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up
cap.release()
cv2.destroyAllWindows()   i want this to record a 10 secs video if it detect fighting