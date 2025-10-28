import streamlit as st
import google.generativeai as genai
import os

# Configure page
st.set_page_config(page_title="Gemini AI Summarizer", page_icon="🧠", layout="wide")

# Custom global CSS
st.markdown("""
<style>
/* Remove Streamlit’s default padding, header, footer, and block backgrounds */
header, footer, [data-testid="stDecoration"], [data-testid="stToolbar"], 
[data-testid="stSidebar"], [data-testid="stStatusWidget"], 
[data-testid="stHeader"], [data-testid="stVerticalBlock"] > div:first-child {
    display: none !important;
}
section.main {
    padding-top: 0 !important;
    padding-bottom: 0 !important;
}

/* Center everything in one main plate */
.main-container {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #0f1116;
}

/* Card style */
.card {
    background-color: #1c1e24;
    width: 75%;
    max-width: 900px;
    padding: 3rem 4rem;
    border-radius: 18px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.5);
}

/* Typography and widgets */
h1 {
    text-align: center;
    color: #f9fafb;
    margin-bottom: 0.5rem;
    font-size: 2.2rem;
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
    color: #f9fafb !important;
    font-size: 16px !important;
}
.stButton>button {
    background: #6366f1;
    color: white;
    border-radius: 8px;
    padding: 0.7rem 1.6rem;
    border: none;
    font-size: 1rem;
    transition: background 0.2s;
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

# Configure Gemini API
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("Missing environment variable: GEMINI_API_KEY")
else:
    genai.configure(api_key=api_key)

# Unified container for all UI
st.markdown("<div class='main-container'><div class='card'>", unsafe_allow_html=True)

st.markdown("<h1>🧠 Gemini AI Summarizer</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtext'>Summarize any text into 3–4 lines using Google's Gemini model.</p>", unsafe_allow_html=True)

text = st.text_area("Enter or paste text here:", height=200, placeholder="Paste your article or paragraph...")

if st.button("Summarize"):
    if not text.strip():
        st.warning("Please enter some text.")
    else:
        try:
            model = genai.GenerativeModel("gemini-2.5-flash")
            with st.spinner("Summarizing..."):
                prompt = f"Summarize this text in 3–4 lines, keeping key points only:\n\n{text}"
                response = model.generate_content(prompt)
                summary = response.text.strip()

            st.markdown("<div class='summary-box'>", unsafe_allow_html=True)
            st.markdown("<div class='summary-title'>✨ Summary:</div>", unsafe_allow_html=True)
            st.markdown(f"<p style='color:#e5e7eb; font-size:1rem; line-height:1.6;'>{summary}</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error: {e}")

st.markdown("</div></div>", unsafe_allow_html=True)
