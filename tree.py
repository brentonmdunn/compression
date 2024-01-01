"""Class file for Tree object."""

from queue import PriorityQueue
from typing import Dict, List
from node import Node
from read import Read
from write import Write

class Tree:
    """Creates Huffman tree."""

    def __init__(self):
        self.root: Node = None


    def create_tree(self, freq_dict: Dict[str, int]):
        """Creates Huffman tree."""

        pq: Node = PriorityQueue()

        # Adds non-zero nodes to pq
        for key, value in freq_dict.items():
            if value > 0:
                pq.put(Node(key, value, [key]))

        while pq.qsize() > 1:

            node1: Node = pq.get()
            node2: Node = pq.get()

            leaves: List[str] = (node1.leaves + node2.leaves)
            combined: Node = Node(node1.identifier, node1.freq + node2.freq, leaves)
            node1.parent = combined
            node2.parent = combined
            combined.lchild = node1
            combined.rchild = node2

            pq.put(combined)

        self.root = pq.get()


    def encode(self, identifier: str, writer: Write):
        """Encodes node."""

        curr: Node = self.root
        encoding: str = ""

        while len(curr.leaves) > 1:     # If curr.leaves == 1, it is leaf node
            if curr.rchild is None or identifier in curr.lchild.leaves:
                curr = curr.lchild
                encoding += "0"

            elif curr.lchild is None or identifier in curr.rchild.leaves:
                curr = curr.rchild
                encoding += "1"

        writer.write_nonstd(encoding)


    def decode(self, reader: Read):
        """Decodes the compressed file."""

        curr_node: Node = self.root
        while len(curr_node.leaves) != 1:   # If curr.leaves == 1, it is leaf node
            curr_bit = reader.read_bit()
            if curr_bit is None:
                return None

            if curr_bit == "0":
                curr_node = curr_node.lchild
            else:
                curr_node = curr_node.rchild

        return curr_node.identifier
