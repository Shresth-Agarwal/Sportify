import streamlit as st
import json
import os

USER_FILE = "users.json"

def load_users():
    if not os.path.exists(USER_FILE):
        return {}
    with open(USER_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=4)

BG_LINK = "https://iili.io/KuWHtja.jpg"   # background
LOGO_LINK = "https://iili.io/KAslsAN.jpg" # updated logo

# Enhanced CSS with themed styling
BG_AND_CENTER_CSS = f"""
<style>
.stApp {{
    background-image: url("{BG_LINK}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
    min-height: 100vh;
    position: relative;
}}

/* Blur overlay (no purple tint, just slight dark for readability) */
.stApp::before {{
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    backdrop-filter: blur(70px);   /* heavy blur */
    background: rgba(0, 0, 0, 0.2); /* optional tint, remove if you want only blur */
    z-index: -1;
}}

/* Kill default spacing */
.block-container {{
    padding-top: 0 !important;
    margin-top: 0 !important;
}}

/* Welcome header */
.welcome-header {{
    text-align: center;
    margin-top: 2rem;   /* adjust if you want more spacing */
    margin-bottom: 0rem;
}}

.welcome-logo {{
    max-height: 200px;
    margin-top: 1rem;
}}

/* Tabs Styling – aligned left */
.stTabs [data-baseweb="tab-list"] {{
    background: rgba(28, 31, 58, 0.6);
    border-radius: 10px;
    padding: 6px;
    gap: 6px;
    justify-content: flex-start;
}}

.stTabs [data-baseweb="tab"] {{
    background: rgba(255,255,255,0.05);
    border-radius: 6px;
    padding: 10px 22px;
    font-weight: 600;
    color: #E0E0E0;
}}

.stTabs [aria-selected="true"] {{
    background: linear-gradient(135deg, #6A82FB, #FC5C7D);
    color: white !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.3);
}}
</style>
"""

def login_page():
    st.markdown(BG_AND_CENTER_CSS, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="welcome-header">
        <img src="{LOGO_LINK}" class="welcome-logo" alt="Athlyze Logo" />
    </div>
    """, unsafe_allow_html=True)

    # Tabs for Login and Signup (removed login-container wrapper)
    tab1, tab2 = st.tabs(["Login", "Create Account"])

    # --- LOGIN ---
    with tab1:
        st.markdown("### Welcome Back!")
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            consent = st.checkbox("I agree to the privacy & security policy", value=False, key="login_consent")
            submitted = st.form_submit_button("🚀Sign In")

            if submitted:
                users = load_users()
                if not username.strip():
                    st.error("⚠ Please enter a username.")
                elif not password:
                    st.error("⚠ Please enter your password.")
                elif not consent:
                    st.error("⚠ Please accept the privacy policy to continue.")
                elif username in users and users[username]["password"] == password:
                    st.success(f"🎉 Welcome back, {username}!")
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.session_state.user_role = users[username]["mode"].lower()
                    st.session_state.current_page = "main"
                    st.rerun()
                else:
                    st.error("Invalid username or password. Please try again.")

    # --- SIGNUP ---
    with tab2:
        st.markdown("### Join Athlyze Today!")
        mode = st.selectbox("I am an : ", ["Athlete", "Coach"])

        with st.form("signup_form"):
            new_user = st.text_input("Full Name", placeholder="Enter your full name")
            new_pass = st.text_input("Create Password", type="password", placeholder="Create a strong password")
            confirm_pass = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
            age = st.number_input("Age", min_value=10, max_value=100, value=20)

            extra = {}
            if mode == "Athlete":
                st.markdown("Athletic Profile")
                extra["sport"] = st.text_input("Primary Sport", placeholder="e.g., Track, Football, Swimming")
                extra["goals"] = st.text_input("Training Goals", placeholder="e.g., increase squat PR, run sub-20 5K")
                extra["fitness"] = st.selectbox("Current Fitness Level", ["Beginner", "Intermediate", "Advanced"])
            elif mode == "Coach":
                st.markdown("Coaching Profile")
                extra["experience"] = st.selectbox("Coaching Experience", ["Junior Coach (0-2 years)", "Intermediate Coach (3-5 years)", "Senior Coach (5+ years)"])
                extra["specialization"] = st.text_input("Specialization", placeholder="e.g., Sprint Training, Strength & Conditioning")
                extra["num_athletes"] = st.number_input("Athletes Currently Coached", min_value=0, max_value=500, value=5)

            agree = st.checkbox("I agree to the privacy & security policy and terms of service", value=False, key="signup_consent")
            create = st.form_submit_button("Create My Account")

            if create:
                users = load_users()
                if not new_user.strip():
                    st.error("⚠ Please enter your full name.")
                elif new_user in users:
                    st.error("⚠ This name is already registered. Please choose a different name or try logging in.")
                elif len(new_pass) < 6:
                    st.error("⚠ Password must be at least 6 characters long.")
                elif new_pass != confirm_pass:
                    st.error("Passwords do not match. Please try again.")
                elif not agree:
                    st.error("⚠ Please accept the privacy policy and terms to create your account.")
                else:
                    users[new_user] = {
                        "password": new_pass,
                        "mode": mode,
                        "age": age,
                        **extra
                    }
                    save_users(users)
                    st.success(f"Welcome to Athlyze, {new_user}! Your {mode.lower()} account has been created successfully.")
                    st.session_state.authenticated = True
                    st.session_state.username = new_user
                    st.session_state.user_role = mode.lower()
                    st.session_state.current_page = "main"
                    st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)  # Close main wrapper