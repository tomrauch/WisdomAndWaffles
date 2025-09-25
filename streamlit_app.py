import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import json
import PyPDF2
import idiotic_idiom  # separate file in same folder

# Load environment variables locally (.env), safe to keep for Streamlit Cloud too
load_dotenv()

# Set up OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load perspectives from JSON
with open("data/perspectives.json", "r") as f:
    perspectives = json.load(f)

# ---------------------------
# App Title + Disclaimer
# ---------------------------
st.title("🧭 Ideology Chatbot")
st.write("Compare how different ideologies analyze history, economics, and policy.")

st.info("⚠️ Disclaimer: This app does not log or save your inputs. "
        "Do not upload personal, sensitive, or confidential documents. "
        "Responses are AI-generated and for educational purposes only.")

# ---------------------------
# Upload File Card
# ---------------------------
with st.container():
    st.markdown("### 📂 Upload a File for Analysis (Optional)")
    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

    file_text = ""
    if uploaded_file:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        file_text = "\n".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])
        st.markdown("#### 📑 Extracted PDF Content")
        st.text(file_text[:1000] + "..." if len(file_text) > 1000 else file_text)

# ---------------------------
# Question + Perspectives (Form)
# ---------------------------
with st.container():
    st.markdown("### ❓ Ask a Question")
    with st.form("ideology_form"):
        user_question = st.text_input("Type your question about history, economics, or the workforce:")

        selected_perspectives = st.multiselect(
            "Choose perspectives (max 3 will be analyzed)",
            list(perspectives.keys())
        )

        submitted = st.form_submit_button("Submit")

    # Enforce a soft max of 3
    if len(selected_perspectives) > 3:
        st.warning("⚠️ You selected more than 3. Only the first 3 will be analyzed.")
        selected_perspectives = selected_perspectives[:3]

# ---------------------------
# Response Generation with Status Overlay
# ---------------------------
if submitted and user_question and selected_perspectives:
    responses = {}

    with st.status("Processing your request...", expanded=True) as status:
        # Step 1: Perspectives
        st.write("🔄 Generating perspectives...")
        for p in selected_perspectives:
            context = f"\n\nRelevant document text:\n{file_text}" if file_text else ""
            prompt = (
                f"You are a chatbot with the following perspective:\n{perspectives[p]}\n\n"
                f"Answer this question:\n{user_question}{context}"
            )
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "system", "content": prompt}],
                temperature=0.7
            )
            try:
                responses[p] = response.choices[0].message["content"]
            except:
                responses[p] = response.choices[0].message.content

        # Step 2: Summary
        summary_text = ""
        if len(responses) > 1:
            st.write("🔄 Generating summary of similarities and differences...")
            summary_prompt = (
                "Compare the following ideological responses. "
                "Highlight major similarities and differences:\n\n"
                + "\n\n".join([f"{p}: {r}" for p, r in responses.items()])
            )
            summary_response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "system", "content": summary_prompt}],
                temperature=0.5
            )
            try:
                summary_text = summary_response.choices[0].message["content"]
            except:
                summary_text = summary_response.choices[0].message.content

        status.update(label="✅ Completed", state="complete", expanded=False)

    # Display responses
    st.markdown("### 📝 Responses")
    cols = st.columns(len(responses))
    for i, (p, r) in enumerate(responses.items()):
        with cols[i]:
            st.subheader(p)
            st.write(r)

    # Display summary in its own card
    if summary_text:
        with st.container():
            st.markdown("### 🔍 Summary of Similarities and Differences")
            st.write(summary_text)

# ---------------------------
# Idiotic Idiom Generator
# ---------------------------
with st.container():
    st.markdown("### 🎲 Just for Fun")
    if st.button("Generate Idiotic Idiom"):
        st.success(f"💡 Idiotic Idiom: {idiotic_idiom.generate_idiom()}")
