import streamlit as st

def render_training_plans():
    """Renders the Personalized Training Plans page."""
    st.title("🎯 Personalized Training Plans")
    st.markdown("Get daily workout suggestions tailored specifically to your fitness level, goals, and preferences.")
    col1, col2, col3 = st.columns(3)
    with col1: st.metric("Today's Target", "Upper Body", "💪")
    with col2: st.metric("Duration", "45 min", "⏱")
    with col3: st.metric("Calories Goal", "350", "🔥")
    st.success("✅ *Completed*: Cardio Warm-up (15 min)")
    st.info("⏳ *Next*: Bench Press (3 sets x 8 reps)")
    st.warning("🔥 *Streak*: 7 days consecutive training!")