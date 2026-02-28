def build_hierarchy(concepts):
    hierarchy = {}
    current_main = None

    for concept in concepts:
        concept = concept.strip()

        # Treat capitalized standalone lines as main sections
        if concept.istitle() or concept.isupper():
            current_main = concept
            hierarchy[current_main] = []
        elif current_main:
            hierarchy[current_main].append(concept)

    return hierarchy