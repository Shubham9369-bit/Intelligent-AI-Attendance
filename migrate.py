import pandas as pd, os
from db import mark

if os.path.exists("attendance.csv"):
    for _, r in pd.read_csv("attendance.csv").iterrows():
        mark(str(r["Name"]), str(r["Date"]), str(r["Time"]))
    print("Migration done")
else:
    print("attendance.csv nahi mili")