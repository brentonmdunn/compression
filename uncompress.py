"""Uncompresses file."""

import sys
from typing import Dict
from read import Read
from tree import Tree
from write import Write
from progress_bar import ProgressBar


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
        header_size: int = int(reader.read_byte(), 2)
        for i in range(256):
            binary_str = format(i, '08b')
            # combined: str = ""
            # for _ in range(header_size):
            #     combined += reader.read_byte()
            combined: str = reader.read_nonstd(header_size)

            freq_dict[binary_str] = int(combined, 2)

    tree = Tree()

    if not file_size_zero:
        tree.create_tree(freq_dict)

    total_size = 0
    for value in freq_dict.values():
        total_size += value

    # Decodes bytes
    progress_bar = ProgressBar()
    prev_round = 0
    total_iter = 1000 if total_size > 1000 else total_size
    progress_bar.print(0, total_iter, prefix = 'Progress:', suffix = 'Complete', length = 50)
    progress_bar_i = 0
    for i in range(total_size):

        # Progress bar
        curr_round = round(((i/total_size) * 100), 1)
        if curr_round != prev_round:    # One decimal point in percentage
            progress_bar.print(progress_bar_i + 1,
                               total_iter,
                               prefix = 'Progress:',
                               suffix = 'Complete',
                               length = 50)
            prev_round = curr_round
            progress_bar_i += 1

        to_write = tree.decode(reader)
        if to_write is None:
            break
        writer.write_nonstd(to_write)


if __name__ == '__main__':
    main()
