import streamlit as st
import google.generativeai as genai
import os

# Configure page
st.set_page_config(page_title="AI Summarizer", page_icon="🧠", layout="centered")

# Custom CSS styling
st.markdown("""
<style>
    body {
        background-color: #f9fafb;
    }
    .main {
        background: white;
        padding: 2rem;
        border-radius: 1rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }
    h1 {
        text-align: center;
        color: #111827;
        margin-bottom: 0.5rem;
    }
    .subtext {
        text-align: center;
        color: #6b7280;
        font-size: 1rem;
        margin-bottom: 2rem;
    }
    textarea {
        border-radius: 0.5rem;
        border: 1px solid #d1d5db !important;
        font-size: 16px !important;
    }
    .stButton>button {
        background: #4f46e5;
        color: white;
        font-weight: 500;
        border-radius: 8px;
        border: none;
        padding: 0.6rem 1.5rem;
        font-size: 1rem;
        transition: background 0.2s;
    }
    .stButton>button:hover {
        background: #4338ca;
    }
    .summary-box {
        background: #f3f4f6;
        padding: 1rem;
        border-radius: 8px;
        margin-top: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Load API key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("Missing environment variable: GEMINI_API_KEY")
else:
    genai.configure(api_key=api_key)

# UI content
st.markdown("<div class='main'>", unsafe_allow_html=True)
st.title("🧠 Gemini AI Summarizer")
st.markdown("<p class='subtext'>Summarize any text into 3–4 lines using Google's Gemini model.</p>", unsafe_allow_html=True)

text = st.text_area("Enter or paste text here", height=200, placeholder="Paste your article or paragraph...")

if st.button("Summarize"):
    if not text.strip():
        st.warning("Please enter some text.")
    else:
        try:
            model = genai.GenerativeModel("gemini-2.5-flash")
            with st.spinner("Summarizing..."):
                prompt = f"Summarize the following text in 3–4 lines, keeping the key details only:\n\n{text}"
                response = model.generate_content(prompt)
                summary = response.text.strip()

            st.markdown("<div class='summary-box'>", unsafe_allow_html=True)
            st.subheader("✨ Summary:")
            st.write(summary)
            st.markdown("</div>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error: {e}")

st.markdown("</div>", unsafe_allow_html=True)
