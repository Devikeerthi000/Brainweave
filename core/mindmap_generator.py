def build_mindmap_json(hierarchy):

    root = {
        "title": "Main Topic",
        "children": []
    }

    for parent, children in hierarchy.items():
        node = {
            "title": parent,
            "children": []
        }

        for child in children:
            node["children"].append({
                "title": child,
                "children": []
            })

        root["children"].append(node)

    return root