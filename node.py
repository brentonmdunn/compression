"""Class file for Node object."""

from typing import List

class Node:
    """Represents each node in Huffman Tree."""

    def __init__(self, identifier: str, freq: int, leaves: List[str]) -> None:
        self.identifier: str = identifier
        self.freq: int = freq
        self.leaves: List[str] = leaves
        self.lchild: Node = None
        self.rchild: Node = None
        self.parent: Node = None


    def __lt__(self, other):
        return self.freq < other.freq
    