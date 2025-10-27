import streamlit as st
import google.generativeai as genai
import os

# Page setup
st.set_page_config(page_title="Gemini AI Summarizer", page_icon="🧠", layout="wide")

# Custom CSS to center content and create a shadow card
st.markdown("""
<style>
body {
    background-color: #0f1116;
}
.main {
    display: flex;
    justify-content: center;
}
.card {
    background-color: #1c1e24;
    width: 70%;
    padding: 3rem 4rem;
    border-radius: 16px;
    box-shadow: 0 4px 25px rgba(0,0,0,0.4);
}
h1 {
    text-align: center;
    color: #e5e7eb;
    margin-bottom: 0.3rem;
}
.subtext {
    text-align: center;
    color: #9ca3af;
    font-size: 1rem;
    margin-bottom: 2rem;
}
textarea {
    border-radius: 8px !important;
    border: 1px solid #374151 !important;
    background: #111319 !important;
    color: #e5e7eb !important;
    font-size: 16px !important;
}
.stButton>button {
    background: #6366f1;
    color: white;
    font-weight: 500;
    border-radius: 8px;
    border: none;
    padding: 0.6rem 1.5rem;
    font-size: 1rem;
    transition: 0.2s;
}
.stButton>button:hover {
    background: #4f46e5;
}
.summary-box {
    background: #111319;
    border: 1px solid #2e3036;
    padding: 1rem 1.5rem;
    border-radius: 10px;
    margin-top: 1.5rem;
}
.summary-title {
    color: #facc15;
    font-weight: 700;
    font-size: 1.2rem;
    margin-bottom: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

# Gemini configuration
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("Missing environment variable: GEMINI_API_KEY")
else:
    genai.configure(api_key=api_key)

# Center the app inside one card
st.markdown("<div class='main'><div class='card'>", unsafe_allow_html=True)

st.markdown("<h1>🧠 Gemini AI Summarizer</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtext'>Summarize any text into 3–4 lines using Google's Gemini model.</p>", unsafe_allow_html=True)

text = st.text_area("Enter or paste text here:", height=200, placeholder="Paste your article or paragraph here...")

if st.button("Summarize"):
    if not text.strip():
        st.warning("Please enter some text.")
    else:
        try:
            model = genai.GenerativeModel("gemini-2.5-flash")
            with st.spinner("Summarizing..."):
                prompt = f"Summarize this text in 3–4 lines, keeping only the key information:\n\n{text}"
                response = model.generate_content(prompt)
                summary = response.text.strip()
            st.markdown("<div class='summary-box'>", unsafe_allow_html=True)
            st.markdown("<div class='summary-title'>✨ Summary:</div>", unsafe_allow_html=True)
            st.markdown(f"<p style='color:#d1d5db; font-size:1rem; line-height:1.6;'>{summary}</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error: {e}")

st.markdown("</div></div>", unsafe_allow_html=True)
