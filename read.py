""" Class file for Read object."""

import os
from typing import List, Generator

class Read:
    """Reads from a specified file."""

    def __init__(self, file_path: str):
        self.file_path: str = file_path
        self.current_buffer: List[str] = [0 for _ in range(8)]
        self.current_buffer_idx: int = 7
        self.byte_gen: Generator = self.get_byte()
        self.file_size = os.path.getsize(file_path)


    def reset_gen(self) -> None:
        """Creates a new instance of generator (resets it)."""
        self.byte_gen = self.get_byte()


    def get_byte(self) -> Generator[bytes, any, None]:
        """
        Generator function that reads next byte from file.
        Yeilds: next byte
        """
        with open(self.file_path, 'rb') as f:
            byte = f.read(1)
            while byte:
                yield byte
                byte = f.read(1)


    def read_byte(self) -> str:
        """Returns next byte in file."""
        try:
            return format(next(self.byte_gen)[0], '08b')
        except StopIteration:
            return None


    def read_bit(self) -> str:
        """Returns next bit in file."""
        self.current_buffer_idx += 1
        if self.current_buffer_idx == 8:
            next_byte = self.read_byte()
            if next_byte is None:
                return None
            self.current_buffer = list(next_byte)
            self.current_buffer_idx = 0
        return self.current_buffer[self.current_buffer_idx]


    def read_nonstd(self, num: int) -> str:
        """Reads a non-standard (i.e., not a byte) amount of bits."""
        output = ""
        for _ in range(num):
            output += self.read_bit()
        return output
