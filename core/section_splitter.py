def split_into_sections(text, chunk_size=3000):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]