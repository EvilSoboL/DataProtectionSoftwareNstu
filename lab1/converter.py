def bytes_to_binary(data):
    return ' '.join(format(byte, '08b') for byte in data)


def binary_to_bytes(data):
    """Преобразует строку двоичного представления в байты."""
    try:
        return bytearray(int(b, 2) for b in data.split())
    except ValueError:
        raise ValueError("Некорректный двоичный формат.")