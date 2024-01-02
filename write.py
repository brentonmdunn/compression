"""Class file for Read object."""

from typing import List, Union

class Write:
    """Writes to specified file."""

    def __init__(self, file_path: str):
        self.file_path: str = file_path
        self.current_buffer: List[str] = [0 for _ in range(8)]
        self.current_buffer_idx: int = 0


    def flush_buffer(self) -> None:
        """Resets buffer to all 0s."""
        self.current_buffer = [0 for _ in range(8)]


    def reset(self) -> None:
        """Resets buffer."""
        self.current_buffer: List[str] = [0 for _ in range(8)]
        self.current_buffer_idx: int = 0


    def write_byte(self, bit_str: Union[str, List[str]]) -> None:
        """Writes bytes to file."""

        if len(bit_str) != 8:
            raise ValueError("Byte must be 8 digits.")
        
        # Puts bits in list if not already
        if not isinstance(bit_str, list):
            bits: List[int] = [int(char) for char in bit_str if char.isdigit()]
        else:
            bits: List[int] = bit_str

        with open(self.file_path, 'ab') as f:
            byte = 0
            bit_count = 0

            # Takes each bit in array and bit shifts it into `byte`
            for bit in bits:
                byte = (byte << 1) | bit
                bit_count += 1

                # When full byte, writes byte and resets counts to 0
                if (bit_count == 8):
                    f.write(bytes([byte]))
                    byte = 0
                    bit_count = 0

            # If less than full byte, adds additional 0s at end
            if bit_count > 0:
                byte <<= (8-bit_count)
                f.write(bytes([byte]))


    def write_bit(self, bit: str) -> None:
        """Writes bit to file."""

        if len(bit) != 1:
            raise ValueError("Bit must be 1 number.")

        # Keeps track of current index and adds newest bit in next untouched index
        self.current_buffer[self.current_buffer_idx] = int(bit)
        self.current_buffer_idx += 1

        # Writes byte when a full byte is created
        if (self.current_buffer_idx == 8):
            self.current_buffer_idx = 0
            self.write_byte(self.current_buffer)


    def write_nonstd(self, value: str) -> None:
        """Writes a non-standard (i.e., not a byte) amount of bits."""
        for char in value:
            self.write_bit(char)


    def write_final(self) -> None:
        """
        Writes additional 0s so that a full byte is written. 
        Forces buffer to write since it doesn't write until all 8 bits are in list.
        """

        if self.current_buffer_idx != 0:
            for _ in range(self.current_buffer_idx, 8):
                self.write_bit('0')
