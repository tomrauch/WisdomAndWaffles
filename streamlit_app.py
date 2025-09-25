import streamlit as st
from openai import OpenAI
import os
import json
import PyPDF2

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load perspectives
with open("data/perspectives.json", "r") as f:
    perspectives = json.load(f)

# ---------------------------
# App Title & Disclaimer
# ---------------------------
st.title("Ideology Chatbot")
st.write("Compare how different ideologies analyze history, economics, and policy.")

st.info("⚠️ Disclaimer: This app does not log or save your inputs. "
        "Do not upload personal, sensitive, or confidential documents. "
        "Responses are AI-generated and for educational purposes only.")

# ---------------------------
# File Upload Card
# ---------------------------
with st.container():
    st.markdown("### 📂 Upload a File for Analysis (Optional)")
    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
    uploaded_text = ""

    if uploaded_file is not None:
        try:
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            uploaded_text = " ".join([page.extract_text() or "" for page in pdf_reader.pages])
            st.success("✅ PDF uploaded and text extracted successfully!")
            st.markdown("#### Extracted PDF Content")
            st.write(uploaded_text[:1000] + ("..." if len(uploaded_text) > 1000 else ""))
        except Exception as e:
            st.error(f"Error reading PDF: {e}")

# ---------------------------
# Question & Perspectives Card
# ---------------------------
with st.container():
    st.markdown("### ❓ Ask a Question")

    with st.form("question_form"):
        user_question = st.text_input(
            "Type your question about history, economics, or the workforce:",
            key="user_question",
            label_visibility="visible"
        )

        selected_perspectives = st.multiselect(
            "Choose up to 3 perspectives",
            options=list(perspectives.keys()),
            max_selections=3,
        )

        submit_button = st.form_submit_button("🔍 Submit Question")

# ---------------------------
# Handle Submit
# ---------------------------
if submit_button and user_question and selected_perspectives:
    results = {}

    with st.spinner("⚙️ Generating perspectives..."):
        for perspective in selected_perspectives:
            prompt = f"""
            You are a chatbot with the following perspective: {perspectives[perspective]}.
            Question: {user_question}
            Uploaded text (if relevant): {uploaded_text[:1000]}
            Provide a thoughtful answer from this perspective.
            """

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "system", "content": prompt}],
                temperature=0.7
            )
            results[perspective] = response.choices[0].message.content

    # Display each perspective in its own card
    for perspective, answer in results.items():
        with st.container():
            st.markdown(f"#### {perspective}")
            st.write(answer)

    # Generate summary
    with st.spinner("📝 Generating summary of similarities and differences..."):
        combined_text = "\n\n".join([f"{k}: {v}" for k, v in results.items()])
        summary_prompt = f"""
        Compare the following ideological perspectives' answers.
        Summarize the most important similarities and differences clearly.

        {combined_text}
        """

        summary_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": summary_prompt}],
            temperature=0.5
        )

        with st.container():
            st.markdown("### 🔎 Summary of Similarities and Differences")
            st.write(summary_response.choices[0].message.content)

# ---------------------------
# Idiotic Idiom Badge
# ---------------------------
import idiotic_idiom
idiotic_idiom.render_idiom_badge(st)

