import streamlit as st

def render_alerts_reports():
    """Renders the Alerts & Reports page."""
    st.header("🚨 Alerts & Reports Dashboard")

    st.subheader("Active Alerts")
    for idx, alert in enumerate(st.session_state.get("alerts", [])):
        if alert.get("status") == "Active":
            cols = st.columns([4, 1])
            cols[0].error(f"{alert['priority']} - {alert['msg']}")
            if cols[1].button("Resolve", key=f"resolve_{idx}"):
                st.session_state.alerts[idx]["status"] = "Resolved"
                st.rerun()

    st.subheader("Generate Reports")
    col1, col2, col3 = st.columns(3)
    if col1.button("📊 Weekly Performance Report"):
        st.success("📊 Weekly report generated (mock).")
    if col2.button("🏥 Injury Report"):
        st.success("🏥 Injury report generated (mock).")
    if col3.button("📈 Progress Summary"):
        st.success("📈 Progress summary generated (mock).")