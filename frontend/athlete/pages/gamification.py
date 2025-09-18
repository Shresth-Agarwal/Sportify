import streamlit as st

def render_gamification():
    """Renders the Gamification page."""
    st.title("🎮 Achievement System")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("🏅 Gold Medals", "5")
        st.metric("🥈 Silver Medals", "12")
        st.metric("🥉 Bronze Medals", "18")
    with col2:
        st.metric("Current Streak", "7 days")
        st.metric("Total Points", "2,450")
        st.metric("Global Rank", "#1,289")

    st.subheader("Recent Achievements")
    st.success("🥇 **7-Day Streak Master!** - Awarded for training every day for a week.")
    st.info("🎯 **Personal Best!** - You beat your previous squat record.")
    st.warning("⚡ **Speed Demon!** - Completed your 5K run faster than ever before.")