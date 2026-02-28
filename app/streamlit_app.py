import sys
import os

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

from core.pdf_parser import extract_text_from_pdf
from core.text_cleaner import clean_text
from core.section_splitter import split_into_sections
from core.summarizer import summarize_chunks


# ----------------- STREAMLIT CONFIG -----------------

st.set_page_config(page_title="MindForge", layout="wide")
st.title("🧠 MindForge - PDF to Mindmap")

uploaded_file = st.file_uploader("Upload PDF", type="pdf")


# ----------------- MINDMAP DRAW FUNCTION -----------------

def draw_mindmap(mindmap):
    G = nx.DiGraph()

    def add_edges(node, parent=None):
        if parent:
            G.add_edge(parent, node["title"])
        for child in node.get("children", []):
            add_edges(child, node["title"])

    add_edges(mindmap)

    plt.figure(figsize=(14, 10))
    pos = nx.spring_layout(G, seed=42)

    nx.draw(
        G,
        pos,
        with_labels=True,
        node_size=3000,
        node_color="lightblue",
        font_size=8,
        font_weight="bold"
    )

    st.pyplot(plt)


# ----------------- MAIN PIPELINE -----------------

if uploaded_file:
    with st.spinner("Extracting text..."):
        raw_text = extract_text_from_pdf(uploaded_file)

    cleaned = clean_text(raw_text)
    sections = split_into_sections(cleaned)

    with st.spinner("Generating Mindmap Structure..."):
        mindmap = summarize_chunks(sections)

    st.subheader("🧠 Visual Mindmap")
    draw_mindmap(mindmap)