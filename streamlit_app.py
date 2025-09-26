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
    .stApp {
        background-color: #fdf3e7;
        background-image: url('https://www.transparenttextures.com/patterns/cream-pixels.png');
    }
    h2, h3 {
        font-family: 'Courier New', monospace;
        color: #5a2d0c;
    }
    .stCard {
        background-color: #fff9f4;
        border: 2px solid #8B0000;
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 4px 4px 8px rgba(0,0,0,0.15);
    }
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
# Banner & Mission Statement
# ---------------------------
st.markdown(
    """
    <div style="text-align: center; margin-bottom: 20px;">
        <img src="assets/waffle_banner.png" style="width: 100%; max-height: 250px; object-fit: cover; border-bottom: 4px double #8B0000;" alt="Wisdom & Waffles Banner">
    </div>
    <div style="text-align: center; font-family: Georgia, serif; font-size: 18px; color: #5a2d0c; margin: 15px 0 25px 0;">
        Welcome to <b>Wisdom & Waffles</b> 🧇☕ <br><br>
        A diner where ideas are served hot, and everyone has a seat at the table.  
        Here, people from across the political and ideological spectrum come together  
        to share perspectives, foster civil debate, and seek common ground  
        for the benefit of all.
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------------------
# Disclaimer
# ---------------------------
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
        "Choose perspectives (max 3)",
        list(perspectives.keys())
    )

    if len(perspectives_selected) > 3:
        st.warning("🚦 Please limit your selection to 3 perspectives. Only the first 3 will be used.")
        perspectives_selected = perspectives_selected[:3]

    submitted = st.form_submit_button("🍳 Place Your Order")

# ---------------------------
# Generate Responses
# ---------------------------
if submitted and user_question and perspectives_selected:
    with st.spinner("🍳 Cooking up your perspectives... please wait!"):
        progress_container = st.empty()
        progress_bar = st.progress(0)

        responses = {}
        for i, p in enumerate(perspectives_selected, start=1):
            progress_container.markdown(f"👓 Generating **{p}** perspective...")
            prompt = f"You are a chatbot with the following perspective:\n{perspectives[p]}\n\nAnswer this question:\n{user_question}\n\nAdditional context:\n{extracted_text}"
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "system", "content": prompt}],
                temperature=0.7
            )
            responses[p] = response.choices[0].message.content
            progress_bar.progress(int((i / len(perspectives_selected)) * 100))

        progress_container.markdown("🍽️ Generating summary of similarities and differences...")
        summary_prompt = f"Compare the following ideological responses. Summarize the key similarities and differences:\n\n{responses}"
        summary_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": summary_prompt}],
            temperature=0.7
        )
        summary_text = summary_response.choices[0].message.content
        progress_bar.progress(100)

    progress_container.empty()
    progress_bar.empty()

    st.subheader("🍽️ Responses from the Diner Booths")
    cols = st.columns(len(perspectives_selected))
    for idx, (p, ans) in enumerate(responses.items()):
        with cols[idx]:
            st.markdown(f"### {p}")
            st.write(ans)

    st.subheader("👨‍🍳 Chef’s Special: Perspectives Compared")
    st.info(summary_text)

# ---------------------------
# Idiotic Idiom (Fortune Cookie)
# ---------------------------
st.markdown("---")
idiotic_idiom.render_idiom_badge(st)

