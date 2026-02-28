import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def summarize_chunks(chunks):
    full_text = "\n".join(chunks[:3])

    prompt = f"""
You are an academic abstraction engine.

STEP 1:
Summarize the content into high-level concepts only.
Remove examples.
Remove repetitive details.
Keep only major themes.

STEP 2:
Convert that summary into a clean mindmap JSON.

STRICT RULES:
- Maximum 6 main branches.
- Each branch max 4 children.
- Maximum depth: 3 levels.
- Use short phrases (2-4 words).
- Do NOT include individual examples like specific algorithms.
- Group similar ideas together.
- Output ONLY valid JSON.

Format:
{{
  "title": "Main Topic",
  "children": [
    {{
      "title": "Major Concept",
      "children": [
        {{
          "title": "Key Idea",
          "children": []
        }}
      ]
    }}
  ]
}}

Content:
{full_text}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You strictly output valid JSON tree structures."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    raw_output = response.choices[0].message.content

    # Extract JSON safely
    start = raw_output.find("{")
    end = raw_output.rfind("}") + 1
    json_string = raw_output[start:end]

    return json.loads(json_string)