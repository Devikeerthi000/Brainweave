# 🧠 Brainweave — From PDFs to Structured Mindmaps

Brainweave is an AI-powered knowledge abstraction system that converts academic PDFs into structured visual mindmaps.

Instead of simply extracting text, Brainweave performs intelligent summarization and hierarchical structuring to transform dense academic content into cognitively organized visual maps.

---

## 🚀 Features

- 📄 Upload and extract text from PDFs  
- 🧠 High-level abstraction using Groq LLM  
- 🌳 Controlled hierarchical JSON tree generation  
- 🎨 Radial mindmap visualization  
- 🧩 Modular and extensible architecture  
- ⚡ Lightweight Streamlit interface  

---
---

## 🧠 How It Works

### 1️⃣ PDF Extraction  
Text is extracted from uploaded documents using PyMuPDF.

### 2️⃣ Intelligent Abstraction  
The Groq LLM:
- Removes repetitive information  
- Eliminates unnecessary examples  
- Extracts only major conceptual themes  
- Limits depth and branch count  

### 3️⃣ Structured Tree Output  

The model returns a strict JSON structure:

{
  "title": "Main Topic",
  "children": [
    {
      "title": "Major Concept",
      "children": [
        {
          "title": "Key Idea",
          "children": []
        }
      ]
    }
  ]
}

### 4️⃣ Mindmap Rendering  
NetworkX generates a radial tree visualization for clear conceptual mapping.

---
---

## 🛠️ Tech Stack

- Python 3.12  
- Streamlit  
- Groq API  
- NetworkX  
- Matplotlib  
- PyMuPDF  
- python-dotenv  

---

## 🎯 Design Philosophy

Brainweave is built around:

- Knowledge abstraction over raw extraction  
- Controlled hierarchical structuring  
- Depth-limited conceptual trees  
- Visualization-first architecture  
- Modular backend design  

---

## 🔮 Future Improvements

- Interactive zoomable mindmap  
- Expand / collapse nodes  
- Export as PNG / PDF  
- Multi-document synthesis  
- Embedding-based clustering  
- Branch ranking algorithm  
- UI customization controls  

---

## 👩‍💻 Author

Devi Keerthi Adapa  
AI Backend Engineer  

---

## ⭐ Support

If you found this project useful, consider starring the repository.
