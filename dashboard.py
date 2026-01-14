import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import base64
import cv2
import tempfile

st.set_page_config(
    page_title="WFH Productivity Analytics",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #020617, #020617);
    color: #e5e7eb;
    font-family: Inter, system-ui;
}

.login-box {
    max-width: 420px;
    margin: 15vh auto;
    padding: 32px;
    background: rgba(255,255,255,0.05);
    border-radius: 18px;
    box-shadow: 0 25px 60px rgba(0,0,0,0.6);
}

button[kind="primary"] {
    background: linear-gradient(135deg,#3b82f6,#22c55e);
    border-radius: 12px;
    border: none;
}

.card {
    background: rgba(255,255,255,0.06);
    padding: 24px;
    border-radius: 18px;
    box-shadow: 0 18px 40px rgba(0,0,0,0.45);
}

.card-title {
    font-size: 13px;
    color: #9ca3af;
}

.card-value {
    font-size: 34px;
    font-weight: 800;
    color: #60a5fa;
}
</style>
""", unsafe_allow_html=True)

USERS = {"admin": "admin123"}

if "auth" not in st.session_state:
    st.session_state.auth = False

def login_page():
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.markdown("### Secure Access")
    st.markdown("Authentication required")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login", type="primary"):
        if USERS.get(username) == password:
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Invalid credentials")

    st.markdown("</div>", unsafe_allow_html=True)

if not st.session_state.auth:
    login_page()
    st.stop()

df = pd.read_csv("daily_report.csv", header=None)
df.columns = ["Date", "Focus_Min", "Idle_Min", "Away_Min", "Productivity_%"]
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date")
latest = df.iloc[-1]

st.markdown("## WFH Productivity & Behavioral Analytics Platform")
st.markdown("AI-driven insights derived from computer vision and time-series analytics")

c1, c2, c3, c4 = st.columns(4)

def metric(title, value):
    return f"""
    <div class="card">
        <div class="card-title">{title}</div>
        <div class="card-value">{value}</div>
    </div>
    """

c1.markdown(metric("FOCUS TIME (MIN)", round(latest["Focus_Min"], 2)), unsafe_allow_html=True)
c2.markdown(metric("IDLE TIME (MIN)", round(latest["Idle_Min"], 2)), unsafe_allow_html=True)
c3.markdown(metric("AWAY TIME (MIN)", round(latest["Away_Min"], 2)), unsafe_allow_html=True)
c4.markdown(metric("PRODUCTIVITY SCORE", f'{round(latest["Productivity_%"], 2)}%'), unsafe_allow_html=True)

weekly = df.resample("W", on="Date").mean(numeric_only=True)

fig, ax = plt.subplots(figsize=(9, 4))
ax.bar(weekly.index.strftime("%Y-%m-%d"), weekly["Productivity_%"], color="#3b82f6")
ax.set_ylim(0, 100)
ax.set_ylabel("Productivity (%)")
ax.set_xlabel("Week")
st.pyplot(fig)
