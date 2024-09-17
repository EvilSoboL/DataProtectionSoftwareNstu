def bytes_to_binary(data):
    """Преобразует байты в строку двоичного представления."""
    return ' '.join(format(byte, '08b') for byte in data)


def bytes_to_hex(data):
    """Преобразует байты в строку шестнадцатеричного представления."""
    return data.hex()


def bytes_to_text(data):
    """Преобразует байты в строку текста (Windows-1251)."""
    try:
        # Попробуем декодировать байты напрямую в Windows-1251
        return data.decode('windows-1251')
    except UnicodeDecodeError:
        # Если не удалось декодировать, возвращаем шестнадцатеричное представление
        return bytes_to_hex(data)


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
    """Преобразует строку текста (Windows-1251) обратно в байты."""
    try:
        return data.encode('windows-1251')
    except UnicodeEncodeError:
        raise ValueError("Некорректный текст для кодировки Windows-1251.")
