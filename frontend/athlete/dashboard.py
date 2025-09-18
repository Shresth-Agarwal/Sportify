import streamlit as st
from .sidebar import sidebar_navigation
from .pages.training_plans import render_training_plans
from .pages.diet import render_diet
from .pages.progress import render_progress
from .pages.goals import render_goals
from .pages.gamification import render_gamification
from .pages.analysis import render_analysis
from .pages.webcam import render_webcam_recorder # <-- 1. IMPORT THE NEW PAGE

def athlete_dashboard():
    """The main controller for the athlete dashboard."""
    
    choice = sidebar_navigation()

    # Map the sidebar choices to their corresponding render functions
    page_map = {
        "Personalized Training Plans": render_training_plans,
        "Diet Recommendations": render_diet,
        "Progress Tracking": render_progress,
        "Goal Visualization": render_goals,
        "Gamification": render_gamification,
        "Detailed Analysis": render_analysis,
        "Record My Form": render_webcam_recorder # <-- 2. ADD THE NEW PAGE TO THE MAP
    }

    # Execute the function associated with the user's choice
    if choice in page_map:
        page_map[choice]()
    else:
        # Default welcome page if no specific choice is made yet
        st.title("🏃‍♂ Welcome to Your Athlete Dashboard")
        st.write("Select an option from the sidebar to view your plans, track progress, or record your form.")