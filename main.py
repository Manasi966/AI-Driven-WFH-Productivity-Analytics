import cv2
import time
import csv
from datetime import datetime
import os

# Load Haar Cascade Face Detector

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

cap = cv2.VideoCapture(0)

# Time tracking 

focus_time = 0.0
idle_time = 0.0
away_time = 0.0

last_time = time.time()
last_gray = None
current_state = "AWAY"


# Session settings (change if needed)

SESSION_DURATION = 30 * 60  # 30 minutes
session_start = time.time()

print("AI WFH Focus & Presence System Started")
print("Press Q to stop session manually")


# Main Loop

while True:
    ret, frame = cap.read()
    if not ret:
        print("Camera error")
        break

    now = time.time()
    elapsed = now - last_time
    last_time = now

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.2, minNeighbors=5, minSize=(80, 80)
    )

    # Movment decect
    movement = False
    if last_gray is not None:
        diff = cv2.absdiff(last_gray, gray)
        movement = diff.mean() > 2

    last_gray = gray.copy()


    # State Logic

    if len(faces) > 0:
        if movement:
            current_state = "FOCUSED"
            focus_time += elapsed
            color = (0, 255, 0)
        else:
            current_state = "IDLE"
            idle_time += elapsed
            color = (0, 255, 255)
    else:
        current_state = "AWAY"
        away_time += elapsed
        color = (0, 0, 255)

    # Draw Face Box

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

    # Productivity Calculation
 
    total_time = focus_time + idle_time + away_time
    productivity = (focus_time / total_time) * 100 if total_time > 0 else 0

    # UI Dashboard

    cv2.rectangle(frame, (10, 10), (430, 210), (40, 40, 40), -1)

    cv2.putText(frame, f"Status: {current_state}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

    cv2.putText(frame, f"Focus Time: {round(focus_time/60, 2)} min", (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

    cv2.putText(frame, f"Idle Time: {round(idle_time/60, 2)} min", (20, 115),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

    cv2.putText(frame, f"Away Time: {round(away_time/60, 2)} min", (20, 150),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

    cv2.putText(frame, f"Productivity: {round(productivity, 2)}%",
                (20, 185), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)

    cv2.imshow("AI WFH Focus & Presence Monitor", frame)


    # Session Auto-End
 
    if now - session_start >= SESSION_DURATION:
        print("Session ended automatically")
        break

    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Session ended manually")
        break

cap.release()
cv2.destroyAllWindows()


# SAVE DAILY 
focus_min = round(focus_time / 60, 2)
idle_min = round(idle_time / 60, 2)
away_min = round(away_time / 60, 2)
productivity = round(productivity, 2)

date = datetime.now().strftime("%Y-%m-%d")

file_exists = os.path.exists("daily_report.csv")

with open("daily_report.csv", "a", newline="") as f:
    writer = csv.writer(f)
    if not file_exists:
        writer.writerow(["Date", "Focus_Min", "Idle_Min", "Away_Min", "Productivity_%"])
    writer.writerow([date, focus_min, idle_min, away_min, productivity])

print("Daily report saved successfully to daily_report.csv")

