import streamlit as st

def sidebar_navigation():
    """Renders the sidebar navigation for the athlete using individual buttons."""
    st.sidebar.markdown('<div style="font-weight:bold; font-size:18px; margin-bottom:10px;">🏃‍♂ Athlete Hub</div>', unsafe_allow_html=True)
    
    # Add the new webcam recorder page to the navigation options
    nav_options = [
        "Personalized Training Plans",
        "Diet Recommendations",
        "Progress Tracking",
        "Goal Visualization",
        "Gamification",
        "Detailed Analysis",
        "Record My Form"  # <-- Added the new page here
    ]
    
    # Set a default page if none is selected
    if "athlete_nav" not in st.session_state:
        st.session_state.athlete_nav = nav_options[0]

    # Create a button for each navigation option
    for option in nav_options:
        # Use a more descriptive key to avoid potential conflicts
        if st.sidebar.button(option, key=f"athlete_nav_{option}", use_container_width=True):
            st.session_state.athlete_nav = option
    
    # --- Account Section ---
    st.sidebar.markdown('<hr><div style="font-weight:bold; margin-top:10px;">Account</div>', unsafe_allow_html=True)
    if st.sidebar.button("Logout", key="logout_athlete", use_container_width=True):
        # Clear all relevant session state keys on logout
        for key in list(st.session_state.keys()):
            if key in ['authenticated', 'username', 'user_role', 'athlete_nav']:
                del st.session_state[key]
        st.rerun()
    
    return st.session_state.athlete_nav