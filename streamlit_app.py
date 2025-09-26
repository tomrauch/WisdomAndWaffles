import streamlit as st
import os
import json
import random
from openai import OpenAI
from PyPDF2 import PdfReader

# ---------------------------
# Load API Key
# ---------------------------
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ---------------------------
# Load Perspectives
# ---------------------------
with open("data/perspectives.json", "r") as f:
    perspectives = json.load(f)

# ---------------------------
# Banner Section
# ---------------------------
banner_path = os.path.join("assets", "waffle_banner.png")

st.image(banner_path, use_container_width=True, caption="Wisdom & Waffles Banner")

st.markdown(
    """
    <h2 style="text-align: center; color: #4B2E2E;">
        Welcome to <b>Wisdom & Waffles</b> 🧇 ☕
    </h2>
    <p style="text-align: center; font-size: 18px; color: #5C4033;">
        A cozy diner-inspired space where people from across the political spectrum
        can share their views, find common ground, and foster civil debate
        for the benefit of all.
    </p>
    """,
    unsafe_allow_html=True
)

# ---------------------------
# Disclaimer Banner
# ---------------------------
st.markdown(
    """
    <div style="background-color:#f9f9f9; padding:10px; border-radius:8px; border-left: 5px solid #FFCC00;">
        ⚠️ <b>Disclaimer:</b> This app does not log or save your inputs.
        Do not upload personal, sensitive, or confidential documents. 
        Responses are AI-generated and for educational purposes only.
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------------------
# File Upload Card
# ---------------------------
with st.container():
    st.subheader("📂 Upload a File for Analysis (Optional)")
    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
    pdf_text = ""
    if uploaded_file is not None:
        reader = PdfReader(uploaded_file)
        for page in reader.pages:
            pdf_text += page.extract_text() or ""
        st.markdown("### 📄 Extracted PDF Content")
        st.write(pdf_text[:1000] + ("..." if len(pdf_text) > 1000 else ""))

# ---------------------------
# Question + Perspective Card
# ---------------------------
st.subheader("❓ Ask a Question")

user_question = st.text_area(
    "Type your question about history, economics, or the workforce:",
    placeholder="What is the importance of the second amendment of the constitution?",
)

selected_perspectives = st.multiselect(
    "Choose up to 3 perspectives",
    list(perspectives.keys()),
    max_selections=3,
)

# Submit button
submit = st.button("Submit Question")

# ---------------------------
# Generate Responses
# ---------------------------
if submit and user_question and selected_perspectives:
    # Show locked overlay with progress
    with st.spinner("Generating perspectives..."):
        responses = {}
        for perspective in selected_perspectives:
            prompt = f"You are a chatbot with the following perspective:\n{perspectives[perspective]}\n\nAnswer this question:\n{user_question}\n\nContext (if any): {pdf_text}"
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "system", "content": prompt}],
                temperature=0.7,
            )
            responses[perspective] = resp.choices[0].message.content

    # Display perspective responses
    st.markdown("## 🍽️ Perspectives")
    cols = st.columns(len(selected_perspectives))
    for idx, perspective in enumerate(selected_perspectives):
        with cols[idx]:
            st.markdown(f"### {perspective}")
            st.write(responses[perspective])

    # Generate similarities/differences summary
    with st.spinner("Generating summary..."):
        comparison_prompt = f"Compare and summarize the major similarities and differences among these perspectives:\n\n{json.dumps(responses, indent=2)}"
        summary_resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": comparison_prompt}],
            temperature=0.7,
        )
        summary = summary_resp.choices[0].message.content

    st.markdown("## 🔎 Summary of Similarities and Differences")
    st.write(summary)

# ---------------------------
# Idiotic Idiom Generator
# ---------------------------
def generate_idiom():
    subjects = [
        "a frog", "teacher", "no sandwich", "a cloud", "my toothbrush",
        "a penguin", "this laptop", "my neighbor’s cat", "an elevator", "a cactus"
    ]
    verbs = [
        "jumps over", "complains about", "tickles", "dances with", "argues with",
        "confuses", "balances on", "runs away from", "interviews", "ignores"
    ]
    objects = [
        "the moon", "a spatula", "quantum foam", "regret", "a lazy river",
        "traffic cones", "a potato chip", "the stock market", "a shoelace", "jellybeans"
    ]
    endings = [
        "on Thursdays", "without warning", "if nobody watches", "in traffic", "during tax season",
        "while humming loudly", "before lunch", "after midnight", "on roller skates", "inside a dream"
    ]
    return f"{random.choice(subjects)} {random.choice(verbs)} {random.choice(objects)} {random.choice(endings)}."

if st.button("🎲 Generate Idiotic Idiom"):
    st.success(f"💡 Idiotic Idiom: {generate_idiom()}")
