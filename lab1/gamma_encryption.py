import os


def generate_key(length: int) -> bytes:
    return os.urandom(length)


def encrypt(data: bytes, key: bytes) -> bytes:
    return bytes(a ^ b for a, b in zip(data, key))
