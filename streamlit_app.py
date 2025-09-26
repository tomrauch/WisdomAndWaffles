import os
import random
import streamlit as st
from openai import OpenAI
from PyPDF2 import PdfReader
import idiotic_idiom

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ---------------------------
# Banner + Diner Mission Text
# ---------------------------

st.markdown(
    """
    <div style="text-align:center; margin-bottom: 1rem;">
        <img src="assets/waffle_banner.png" width="500">
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <h2 style='text-align: center; color: #4B2E2E; font-family: Georgia;'>
        Welcome to <b>Wisdom & Waffles</b> 🧇☕
    </h2>
    <p style='text-align: center; font-size: 1.1rem; max-width: 800px; margin: auto; color: #333;'>
        A friendly diner for ideas — where people from across the political spectrum can 
        share their views, find similarities and differences, and seek common ground 
        for the benefit of all. Pull up a booth, grab some coffee, and join the conversation.
    </p>
    """,
    unsafe_allow_html=True
)

# ---------------------------
# Custom CSS for diner look
# ---------------------------
st.markdown(
    """
    <style>
        .stCard {
            background-color: #fdfaf5;
            border: 1px solid #e0d6c8;
            border-radius: 8px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            box-shadow: 2px 2px 8px rgba(0,0,0,0.05);
        }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------
# File Upload Card
# ---------------------------
with st.container():
    st.markdown("## 📂 Upload a File for Analysis (Optional)")
    uploaded_file = st.file_uploader("Upload PDF", type="pdf")
    pdf_text = ""
    if uploaded_file is not None:
        reader = PdfReader(uploaded_file)
        for page in reader.pages:
            pdf_text += page.extract_text() or ""
        st.markdown("### 📝 Extracted PDF Content")
        st.write(pdf_text[:1000] + ("..." if len(pdf_text) > 1000 else ""))

# ---------------------------
# Ask a Question Card
# ---------------------------
with st.container():
    st.markdown("## ❓ Ask a Question")
    user_question = st.text_area(
        "Type your question about history, economics, or the workforce:",
        placeholder="What are the benefits of tariffs for the US economy?",
        height=70
    )

# ---------------------------
# Choose Perspectives Card
# ---------------------------
with st.container():
    st.markdown("## 👓 Choose Perspectives")
    perspectives = {
        "Populist": "Analyze from a populist viewpoint, focusing on common people vs. elites.",
        "Neoclassical": "Analyze with emphasis on markets, efficiency, and rational choice.",
        "Progressive": "Analyze with focus on reform, equity, and social welfare.",
        "Libertarian": "Analyze from an individual freedom and limited government view.",
        "Keynesian": "Analyze with focus on government intervention and demand management.",
        "Green/New Deal": "Analyze with emphasis on climate, sustainability, and systemic reform."
    }

    selected_perspectives = st.multiselect(
        "Choose up to 3 perspectives",
        options=list(perspectives.keys()),
        max_selections=3
    )

    submit = st.button("Submit")

# ---------------------------
# Process User Input
# ---------------------------
if submit and user_question and selected_perspectives:
    with st.spinner("🍳 Cooking up perspectives..."):
        responses = {}
        for perspective in selected_perspectives:
            prompt = f"You are a chatbot with the following perspective: {perspectives[perspective]}\n\nQuestion: {user_question}"
            completion = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "system", "content": prompt}],
                temperature=0.7
            )
            responses[perspective] = completion.choices[0].message.content

        # Display results side-by-side
        cols = st.columns(len(selected_perspectives))
        for col, perspective in zip(cols, selected_perspectives):
            with col:
                st.markdown(f"### {perspective}")
                st.write(responses[perspective])

        # Generate summary of similarities and differences
        if len(selected_perspectives) > 1:
            summary_prompt = (
                f"Compare and summarize the major similarities and differences between these perspectives: {', '.join(selected_perspectives)}.\n"
                f"Here are their responses to the question '{user_question}':\n"
                + "\n".join([f"{p}: {r}" for p, r in responses.items()])
            )
            summary_completion = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "system", "content": summary_prompt}],
                temperature=0.7
            )
            summary = summary_completion.choices[0].message.content

            with st.container():
                st.markdown("## 🔎 Summary of Similarities and Differences")
                st.write(summary)

# ---------------------------
# Idiotic Idiom Badge
# ---------------------------
idiotic_idiom.render_idiom_badge(st)
