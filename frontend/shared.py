import streamlit as st

def init_session_state():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "username" not in st.session_state:
        st.session_state.username = ""
    if "current_page" not in st.session_state:
        st.session_state.current_page = "main"

def render_modern_header(page_name="default"):

    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = True

    user_display = st.session_state.username if "username" in st.session_state else "User"

    # --- CSS (No change here) ---
    css = """
    <style>
    /* ... existing CSS ... */
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

    # --- HEADER LAYOUT ---
    col1, col2 = st.columns([7, 3])

    with col1:
        search_query = st.text_input(
            "Search",
            placeholder="Search athletes, workouts, plans...",
            label_visibility="collapsed",
            key=f"search_bar_{page_name}"
        )

    with col2:
        icon_cols = st.columns([1, 1, 2])

        # This is the notification popover code, it is fully functional
        with icon_cols[0]:
            notif = st.popover("🔔")
            with notif:
                st.markdown(
                    """
                    <div class="dropdown-box">
                        <h4>Notifications</h4>
                        <div class="dropdown-item">📢 New workout uploaded</div>
                        <div class="dropdown-item">🏆 Weekly leaderboard updated</div>
                        <div class="dropdown-item">💬 You have 2 new messages</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        with icon_cols[1]:
            settings = st.popover("⚙")
            with settings:
                st.markdown(
                    """
                    <div class="dropdown-box">
                        <h4>Settings</h4>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                if st.button("🌙 Toggle Dark Mode", key=f"dark_mode_toggle_{page_name}"):
                    st.session_state.dark_mode = not st.session_state.dark_mode
                    st.rerun()
                st.button("Change Password", key=f"change_password_{page_name}")
                st.button("Logout", key=f"logout_header_{page_name}")

        with icon_cols[2]:
            profile = st.popover(f"👤 {user_display}")
            with profile:
                st.markdown(
                    f"""
                    <div class="dropdown-box">
                        <h4>Profile</h4>
                        <div class="dropdown-item"><b>Name:</b> {user_display}</div>
                        <div class="dropdown-item"><b>Email:</b> user@example.com</div>
                        <div class="dropdown-item"><b>Role:</b> {st.session_state.get("user_role", "N/A").title()}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                with st.expander("✏️ Edit Profile"):
                    new_name = st.text_input("Update Name", value=user_display, key=f"update_name_{page_name}")
                    if st.button("Save Changes", key=f"save_changes_{page_name}"):
                        st.session_state.username = new_name
                        st.success("✅ Profile updated!")

    if search_query:
        st.write(f"🔍 You searched for: **{search_query}**")
        
def apply_theme_background():
    """Applies the themed background with blurred image and gradient overlay"""
    st.markdown("""
    <style>
    /* Theme Background */
    .stApp {
        background-image: url("https://iili.io/KuWHtja.jpg");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        filter: blur(0px);
    }
    
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, rgba(13, 15, 36, 0.85), rgba(27, 30, 58, 0.85));
        z-index: -1;
        backdrop-filter: blur(90px);
    }
    
    /* Sidebar Theme */
    .css-1d391kg {
        background: rgba(28, 31, 58, 0.9) !important;
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(165, 139, 181, 0.2);
    }
    
    /* Sidebar Navigation Items */
    .stRadio > div {
        background: transparent;
    }
    
    .stRadio > div > label {
        background: rgba(58, 42, 94, 0.3) !important;
        border: 1px solid rgba(165, 139, 181, 0.2);
        border-radius: 12px;
        padding: 12px 16px;
        margin: 6px 0;
        color: #E0E0E0 !important;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .stRadio > div > label:hover {
        background: rgba(123, 47, 101, 0.4) !important;
        border-color: rgba(165, 139, 181, 0.4);
        color: #A58BB5 !important;
        transform: translateX(4px);
        box-shadow: 0 4px 15px rgba(123, 47, 101, 0.3);
    }
    
    .stRadio > div > label[data-checked="true"] {
        background: linear-gradient(135deg, #7B2F65, #3A2A5E) !important;
        border-color: #7B2F65;
        color: white !important;
        box-shadow: 0 4px 20px rgba(123, 47, 101, 0.4);
    }
    
    /* Sidebar Text */
    .css-1d391kg .stMarkdown {
        color: #E0E0E0;
    }
    
    .css-1d391kg h2 {
        color: #A58BB5;
        font-weight: bold;
    }
    
    .css-1d391kg h3 {
        color: #7B2F65;
    }
    
    /* Main Content Cards */
    .stContainer > div {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(165, 139, 181, 0.2);
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
    }
    
    /* Text Colors */
    .stMarkdown h1 {
        color: white;
        font-weight: bold;
    }
    
    .stMarkdown h2 {
        color: #A58BB5;
    }
    
    .stMarkdown h3 {
        color: #A58BB5;
    }
    
    .stMarkdown p {
        color: #E0E0E0;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #7B2F65, #3A2A5E);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 24px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(123, 47, 101, 0.4);
        filter: brightness(1.1);
    }
    
    /* Input Fields */
    .stTextInput > div > div > input {
        background: rgba(28, 31, 58, 0.6);
        color: white;
        border: 2px solid rgba(165, 139, 181, 0.3);
        border-radius: 12px;
        backdrop-filter: blur(10px);
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #A58BB5;
        box-shadow: 0 0 15px rgba(165, 139, 181, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)
