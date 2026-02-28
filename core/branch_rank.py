def rank_concepts(concepts):
    scored = []

    for concept in concepts:
        score = len(concept.split())
        scored.append((concept, score))

    scored.sort(key=lambda x: x[1], reverse=True)
    return [c[0] for c in scored]