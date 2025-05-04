import streamlit as st
from openai import OpenAI

# Load OpenAI client with API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# App title and description
st.title("Mood Tracker & Journal Assistant 😊")
st.write("Reflect on your day, and let me help you journal your thoughts.")

# User input
user_input = st.text_area("How are you feeling today?", height=150)

# Submit button
if st.button("Submit Entry") and user_input:
    with st.spinner("Thinking..."):
        try:
            response = client.chat.completions.create(
                model="gpt-4.1-2025-04-14",
                messages=[
                    {"role": "system", "content": "You're a helpful mood tracking and journaling assistant. Summarize and respond empathetically to the user's emotions."},
                    {"role": "user", "content": user_input}
                ]
            )
            journal_entry = response.choices[0].message.content
            st.subheader("Your Journal Entry ✍️")
            st.write(journal_entry)
        except Exception as e:
            st.error(f"Something went wrong: {e}")
