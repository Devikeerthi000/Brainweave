# 🧠 BrainWeave

**Transform PDF documents into insightful, hierarchical mind maps using AI**

🔗 **Live Demo:** [brainweave-wubg5q3hwszxnm53gdpzdx.streamlit.app](https://brainweave-wubg5q3hwszxnm53gdpzdx.streamlit.app/)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📄 **PDF Processing** | Extract and clean text while preserving document structure |
| 🧠 **AI-Powered Analysis** | Uses Groq LLM (Llama 3.1) to identify key concepts and themes |
| 🗺️ **Hierarchical Visualization** | True mind map layout with central node and radiating branches |
| 💾 **Multiple Export Formats** | Download as JSON, Markdown, or Text Tree |
| ⚡ **Fast Processing** | Processes documents in seconds |

---

## 🖼️ How It Works

```
PDF Upload → Text Extraction → Smart Chunking → AI Analysis → Mind Map Generation
```

1. **Extract** - PDF text extracted using PyMuPDF
2. **Clean** - Preserves paragraph structure while removing noise
3. **Split** - Intelligent chunking at sentence/paragraph boundaries  
4. **Analyze** - Samples from entire document sent to LLM
5. **Generate** - AI creates hierarchical mind map
6. **Visualize** - Interactive display with branches radiating from center

---

## 🗂️ Project Structure

```
brainweave/
├── app/
│   └── streamlit_app.py      # Streamlit web application
├── core/
│   ├── pdf_parser.py         # PDF text extraction
│   ├── text_cleaner.py       # Text preprocessing
│   ├── section_splitter.py   # Smart document chunking
│   ├── summarizer.py         # LLM-powered mind map generation
│   └── mindmap_generator.py  # Export utilities
├── models/
│   └── schemas.py            # Data models
├── utils/
│   └── helpers.py            # Helper functions
└── requirements.txt
```

---

## 🧩 Mind Map Output Structure

```json
{
  "title": "Core Topic",
  "children": [
    {
      "title": "Major Theme",
      "children": [
        {"title": "Key Insight", "children": []},
        {"title": "Key Insight", "children": []}
      ]
    }
  ]
}
```

**Constraints:**
- Maximum **6** main branches
- Maximum **4-5** items per branch
- Maximum depth: **3-4** levels

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit
- **AI/LLM:** Groq (Llama 3.1)
- **PDF Processing:** PyMuPDF
- **Data Validation:** Pydantic

---

## 👤 Author

**Devi Keerthi**

- GitHub: [@Devikeerthi000](https://github.com/Devikeerthi000)

## License

MIT
