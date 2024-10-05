import re


def validate_binary(data: str) -> bool:
    pattern = r'^([01]{8} ?)+$'
    return re.fullmatch(pattern, data.strip()) is not None


def validate_hexadecimal(data: str) -> bool:
    pattern = r'^[0-9a-fA-F]+$'
    return re.fullmatch(pattern, data.strip()) is not None
