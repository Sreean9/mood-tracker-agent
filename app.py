import streamlit as st
import openai
from datetime import datetime
import pandas as pd

# Config
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("🧘 Mood Tracker & Journal Agent")

# Mood selection
mood = st.selectbox("How are you feeling today?", ["😄 Happy", "😊 Content", "😐 Meh", "😞 Sad", "😡 Angry", "😢 Anxious"])

# Journal input
journal_text = st.text_area("Want to reflect a bit more?", placeholder="Type here...")

# Submit
if st.button("Submit Entry"):
    prompt = f"Analyze the mood and tone of this entry: '{journal_text}'. Rate sentiment from -1 to 1 and give a one-line summary."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    result = response['choices'][0]['message']['content']

    if "data" not in st.session_state:
        st.session_state.data = []

    st.session_state.data.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "mood": mood,
        "journal": journal_text,
        "analysis": result
    })

    st.success("Journal saved! Here's what the AI said:")
    st.write(result)

if "data" in st.session_state and len(st.session_state.data) > 0:
    st.subheader("📈 Your Mood Journal")
    df = pd.DataFrame(st.session_state.data)
    st.dataframe(df)
