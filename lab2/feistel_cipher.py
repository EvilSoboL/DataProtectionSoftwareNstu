def feistel_round(left, right, key):
    """Простая операция XOR для каждого раунда."""
    return right, left ^ (right ^ key)

def feistel_encrypt(text, key, rounds=16):
    """Шифрование сетью Фейстеля."""
    left, right = text[:len(text)//2], text[len(text)//2:]
    for i in range(rounds):
        left, right = feistel_round(left, right, key[i % len(key)])
    return left + right

def feistel_decrypt(ciphertext, key, rounds=16):
    """Дешифрование сетью Фейстеля."""
    left, right = ciphertext[:len(ciphertext)//2], ciphertext[len(ciphertext)//2:]
    for i in range(rounds):
        left, right = feistel_round(left, right, key[-(i % len(key))])
    return left + right
