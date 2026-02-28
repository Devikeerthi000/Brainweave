def extract_concepts(summary_text):
    lines = summary_text.split("\n")
    concepts = []

    for line in lines:
        line = line.strip("- ").strip()
        if len(line) > 4:
            concepts.append(line)

    return concepts