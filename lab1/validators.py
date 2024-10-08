import re


def validate_binary(data):
    """Проверяет, что данные содержат только 0 и 1 в виде байтов (8 бит) разделённых пробелами."""
    pattern = r'^([01]{8} ?)+$'
    return re.fullmatch(pattern, data.strip()) is not None


def validate_hexadecimal(data):
    """Проверяет, что данные содержат только шестнадцатеричные символы."""
    pattern = r'^[0-9a-fA-F]+$'
    return re.fullmatch(pattern, data.strip()) is not None


def validate_text(data):
    """Проверяет, что данные являются корректным текстом (UTF-8)."""
    try:
        data.encode('utf-8')
        return True
    except UnicodeEncodeError:
        return False


def validate_length(original_length, new_data):
    """Проверяет, что новая строка имеет такую же длину, что и оригинальная."""
    return len(original_length) == len(new_data)
