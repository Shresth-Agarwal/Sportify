import streamlit as st
import matplotlib.pyplot as plt

def render_performance_analytics():
    """Renders the Performance Analytics page."""
    st.header("📊 Performance Analytics Center")

    weeks = list(range(1, 9))
    john = [60, 62, 65, 68, 70, 73, 75, 78]
    emily = [75, 78, 80, 83, 85, 87, 89, 92]
    raj = [45, 50, 55, 58, 62, 65, 68, 72]

    fig, ax = plt.subplots(figsize=(12, 7))
    ax.plot(weeks, john, label="John Mitchell", marker='o', linewidth=3, color='#7B2F65')
    ax.plot(weeks, emily, label="Emily Chen", marker='s', linewidth=3, color='#3A2A5E')
    ax.plot(weeks, raj, label="Raj Patel", marker='^', linewidth=3, color='#A58BB5')

    ax.set_xlabel("Training Weeks", fontsize=12, fontweight='bold')
    ax.set_ylabel("Performance Score (%)", fontsize=12, fontweight='bold')
    ax.set_title("8-Week Performance Progression", fontsize=16, fontweight='bold')
    ax.legend(loc='upper left', framealpha=0.9)
    ax.grid(True, alpha=0.3)
    
    st.pyplot(fig)

    col1, col2 = st.columns(2)
    with col1:
        st.success("🏆 *Top Performer*: Emily Chen (92% avg)")
        st.info("📈 *Most Improved*: Raj Patel (+27 points)")
    with col2:
        st.warning("⚠️ *Needs Attention*: 3 athletes below 70%")
        st.metric("Team Average", "79.3%", "+4.2%")