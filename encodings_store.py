import face_recognition, os, pickle

EXT = (".jpg", ".jpeg", ".png")

def _sig(path):
    return [(f, os.path.getmtime(f"{path}/{f}"), os.path.getsize(f"{path}/{f}"))
            for f in sorted(os.listdir(path)) if f.lower().endswith(EXT)]

def load_known(path="known_faces", cache="encodings.pkl"):
    os.makedirs(path, exist_ok=True)
    sig = _sig(path)
    if os.path.exists(cache):
        try:
            with open(cache, "rb") as fh:
                data = pickle.load(fh)
            if data["sig"] == sig:
                return data["encodings"], data["names"]
        except Exception:
            pass
    encodings, names = [], []
    for f, _, _ in sig:
        img = face_recognition.load_image_file(f"{path}/{f}")
        enc = face_recognition.face_encodings(img)
        if enc:
            encodings.append(enc[0])
            names.append(os.path.splitext(f)[0])
    with open(cache, "wb") as fh:
        pickle.dump({"sig": sig, "encodings": encodings, "names": names}, fh)
    return encodings, names