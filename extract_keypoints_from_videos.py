import os
import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False)
DATA_DIR = 'data/'
SAVE_DIR = 'keypoints_data/'
SEQUENCE_LENGTH = 30
EXPECTED_KEYPOINTS = 33 * 2  # 33 landmarks × (x, y)

def extract_video_keypoints(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"❌ Failed to open: {video_path}")
        return []

    sequence = []
    keypoints_sequence = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(frame_rgb)

        keypoints = []
        if results.pose_landmarks:
            for lm in results.pose_landmarks.landmark:
                keypoints.extend([lm.x, lm.y])
            if len(keypoints) != EXPECTED_KEYPOINTS:
                # Fallback in case landmarks are fewer than expected
                keypoints = [0.0] * EXPECTED_KEYPOINTS
        else:
            keypoints = [0.0] * EXPECTED_KEYPOINTS

        sequence.append(keypoints)

        # Only store when we have a full 30-frame sequence
        if len(sequence) == SEQUENCE_LENGTH:
            keypoints_sequence.append(sequence)
            sequence = []

    cap.release()
    return np.array(keypoints_sequence)  # shape: (N, 30, 66)

# Run on all videos
for label in ['fight', 'non_fight']:
    path = os.path.join(DATA_DIR, label)
    if not os.path.exists(path):
        print(f"⚠️ Directory not found: {path}")
        continue

    for video_file in os.listdir(path):
        if not video_file.endswith(('.mp4', '.avi', '.mov')):
            continue  # skip non-video files

        video_path = os.path.join(path, video_file)
        keypoints_batches = extract_video_keypoints(video_path)

        # Skip if extraction failed or empty
        if len(keypoints_batches) == 0:
            print(f"⚠️ Skipped empty or invalid: {video_file}")
            continue

        label_folder = os.path.join(SAVE_DIR, label)
        os.makedirs(label_folder, exist_ok=True)

        for idx, keypoints in enumerate(keypoints_batches):
            if keypoints.shape != (SEQUENCE_LENGTH, EXPECTED_KEYPOINTS):
                print(f"⚠️ Wrong shape {keypoints.shape} in {video_file}, skipping...")
                continue

            filename = f"{os.path.splitext(video_file)[0]}_{idx}.npy"
            filepath = os.path.join(label_folder, filename)
            np.save(filepath, keypoints)

print("✅ Keypoints extraction complete.")
