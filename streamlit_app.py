import os
import json
import streamlit as st
from openai import OpenAI
import PyPDF2
import idiotic_idiom

# Load perspectives from JSON
with open("data/perspectives.json", "r") as f:
    perspectives = json.load(f)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ---------------------------
# Retro Diner Theme Styling
# ---------------------------
st.markdown(
    """
    <style>
    /* Diner background (tablecloth) */
    .stApp {
        background-color: #fdf3e7;
        background-image: url('https://www.transparenttextures.com/patterns/cream-pixels.png');
    }

    /* Title */
    h1 {
        font-family: 'Georgia', serif;
        font-size: 3em;
        color: #8B0000;
        text-align: center;
        border-bottom: 3px double #8B0000;
        padding-bottom: 0.2em;
    }

    /* Subheadings */
    h2, h3 {
        font-family: 'Courier New', monospace;
        color: #5a2d0c;
    }

    /* Cards */
    .stCard {
        background-color: #fff9f4;
        border: 2px solid #8B0000;
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 4px 4px 8px rgba(0,0,0,0.15);
    }

    /* Buttons */
    .stButton > button {
        background-color: #ffcc00;
        color: black;
        border-radius: 12px;
        font-weight: bold;
        padding: 10px 20px;
        border: 2px solid #8B0000;
    }
    .stButton > button:hover {
        background-color: #ffa500;
        color: white;
    }

    /* Disclaimer */
    .stAlert {
        background-color: #fff3cd;
        border: 2px dashed #856404;
        border-radius: 10px;
        font-family: 'Courier New', monospace;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------
# App Title & Disclaimer
# ---------------------------
st.title("🧇 Wisdom & Waffles: The Ideology Diner")

st.info(
    "⚠️ Disclaimer: This app does not log or save your inputs. "
    "Do not upload personal, sensitive, or confidential documents. "
    "Responses are AI-generated and for educational purposes only."
)

# ---------------------------
# File Upload
# ---------------------------
with st.container():
    st.subheader("📂 Upload a File for Analysis (Optional)")
    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

    extracted_text = ""
    if uploaded_file is not None:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        extracted_text = " ".join([page.extract_text() or "" for page in pdf_reader.pages])
        st.markdown("#### 📑 Extracted PDF Content")
        st.write(extracted_text[:1000] + ("..." if len(extracted_text) > 1000 else ""))

# ---------------------------
# Ask a Question + Perspectives
# ---------------------------
with st.form("ideology_form"):
    st.subheader("❓ Ask a Question")
    user_question = st.text_area(
        "Type your question about history, economics, or the workforce:",
        placeholder="What is the importance of the second amendment of the constitution?",
        height=60
    )

    st.subheader("👓 Choose Perspectives")
    perspectives_selected = st.multiselect(
        "Choose up to 3 perspectives",
        list(perspectives.keys()),
        max_selections=3
    )

    submitted = st.form_submit_button("🍳 Place Your Order")

# ---------------------------
# Generate Responses
# ---------------------------
if submitted and user_question and perspectives_selected:
    responses = {}
    progress_text = st.empty()
    progress_bar = st.progress(0)

    for i, p in enumerate(perspectives_selected, start=1):
        progress_text.text(f"👓 Generating {p} perspective...")
        prompt = f"You are a chatbot with the following perspective:\n{perspectives[p]}\n\nAnswer this question:\n{user_question}\n\nAdditional context:\n{extracted_text}"
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": prompt}],
            temperature=0.7
        )
        responses[p] = response.choices[0].message.content
        progress_bar.progress(int((i / len(perspectives_selected)) * 100))

    progress_text.text("🍽️ Generating summary of similarities and differences...")
    summary_prompt = f"Compare the following ideological responses. Summarize the key similarities and differences:\n\n{responses}"
    summary_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": summary_prompt}],
        temperature=0.7
    )
    summary_text = summary_response.choices[0].message.content
    progress_bar.progress(100)
    progress_text.text("✅ Done!")

    # Display responses
    st.subheader("🍽️ Responses from the Diner Booths")
    cols = st.columns(len(perspectives_selected))
    for idx, (p, ans) in enumerate(responses.items()):
        with cols[idx]:
            st.markdown(f"### {p}")
            st.write(ans)

    # Summary card
    st.subheader("👨‍🍳 Chef’s Special: Perspectives Compared")
    st.info(summary_text)

# ---------------------------
# Idiotic Idiom (Fortune Cookie)
# ---------------------------
st.markdown("---")
idiotic_idiom.render_idiom_badge(st)
