import streamlit as st
from login import login_page
from shared import init_session_state, apply_theme_background, render_modern_header
from athlete.dashboard import athlete_dashboard  # <-- CORRECTED PATH
from coach.dashboard import coach_dashboard    # <-- CORRECTED PATH

# Page configuration
st.set_page_config(
    page_title="Athlyze - Sports Performance Platform",
    page_icon="🏃‍♂",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state (should be called before theme)
init_session_state()

# Apply the custom theme and background
apply_theme_background()

# Router
if not st.session_state.authenticated:
    login_page()
else:
    # Get the user role from session state
    user_role = st.session_state.get("user_role", "").lower()
    
    # Render the shared header on all authenticated pages
    # We pass the role to ensure widget keys are unique
    render_modern_header(page_name=user_role)

    # Route user to correct dashboard
    if user_role == "athlete":
        athlete_dashboard()
    elif user_role == "coach":
        coach_dashboard()
