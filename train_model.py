import os
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib  # for saving the model

DATA_PATH = 'keypoints_data'

def load_data():
    X, y = [], []
    for label, class_id in zip(['fight', 'non_fight'], [1, 0]):
        class_path = os.path.join(DATA_PATH, label)
        print(f"Reading from: {class_path}")  # ✅ Check directory
        if not os.path.exists(class_path):
            print(f"⚠️ Folder not found: {class_path}")
            continue
        for file in os.listdir(class_path):
            if file.endswith('.npy'):
                data = np.load(os.path.join(class_path, file), allow_pickle=True)
                flat = data.flatten()
                if flat.shape[0] == 1980:  # 66 keypoints * 30 frames
                    X.append(flat)
                    y.append(class_id)
                else:
                    print(f"⚠️ Skipped {file}: wrong shape {flat.shape}")
    print(f"✅ Total samples loaded: {len(X)}")
    return np.array(X), np.array(y)


def train():
    X, y = load_data()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    print(classification_report(y_test, y_pred))

    # Save the model
    joblib.dump(clf, 'fight_detector_model.pkl')
    print("✅ Model saved as fight_detector_model.pkl")

if __name__ == "__main__":
    train()
