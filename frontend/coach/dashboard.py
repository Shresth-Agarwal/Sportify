import streamlit as st
from shared import apply_theme_background
from .sidebar import sidebar_navigation
from .pages.athlete_management import render_athlete_management
from .pages.performance_analytics import render_performance_analytics
from .pages.schedule_management import render_schedule_management
from .pages.communication_hub import render_communication_hub
from .pages.alerts_reports import render_alerts_reports
def coach_dashboard():
    """The main controller for the coach dashboard."""
    apply_theme_background()

    # --- Ensure session state keys exist ---
    if "sessions" not in st.session_state:
        st.session_state.sessions = []
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "alerts" not in st.session_state:
        st.session_state.alerts = [
            {"priority": "🚨 HIGH", "msg": "Sarah Johnson reported knee pain", "status": "Active"},
            {"priority": "⚠️ MEDIUM", "msg": "Mike Wilson missed 3 consecutive sessions", "status": "Active"}
        ]
        
    section = sidebar_navigation()

    page_map = {
        "Athlete Management": render_athlete_management,
        "Performance Analytics": render_performance_analytics,
        "Schedule Management": render_schedule_management,
        "Communication Hub": render_communication_hub,
        "Alerts & Reports": render_alerts_reports
    }

    # Run the function corresponding to the user's choice
    if section in page_map:
        page_map[section]()
    else:
        # Default to the first page if something goes wrong
        render_athlete_management()