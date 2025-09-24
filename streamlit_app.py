from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import json
from openai import OpenAI
from PyPDF2 import PdfReader

# Load perspectives
with open("data/perspectives.json", "r") as f:
    perspectives = json.load(f)

# OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ---------------------------
# App Title & Disclaimer
# ---------------------------
st.title("Ideology Chatbot")
st.write("Compare how different ideologies analyze history, economics, and policy.")

st.info(
    "⚠️ **Disclaimer:** This app does not log or save your inputs. "
    "Do not upload personal, sensitive, or confidential documents. "
    "Responses are AI-generated and for educational purposes only."
)

# ---------------------------
# Optional File Upload
# ---------------------------
st.subheader("📂 Upload a File for Analysis (Optional)")
uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

file_text = None
if uploaded_file is not None:
    pdf_reader = PdfReader(uploaded_file)
    file_text = ""
    for page in pdf_reader.pages:
        file_text += page.extract_text()

# ---------------------------
# User Question
# ---------------------------
st.subheader("❓ Ask a question")
user_question = st.text_input("Ask a question about history, economics, or the workforce:")

# ---------------------------
# Perspectives Selection
# ---------------------------
st.subheader("👓 Choose Perspectives")
selected_perspectives = st.multiselect(
    "Select up to 3 perspectives",
    list(perspectives.keys()),
    max_selections=3
)

# ---------------------------
# Submit Button
# ---------------------------
if st.button("Submit"):
    if user_question and selected_perspectives:
        responses = {}
        for perspective in selected_perspectives:
            context = file_text if file_text else ""
            prompt = f"You are a chatbot with the following perspective:\n{perspectives[perspective]}\n\n"
            if context:
                prompt += f"Here is some context from an uploaded file:\n{context}\n\n"
            prompt += f"Answer this question:\n{user_question}"

            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "system", "content": prompt}],
                temperature=0.7
            )
            responses[perspective] = response.choices[0].message.content

        # Display side-by-side
        cols = st.columns(len(responses))
        for i, (perspective, answer) in enumerate(responses.items()):
            with cols[i]:
                st.markdown(f"### {perspective} Perspective")
                st.write(answer)

        # Add a similarities/differences summary
        if len(responses) > 1:
            combined_text = "\n\n".join(
                [f"{p}: {a}" for p, a in responses.items()]
            )
            summary_prompt = (
                "Compare the following ideological perspectives. "
                "Highlight major similarities and differences clearly:\n\n"
                f"{combined_text}"
            )
            summary_response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "system", "content": summary_prompt}],
                temperature=0.7
            )
            st.markdown("## 🔎 Similarities and Differences")
            st.write(summary_response.choices[0].message.content)

# ---------------------------
# Idiotic Idiom Badge
# ---------------------------
if st.button("🎲 Generate Idiotic Idiom"):
    from idiotic_idiom import generate_idiom
    idiom = generate_idiom()
    st.success(f"💡 Idiotic Idiom: {idiom}")
