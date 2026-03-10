import os
import json
from groq import Groq
from dotenv import load_dotenv
from core.section_splitter import get_document_overview

load_dotenv()

# Support both .env (local) and Streamlit secrets (cloud)
def get_api_key():
    # Try Streamlit secrets first (for cloud deployment)
    try:
        import streamlit as st
        if hasattr(st, 'secrets') and 'GROQ_API_KEY' in st.secrets:
            return st.secrets['GROQ_API_KEY']
    except:
        pass
    # Fall back to environment variable
    return os.getenv("GROQ_API_KEY")

client = Groq(api_key=get_api_key())


def summarize_chunks(chunks):
    """
    Generate an insightful mindmap from document chunks.
    Uses document overview to capture the full document, not just beginning.
    """
    # Get balanced overview from ALL chunks (not just first 3)
    full_text = get_document_overview(chunks, max_chars=6000)
    
    prompt = f"""You are a knowledge architect. Analyze this document and create an INSIGHTFUL mind map.

ANALYSIS STEPS:
1. Identify the CORE TOPIC - what is this document fundamentally about?
2. Extract KEY THEMES - major categories of ideas (not surface-level headings)
3. Find MEANINGFUL INSIGHTS - what are the important takeaways?
4. Discover RELATIONSHIPS - how do concepts connect?

MINDMAP RULES:
- Root: The central thesis/topic (not generic like "Document Summary")
- Level 1: 4-6 major themes/pillars (conceptual categories)
- Level 2: Key insights under each theme (2-4 per branch)
- Level 3: Supporting details only if essential (1-3 max)

QUALITY REQUIREMENTS:
- Use NOUN PHRASES or short concept labels (2-5 words)
- Make it INSIGHTFUL - someone should understand the document's essence
- AVOID generic labels like "Introduction", "Details", "Conclusion"
- AVOID copying section headings verbatim - synthesize meaning
- GROUP related ideas - don't just list everything
- PRIORITIZE importance over completeness

OUTPUT FORMAT (strict JSON):
{{
  "title": "Core Topic Name",
  "children": [
    {{
      "title": "Major Theme",
      "children": [
        {{"title": "Key Insight", "children": []}},
        {{"title": "Key Insight", "children": []}}
      ]
    }}
  ]
}}

DOCUMENT CONTENT:
{full_text}

Return ONLY valid JSON. No explanations."""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system", 
                    "content": "You are an expert at distilling documents into insightful, hierarchical knowledge structures. Output only valid JSON."
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=2000
        )

        raw_output = response.choices[0].message.content

        # Extract JSON safely
        start = raw_output.find("{")
        end = raw_output.rfind("}") + 1
        
        if start == -1 or end == 0:
            return _fallback_mindmap("Could not parse response")
            
        json_string = raw_output[start:end]
        mindmap = json.loads(json_string)
        
        # Validate structure
        if "title" not in mindmap:
            mindmap["title"] = "Document Overview"
        if "children" not in mindmap:
            mindmap["children"] = []
            
        return mindmap
        
    except json.JSONDecodeError as e:
        return _fallback_mindmap(f"JSON parse error: {str(e)}")
    except Exception as e:
        return _fallback_mindmap(f"Error: {str(e)}")


def _fallback_mindmap(error_msg):
    """Return a fallback mindmap structure when processing fails."""
    return {
        "title": "Processing Error",
        "children": [
            {
                "title": error_msg,
                "children": []
            }
        ]
    }