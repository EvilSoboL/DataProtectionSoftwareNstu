import os

def generate_key(length):
    return os.urandom(length)

def encrypt(data, key):
    return bytes(a ^ b for a, b in zip(data, key))

def lfsr(polynomial, seed, length):
    """Генерация псевдослучайной последовательности на основе LFSR с начальным значением (IV)."""
    state = seed  # Начальное значение (IV)
    output = bytearray()

    for _ in range(length):
        new_bit = 0
        for tap in polynomial:
            new_bit ^= (state >> tap) & 1
        state = (state << 1) | new_bit
        state &= (1 << max(polynomial)) - 1  # Ограничиваем длину регистра
        output.append(state & 0xFF)

    return bytes(output)

def scramble_encrypt(data, scrambler_type, iv):
    """Шифрование данных с использованием скремблера."""
    # Определяем длину регистра в зависимости от типа скремблера
    if scrambler_type == "x^11 + x^5 + x^2 + 1":
        register_length = 11
        polynomial = [11, 5, 2, 0]
    elif scrambler_type == "x^11 + x^2 + 1":
        register_length = 11
        polynomial = [11, 2, 0]
    else:
        raise ValueError("Неизвестный тип скремблера")

    # Проверка длины IV
    if len(iv) != register_length:
        raise ValueError(f"Начальное значение скремблера должно быть {register_length} бит.")

    # Преобразование IV в целое число
    iv_int = int(iv, 2)  # Ожидаем, что IV введен как двоичная строка

    # Генерация псевдослучайной последовательности на основе LFSR
    lfsr_output = lfsr(polynomial, iv_int, len(data))

    # Шифрование XOR с псевдослучайной последовательностью
    encrypted_data = bytes([b ^ lfsr_output[i] for i, b in enumerate(data)])

    return encrypted_data

def scramble_decrypt(data, scrambler_type, iv):
    """Расшифровка данных, зашифрованных скремблером."""
    # Процесс расшифровки идентичен шифрованию, так как алгоритм симметричный
    return scramble_encrypt(data, scrambler_type, iv)

