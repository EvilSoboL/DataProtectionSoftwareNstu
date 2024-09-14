def bytes_to_binary(data):
    """Преобразует байты в строку двоичного представления."""
    return ' '.join(format(byte, '08b') for byte in data)


def bytes_to_hex(data):
    """Преобразует байты в строку шестнадцатеричного представления."""
    return data.hex()


def bytes_to_text(data):
    """Преобразует байты в строку текста (UTF-8)."""
    try:
        return data.decode('utf-8')
    except UnicodeDecodeError:
        return '<Некорректные символы для UTF-8>'


def binary_to_bytes(data):
    """Преобразует строку двоичного представления в байты."""
    try:
        return bytearray(int(b, 2) for b in data.split())
    except ValueError:
        raise ValueError("Некорректный двоичный формат.")


def hex_to_bytes(data):
    """Преобразует строку шестнадцатеричного представления в байты."""
    try:
        return bytearray.fromhex(data)
    except ValueError:
        raise ValueError("Некорректный шестнадцатеричный формат.")


def text_to_bytes(data):
    """Преобразует строку текста в байты (UTF-8)."""
    return data.encode('utf-8')
