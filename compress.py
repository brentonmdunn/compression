"""Compresses file."""

import sys
from typing import Dict
from read import Read
from tree import Tree
from write import Write
import math

class FileTooLargeError(Exception):
    def __init__(self, message="File is too big"):
        self.message = message
        super().__init__(self.message)

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
    bits_needed = math.ceil(math.log(reader.file_size, 2))
    if bits_needed > 255:
        raise FileTooLargeError("The file is too big to process.")
    writer.write_byte(format(bits_needed, '08b'))
    print(bits_needed)
    for _, value in freq_dict.items():
        writer.write_nonstd(format(value, f'0{bits_needed}b'))

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
