import streamlit as st
from apis.semantic_scholar import fetch_papers_from_sematic_scholar
from apis.pubmed import fetch_papers_from_pubmed
from apis.arxiv_api import get_arxiv_papers
from apis.core_api import fetch_papers_from_core
from models.summariser import load_summarizer
from models.utils import chunk_text
import traceback

@st.cache_data
def fetch_papers(source, query):
    """
    Fetches papers from the selected source based on the query.
    Caches the results to avoid repeated API calls.
    """
    try:
        if source == "Semantic Scholar":
            return fetch_papers_from_sematic_scholar(query)
        elif source == "PubMed":
            return fetch_papers_from_pubmed(query)
        elif source == "Arxiv":
            return get_arxiv_papers(query)
        elif source == "CORE":
            return fetch_papers_from_core(query)
        else:
            return []
    except Exception as e:
        st.error(f"Error fetching papers from {source}: {e}")
        st.error(traceback.format_exc())
        return []

@st.cache_resource
def get_summarizer():
    """
    Loads and caches the summarization model.
    """
    return load_summarizer()

def summarize_text(text, max_length=150):
    """
    Summarizes the given text using the pre-loaded summarizer model.
    """
    summarizer = get_summarizer()
    chunks = chunk_text(text)
    summary = ""
    for i, chunk in enumerate(chunks):
        result = summarizer(chunk, max_length=max_length, min_length=30, do_sample=False)
        summary += result[0]["summary_text"] + "\n\n"
    return summary
