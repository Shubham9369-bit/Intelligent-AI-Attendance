import streamlit as st
import pandas as pd
import os
from datetime import date

EXT = (".jpg", ".jpeg", ".png")
os.makedirs("known_faces", exist_ok=True)

st.set_page_config(page_title="Attendance Dashboard", layout="wide")
st.title("AI Attendance Dashboard")

# ---- Enrollment ----
with st.sidebar:
    st.header("Naya student add karo")
    name = st.text_input("Naam")
    method = st.radio("Photo", ["Camera", "Upload"], horizontal=True)
    if method == "Camera":
        pic = st.camera_input("Photo lo")
    else:
        pic = st.file_uploader("Photo chuno", type=["jpg", "jpeg", "png"])
    if st.button("Save"):
        clean = name.strip().replace(" ", "_")
        if not clean or pic is None:
            st.error("Naam aur photo dono chahiye.")
        else:
            with open(f"known_faces/{clean}.jpg", "wb") as f:
                f.write(pic.getvalue())
            st.success(f"{clean} add ho gaya. attendance.py dobara chalao.")

all_names = [os.path.splitext(f)[0] for f in os.listdir("known_faces")
             if f.lower().endswith(EXT)]

# ---- Dashboard ----
if not os.path.exists("attendance.csv"):
    st.warning("Abhi koi attendance record nahi hai.")
    st.stop()

df = pd.read_csv("attendance.csv")
d = st.date_input("Date chuno", date.today())
day = df[df["Date"].astype(str) == str(d)]
present = sorted(day["Name"].unique())
absent = sorted(set(all_names) - set(present))

c1, c2, c3 = st.columns(3)
c1.metric("Total", len(all_names))
c2.metric("Present", len(present))
c3.metric("Absent", len(absent))

left, right = st.columns(2)
left.subheader("Present")
left.dataframe(day, width="stretch")
right.subheader("Absent")
right.write(absent if absent else "Sab present hain")

st.subheader("Poora record")
st.dataframe(df, width="stretch")
st.download_button("CSV download", df.to_csv(index=False), "attendance.csv")