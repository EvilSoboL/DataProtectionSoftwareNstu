import struct


class FeistelCipher:
    def __init__(self, rounds=16):
        self.rounds = rounds

    def _feistel_round(self, left, right, key):
        # Простейшая функция раунда, может быть изменена
        return right, left ^ self._round_function(right, key)

    def _round_function(self, data, key):
        # Простая XOR операция с ключом, можно заменить на более сложную
        return data ^ key

    def encrypt(self, plaintext, key):
        # Преобразование текста в 64-битные блоки
        blocks = self._split_blocks(plaintext)

        # Шифрование блоков
        encrypted_blocks = [self._process_block(block, key, encrypt=True) for block in blocks]

        # Преобразование зашифрованных блоков в байты
        return b''.join(struct.pack('>Q', block) for block in encrypted_blocks)

    def decrypt(self, ciphertext, key):
        # Преобразование байтов в 64-битные блоки
        blocks = self._split_blocks(ciphertext, byte_input=True)

        # Расшифровка блоков
        decrypted_blocks = [self._process_block(block, key, encrypt=False) for block in blocks]

        # Преобразование расшифрованных блоков обратно в байты
        return b''.join(struct.pack('>Q', block) for block in decrypted_blocks)

    def _process_block(self, block, key, encrypt=True):
        # Разделяем блок на левую и правую части
        left = (block >> 32) & 0xFFFFFFFF
        right = block & 0xFFFFFFFF

        # Выполняем раунды шифрования/дешифрования
        for i in range(self.rounds):
            if encrypt:
                left, right = self._feistel_round(left, right, key)
            else:
                right, left = self._feistel_round(right, left, key)

        return (left << 32) | right

    def _split_blocks(self, data, byte_input=False):
        # Разделение данных на 64-битные блоки
        if byte_input:
            return [struct.unpack('>Q', data[i:i+8])[0] for i in range(0, len(data), 8)]
        else:
            return [int.from_bytes(data[i:i+8], byteorder='big') for i in range(0, len(data), 8)]
