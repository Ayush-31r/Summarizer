import streamlit as st
import google.generativeai as genai
import os

st.set_page_config(page_title="Gemini AI Summarizer", page_icon="🧠")

# Configure Gemini
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("Missing environment variable: GEMINI_API_KEY")
else:
    genai.configure(api_key=api_key)

st.title("🧠 Gemini AI Summarizer")
st.write("Summarize any text into 3–4 lines using Google's Gemini model.")

text = st.text_area("Enter your text below:", height=200)

if st.button("Summarize"):
    if not text.strip():
        st.warning("Please enter some text.")
    else:
        try:
            model = genai.GenerativeModel("gemini-2.5-flash")
            with st.spinner("Summarizing..."):
                prompt = f"Summarize this text in 3–4 lines, keeping only the key ideas:\n\n{text}"
                response = model.generate_content(prompt)
                summary = response.text.strip()
            st.subheader("Summary:")
            st.success(summary)
        except Exception as e:
            st.error(f"Error: {e}")
