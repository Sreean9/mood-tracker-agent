import streamlit as st
import requests

HF_TOKEN = st.secrets["HF_TOKEN"]
API_URL = "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    try:
        return response.json()
    except Exception:
        return {"error": response.text}

# ...

if st.button("Submit Entry") and user_input:
    with st.spinner("Thinking..."):
        prompt = f"You are an emotional wellbeing assistant. Reflect on this journal entry with care and insight:\n\n{user_input}\n\nResponse:"
        output = query({
            "inputs": prompt,
            "parameters": {"max_new_tokens": 150, "temperature": 0.7}
        })
        if "error" in output:
            st.error(f"API Error: {output['error']}")
        elif isinstance(output, list) and "generated_text" in output[0]:
            result = output[0]["generated_text"].split("Response:")[-1].strip()
            st.subheader("Your Journal Entry ✍️")
            st.write(result)
        else:
            st.error("Unexpected response format. Please try again later.")


# UI
st.title("Mood Tracker & Journal Assistant 🧠")
st.write("Express yourself — let the AI reflect with empathy and insight.")

user_input = st.text_area("How are you feeling today?", height=150)

if st.button("Submit Entry") and user_input:
    with st.spinner("Thinking..."):
        prompt = f"You are an emotional wellbeing assistant. Reflect on this journal entry with care and insight:\n\n{user_input}\n\nResponse:"
        output = query({
            "inputs": prompt,
            "parameters": {"max_new_tokens": 150, "temperature": 0.7}
        })
        try:
            result = output[0]["generated_text"].split("Response:")[-1].strip()
            st.subheader("Your Journal Entry ✍️")
            st.write(result)
        except Exception as e:
            st.error(f"Failed to generate: {e}")
