import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import base64

st.set_page_config(
    page_title="WFH Productivity Analytics Platform",
    layout="wide",
    initial_sidebar_state="collapsed"
)

USERS = {"admin": "admin123"}

if "auth" not in st.session_state:
    st.session_state.auth = False

st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f172a, #020617);
    font-family: 'Inter', 'Segoe UI', system-ui;
}

.login-wrapper {
    max-width: 420px;
    margin: 10vh auto 0 auto;
    padding: 32px 36px 36px 36px;
    background: rgba(255,255,255,0.06);
    backdrop-filter: blur(18px);
    border-radius: 20px;
    border: 1px solid rgba(255,255,255,0.15);
    box-shadow: 0 30px 80px rgba(0,0,0,0.65);
    animation: fadeIn 0.9s ease;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(18px); }
    to { opacity: 1; transform: translateY(0); }
}

.login-title {
    font-size: 26px;
    font-weight: 700;
    color: #f8fafc;
    text-align: center;
    margin-bottom: 6px;
}

.login-sub {
    font-size: 14px;
    color: #94a3b8;
    text-align: center;
    margin-bottom: 26px;
}

input {
    background-color: rgba(255,255,255,0.08) !important;
    color: #f8fafc !important;
    border-radius: 12px !important;
    border: 1px solid rgba(255,255,255,0.25) !important;
}

label {
    color: #cbd5f5 !important;
    font-weight: 500;
}

button[kind="primary"] {
    width: 100%;
    height: 44px;
    border-radius: 12px;
    background: linear-gradient(135deg, #3b82f6, #22c55e);
    color: white;
    font-weight: 600;
    border: none;
    transition: transform 0.25s ease, box-shadow 0.25s ease;
}

button[kind="primary"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 30px rgba(34,197,94,0.35);
}

.card {
    background: rgba(255,255,255,0.06);
    border-radius: 20px;
    padding: 24px;
    box-shadow: 0 18px 50px rgba(0,0,0,0.4);
}

.card-title {
    font-size: 13px;
    color: #9ca3af;
}

.card-value {
    font-size: 36px;
    font-weight: 800;
    color: #3b82f6;
}

.footer {
    text-align: center;
    font-size: 13px;
    color: #9ca3af;
    margin-top: 50px;
}
</style>
""", unsafe_allow_html=True)

def login_page():
    st.markdown("""
    <div class="login-wrapper">
        <div class="login-title">Secure Access</div>
        <div class="login-sub">Authentication required to access analytics</div>
    """, unsafe_allow_html=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login", type="primary"):
        if username in USERS and USERS[username] == password:
            st.session_state.auth = True
            st.session_state.user = username
            st.rerun()
        else:
            st.error("Invalid username or password")

    st.markdown("</div>", unsafe_allow_html=True)

if not st.session_state.auth:
    login_page()
    st.stop()

st.sidebar.write(f"Logged in as: {st.session_state.user}")
if st.sidebar.button("Logout"):
    st.session_state.auth = False
    st.rerun()

df = pd.read_csv("daily_report.csv", header=None)
df.columns = ["Date", "Focus_Min", "Idle_Min", "Away_Min", "Productivity_%"]
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date")
latest = df.iloc[-1]

st.markdown("## WFH Productivity & Behavioral Analytics Platform")
st.markdown("AI-driven insights derived from computer vision and time-series analytics")

c1, c2, c3, c4 = st.columns(4)

def card_ui(title, value):
    return f"""
    <div class="card">
        <div class="card-title">{title}</div>
        <div class="card-value">{value}</div>
    </div>
    """

c1.markdown(card_ui("FOCUS TIME (MIN)", latest["Focus_Min"]), unsafe_allow_html=True)
c2.markdown(card_ui("IDLE TIME (MIN)", latest["Idle_Min"]), unsafe_allow_html=True)
c3.markdown(card_ui("AWAY TIME (MIN)", latest["Away_Min"]), unsafe_allow_html=True)
c4.markdown(card_ui("PRODUCTIVITY SCORE", f'{latest["Productivity_%"]}%'), unsafe_allow_html=True)

weekly = df.resample("W", on="Date").mean(numeric_only=True)
fig1, ax1 = plt.subplots(figsize=(9,4))
ax1.bar(weekly.index.strftime("%Y-%m-%d"), weekly["Productivity_%"], color="#3b82f6")
ax1.set_ylim(0,100)
st.pyplot(fig1)

csv = df.to_csv(index=False)
b64 = base64.b64encode(csv.encode()).decode()
st.markdown(
    f'<a href="data:file/csv;base64,{b64}" download="wfh_productivity_report.csv">Download Analytics Report</a>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="footer">
Secure, access-controlled AI productivity analytics platform
</div>
""", unsafe_allow_html=True)
