import streamlit as st

def render_diet():
    """Renders the Diet Recommendations page."""
    st.title("🥗 Smart Nutrition Guidance")
    st.markdown("Receive personalized meal recommendations based on your training goals and dietary preferences.")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Today's Meal Plan")
        st.write("🍳 *Breakfast*: Oatmeal with berries (320 cal)")
        st.write("🥗 *Lunch*: Grilled chicken salad (450 cal)")
        st.write("🍽 *Dinner*: Salmon with quinoa (520 cal)")
    with col2:
        st.subheader("Nutrition Goals")
        st.metric("Calories", "1,890/2,100", "210 remaining")
        st.metric("Protein", "142g/150g", "8g needed")
        st.metric("Carbs", "185g/200g", "15g remaining")