import streamlit as st
from openai import OpenAI
import os
import json
from dotenv import load_dotenv
import PyPDF2
import random

# Load environment variables from .env
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load perspectives from JSON file
with open("data/perspectives.json", "r") as f:
    perspectives = json.load(f)

st.title("Ideology Chatbot")
st.write("Compare how different ideologies analyze history, economics, and policy.")

st.info(
    "⚠️ **Disclaimer:** This app does not log or save your inputs. "
    "Do not upload personal, sensitive, or confidential documents. "
    "Responses are AI-generated and for educational purposes only."
)

# ---------------------------
# Idiotic Idiom Badge
# ---------------------------
from idiotic_idiom import generate_idiom

# ---------------------------
# Idiotic Idiom Badge
# ---------------------------
if st.button("🎲 Generate a Random Idiotic Idiom For Fun!"):
    idiom = generate_idiom()
    st.success(f"💡 Idiotic Idiom: {idiom}")

# ---------------------------
# File Upload Section
# ---------------------------
st.subheader("📂 Upload a File for Analysis (Optional)")

uploaded_file = st.file_uploader(
    "Upload a text, PDF, or image file",
    type=["txt", "md", "pdf", "png", "jpg", "jpeg"]
)

uploaded_text = None
if uploaded_file:
    file_type = uploaded_file.type

    if file_type in ["text/plain", "text/markdown"]:
        uploaded_text = uploaded_file.read().decode("utf-8")
        st.markdown("### 📄 File Content")
        st.write(uploaded_text)

    elif file_type == "application/pdf":
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        extracted_text = []
        for page in pdf_reader.pages:
            extracted_text.append(page.extract_text() or "")
        uploaded_text = "\n".join(extracted_text)
        st.markdown("### 📄 Extracted PDF Content")
        st.write(uploaded_text[:2000])  # preview only first 2000 chars

    elif file_type in ["image/png", "image/jpeg"]:
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
        st.info("Image analysis not enabled yet. Currently, only preview is available.")

    else:
        st.warning("Unsupported file type.")

# ---------------------------
# Question Section
# ---------------------------
st.subheader("❓ Ask a Question")

user_question = st.text_input("Ask about history, economics, or the workforce:")

# ---------------------------
# Perspectives Section
# ---------------------------
st.subheader("👓 Choose Perspectives")

choices = st.multiselect(
    "Select one or more perspectives",
    options=list(perspectives.keys()),
    default=[]
)

if st.button("Select All"):
    choices = list(perspectives.keys())

# ---------------------------
# Generate Responses
# ---------------------------
if user_question and choices:
    outputs = []
    cols = st.columns(len(choices))

    for i, p in enumerate(choices):
        messages = [
            {"role": "system", "content": f"You are a chatbot with the following perspective:\n{perspectives[p]}"},
        ]
        if uploaded_text:
            messages.append({"role": "user", "content": f"Here is some reference text from an uploaded file:\n\n{uploaded_text}"})
        messages.append({"role": "user", "content": f"Now answer this question:\n{user_question}"})

        with cols[i]:
            with st.spinner(f"Thinking like a {p}..."):
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=messages,
                    temperature=0.7
                )
                text = response.choices[0].message.content
                outputs.append((p, text))
                st.markdown(f"### {p}")
                st.write(text)

    # ---------------------------
    # Comparison Summary
    # ---------------------------
    if len(outputs) > 1:
        combined_text = "\n\n".join([f"{p}: {text}" for p, text in outputs])
        compare_prompt = f"""Compare the following perspectives side-by-side. 
        Highlight the major similarities and differences in how they approach the question:

        {combined_text}
        """

        with st.spinner("Summarizing similarities and differences..."):
            summary = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are an expert comparative analyst of ideologies."},
                    {"role": "user", "content": compare_prompt}
                ],
                temperature=0.5
            )
            st.subheader("🔎 Summary of Similarities and Differences")
            st.write(summary.choices[0].message.content)
