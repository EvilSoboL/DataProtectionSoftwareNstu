import os


def generate_key(length):
    return os.urandom(length)


def encrypt(data, key):
    return bytes(a ^ b for a, b in zip(data, key))


def lfsr(polynomial, seed, length):
    """Генерация псевдослучайной последовательности на основе LFSR с начальным значением (IV)."""
    state = seed  # Начальное значение (IV)
    output = []

    for _ in range(length * 8):  # Генерация битов (для каждого байта 8 бит)
        new_bit = 0
        for tap in polynomial:
            new_bit ^= (state >> (tap - 1)) & 1  # Получаем бит с нужной позиции (tap-1, так как позиции считаются с 1)
        state = ((state << 1) | new_bit) & ((1 << max(polynomial)) - 1)  # Сдвигаем и добавляем новый бит
        output.append(new_bit)

    # Преобразуем список битов в байты
    byte_output = bytearray()
    for i in range(0, len(output), 8):
        byte_output.append(int(''.join(map(str, output[i:i + 8])), 2))

    return bytes(byte_output)


def scramble_encrypt(data, scrambler_type, iv):
    """Шифрование данных с использованием скремблера."""
    # Определяем длину регистра в зависимости от типа скремблера
    if scrambler_type == "x^11 + x^5 + x^2 + 1":
        polynomial = [11, 5, 2, 1]  # Полином в виде позиций битов (нумерация с 1)
    elif scrambler_type == "x^11 + x^2 + 1":
        polynomial = [11, 2, 1]
    else:
        raise ValueError("Неизвестный тип скремблера")

    # Проверка длины IV
    if len(iv) != 11:  # IV должен быть 11 бит для обоих полиномов
        raise ValueError("Начальное значение скремблера должно быть 11 бит.")

    # Преобразование IV в целое число
    iv_int = int(iv, 2)

    # Генерация псевдослучайной последовательности на основе LFSR
    lfsr_output = lfsr(polynomial, iv_int, len(data))

    # Шифрование XOR с псевдослучайной последовательностью
    encrypted_data = bytes([b ^ lfsr_output[i] for i, b in enumerate(data)])

    return encrypted_data


def scramble_decrypt(data, scrambler_type, iv):
    """Расшифровка данных, зашифрованных скремблером."""
    return scramble_encrypt(data, scrambler_type, iv)  # Процесс идентичен шифрованию
