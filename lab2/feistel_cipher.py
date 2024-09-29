import struct


class FeistelCipher:
    def __init__(self, key: int, rounds: int = 16, subkey_method: int = 0):
        self.rounds = rounds
        self.subkey_method = subkey_method  # 0 для метода A, 1 для метода B
        self.key_bits = f"{key:064b}"  # Ключ в виде 64-битной битовой строки

    def encrypt(self, plaintext: bytes) -> bytes:
        blocks = self._split_blocks(plaintext)
        encrypted_blocks = [self._process_block(block, encrypt=True) for block in blocks]
        return b''.join(struct.pack('>Q', block) for block in encrypted_blocks)

    def decrypt(self, ciphertext: bytes) -> bytes:
        blocks = self._split_blocks(ciphertext, byte_input=True)
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
        new_right = left ^ self._round_function(right, subkey)
        return new_left, new_right

    def _round_function(self, data: int, subkey: int) -> int:
        return data ^ subkey  # Простейшая round-функция

    def _get_subkey(self, round_num: int) -> int:
        if self.subkey_method == 0:
            return self.get_subkey_method_a(round_num)
        elif self.subkey_method == 1:
            return self.get_subkey_method_b(round_num)
        else:
            raise ValueError("Неподдерживаемый метод генерации подключей.")

    # Способ A: Циклическая цепочка из 32 бит
    def get_subkey_method_a(self, round_num: int) -> int:
        start_bit = round_num % 64  # Определяем начальный бит
        key_bits_extended = self.key_bits * 2  # Удваиваем ключ для циклического повторения
        subkey_bits = key_bits_extended[start_bit:start_bit + 32]  # Получаем 32 бита
        return int(subkey_bits, 2)  # Возвращаем в виде целого числа

    # Способ B: Скремблер
    def get_subkey_method_b(self, round_num: int) -> int:
        start_bit = round_num % 64  # Определяем начальный бит
        key_bits_extended = self.key_bits * 2  # Удваиваем ключ для циклического повторения
        initial_bits = key_bits_extended[start_bit:start_bit + 8]  # Получаем начальные 8 бит
        initial_value = int(initial_bits, 2)  # Преобразуем в число

        scrambled_value = self.scrambler(initial_value)

        return scrambled_value

    def scrambler(self, value: int) -> int:
        scrambled = value
        for _ in range(4):  # Генерация 32-битного подключа
            scrambled = ((scrambled << 1) & 0xFF) ^ ((scrambled >> 7) & 0x01)
        return scrambled

    def _split_blocks(self, data: bytes, byte_input: bool = False) -> list:
        if len(data) % 8 != 0:
            data += b'\0' * (8 - len(data) % 8)  # Дополнение данных до кратности 8 байтам

        if byte_input:
            return [struct.unpack('>Q', data[i:i+8])[0] for i in range(0, len(data), 8)]
        else:
            return [int.from_bytes(data[i:i+8], byteorder='big') for i in range(0, len(data), 8)]
