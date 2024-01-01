"""Compresses file."""

import sys
from typing import Dict
from read import Read
from tree import Tree
from write import Write

def main() -> None:
    """Main method for compress.py."""

    if len(sys.argv) != 3:
        raise ValueError("Invalid number of arguments. Expected exactly two arguments.")

    freq_dict: Dict[str, int] = {format(i, '08b'): 0 for i in range(256)}

    reader = Read(sys.argv[1])
    writer = Write(sys.argv[2])

    file_size_zero: bool = reader.file_size == 0

    # Gets frequencies of each byte
    next_byte = reader.read_byte()
    while next_byte is not None:
        freq_dict[next_byte] += 1
        next_byte = reader.read_byte()

    tree = Tree()

    # Creates blank file if original file is also blank
    if file_size_zero:
        with open(sys.argv[2], 'w', encoding='utf-8'):
            return

    tree.create_tree(freq_dict)

    # Create header (right now it is 3 byte header)
    for _, value in freq_dict.items():

        byte1 = format((value >> 16) & 0xFF, '08b')
        byte2 = format((value >> 8) & 0xFF, '08b')
        byte3 = format(value & 0xFF, '08b')

        writer.write_byte(byte1)
        writer.write_byte(byte2)
        writer.write_byte(byte3)

    writer.reset()
    reader.reset_gen()

    # Ecodes bytes
    curr_byte = ""
    while curr_byte is not None:
        curr_byte = reader.read_byte()
        if curr_byte is None:
            break
        identifier = curr_byte
        tree.encode(identifier, writer)

    writer.write_final()


if __name__ == '__main__':
    main()
