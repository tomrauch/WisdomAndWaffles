import os
import base64
import streamlit as st
from openai import OpenAI
from PyPDF2 import PdfReader
import idiotic_idiom

# ---------------------------
# Setup
# ---------------------------
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
st.set_page_config(page_title="Wisdom & Waffles", layout="centered")

# ---------------------------
# Banner / Intro
# ---------------------------
st.markdown(
    """
    <div style="text-align:center; padding:15px;">
        <h1 style="color:#5a381e; font-family:Georgia, serif;">☕ Wisdom & Waffles 🧇</h1>
        <p style="font-size:18px; color:#5a381e; font-family:Georgia, serif;">
            A diner-themed space where different perspectives meet.  
            Explore history, economics, and policy together — share ideas, find common ground, and spark civil debate.  
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------------------
# Disclaimer with PDF Button
# ---------------------------
pdf_path = "ideology_chatbot_sources.pdf"
if os.path.exists(pdf_path):
    with open(pdf_path, "rb") as pdf_file:
        pdf_bytes = pdf_file.read()
    b64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")

    st.markdown(
        f"""
        <div style="background-color:#f9f9f9; padding:15px; border-radius:8px; 
                    border-left: 5px solid #FFCC00; margin-bottom: 1.5rem;">
            ⚠️ <b>Disclaimer:</b> This app does not log or save your inputs.  
            Do not upload personal, sensitive, or confidential documents.  
            Responses are AI-generated and for educational purposes only.  
            <br><br>
            📄 <a href="data:application/pdf;base64,{b64_pdf}" 
            target="_blank" style="text-decoration:none; color:#0066cc; font-weight:bold;">
            View Sources PDF
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.warning("⚠️ Disclaimer: No sources PDF found. Please ensure ideology_chatbot_sources.pdf is in the project folder.")

# ---------------------------
# File Upload
# ---------------------------
st.subheader("📂 Upload a File for Analysis (Optional)")
uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

pdf_text = ""
if uploaded_file is not None:
    reader = PdfReader(uploaded_file)
    for page in reader.pages:
        pdf_text += page.extract_text()

# ---------------------------
# Question Input
# ---------------------------
st.subheader("❓ Ask a Question")
user_question = st.text_area(
    "Type your question about history, economics, or the workforce:",
    placeholder="Example: What are the benefits of tariffs for the US economy?"
)

# ---------------------------
# Perspective Selector
# ---------------------------
st.subheader("👓 Choose Perspectives")
perspectives = [
    "Conservative", "Liberal", "Libertarian", "Progressive",
    "Neoclassical", "Keynesian", "Marxist", "Green/New Deal", "Populist"
]

selected_perspectives = st.multiselect(
    "Choose up to 3 perspectives",
    perspectives,
    max_selections=3
)

# ---------------------------
# Submit Button
# ---------------------------
if st.button("🔍 Cook Up Perspectives"):
    if not user_question:
        st.warning("Please enter a question.")
    elif not selected_perspectives:
        st.warning("Please choose at least one perspective.")
    else:
        overlay = st.empty()
        overlay.markdown(
            """
            <div style="position:fixed; top:0; left:0; width:100%; height:100%;
                        background-color:rgba(255,255,255,0.85); z-index:1000;
                        display:flex; flex-direction:column; align-items:center; justify-content:center;">
                <h2 style="color:#5a381e; font-family:Georgia, serif;">🍳 Cooking up perspectives...</h2>
                <progress max="100" value="40" style="width:60%; height:25px;"></progress>
            </div>
            """,
            unsafe_allow_html=True
        )

        responses = {}
        for p in selected_perspectives:
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": f"You are simulating a {p} perspective."},
                        {"role": "user", "content": user_question + ("\n\nContext:\n" + pdf_text if pdf_text else "")}
                    ],
                )
                responses[p] = response.choices[0].message.content.strip()
            except Exception as e:
                responses[p] = f"Error fetching {p} perspective: {str(e)}"

        overlay.markdown(
            """
            <div style="position:fixed; top:0; left:0; width:100%; height:100%;
                        background-color:rgba(255,255,255,0.85); z-index:1000;
                        display:flex; flex-direction:column; align-items:center; justify-content:center;">
                <h2 style="color:#5a381e; font-family:Georgia, serif;">📝 Cooking up summary...</h2>
                <progress max="100" value="80" style="width:60%; height:25px;"></progress>
            </div>
            """,
            unsafe_allow_html=True
        )

        try:
            summary_prompt = (
                f"Compare these perspectives on the question '{user_question}':\n\n"
                + "\n\n".join([f"{p}: {r}" for p, r in responses.items()])
                + "\n\nProvide a brief summary of the major similarities and differences."
            )
            summary_resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a neutral summarizer of ideological perspectives."},
                    {"role": "user", "content": summary_prompt}
                ],
            )
            summary_text = summary_resp.choices[0].message.content.strip()
        except Exception as e:
            summary_text = f"Error generating summary: {str(e)}"

        overlay.empty()

        st.subheader("🍽️ Perspectives")
        for p, r in responses.items():
            st.markdown(f"**{p}:** {r}")

        st.subheader("🔎 Summary of Similarities and Differences")
        st.info(summary_text)

# ---------------------------
# Idiotic Idiom Generator
# ---------------------------
idiotic_idiom.render_idiom_badge(st)
