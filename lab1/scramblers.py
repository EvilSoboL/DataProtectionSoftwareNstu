def scrambler_1(data: bytes) -> bytes:
    """Скремблирование с использованием полинома x^11 + x^5 + x^2 + 1."""
    polynomial = 0b100001001001  # Полином x^11 + x^5 + x^2 + 1
    return apply_scrambler(data, polynomial)

def scrambler_2(data: bytes) -> bytes:
    """Скремблирование с использованием полинома x^11 + x^2 + 1."""
    polynomial = 0b100001000001  # Полином x^11 + x^2 + 1
    return apply_scrambler(data, polynomial)

def apply_scrambler(data: bytes, polynomial: int) -> bytes:
    """Применяет скремблер с заданным полиномом к данным."""
    scrambled_data = bytearray()
    state = 0

    for byte in data:
        for i in range(8):
            bit = (byte >> (7 - i)) & 1
            feedback = (state >> 10) & 1  # Получаем старший бит
            state = ((state << 1) | bit) & 0x7FF  # 11-битный регистр
            if feedback:
                state ^= polynomial  # XOR с полиномом

        scrambled_data.append(state & 0xFF)

    return bytes(scrambled_data)
