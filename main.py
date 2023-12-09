class write:
    def __init__(self, file_path):
        self.file_path = file_path
        self.current_buffer = [0 for _ in range(8)]
        self.current_buffer_idx = 0


    def write_byte(self, bit_str):
        if not isinstance(bit_str, list):
            bits = [int(char) for char in bit_str if char.isdigit()]
        else:
            bits = bit_str
        with open(self.file_path, 'ab') as f:
            byte = 0
            bit_count = 0
            for bit in bits:
                byte = (byte << 1) | bit
                bit_count += 1
                if (bit_count == 8):
                    f.write(bytes([byte]))
                    byte = 0
                    bit_count = 0

            if bit_count > 0:
                byte <<= (8-bit_count)
                f.write(bytes([byte]))

    def write_bit(self, bit):
        self.current_buffer[self.current_buffer_idx] = int(bit)
        self.current_buffer_idx += 1
        if (self.current_buffer_idx == 8):
            self.current_buffer_idx = 0
            self.write_byte(self.current_buffer)

    def write_final(self):
        if self.current_buffer_idx != 0:
            for _ in range(self.current_buffer_idx, 8):
                self.write_bit('0')
