import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables (optional for local dev)
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ---------------------------
# Streamlit Page Config
# ---------------------------
st.set_page_config(
    page_title="Wisdom & Waffles",
    page_icon="🧇",
    layout="wide"
)

# ---------------------------
# Banner & Intro
# ---------------------------
st.markdown(
    """
    <div style="text-align:center; padding: 15px; background-color:#fffaf0; border-radius:10px;">
        <h1 style="color:#6b4226; font-family:Georgia, serif;">☕ Wisdom & Waffles 🧇</h1>
        <p style="font-size:18px; color:#444;">
        A diner-themed space where people from across the political spectrum<br>
        can share their views, understand differences, and seek common ground.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("---")

# ---------------------------
# Upload a File
# ---------------------------
with st.container():
    st.header("📂 Upload a File for Analysis (Optional)")
    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

# ---------------------------
# Ask a Question
# ---------------------------
with st.container():
    st.header("❓ Ask a Question")
    question = st.text_area(
        "Type your question about history, economics, or the workforce:",
        placeholder="What are the benefits of tariffs for the US economy?"
    )

# ---------------------------
# Choose Perspectives
# ---------------------------
perspectives = [
    "Populist", "Libertarian", "Progressive", "Conservative",
    "Green/New Deal", "Neoclassical", "Keynesian"
]

with st.container():
    st.header("👓 Choose Perspectives")
    selected = st.multiselect(
        "Choose up to 3 perspectives",
        perspectives,
        max_selections=3
    )

# ---------------------------
# Submit Button
# ---------------------------
if st.button("🍳 Cook Up Perspectives", type="primary"):
    if not question.strip():
        st.error("Please enter a question first.")
    elif not selected:
        st.error("Please choose at least one perspective.")
    else:
        # Progress overlay
        progress = st.empty()
        progress.progress(0, "Firing up the grill...")

        responses = {}
        for i, p in enumerate(selected, start=1):
            progress.progress(int(i / len(selected) * 100), f"Cooking {p} perspective...")
            # TODO: Replace simulated answer with real OpenAI call
            responses[p] = f"Simulated answer for {p} perspective on '{question}'"

        progress.progress(100, "Plating results... 🍽️")
        progress.empty()

        # Show results
        st.subheader("🍽️ Perspectives")
        results_text = "\n".join([f"**{p}:** {r}" for p, r in responses.items()])
        st.markdown(results_text)

        # Generate summary
        with st.spinner("Summarizing similarities and differences..."):
            summary = "Similarities: Common concerns.\nDifferences: Policy solutions."

        st.subheader("🔎 Summary of Similarities and Differences")
        st.info(summary)

