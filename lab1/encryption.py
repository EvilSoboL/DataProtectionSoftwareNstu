import os
import random


def generate_key(length):
    """Генерирует случайный ключ заданной длины."""
    return bytearray(random.getrandbits(8) for _ in range(length))


def encrypt(data, key):
    """Шифрует данные с помощью ключа методом XOR."""
    return bytearray(a ^ b for a, b in zip(data, key))


def decrypt(encrypted_data, key):
    """Расшифровывает данные с помощью ключа методом XOR."""
    return encrypt(encrypted_data, key)  # XOR является симметричным
