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
fight/
├── pycache/
├── app/ # Flask application logic
├── archive (34)/ # Archived files (videos, logs, etc.)
├── campusRecordedFight/ # Saved campus fight recordings
├── data/ # Preprocessed or raw data
├── keypoints_data/ # Keypoints extracted for ML models
├── Real Life Violence Dataset/
├── real life violence situations/
├── static/ # Static files (images, CSS, etc.)
│ └── images/
├── templates/ # HTML templates (Jinja2)
│ ├── index.html
│ ├── about.html
│ ├── benefits.html
├── fight_detector_model.pkl # Pre-trained model
├── extract_keypoints_from_videos.py
├── fight_videos.py
├── formalFight.py
├── real_time_fight_detection.py
├── train_model.py
└── README.md

