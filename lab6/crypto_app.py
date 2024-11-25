import random
import math
from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes


class RSA:
    def generate_prime(self, min_value=100, max_value=1000):
        def is_prime(n):
            if n < 2:
                return False
            for i in range(2, int(math.sqrt(n)) + 1):
                if n % i == 0:
                    return False
            return True

        prime = random.randrange(min_value, max_value)
        while not is_prime(prime):
            prime = random.randrange(min_value, max_value)
        return prime

    def extended_gcd(self, a, b):
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = self.extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y

    def modinv(self, a, m):
        gcd, x, _ = self.extended_gcd(a, m)
        if gcd != 1:
            raise Exception('Модульная инверсия не существует')
        return x % m

    def generate_keypair(self):
        # Генерация простых чисел p и q
        p = self.generate_prime()
        q = self.generate_prime()
        while p == q:  # Убеждаемся что числа различны
            q = self.generate_prime()

        n = p * q  # Модуль
        phi = (p - 1) * (q - 1)  # Функция Эйлера

        # Выбираем открытую экспоненту e
        e = 65537  # Часто используемое значение для e
        while math.gcd(e, phi) != 1:
            e = random.randrange(2, phi)

        # Вычисляем закрытую экспоненту d
        d = self.modinv(e, phi)

        return ((e, n), (d, n))  # ((public), (private))

    def encrypt(self, public_key, plaintext):
        e, n = public_key
        cipher = pow(plaintext, e, n)
        return cipher

    def decrypt(self, private_key, ciphertext):
        d, n = private_key
        plain = pow(ciphertext, d, n)
        return plain


class CombinedEncryption:
    def __init__(self):
        self.rsa = RSA()
        self.public_key, self.private_key = self.rsa.generate_keypair()

    def pad_text(self, text):
        # Дополняем текст до кратности 8 байт (для DES)
        while len(text) % 8 != 0:
            text += b' '
        return text

    def encrypt_file(self, input_file, encrypted_file, encrypted_key_file):
        # Генерируем случайный ключ для DES
        des_key = get_random_bytes(8)

        # Шифруем ключ DES с помощью RSA
        des_key_int = int.from_bytes(des_key, 'big')
        encrypted_des_key = self.rsa.encrypt(self.public_key, des_key_int)

        # Сохраняем зашифрованный ключ
        with open(encrypted_key_file, 'w') as f:
            f.write(str(encrypted_des_key))

        # Читаем и шифруем файл
        with open(input_file, 'rb') as f:
            plaintext = f.read()

        # Дополняем текст
        plaintext = self.pad_text(plaintext)

        # Создаем шифр DES
        cipher = DES.new(des_key, DES.MODE_ECB)

        # Шифруем данные
        ciphertext = cipher.encrypt(plaintext)

        # Сохраняем зашифрованный текст
        with open(encrypted_file, 'wb') as f:
            f.write(ciphertext)

    def decrypt_file(self, encrypted_file, decrypted_file, encrypted_key_file):
        # Читаем зашифрованный ключ DES
        with open(encrypted_key_file, 'r') as f:
            encrypted_des_key = int(f.read())

        # Расшифровываем ключ DES
        des_key_int = self.rsa.decrypt(self.private_key, encrypted_des_key)
        des_key = des_key_int.to_bytes(8, 'big')

        # Читаем зашифрованный файл
        with open(encrypted_file, 'rb') as f:
            ciphertext = f.read()

        # Создаем шифр DES
        cipher = DES.new(des_key, DES.MODE_ECB)

        # Расшифровываем данные
        plaintext = cipher.decrypt(ciphertext)

        # Сохраняем расшифрованный текст
        with open(decrypted_file, 'wb') as f:
            f.write(plaintext.rstrip(b' '))

    def save_keys(self, public_key_file, private_key_file):
        # Сохраняем открытый ключ
        with open(public_key_file, 'w') as f:
            f.write(f"{self.public_key[0]},{self.public_key[1]}")

        # Сохраняем закрытый ключ
        with open(private_key_file, 'w') as f:
            f.write(f"{self.private_key[0]},{self.private_key[1]}")


def hex_view(filename):
    """Просмотр файла в шестнадцатеричном виде"""
    with open(filename, 'rb') as f:
        content = f.read()

    hex_content = ' '.join(f'{b:02x}' for b in content)
    text_content = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in content)

    return hex_content, text_content


# Пример использования
if __name__ == "__main__":
    # Создаем экземпляр класса комбинированного шифрования
    crypto = CombinedEncryption()

    # Сохраняем ключи
    crypto.save_keys('public_key.txt', 'private_key.txt')

    # Шифруем файл
    crypto.encrypt_file('input.txt', 'encrypted.bin', 'encrypted_key.txt')

    # Просмотр зашифрованного файла
    hex_view, text_view = hex_view('encrypted.bin')
    print("Шестнадцатеричное представление:")
    print(hex_view)
    print("\nСимвольное представление:")
    print(text_view)

    # Расшифровываем файл
    crypto.decrypt_file('encrypted.bin', 'decrypted.txt', 'encrypted_key.txt')