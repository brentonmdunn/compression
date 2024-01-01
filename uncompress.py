"""Uncompresses file."""

import sys
from typing import Dict
from read import Read
from tree import Tree
from write import Write

def main() -> None:
    """Main file for uncompress.py."""

    if len(sys.argv) != 3:
        raise ValueError("Invalid number of arguments. Expected exactly two arguments.")

    freq_dict: Dict[str, int] = {format(i, '08b'): 0 for i in range(256)}

    reader = Read(sys.argv[1])
    writer = Write(sys.argv[2])
    file_size_zero: bool = reader.file_size == 0

    # Read header
    if not file_size_zero:
        for i in range(256):
            binary_str = format(i, '08b')
            byte1 = reader.read_byte()
            byte2 = reader.read_byte()
            byte3 = reader.read_byte()

            combined = byte1 + byte2 + byte3

            freq_dict[binary_str] = int(combined, 2)

    tree = Tree()

    if not file_size_zero:
        tree.create_tree(freq_dict)

    total_size = 0
    for value in freq_dict.values():
        total_size += value

    # Decodes bytes.
    for _ in range(total_size):
        to_write = tree.decode(reader)
        if to_write is None:
            break
        writer.write_nonstd(to_write)


if __name__ == '__main__':
    main()
