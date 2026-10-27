import face_recognition, cv2, numpy as np
from liveness import BlinkDetector
from encodings_store import load_known
from db import mark

encodings, names = load_known()
if not encodings:
    raise SystemExit("known_faces me koi valid face photo nahi hai.")

marked = set()
live = BlinkDetector()

S = 0.5
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if not ret:
        break
    small = cv2.resize(frame, (0, 0), fx=S, fy=S)
    rgb = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)
    locs = face_recognition.face_locations(rgb)
    encs = face_recognition.face_encodings(rgb, locs)
    lms = face_recognition.face_landmarks(rgb, locs)

    for enc, loc, lm in zip(encs, locs, lms):
        d = face_recognition.face_distance(encodings, enc)
        i = np.argmin(d)
        t, r, b, l = [int(v / S) for v in loc]
        if d[i] >= 0.5:
            cv2.rectangle(frame, (l, t), (r, b), (0, 0, 255), 2)
            cv2.putText(frame, "Unknown", (l, t - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            continue

        name = names[i]
        live.update(name, lm)

        if name in marked:
            status, color = f"{name} - Present", (0, 255, 0)
        elif live.is_live(name):
            marked.add(name)
            mark(name)
            status, color = f"{name} - Marked", (0, 255, 0)
        else:
            status, color = f"{name} - Blink karo", (0, 165, 255)

        cv2.rectangle(frame, (l, t), (r, b), color, 2)
        cv2.putText(frame, status, (l, t - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

    cv2.imshow("Attendance", frame)
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()