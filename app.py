import json
import streamlit as st
import pandas as pd

from utils.extractor import extract_text, clean_text
from utils.parser import parse_resume

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Resume Parser",
    page_icon="📄",
    layout="wide",
)

st.title("📄 Resume Parser")
st.markdown("Upload a resume (PDF or DOCX) to extract structured information.")

# ── File upload ───────────────────────────────────────────────────────────────
uploaded_file = st.file_uploader(
    "Choose a resume file", type=["pdf", "docx", "txt"]
)

if uploaded_file:
    with st.spinner("Extracting and parsing resume..."):
        raw_text = extract_text(uploaded_file, uploaded_file.name)
        clean = clean_text(raw_text)
        result = parse_resume(clean)

    st.success("✅ Resume parsed successfully!")

    # ── Layout: two columns ───────────────────────────────────────────────────
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("👤 Personal Info")
        info_data = {
            "Field": ["Name", "Email", "Phone", "LinkedIn", "GitHub"],
            "Value": [
                result["name"]    or "—",
                result["email"]   or "—",
                result["phone"]   or "—",
                result["linkedin"] or "—",
                result["github"]  or "—",
            ],
        }
        st.table(pd.DataFrame(info_data))

        st.subheader("🎓 Education")
        if result["education"]:
            for line in result["education"]:
                st.markdown(f"- {line}")
        else:
            st.write("No education section found.")

        st.subheader("📜 Certifications")
        if result["certifications"]:
            st.text(result["certifications"][:500])
        else:
            st.write("None found.")

    with col2:
        st.subheader("🛠️ Skills Detected")
        if result["skills"]:
            # Display as colored pills using columns
            skills = result["skills"]
            cols = st.columns(3)
            for i, skill in enumerate(skills):
                cols[i % 3].markdown(
                    f"<span style='background:#1f77b4;color:white;"
                    f"padding:3px 10px;border-radius:12px;"
                    f"font-size:13px;display:inline-block;margin:3px'>"
                    f"{skill}</span>",
                    unsafe_allow_html=True,
                )
        else:
            st.write("No skills detected.")

        st.subheader("💼 Experience")
        if result["experience"]:
            for line in result["experience"]:
                st.markdown(f"- {line}")
        else:
            st.write("No experience section found.")

        st.subheader("🚀 Projects")
        if result["projects"]:
            st.text(result["projects"][:600])
        else:
            st.write("None found.")

    # ── Raw text & JSON export ────────────────────────────────────────────────
    st.divider()
    with st.expander("🔍 View Raw Extracted Text"):
        st.text(clean[:3000])

    with st.expander("📦 View JSON Output"):
        st.json(result)

    st.download_button(
        label="⬇️ Download JSON",
        data=json.dumps(result, indent=2),
        file_name="parsed_resume.json",
        mime="application/json",
    )
