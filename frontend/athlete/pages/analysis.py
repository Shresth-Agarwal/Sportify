import streamlit as st

def render_analysis():
    """Renders the Detailed Analysis page."""
    st.title("📊 Performance Intelligence")
    
    st.subheader("💡 AI-Powered Insights")
    col1, col2 = st.columns(2)
    with col1:
        st.info("**Strength Improvement:** Your squat performance has increased by 15% over the last month. Keep focusing on progressive overload.")
        st.success("**Consistency:** You have an 85% workout attendance rate. This is a key factor in your recent performance gains.")
    with col2:
        st.warning("**Recovery Imbalance:** Your workout intensity is high, but your average sleep is below the recommended 7 hours. Prioritize rest to prevent burnout.")
        st.error("**Nutritional Gap:** Protein intake is slightly below the target for your current training load. Consider adding a post-workout protein source.")

    summary_data = {
        "Metric": ["Workouts Completed", "Avg Performance Score", "Calories Burned", "Avg. Sleep"],
        "This Week": ["5/6", "82%", "1,750 kcal", "7.2h"],
        "Last Week": ["4/6", "78%", "1,580 kcal", "6.8h"],
        "Change": ["+1 workout", "+4 points", "+170 kcal", "+0.4h"]
    }
    st.subheader("Weekly Summary")
    st.table(summary_data)
    
    st.subheader("📑 Generate Detailed Report")
    report_type = st.selectbox("Select Report Type", ["Monthly Performance", "Injury Risk Analysis", "Nutritional Breakdown"])
    if st.button(f"Generate {report_type} Report"):
        with st.spinner("Analyzing data and generating your report..."):
            st.success(f"Your {report_type} report is ready for download! (Mock)")