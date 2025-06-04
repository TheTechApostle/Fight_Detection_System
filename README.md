# 🎥 Campus Fight Detection System

An intelligent surveillance system that leverages computer vision to automatically detect and log physical altercations on school campuses using real-time video feeds. This system empowers campus security by providing a centralized dashboard for reviewing and managing detected incidents.

---

## 📌 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Usage](#-usage)
- [Screenshots](#-screenshots)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

- 🎯 Real-time fight detection using computer vision models
- 📁 Automatic video recording and storage on detection
- 📊 Web dashboard to view, manage, and delete captured videos
- 🔍 Responsive interface with Bootstrap
- 🔐 Role-based user authentication (optional)
- 📜 Descriptive About and Benefits sections
- 🎨 Background image styling for better UX

---

## 🛠 Tech Stack

- **Backend**: Python, Flask
- **Computer Vision**: OpenCV, Custom Model
- **Frontend**: HTML, Bootstrap 5
- **Templating**: Jinja2
- **Deployment**: Localhost / Flask Server
- **Database (optional)**: SQLite / MySQL (if you track users)

---

## 📁 Project Structure
campus-fight-detection/
│
├── __pycache__/                     # Compiled Python files
│
├── app/                             # Main Flask app logic (e.g., routes, views)
│
├── archive (34)/                    # Archived resources (videos, documents, etc.)
│
├── campusRecordedFight/            # Directory for saving detected fight recordings
│
├── data/                            # Processed data for training or testing
│
├── keypoints_data/                 # Extracted keypoints from videos for model input
│
├── Real Life Violence Dataset/     # Original dataset of violence videos
│
├── real life violence situations/  # Additional dataset (raw videos or supplementary)
│
├── static/                          # Static assets (images, CSS, JS)
│   └── images/
│
├── templates/                       # HTML templates (Flask + Jinja2)
│   ├── index.html
│   ├── about.html
│   └── benefits.html
│
├── fight_detector_model.pkl         # Trained ML model for detecting fights
│
├── extract_keypoints_from_videos.py # Script for extracting pose/keypoint data
│
├── fight_videos.py                  # Script or module for processing or classifying videos
│
├── formalFight.py                   # Possibly pre-trained model runner or data formatter
│
├── real_time_fight_detection.py     # Main real-time detection script (OpenCV + ML)
│
├── train_model.py                   # Script for training the fight detection model
│
└── README.md                        # Project overview and documentation


