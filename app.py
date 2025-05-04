import streamlit as st
from transformers import pipeline, set_seed

# Load Hugging Face text generation pipeline
@st.cache_resource
def load_model():
    gen = pipeline("text-generation", model="distilgpt2")
    set_seed(42)
    return gen

generator = load_model()

# App UI
st.title("Mood Tracker & Journal Assistant 😊")
st.write("Reflect on your day — get a warm journaling suggestion in return.")

# User input
user_input = st.text_area("How are you feeling today?", height=150)

# Submit
if st.button("Submit Entry") and user_input:
    with st.spinner("Thinking..."):
        prompt = f"User journal entry: {user_input}\nAI reflective response:"
        result = generator(prompt, max_length=150, num_return_sequences=1)[0]["generated_text"]
        # Remove the original input from the result
        cleaned = result.replace(prompt, "").strip()
        st.subheader("Your Journal Entry ✍️")
        st.write(cleaned)
