import streamlit as st
import os
import datetime
import uuid
from streamlit_webrtc import webrtc_streamer, WebRtcMode
from aiortc.contrib.media import MediaRecorder

# --- Directory for saving recordings ---
RECORDINGS_DIR = "recordings"
if not os.path.exists(RECORDINGS_DIR):
    os.makedirs(RECORDINGS_DIR)


def render_webcam_recorder():
    st.title("🎬 Record Your Exercise Form")
    st.info(
        """
        To get expert feedback on your technique, please record a short video of your exercise.
        Ensure your entire body is visible and the lighting is good.
        """
    )

    # --- 1. User Consent ---
    st.markdown("---")
    consent = st.checkbox("I consent to my webcam being used for this recording session.")
    st.warning(
        """
        By checking this box, you agree to have your video recorded and stored on our server
        for analysis purposes. Your privacy is important to us, and your data will be handled securely.
        """
    )

    if not consent:
        st.error("You must consent to use the webcam recorder.")
        st.stop()

    # --- 2. Webcam Recorder Component ---
    RTC_CONFIGURATION = {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}

    if "temp_video_path" not in st.session_state:
        st.session_state.temp_video_path = os.path.join(
            RECORDINGS_DIR, f"temp_{st.session_state.username}_{uuid.uuid4().hex}.mp4"
        )

    temp_video_path = st.session_state.temp_video_path

    webrtc_ctx = webrtc_streamer(
        key="form-recorder",
        mode=WebRtcMode.SENDRECV,
        rtc_configuration=RTC_CONFIGURATION,
        media_stream_constraints={"video": True, "audio": False},
        video_html_attrs={
            "style": {
                "width": "100%",
                "margin": "0 auto",
                "border": "5px #A58BB5 solid",
                "border-radius": "12px",
            },
            "autoPlay": True,
            "controls": False,
        },
        out_recorder_factory=lambda: MediaRecorder(temp_video_path),
    )

    # --- 3. After recording is stopped ---
    if not webrtc_ctx.state.playing and os.path.exists(temp_video_path):
        st.markdown("---")
        st.subheader("✅ Recording Complete")

        if os.path.getsize(temp_video_path) > 0:
            st.info("Your video has been saved temporarily. Please review it below:")

            st.video(temp_video_path)

            col1, col2 = st.columns([1, 1])

            # ✅ Submit
            with col1:
                if st.button("Submit My Video for Analysis", use_container_width=True):
                    with st.spinner("Submitting your video..."):
                        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                        final_video_path = os.path.join(
                            RECORDINGS_DIR,
                            f"{st.session_state.username}_form_{timestamp}.mp4",
                        )
                        os.rename(temp_video_path, final_video_path)

                        st.success("Video submitted successfully! It is now available for your coach.")
                        st.session_state.pop("temp_video_path", None)

            # ❌ Delete
            with col2:
                if st.button("Delete and Record Again", type="secondary", use_container_width=True):
                    if os.path.exists(temp_video_path):
                        try:
                            os.remove(temp_video_path)
                        except PermissionError:
                            st.warning("File is still in use. Please wait a moment and try again.")

                    st.success("Video deleted. You can record a new one now.")
                    st.session_state.pop("temp_video_path", None)
                    st.rerun()

        else:
            st.warning("Recording file is empty. Please try recording again.")
