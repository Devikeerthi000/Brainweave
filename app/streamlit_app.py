import sys
import os

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import streamlit.components.v1 as components
import json

from core.pdf_parser import extract_text_from_pdf
from core.text_cleaner import clean_text
from core.section_splitter import split_into_sections
from core.summarizer import summarize_chunks
from core.mindmap_generator import mindmap_to_markdown, mindmap_to_text_tree, count_nodes, get_depth


# ----------------- STREAMLIT CONFIG -----------------

st.set_page_config(page_title="MindCity", layout="wide", page_icon="🧠")

st.title("🧠 MindCity")
st.caption("Transform documents into insightful mind maps")

# Sidebar for settings
with st.sidebar:
    st.header("Settings")
    chunk_size = st.slider("Chunk size", 1000, 5000, 2500, 500)
    show_stats = st.checkbox("Show document stats", value=True)
    export_format = st.selectbox("Export format", ["JSON", "Markdown", "Text Tree"])

uploaded_file = st.file_uploader("Upload PDF", type="pdf")


# ----------------- INTERACTIVE MINDMAP DISPLAY -----------------

def render_mindmap_html(mindmap):
    """Generate a true hierarchical mind map with branches radiating from center."""
    
    title = mindmap.get("title", "Mind Map")
    children = mindmap.get("children", [])
    
    branch_colors = ["#3498db", "#27ae60", "#e74c3c", "#9b59b6", "#f39c12", "#1abc9c"]
    
    # Split branches into left and right sides
    mid = (len(children) + 1) // 2
    left_branches = children[:mid]
    right_branches = children[mid:]
    
    def build_branch_html(branch, color, side):
        branch_title = branch.get("title", "")
        sub_children = branch.get("children", [])
        
        sub_items = ""
        for sub in sub_children:
            sub_title = sub.get("title", "")
            leaves = sub.get("children", [])
            
            leaf_items = ""
            for leaf in leaves:
                leaf_title = leaf.get("title", "")
                leaf_items += f'<div class="leaf">{leaf_title}</div>'
            
            leaf_container = f'<div class="leaves">{leaf_items}</div>' if leaf_items else ''
            sub_items += f'''
                <div class="sub-branch">
                    <div class="sub-node" style="background:{color};">{sub_title}</div>
                    {leaf_container}
                </div>
            '''
        
        return f'''
            <div class="branch {side}">
                <div class="branch-content">
                    <div class="main-node" style="background:{color};">{branch_title}</div>
                    <div class="sub-branches">
                        {sub_items}
                    </div>
                </div>
                <div class="connector" style="background:{color};"></div>
            </div>
        '''
    
    left_html = ""
    for i, branch in enumerate(left_branches):
        color = branch_colors[i % len(branch_colors)]
        left_html += build_branch_html(branch, color, "left")
    
    right_html = ""
    for i, branch in enumerate(right_branches):
        color = branch_colors[(i + mid) % len(branch_colors)]
        right_html += build_branch_html(branch, color, "right")
    
    # Calculate height
    max_subs = max([len(b.get("children", [])) for b in children] or [1])
    estimated_height = max(500, len(children) * 100 + max_subs * 50)
    
    html = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{
                font-family: 'Segoe UI', sans-serif;
                background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
                padding: 30px 10px;
                min-height: 100vh;
            }}
            
            .mindmap {{
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 0;
                max-width: 1400px;
                margin: 0 auto;
            }}
            
            .center-node {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 25px 35px;
                border-radius: 50px;
                font-size: 18px;
                font-weight: bold;
                text-align: center;
                min-width: 200px;
                max-width: 280px;
                box-shadow: 0 10px 40px rgba(102, 126, 234, 0.5);
                z-index: 10;
                position: relative;
            }}
            
            .left-side, .right-side {{
                display: flex;
                flex-direction: column;
                gap: 15px;
                flex: 1;
            }}
            
            .branch {{
                display: flex;
                align-items: center;
            }}
            
            .branch.left {{
                flex-direction: row-reverse;
                text-align: right;
            }}
            
            .branch.right {{
                flex-direction: row;
                text-align: left;
            }}
            
            .connector {{
                width: 40px;
                height: 3px;
                flex-shrink: 0;
            }}
            
            .branch-content {{
                background: white;
                border-radius: 15px;
                padding: 12px 15px;
                box-shadow: 0 3px 15px rgba(0,0,0,0.08);
                max-width: 350px;
            }}
            
            .main-node {{
                color: white;
                padding: 10px 18px;
                border-radius: 20px;
                font-size: 14px;
                font-weight: 600;
                display: inline-block;
                margin-bottom: 8px;
            }}
            
            .sub-branches {{
                padding: 5px 0;
            }}
            
            .sub-branch {{
                margin: 8px 0;
                padding-left: 15px;
                border-left: 2px solid #e0e0e0;
            }}
            
            .branch.left .sub-branch {{
                padding-left: 0;
                padding-right: 15px;
                border-left: none;
                border-right: 2px solid #e0e0e0;
            }}
            
            .sub-node {{
                color: white;
                padding: 6px 12px;
                border-radius: 15px;
                font-size: 12px;
                display: inline-block;
                opacity: 0.9;
            }}
            
            .leaves {{
                margin-top: 5px;
                padding-left: 10px;
            }}
            
            .branch.left .leaves {{
                padding-left: 0;
                padding-right: 10px;
            }}
            
            .leaf {{
                background: #f5f5f5;
                color: #666;
                padding: 4px 10px;
                border-radius: 10px;
                font-size: 11px;
                margin: 3px 0;
                display: inline-block;
            }}
            
            /* Vertical lines from center */
            .center-node::before,
            .center-node::after {{
                content: '';
                position: absolute;
                top: 50%;
                width: 20px;
                height: 3px;
                background: linear-gradient(90deg, #667eea, #764ba2);
            }}
            .center-node::before {{ left: -20px; }}
            .center-node::after {{ right: -20px; }}
        </style>
    </head>
    <body>
        <div class="mindmap">
            <div class="left-side">
                {left_html}
            </div>
            <div class="center-node">{title}</div>
            <div class="right-side">
                {right_html}
            </div>
        </div>
    </body>
    </html>
    '''
    
    return html, estimated_height


def render_mindmap_columns(mindmap):
    """Render mindmap in a column layout for better readability."""
    
    st.markdown(f"### 🎯 {mindmap.get('title', 'Mind Map')}")
    st.markdown("---")
    
    children = mindmap.get("children", [])
    
    if not children:
        st.warning("No branches generated")
        return
    
    # Create columns based on number of main branches
    num_cols = min(len(children), 3)
    cols = st.columns(num_cols)
    
    for i, branch in enumerate(children):
        with cols[i % num_cols]:
            branch_title = branch.get("title", "Branch")
            st.markdown(f"**🔹 {branch_title}**")
            
            sub_children = branch.get("children", [])
            for sub in sub_children:
                sub_title = sub.get("title", "")
                st.markdown(f"&nbsp;&nbsp;&nbsp;• {sub_title}")
                
                # Level 3
                for leaf in sub.get("children", []):
                    leaf_title = leaf.get("title", "")
                    st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;◦ {leaf_title}")
            
            st.markdown("")  # Spacing


# ----------------- MAIN PIPELINE -----------------

if uploaded_file:
    # Progress tracking
    progress = st.progress(0)
    status = st.empty()
    
    # Step 1: Extract
    status.text("📄 Extracting text from PDF...")
    progress.progress(20)
    raw_text = extract_text_from_pdf(uploaded_file)
    
    # Step 2: Clean
    status.text("🧹 Cleaning text...")
    progress.progress(40)
    cleaned = clean_text(raw_text)
    
    # Step 3: Split
    status.text("✂️ Splitting into sections...")
    progress.progress(60)
    sections = split_into_sections(cleaned, chunk_size=chunk_size)
    
    # Step 4: Generate mindmap
    status.text("🧠 Generating mind map with AI...")
    progress.progress(80)
    mindmap = summarize_chunks(sections)
    
    progress.progress(100)
    status.text("✅ Complete!")
    
    # Show stats
    if show_stats:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Characters", f"{len(raw_text):,}")
        col2.metric("Sections", len(sections))
        col3.metric("Nodes", count_nodes(mindmap))
        col4.metric("Depth", get_depth(mindmap))
    
    st.markdown("---")
    
    # Display tabs
    tab1, tab2, tab3 = st.tabs(["🗺️ Visual Map", "📝 Text View", "💾 Export"])
    
    with tab1:
        html_content, height = render_mindmap_html(mindmap)
        components.html(html_content, height=height, scrolling=True)
    
    with tab2:
        st.subheader("Tree View")
        st.code(mindmap_to_text_tree(mindmap), language=None)
        
        st.subheader("Markdown View")
        st.markdown(mindmap_to_markdown(mindmap))
    
    with tab3:
        st.subheader("Download Mind Map")
        
        # JSON export
        json_str = json.dumps(mindmap, indent=2)
        st.download_button(
            "📥 Download JSON",
            json_str,
            file_name="mindmap.json",
            mime="application/json"
        )
        
        # Markdown export
        md_str = mindmap_to_markdown(mindmap)
        st.download_button(
            "📥 Download Markdown",
            md_str,
            file_name="mindmap.md",
            mime="text/markdown"
        )
        
        # Text tree export
        tree_str = mindmap_to_text_tree(mindmap)
        st.download_button(
            "📥 Download Text Tree",
            tree_str,
            file_name="mindmap.txt",
            mime="text/plain"
        )
        
        st.subheader("Raw JSON")
        st.json(mindmap)

else:
    # Welcome message
    st.info("👆 Upload a PDF document to generate an insightful mind map")
    
    st.markdown("""
    ### How it works:
    1. **Upload** - Drop your PDF document
    2. **Process** - AI extracts key concepts and themes
    3. **Visualize** - See your document as an interactive mind map
    4. **Export** - Download as JSON, Markdown, or text
    
    ### Features:
    - 🎯 **Insightful** - Captures meaning, not just headings
    - 🌳 **Hierarchical** - 3-4 levels of depth
    - 📊 **Balanced** - Max 6 branches, 4-5 items each
    - 💾 **Exportable** - Multiple format options
    """)