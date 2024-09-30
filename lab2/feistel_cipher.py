import struct

class FeistelCipher:
    def __init__(self, key: int, rounds: int = 16, subkey_method: int = 0, function_type: int = 0):
        self.rounds = rounds
        self.subkey_method = subkey_method
        self.key_bits = f"{key:064b}"
        self.function_type = function_type

    def encrypt(self, plaintext: bytes) -> bytes:
        blocks = self._split_blocks(plaintext)
        encrypted_blocks = [self._process_block(block, encrypt=True) for block in blocks]
        return b''.join(struct.pack('>Q', block) for block in encrypted_blocks)

    def decrypt(self, ciphertext: bytes) -> bytes:
        blocks = self._split_blocks(ciphertext)
        decrypted_blocks = [self._process_block(block, encrypt=False) for block in blocks]
        return b''.join(struct.pack('>Q', block) for block in decrypted_blocks)

    def _process_block(self, block: int, encrypt: bool = True) -> int:
        left = (block >> 32) & 0xFFFFFFFF
        right = block & 0xFFFFFFFF

        if encrypt:
            for round_num in range(self.rounds):
                left, right = self._feistel_round(left, right, round_num)
        else:
            for round_num in reversed(range(self.rounds)):
                right, left = self._feistel_round(right, left, round_num)

        return (left << 32) | right

    def _feistel_round(self, left: int, right: int, round_num: int) -> tuple:
        subkey = self._get_subkey(round_num)
        new_left = right

        if self.function_type == 0:
            new_right = left ^ self.F(right)
        elif self.function_type == 1:
            new_right = left ^ self.F_with_X(right, subkey)
        else:
            raise ValueError("Неподдерживаемый тип функции.")

        return new_left, new_right

    def F(self, Vi: int) -> int:
        return ((Vi << 3) & 0xFFFFFFFF) | (Vi >> 5)  # Более сложная функция F

    def F_with_X(self, Vi: int, Xi: int) -> int:
        scrambled_value = self.scrambler(Xi)
        return scrambled_value ^ Vi

    def scrambler(self, value: int) -> int:
        return ((value << 3) & 0xFFFFFFFF) | (value >> 5)  # Пример скремблера

    def get_subkey_method_a(self, round_num: int) -> int:
        start_bit = round_num % 64
        key_bits_extended = self.key_bits * 2
        subkey_bits = key_bits_extended[start_bit:start_bit + 32]
        return int(subkey_bits, 2)

    def get_subkey_method_b(self, round_num: int) -> int:
        start_bit = round_num % 64
        key_bits_extended = self.key_bits * 2
        initial_bits = key_bits_extended[start_bit:start_bit + 8]
        initial_value = int(initial_bits, 2)
        return self.scrambler(initial_value)

    def _get_subkey(self, round_num: int) -> int:
        if self.subkey_method == 0:
            return self.get_subkey_method_a(round_num)
        elif self.subkey_method == 1:
            return self.get_subkey_method_b(round_num)
        else:
            raise ValueError("Неподдерживаемый метод генерации подключей.")

    def _split_blocks(self, data: bytes) -> list:
        if not isinstance(data, bytes):
            raise ValueError("Data must be of type 'bytes'.")
        original_length = len(data)
        if original_length % 8 != 0:
            data += b'\0' * (8 - original_length % 8)
        blocks = []
        for i in range(0, len(data), 8):
            block = int.from_bytes(data[i:i + 8], byteorder='big')
            blocks.append(block)
        return blocks