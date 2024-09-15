import os


def generate_key(length):
    return os.urandom(length)


def encrypt(data, key):
    return bytes(a ^ b for a, b in zip(data, key))


def lfsr(polynomial, seed, length):
    """Генерация псевдослучайной последовательности на основе LFSR."""
    state = seed
    output = bytearray()

    for _ in range(length):
        # Сдвиг и генерация нового бита
        new_bit = 0
        for tap in polynomial:
            new_bit ^= (state >> tap) & 1
        state = (state << 1) | new_bit
        state &= (1 << max(polynomial)) - 1  # Ограничение длины регистра
        output.append(state & 0xFF)

    return bytes(output)


def scramble_encrypt(data, scrambler_type, iv):
    # Преобразование IV в число
    iv_bytes = iv.encode('utf-8')
    iv_int = int.from_bytes(iv_bytes, 'big')

    if scrambler_type == "x^11 + x^5 + x^2 + 1":
        # Полином для скремблера x^11 + x^5 + x^2 + 1
        polynomial = [11, 5, 2, 0]
    elif scrambler_type == "x^11 + x^2 + 1":
        # Полином для скремблера x^11 + x^2 + 1
        polynomial = [11, 2, 0]
    else:
        raise ValueError("Неизвестный тип скремблера")

    # Генерация псевдослучайной последовательности на основе LFSR
    lfsr_output = lfsr(polynomial, iv_int, len(data))

    # Шифрование XOR с псевдослучайной последовательностью
    encrypted_data = bytes([b ^ lfsr_output[i] for i, b in enumerate(data)])

    return encrypted_data

