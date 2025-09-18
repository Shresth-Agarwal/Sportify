import streamlit as st

def sidebar_navigation():
    """Renders the coach's sidebar using individual buttons."""
    st.sidebar.markdown('<div class="sidebar-title">🎓 Coach Control Center</div>', unsafe_allow_html=True)

    nav_options = [
        "Athlete Management", 
        "Performance Analytics", 
        "Schedule Management", 
        "Communication Hub", 
        "Alerts & Reports"
    ]
    
    # Set default navigation page if not already set
    if "coach_nav_page" not in st.session_state:
        st.session_state.coach_nav_page = nav_options[0]

    # Create a button for each navigation option
    for option in nav_options:
        if st.sidebar.button(option, key=f"coach_nav_{option}", use_container_width=True):
            st.session_state.coach_nav_page = option
            
    section = st.session_state.coach_nav_page

    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 Logout", key="logout_coach", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.username = ""
        st.rerun()
        
    return section