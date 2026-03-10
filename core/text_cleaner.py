import re

def clean_text(text):
    """
    Clean text while preserving document structure (paragraphs, headings).
    """
    # Remove page numbers and headers/footers patterns
    text = re.sub(r'\n\s*\d+\s*\n', '\n', text)
    
    # Normalize multiple blank lines to double newline (preserve paragraph breaks)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Replace multiple spaces (but NOT newlines) with single space
    text = re.sub(r'[^\S\n]+', ' ', text)
    
    # Remove leading/trailing whitespace from each line
    lines = [line.strip() for line in text.split('\n')]
    text = '\n'.join(lines)
    
    # Remove empty lines at start/end
    text = text.strip()
    
    return text


def extract_headings(text):
    """
    Extract potential headings/section titles from text.
    """
    headings = []
    lines = text.split('\n')
    
    for i, line in enumerate(lines):
        line = line.strip()
        # Likely heading: short line, possibly numbered, followed by content
        if len(line) > 3 and len(line) < 100:
            # Check patterns: numbered sections, ALL CAPS, Title Case short lines
            if re.match(r'^(\d+\.|\d+\)|[A-Z]{2,}|Chapter|Section)', line):
                headings.append(line)
            elif line.istitle() and len(line.split()) <= 6:
                headings.append(line)
    
    return headings