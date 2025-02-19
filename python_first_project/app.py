import streamlit as st
import pandas as pd
import requests
import datetime
import random

# Set Page Config
st.set_page_config(page_title="Growth Mindset Challenge", page_icon="🌱", layout="wide")

# Dark Mode Toggle
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

if st.button("🌙 Toggle Dark Mode"):
    st.session_state.dark_mode = not st.session_state.dark_mode

if st.session_state.dark_mode:
    st.markdown("""
        <style>
            body { background-color: #222; color: white; }
        </style>
    """, unsafe_allow_html=True)

# ✅ Fix: Alternative Motivational Quotes API
quote_url = "https://type.fit/api/quotes"
try:
    response = requests.get(quote_url, timeout=5)  # Timeout added
    response.raise_for_status()
    quote_data = response.json()
    random_quote = random.choice(quote_data)
    st.sidebar.markdown(f"> **{random_quote['text']}** - *{random_quote.get('author', 'Unknown')}*")
except requests.exceptions.RequestException:
    st.sidebar.error("⚠️ Could not fetch quote. Using default quote.")
    st.sidebar.markdown("> **Keep pushing forward!** - *Anonymous*")

# User Progress Tracker
st.title("🌱 Growth Mindset Challenge")
st.subheader("Track Your Learning Progress")

date_today = datetime.date.today()
progress_data = st.session_state.get("progress_data", [])

goal = st.text_input("🎯 Enter today's learning goal:")
progress = st.slider("📊 How much progress did you make?", 0, 100, 50)

if st.button("Save Progress"):
    progress_data.append({"date": str(date_today), "goal": goal, "progress": progress})
    st.session_state.progress_data = progress_data
    st.success("✅ Progress saved!")

# Show progress history
df = pd.DataFrame(progress_data)
if not df.empty:
    st.write("### Your Progress Over Time")
    st.line_chart(df.set_index("date")[["progress"]])

# Daily Journal Feature
st.subheader("📝 Daily Journal")
if "journal_entries" not in st.session_state:
    st.session_state.journal_entries = []

journal_text = st.text_area("Write about today's learning experience:")
if st.button("Save Journal Entry"):
    st.session_state.journal_entries.append({"date": str(date_today), "entry": journal_text})
    st.success("✅ Journal entry saved!")

# Show Journal Entries
if st.session_state.journal_entries:
    st.write("### Past Journal Entries")
    for entry in reversed(st.session_state.journal_entries):
        st.markdown(f"**{entry['date']}** - {entry['entry']}")

# Resources Section
st.subheader("📚 Useful Learning Resources")
st.markdown("""
- [🔗 Growth Mindset - Carol Dweck](https://www.mindsetworks.com/science/)
- [📖 Article: Developing a Growth Mindset](https://www.edutopia.org/article/developing-growth-mindset)
- [🎥 Video: The Power of Belief](https://www.youtube.com/watch?v=pN34FNbOKXc)
- [💡 Free Courses on Coursera](https://www.coursera.org/)
- [Growth Mindset Guide](https://www.mindsetworks.com)
- [Streamlit Documentation](https://docs.streamlit.io)
""")
# Resources

# Footer
st.write("---")
st.write("This app was built using **Streamlit**. Keep learning and growing!")
