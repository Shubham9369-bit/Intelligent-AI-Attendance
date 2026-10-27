# AI Attendance System

Face recognition based attendance system with blink liveness detection (anti-spoofing), web dashboard and SQLite storage.

## Features
- Real-time face recognition via webcam (OpenCV + face_recognition)
- Blink-based liveness check: a static photo cannot mark attendance
- Encodings cache (`encodings.pkl`) for fast startup
- SQLite database with one entry per person per day
- Streamlit dashboard: present/absent report, date filter, CSV download
- Web enrollment: add a student by camera or upload

## Project Structure
```
AI Attendance/
├── attendance.py        # main webcam attendance script
├── liveness.py          # blink detection
├── encodings_store.py   # face encoding cache
├── db.py                # SQLite helpers
├── migrate.py           # one-time CSV -> SQLite migration
├── dashboard.py         # Streamlit dashboard + enrollment
└── known_faces/         # one photo per person (Name.jpg)
```

## Installation
Python 3.11+ recommended.
```
pip install dlib-bin
pip install face_recognition --no-deps
pip install face_recognition_models click Pillow numpy opencv-python pandas streamlit
pip install "setuptools<81"
```

## Usage
1. Add photos to `known_faces/` (file name = person name, e.g. `Rahul_Sharma.jpg`), or use the dashboard sidebar.
2. Run attendance (press `q` to quit):
   ```
   python attendance.py
   ```
   Face the camera and blink once to get marked.
3. Open dashboard:
   ```
   python -m streamlit run dashboard.py
   ```

## How It Works
1. Each known photo is converted to a 128-d face embedding.
2. Webcam faces are matched by Euclidean distance (threshold 0.5).
3. Eye Aspect Ratio (EAR) detects a blink; attendance is marked only after a live blink.
4. Entry is saved in `attendance.db` (unique per name and date).

## Configuration
| Setting | File | Default |
|---|---|---|
| Match threshold | `attendance.py` | 0.5 |
| Blink threshold (EAR) | `liveness.py` | 0.21 |
| Frames eyes closed | `liveness.py` | 2 |

## Limitations
- Video replay attacks may bypass blink detection.
- One photo per person; accuracy depends on lighting and photo quality.

## Security
Do not commit `known_faces/` or `attendance.db` to GitHub. Add them to `.gitignore`.

## Future Work
- Multiple photos per person
- Head-turn liveness
- Email alerts for absent students
- Mask and low-light handling