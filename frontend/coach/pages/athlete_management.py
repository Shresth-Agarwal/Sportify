import streamlit as st

def render_athlete_management():
    """Renders the Athlete Management page."""
    st.header("Athlete Management Dashboard")

    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Total Athletes", "23", "+3")
    with col2: st.metric("Active Today", "18", "+2")
    with col3: st.metric("Avg Performance", "78%", "+5%")
    with col4: st.metric("Injuries", "2", "-1")

    st.subheader("Athlete Roster")
    athlete_data = {
        "Name": ["John Mitchell", "Emily Chen", "Raj Patel", "Sarah Johnson", "Mike Wilson"],
        "Sport": ["Running", "Swimming", "Football", "Tennis", "Basketball"],
        "Last Active": ["2 hours ago", "1 day ago", "4 hours ago", "Today", "3 hours ago"],
    }
    st.table(athlete_data)