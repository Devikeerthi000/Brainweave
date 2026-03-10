import json

def build_mindmap_json(hierarchy):
    """
    Convert a hierarchy dict to mindmap JSON format.
    Used when building mindmaps from extracted concepts (non-LLM path).
    """
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


def validate_mindmap(mindmap):
    """
    Validate and fix common mindmap structure issues.
    """
    if not isinstance(mindmap, dict):
        return {"title": "Invalid", "children": []}
    
    if "title" not in mindmap:
        mindmap["title"] = "Untitled"
    
    if "children" not in mindmap:
        mindmap["children"] = []
    
    # Recursively validate children
    validated_children = []
    for child in mindmap.get("children", []):
        if isinstance(child, dict):
            validated_children.append(validate_mindmap(child))
        elif isinstance(child, str):
            validated_children.append({"title": child, "children": []})
    
    mindmap["children"] = validated_children
    return mindmap


def mindmap_to_markdown(mindmap, level=0):
    """
    Convert mindmap JSON to markdown outline format.
    """
    indent = "  " * level
    prefix = "#" * (level + 1) if level < 3 else "-"
    
    if level < 3:
        md = f"{prefix} {mindmap.get('title', 'Untitled')}\n\n"
    else:
        md = f"{indent}- {mindmap.get('title', 'Untitled')}\n"
    
    for child in mindmap.get("children", []):
        md += mindmap_to_markdown(child, level + 1)
    
    return md


def mindmap_to_text_tree(mindmap, prefix="", is_last=True):
    """
    Convert mindmap JSON to ASCII tree format.
    """
    connector = "└── " if is_last else "├── "
    output = prefix + connector + mindmap.get("title", "") + "\n"
    
    children = mindmap.get("children", [])
    child_prefix = prefix + ("    " if is_last else "│   ")
    
    for i, child in enumerate(children):
        is_child_last = (i == len(children) - 1)
        output += mindmap_to_text_tree(child, child_prefix, is_child_last)
    
    return output


def count_nodes(mindmap):
    """Count total nodes in mindmap."""
    count = 1  # Current node
    for child in mindmap.get("children", []):
        count += count_nodes(child)
    return count


def get_depth(mindmap, current_depth=0):
    """Get maximum depth of mindmap."""
    if not mindmap.get("children"):
        return current_depth
    
    max_child_depth = current_depth
    for child in mindmap.get("children", []):
        child_depth = get_depth(child, current_depth + 1)
        max_child_depth = max(max_child_depth, child_depth)
    
    return max_child_depth