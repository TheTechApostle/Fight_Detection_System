from flask import Flask, render_template, send_from_directory, abort, request
import sqlite3
import os
import datetime

app = Flask(__name__)

# Constants
VIDEO_FOLDER = os.path.join('static', 'campusRecordedFight')
DATABASE = 'fight_videos.db'

# Ensure video folder exists
os.makedirs(VIDEO_FOLDER, exist_ok=True)

# Initialize database
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS videos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            datetime DATE NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Insert video record (can be called by another script)
def insert_video_to_db(video_filename):
    video_filename_only = os.path.basename(video_filename)
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO videos (filename, datetime) VALUES (?, ?)",
                   (video_filename_only, datetime.datetime.now()))
    conn.commit()
    conn.close()

# Dashboard route with optional search
@app.route('/')
def dashboard():
    search_query = request.args.get('search', '').strip().lower()
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    if search_query:
        query = '''
            SELECT * FROM videos
            WHERE LOWER(filename) LIKE ?
               OR strftime('%d', datetime) LIKE ?
               OR strftime('%m', datetime) LIKE ?
            ORDER BY datetime DESC
        '''
        wildcard = f'%{search_query}%'
        cursor.execute(query, (wildcard, wildcard, wildcard))
    else:
        cursor.execute("SELECT * FROM videos ORDER BY datetime DESC")

    videos = cursor.fetchall()
    conn.close()
    return render_template('dashboard.html', videos=videos)

# Download route
@app.route('/download/<path:filename>')
def download_video(filename):
    file_path = os.path.join(VIDEO_FOLDER, filename)
    if not os.path.isfile(file_path):
        abort(404)
    return send_from_directory(VIDEO_FOLDER, filename, as_attachment=True)

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/benefits')
def benefits():
	return render_template('benefits.html')


if __name__ == '__main__':
    app.run(debug=True)
