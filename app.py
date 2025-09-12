# app.py

import streamlit as st
from logic.core import fetch_papers, summarize_text
from models.utils import save_summary_to_pdf
import os

def get_paper_display(paper):
    """Formats the paper details for display."""
    display = f"**{paper['title']}**"
    if paper.get('authors'):
        display += f" by {', '.join(paper['authors'])}"
    if paper.get('year'):
        display += f" ({paper['year']})"
    return display

# App title
st.set_page_config(page_title="Research Agent", layout="wide")
st.title("📚 Research Agent – Summarize Academic Papers")

# Initialize session state
if 'papers' not in st.session_state:
    st.session_state.papers = []

# Source selection
source = st.selectbox("Select Source", ["Semantic Scholar", "PubMed", "Arxiv", "CORE"])

query = st.text_input("Enter your search query")

max_length = st.slider("Select max summary length", 50, 500, 150, 10)

# Search trigger
if st.button("Search"):
    st.info("Fetching papers...")
    st.session_state.papers = fetch_papers(source, query)
    if not st.session_state.papers:
        st.warning("No papers found.")

if st.session_state.papers:
    paper_options = {get_paper_display(p): p for p in st.session_state.papers}
    selected_display = st.selectbox("Select a paper to summarize", list(paper_options.keys()))
    selected_paper = paper_options[selected_display]

    if st.button("Generate Summary"):
        st.info("Summarizing...")

        summary = summarize_text(selected_paper["content"], max_length=max_length)

        st.success("Summary generated!")

        # Display summary
        st.subheader("🔍 Summary")
        st.write(summary)

        # Ensure the data/summaries directory exists
        os.makedirs("data/summaries", exist_ok=True)

        # Save summary files
        save_summary_to_pdf(summary, selected_paper['title'])

        # Download buttons
        pdf_path = f"data/summaries/{selected_paper['title'].replace(' ', '_')[:50]}.pdf"
        txt_path = f"data/summaries/{selected_paper['title'].replace(' ', '_')[:50]}.txt"

        with open(pdf_path, "rb") as f:
            st.download_button("Download PDF", f, file_name="summary.pdf")

        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(summary)

        with open(txt_path, "rb") as f:
            st.download_button("Download Text", f, file_name="summary.txt")
