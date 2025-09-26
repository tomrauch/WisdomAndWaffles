import os
import json
import streamlit as st
from openai import OpenAI
import PyPDF2

# ---------------------------
# OpenAI Client
# ---------------------------
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ---------------------------
# Disclaimer Banner
# ---------------------------
st.markdown(
    """
    <div style='background-color: #fff3cd; padding: 15px; border-radius: 10px; border: 1px solid #ffeeba;'>
        ⚠️ <b>Disclaimer:</b> This app is for educational and exploratory purposes only. 
        It simulates ideological perspectives using AI. 
        
    </div>
    """,
    unsafe_allow_html=True
)

pdf_path = "assets/ideology_chatbot_sources.pdf"

if os.path.exists(pdf_path):
    with open(pdf_path, "rb") as pdf_file:
        st.download_button(
            label="📄 View Sources PDF",
            data=pdf_file,
            file_name="ideology_chatbot_sources.pdf",
            mime="application/pdf",
        )
else:
    st.warning("⚠️ Sources PDF not found. Please ensure assets/ideology_chatbot_sources.pdf exists.")

    # ---------------------------
# App Header (Mission / Theme)
# ---------------------------
st.markdown(
    """
    <div style='text-align: center; padding: 20px;'>
        <h1 style='margin-bottom: 0;'>🥞 Wisdom & Waffles ☕</h1>
        <p style='font-size: 18px; color: #555;'>
            A diner for ideas — where perspectives from across the political spectrum 
            come together to spark understanding, engage in civil debate, and find common ground.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


# ---------------------------
# Load perspectives
# ---------------------------
with open("data/perspectives.json", "r") as f:
    perspectives = json.load(f)

# ---------------------------
# File Upload Section
# ---------------------------
st.subheader("📂 Upload a File for Analysis (Optional)")
uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

uploaded_text = ""
if uploaded_file is not None:
    try:
        reader = PyPDF2.PdfReader(uploaded_file)
        for page in reader.pages:
            uploaded_text += page.extract_text() or ""
        st.success("✅ File uploaded and processed successfully.")
    except Exception as e:
        st.error(f"Failed to process PDF: {e}")

# ---------------------------
# Question Input
# ---------------------------
st.subheader("❓ Ask a Question")
user_question = st.text_area("Type your question here:")

# ---------------------------
# Perspective Selection
# ---------------------------
st.subheader("👓 Choose Perspectives (up to 3)")
selected_perspectives = st.multiselect(
    "Select perspectives:",
    options=list(perspectives.keys()),
    default=[],
    max_selections=3,
)

# ---------------------------
# Submit Button
# ---------------------------
if st.button("🚀 Submit") and user_question and selected_perspectives:
    with st.spinner("Generating perspectives..."):
        responses = {}
        for p in selected_perspectives:
            prompt = f"You are a chatbot with the following perspective:\n{perspectives[p]}\n\n"
            if uploaded_text:
                prompt += f"Here is context from an uploaded document:\n{uploaded_text[:2000]}\n\n"
            prompt += f"Answer this question:\n{user_question}"

            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "system", "content": prompt}],
                temperature=0.7,
            )
            responses[p] = response.choices[0].message.content

        # Save responses in session state
        st.session_state.responses = responses

        # Generate summary and save
        summary_prompt = (
            "Compare and summarize the key similarities and differences "
            "across the following perspectives:\n\n"
            + "\n".join([f"{p}: {r}" for p, r in responses.items()])
        )
        summary_response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": summary_prompt}],
            temperature=0.7,
        )
        st.session_state.summary = summary_response.choices[0].message.content

# ---------------------------
# Display stored results (persist across reruns)
# ---------------------------
if "responses" in st.session_state:
    cols = st.columns(len(st.session_state.responses))
    for idx, (p, r) in enumerate(st.session_state.responses.items()):
        with cols[idx]:
            st.markdown(f"### {p}")
            st.write(r)

if "summary" in st.session_state:
    st.markdown("---")
    st.subheader("🔍 Summary of Similarities and Differences")
    st.info(st.session_state.summary)

# ---------------------------
# Idiotic Idiom Badge (external file)
# ---------------------------
import idiotic_idiom
idiotic_idiom.render_idiom_badge(st)
