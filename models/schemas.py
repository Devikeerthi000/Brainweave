from pydantic import BaseModel
from typing import List

class MindmapNode(BaseModel):
    title: str
    children: List["MindmapNode"] = []