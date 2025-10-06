import streamlit as st
from pathlib import Path
import json
import os
from openai import OpenAI
import PyPDF2
from PIL import Image
import pytesseract
import idiotic_idiom
from dotenv import load_dotenv
# =====================================================
# PAGE CONFIGURATION
# =====================================================
st.set_page_config(page_title="Wisdom & Waffles", page_icon="🧇", layout="wide")

# =====================================================
# OPENAI CLIENT
# =====================================================
# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# =====================================================
# DEFINE TABS
# =====================================================
tab_chatbot, tab_newsstand  = st.tabs(["🧇 Wisdom & Waffles Chatbot","🗞️ Ideology Newsstand"])



# =====================================================
# CHATBOT TAB
# =====================================================
with tab_chatbot:
    st.markdown(
        """
        <div style='text-align: center; padding: 20px;'>
            <h1 style='margin-bottom: 0;'>🥞 Wisdom & Waffles ☕</h1>
            <p style='font-size: 18px; color: #555;'>
                A diner for ideas — where perspectives from across the spectrum come together to spark understanding, encourage civil debate, and find common ground.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    with open("data/perspectives.json", "r") as f:
        perspectives = json.load(f)

    # Upload Section
    st.subheader("📂 Upload a File for Analysis (Optional)")
    uploaded_file = st.file_uploader(
        "Upload a file", type=["pdf", "txt", "jpg", "jpeg", "png"]
    )

    uploaded_text = ""
    if uploaded_file is not None:
        try:
            if uploaded_file.type == "application/pdf":
                reader = PyPDF2.PdfReader(uploaded_file)
                for page in reader.pages:
                    uploaded_text += page.extract_text() or ""
                st.success("✅ PDF uploaded and processed successfully.")

            elif uploaded_file.type == "text/plain":
                uploaded_text = uploaded_file.read().decode("utf-8")
                st.success("✅ TXT file uploaded and processed successfully.")

            elif uploaded_file.type in ["image/jpeg", "image/png"]:
                image = Image.open(uploaded_file)
                uploaded_text = pytesseract.image_to_string(image)
                st.success("✅ Image uploaded and text extracted successfully.")

        except Exception as e:
            st.error(f"Failed to process file: {e}")

    # Question Input
    st.subheader("❓ Ask a Question")
    user_question = st.text_area("Type your question here:")

    # Perspective Selection
    st.subheader("👓 Choose Perspectives (up to 3)")
    selected_perspectives = st.multiselect(
        "Select perspectives:",
        options=list(perspectives.keys()),
        default=[],
        max_selections=3,
    )

    # Submit Button
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

            # Store responses
            st.session_state.responses = responses

            # Generate summary
            summary_prompt = (
                "Compare and summarize the key similarities and differences across the following perspectives:\n\n"
                + "\n".join([f"{p}: {r}" for p, r in responses.items()])
            )
            summary_response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "system", "content": summary_prompt}],
                temperature=0.7,
            )
            st.session_state.summary = summary_response.choices[0].message.content

    # Display Results
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

    # Idiotic Idiom Badge
    idiotic_idiom.render_idiom_badge(st)

# =====================================================
# NEWSSTAND TAB
# =====================================================
with tab_newsstand:
    st.header("🗞️ Ideology Newsstand")
    st.markdown(
        "_Explore the origins, ideas, and influence of political ideologies throughout history — "
        "and discover how they shape modern thought, leadership, and media._"
    )

    data_path = Path("assets/ideology_newsstand.json")
    if not data_path.exists():
        st.warning("⚠️ No Newsstand data file found at assets/ideology_newsstand.json")
    else:
        with open(data_path, "r", encoding="utf-8") as f:
            ideologies = json.load(f)

        for name, info in ideologies.items():
            with st.container(border=True):
                st.markdown(f"### {name}")

                st.markdown(f"**1) Basic Tenets:** {info.get('tenets', '—')}")
                st.markdown(f"**2) Brief History:** {info.get('history', '—')}")
                st.markdown(f"**3) Popularity (US & World):** {info.get('popularity', '—')}")
                st.markdown(f"**4) Leading Current Politicians & Media Figures:** {info.get('current_figures', '—')}")

                st.markdown("**5) Significant Philosophers & Major Works:**")
                philosophers = info.get("philosophers", [])
                if philosophers:
                    for ph in philosophers:
                        st.markdown(f"- **{ph.get('name')}** — *{ph.get('works')}* ({ph.get('notes')})")
                else:
                    st.markdown("—")

                media_list = info.get("media_outlets", [])
                if media_list:
                    st.markdown("**6) Current Media Outlets:** " + ", ".join(media_list))
                else:
                    st.markdown("**6) Current Media Outlets:** —")

# =====================================================
# FOOTER
# =====================================================
st.markdown("---")
st.caption("© 2025 Wisdom & Waffles — A diner for civil discourse and shared understanding.")
