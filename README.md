# 🧠 MindCity

**Transform documents into insightful mind maps using AI**

MindCity analyzes PDF documents and extracts key concepts, themes, and insights, organizing them into a hierarchical mind map structure.

## Features

- 📄 **PDF Processing** - Extract and clean text while preserving structure
- 🧠 **AI-Powered Analysis** - Uses Groq LLM to identify meaningful concepts
- 🗺️ **Interactive Visualization** - Multiple view formats (visual, tree, markdown)
- 💾 **Export Options** - Download as JSON, Markdown, or text
- ⚡ **Fast** - Processes documents in seconds

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/mindcity.git
cd mindcity

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Get your API key from [Groq Console](https://console.groq.com/).

## Usage

```bash
streamlit run app/streamlit_app.py
```

Then open http://localhost:8501 in your browser.

## Project Structure

```
mindcity/
├── app/
│   └── streamlit_app.py    # Main Streamlit application
├── core/
│   ├── pdf_parser.py       # PDF text extraction
│   ├── text_cleaner.py     # Text cleaning & structure preservation
│   ├── section_splitter.py # Smart document chunking
│   ├── summarizer.py       # LLM-powered mind map generation
│   └── mindmap_generator.py # Export utilities
├── models/
│   └── schemas.py          # Pydantic data models
├── utils/
│   └── helpers.py          # Utility functions
├── requirements.txt
└── README.md
```

## How It Works

1. **Extract** - PDF text is extracted using PyMuPDF
2. **Clean** - Text is cleaned while preserving paragraph structure
3. **Split** - Document is split at sentence/paragraph boundaries
4. **Analyze** - Balanced samples from all parts are sent to LLM
5. **Generate** - AI creates hierarchical mind map JSON
6. **Visualize** - Interactive display with multiple view options

## Mind Map Structure

Output follows this JSON structure:

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
- Maximum 6 main branches
- Maximum 4-5 items per branch
- Maximum depth: 3-4 levels

## License

MIT
