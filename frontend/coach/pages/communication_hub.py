import streamlit as st
import datetime

def render_communication_hub():
    """Renders the Communication Hub page."""
    st.header("📢 Communication Hub")

    col1, col2 = st.columns([2, 1])
    with col1:
        recipient = st.selectbox("Send to:", ["All Athletes", "Active Athletes", "Specific Athlete"])
        if recipient == "Specific Athlete":
            st.selectbox("Choose Athlete:", ["John Mitchell", "Emily Chen", "Raj Patel", "Sarah Johnson", "Mike Wilson"])
    with col2:
        msg_type = st.selectbox("Message Type:", ["General Update", "Reminder", "Motivational", "Important Notice"])

    message = st.text_area("Message:", placeholder="Type your message here...", height=100)
    if st.button("📤 Send Message", type="primary"):
        if message:
            if "messages" not in st.session_state:
                st.session_state.messages = []
            st.session_state.messages.append({
                "to": recipient, "subject": msg_type, "content": message,
                "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            })
            st.success("✅ Message sent successfully!")
        else:
            st.error("⚠️ Please enter a message.")

    st.subheader("Recent Communications")
    if st.session_state.get("messages"):
        for msg in reversed(st.session_state.messages[-5:]):
            st.write(f"📧 [{msg['subject']}] to {msg['to']} ({msg['date']}) - {msg['content'][:50]}...")
    else:
        st.warning("No messages sent yet.")