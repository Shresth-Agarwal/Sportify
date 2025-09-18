import streamlit as st
import datetime

def render_schedule_management():
    """Renders the Schedule Management page."""
    st.header("📅 Training Schedule Center")

    with st.form("schedule_form"):
        col1, col2 = st.columns(2)
        athlete_name = col1.selectbox("Select Athlete", ["John Mitchell", "Emily Chen", "Raj Patel", "Sarah Johnson", "Mike Wilson"])
        training_date = col1.date_input("Training Date", datetime.date.today())
        session_time = col1.time_input("Session Time", datetime.time(10, 0))
        session_type = col2.selectbox("Session Type", ["Strength Training", "Cardio Endurance", "Skill Development", "Recovery", "Assessment"])
        duration = col2.selectbox("Duration", ["30 min", "45 min", "60 min", "90 min", "2 hours"])
        notes = st.text_area("Notes (Optional)", placeholder="Add session goals or special instructions...")

        submitted = st.form_submit_button("📅 Schedule Session")
        if submitted:
            new_session = {
                "athlete": athlete_name, "date": str(training_date), "time": str(session_time),
                "type": session_type, "duration": duration, "notes": notes
            }
            if "sessions" not in st.session_state:
                st.session_state.sessions = []
            st.session_state.sessions.append(new_session)
            st.success(f"✅ Session scheduled for {athlete_name} on {training_date} at {session_time}")

    st.subheader("Upcoming Sessions")
    if st.session_state.get("sessions"):
        for s in st.session_state["sessions"]:
            st.info(f"🗓️ {s['athlete']} | {s['date']} at {s['time']} - {s['type']} ({s['duration']})")
    else:
        st.warning("No upcoming sessions scheduled.")