import os


def generate_key(length):
    """Генерация случайного ключа заданной длины в байтах."""
    return os.urandom(length)


def encrypt(data, key):
    """Шифрование данных с использованием ключа (XOR)."""
    return bytes(a ^ b for a, b in zip(data, key))


def lfsr(polynomial, seed, length):
    """Генерация псевдослучайной последовательности на основе LFSR с начальным значением (IV)."""
    state = seed
    output = []

    for _ in range(length * 8):  # Генерация битов
        new_bit = 0
        for tap in polynomial:
            new_bit ^= (state >> (tap - 1)) & 1
        state = ((state << 1) | new_bit) & ((1 << max(polynomial)) - 1)
        output.append(new_bit)

    # Преобразование списка битов в байты
    byte_output = bytearray()
    for i in range(0, len(output), 8):
        byte_output.append(int(''.join(map(str, output[i:i + 8])), 2))

    return bytes(byte_output)


def get_polynomial(scrambler_type):
    """Возвращает полином в зависимости от типа скремблера."""
    polynomials = {
        "x^11 + x^5 + x^2 + 1": [11, 5, 2, 1],
        "x^11 + x^2 + 1": [11, 2, 1]
    }
    if scrambler_type not in polynomials:
        raise ValueError("Неизвестный тип скремблера")
    return polynomials[scrambler_type]


def scramble_encrypt(data, scrambler_type, iv):
    """Шифрование данных с использованием скремблера."""
    polynomial = get_polynomial(scrambler_type)

    if len(iv) != 11:  # IV должен быть 11 бит
        raise ValueError("Начальное значение скремблера должно быть 11 бит.")

    iv_int = int(iv, 2)
    lfsr_output = lfsr(polynomial, iv_int, len(data))

    return bytes([b ^ lfsr_output[i] for i, b in enumerate(data)])


def scramble_decrypt(data, scrambler_type, iv):
    """Расшифровка данных, зашифрованных скремблером."""
    return scramble_encrypt(data, scrambler_type, iv)  # Процесс идентичен шифрованию
