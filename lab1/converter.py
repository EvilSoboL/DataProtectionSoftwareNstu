def bytes_to_binary(data: bytes) -> str:
    """Преобразует байты в строку двоичного представления"""
    return ' '.join(format(byte, '08b') for byte in data)


def bytes_to_hex(data: bytes) -> str:
    """Преобразует байты в строку шестнадцатеричного представления."""
    return data.hex()


def bytes_to_text(data: bytes) -> str:
    """Преобразует байты в строку текста (Windows-1251)."""
    return data.decode('windows-1251')


def binary_to_bytes(data: str) -> bytes:
    """Преобразует строку двоичного представления в байты"""
    return bytes(int(b, 2) for b in data.split())


def hex_to_bytes(data: str) -> bytes:
    """Преобразует строку шестнадцатеричного представления в байты"""
    return bytearray.fromhex(data)


def text_to_bytes(data: str) -> bytes:
    """Преобразует строку текста (Windows-1251) в байты"""
    return data.encode('windows-1251')


def text_to_hex(data: str) -> str:
    """Преобразование строки текста (Windows-1251) в шестнадцатеричное представление"""
    byte = text_to_bytes(data)
    return byte.hex()


def hex_to_text(data: str) -> str:
    """Преобразование шестнадцатеричной строки в строку текста (Windows-1251)"""
    byte = hex_to_bytes(data)
    return bytes_to_text(byte)
