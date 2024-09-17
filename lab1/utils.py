import base64

def bytes_to_binary(data):
    """Преобразует байты в строку двоичного представления."""
    return ' '.join(format(byte, '08b') for byte in data)

def bytes_to_hex(data):
    """Преобразует байты в строку шестнадцатеричного представления."""
    return data.hex()

def bytes_to_base64(data):
    """Преобразует байты в строку Base64."""
    return base64.b64encode(data).decode('utf-8')

def bytes_to_text(data):
    """Преобразует байты в строку текста (Windows-1251), а также пытается интерпретировать шестнадцатеричные данные как текст."""
    try:
        # Попробуем декодировать байты напрямую в Windows-1251
        return data.decode('windows-1251')
    except UnicodeDecodeError:
        try:
            # Если не получилось, пробуем интерпретировать их как шестнадцатеричные данные
            hex_data = data.hex()
            # Пробуем преобразовать их обратно в байты и декодировать в текст (Windows-1251)
            return bytes.fromhex(hex_data).decode('windows-1251')
        except (UnicodeDecodeError, ValueError):
            # Если не удалось, выбрасываем ошибку
            raise ValueError("Не удалось преобразовать данные в текстовое представление.")




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

def base64_to_bytes(data):
    """Преобразует строку Base64 в байты."""
    try:
        return base64.b64decode(data)
    except ValueError:
        raise ValueError("Некорректный формат Base64.")

def text_to_bytes(data):
    """Преобразует строку текста, представленную в шестнадцатеричном формате, обратно в байты."""
    try:
        # Преобразуем текст в байты, предполагая, что входные данные — это шестнадцатеричное представление
        return hex_to_bytes(data)
    except ValueError:
        raise ValueError("Некорректный шестнадцатеричный формат для символьного представления.")





