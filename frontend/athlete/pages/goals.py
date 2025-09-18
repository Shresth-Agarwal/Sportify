import streamlit as st

def render_goals():
    """Renders the Goal Visualization page."""
    st.title("🏆 Goal Achievement Dashboard")
    
    goals = [
        {"name": "Squat 150kg", "current": 135, "target": 150, "unit": "kg"},
        {"name": "Run 5K in 20min", "current": 22.5, "target": 20, "unit": "min"},
        {"name": "Body Fat to 12%", "current": 15, "target": 12, "unit": "%"}
    ]

    for goal in goals:
        progress = 0
        if goal["unit"] == "min":
            over_target = goal["current"] - goal["target"]
            total_range = 2 * over_target if over_target > 0 else goal["target"]
            progress = max(0, 100 - (over_target / total_range) * 100) if total_range > 0 else 100
        else:
            progress = min((goal["current"] / goal["target"]) * 100, 100) if goal["target"] > 0 else 0

        st.subheader(goal['name'])
        st.progress(progress / 100, text=f"{goal['current']}{goal['unit']} / {goal['target']}{goal['unit']}")
        st.divider()