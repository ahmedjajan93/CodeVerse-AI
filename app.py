import streamlit as st
import requests

# FastAPI endpoint (replace with your server URL)
FASTAPI_URL = "http://127.0.0.1:8080/summon-wizard"

# App UI Setup
st.set_page_config(page_title="CodeVerse AI", page_icon="🧙‍♂️")
st.title("🧙‍♂️ Welcome to CodeVerse AI")
st.markdown("""
**Embark on your coding quest!**  
Solve magical programming challenges with our high-performance AI Wizard.
""")

# Track progress
if "completed_quests" not in st.session_state:
    st.session_state.completed_quests = []

# Quests data
quests = {
    "The Loop Scroll (Loops)": "Explain for loops and while loops in Python.",
    "The List of Light (Lists)": "Describe how Python lists work, including indexing and slicing."
}

# UI Components
challenge = st.selectbox("🧩 Choose your coding quest:", list(quests.keys()))
level = st.radio("📚 Explanation level:", ["👶 ELI5", "🧑‍🎓 Student", "🧑‍💻 Developer"])

if st.button("🔮 Summon the AI Wizard"):
    with st.spinner("The Wizard is conjuring knowledge..."):
        try:
            response = requests.post(
                f"{FASTAPI_URL}/summon-wizard",
                json={"topic": quests[challenge], "level": level},
                timeout=30
            ).json()
            
            st.markdown("---")
            st.markdown(f"### ✨ Wisdom of the Wizard:\n{response['response']}")
            
            if challenge not in st.session_state.completed_quests:
                st.session_state.completed_quests.append(challenge)
                
        except Exception as e:
            st.error(f"Spell failed! {str(e)}")

# Progress tracker
st.markdown("---")
st.subheader("🏆 Your Journey So Far")
for q in st.session_state.completed_quests:
    st.markdown(f"✅ {q}")