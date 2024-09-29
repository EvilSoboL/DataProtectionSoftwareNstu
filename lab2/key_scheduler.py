class KeyScheduler:
    def __init__(self, key: int):
        self.key = key
        self.key_bits = f"{key:064b}"  # Представляем ключ как 64-битное бинарное число

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
