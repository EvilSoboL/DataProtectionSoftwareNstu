def scrambler_1(data: bytes) -> bytes:
    # Полином x^11 + x^5 + x^2 + 1
    # Пример простой реализации скремблирования (детали реализации могут измениться):
    poly = 0b1000000000101
    return apply_scrambler(data, poly)

def scrambler_2(data: bytes) -> bytes:
    # Полином x^11 + x^2 + 1
    poly = 0b1000000000101
    return apply_scrambler(data, poly)

def apply_scrambler(data: bytes, polynomial: int) -> bytes:
    # Пример скремблирования
    scrambled_data = bytearray()
    state = 0

    for byte in data:
        for i in range(8):
            bit = (byte >> (7 - i)) & 1
            feedback = state >> 10  # Получаем старший бит
            state = ((state << 1) | bit) & 0x7FF  # 11-битный регистр
            if feedback:
                state ^= polynomial  # XOR с полиномом

        scrambled_data.append(state & 0xFF)

    return bytes(scrambled_data)
