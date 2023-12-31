from typing import List, Generator

class Read:
    """Reads from a specified file."""

    def __init__(self, file_path):
        self.file_path: str = file_path
        self.current_buffer: List[str] = [0 for _ in range(8)]
        self.current_buffer_idx: int = 7
        self.byte_gen: Generator = self.get_byte()


    def get_byte(self):
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
        return format(next(self.byte_gen)[0], '08b')


    def read_bit(self) -> str:
        """Returns next bit in file."""
        self.current_buffer_idx += 1
        if self.current_buffer_idx == 8:
            self.current_buffer = list(self.read_byte())
            self.current_buffer_idx = 0
        return self.current_buffer[self.current_buffer_idx]


    def read_nonstd(self, num: int):
        output = ""
        for _ in range(num):
            output += self.read_bit()