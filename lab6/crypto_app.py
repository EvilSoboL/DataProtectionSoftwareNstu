import random
import math
from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad


class RSA:
    def miller_rabin_test(self, n, k=5):
        """
        Тест Миллера-Рабина для проверки простоты числа
        n - число для проверки
        k - количество раундов тестирования
        """
        if n <= 1 or n == 4:
            return False
        if n <= 3:
            return True

        # Разложение n-1 на множители вида 2^r * d
        d = n - 1
        r = 0
        while d % 2 == 0:
            d //= 2
            r += 1

        # Тестирование k раз
        for _ in range(k):
            a = random.randint(2, n - 2)
            x = pow(a, d, n)

            if x == 1 or x == n - 1:
                continue

            for _ in range(r - 1):
                x = pow(x, 2, n)
                if x == n - 1:
                    break
            else:
                return False
        return True

    def generate_prime(self, min_bits=512, max_bits=1024, max_attempts=1000):
        """
        Генерация простого числа с использованием теста Миллера-Рабина
        с расширенными настройками генерации
        """
        attempts = 0
        while attempts < max_attempts:
            # Генерируем случайное число нужной битности
            bits = random.randint(min_bits, max_bits)

            # Создаем число с нужным количеством бит, устанавливая старший и младший биты
            prime = (1 << (bits - 1)) | 1  # Устанавливаем старший бит и младший бит

            # Добавляем случайные биты между старшим и младшим
            for _ in range(bits - 2):
                prime |= (random.randint(0, 1) << _)

            # Проверяем простоту
            if self.miller_rabin_test(prime):
                return prime

            attempts += 1

        raise RuntimeError(f"Не удалось найти подходящее простое число за {max_attempts} попыток")

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

    def generate_keypair(self, min_key_bits=512, max_key_bits=1024):
        """
        Генерация пары ключей с контролем битности
        """
        attempts = 0
        max_key_generation_attempts = 100

        while attempts < max_key_generation_attempts:
            # Генерируем два простых числа
            p = self.generate_prime(min_bits=min_key_bits // 2, max_bits=max_key_bits // 2)
            q = self.generate_prime(min_bits=min_key_bits // 2, max_bits=max_key_bits // 2)

            # Убеждаемся, что простые числа различны
            while p == q:
                q = self.generate_prime(min_bits=min_key_bits // 2, max_bits=max_key_bits // 2)

            # Вычисляем модуль
            n = p * q

            # Проверяем битность модуля
            if min_key_bits <= n.bit_length() <= max_key_bits:
                # Вычисляем функцию Эйлера
                phi = (p - 1) * (q - 1)

                # Выбираем открытую экспоненту
                e = 65537  # Стандартное значение
                if math.gcd(e, phi) == 1:
                    # Вычисляем закрытую экспоненту
                    try:
                        d = self.modinv(e, phi)
                        return ((e, n), (d, n))
                    except Exception:
                        pass

            attempts += 1

        raise RuntimeError(f"Не удалось сгенерировать подходящую пару ключей за {max_key_generation_attempts} попыток")


class CombinedEncryption:
    def __init__(self):
        self.rsa = RSA()
        # Keep trying until we get a large enough key pair
        while True:
            try:
                self.public_key, self.private_key = self.rsa.generate_keypair()
                break
            except ValueError:
                continue

    def pad_text(self, text):
        # Дополняем текст до кратности 8 байт (для DES)
        while len(text) % 8 != 0:
            text += b' '
        return text

    def encrypt_file(self, input_file, encrypted_file, encrypted_key_file):
        try:
            # Generate random DES key
            des_key = get_random_bytes(8)
            print(f"Generated DES key (hex): {des_key.hex()}")

            # Convert DES key to integer
            des_key_int = int.from_bytes(des_key, byteorder='big')
            print(f"DES key as integer: {des_key_int}")

            # Verify the RSA modulus is large enough
            if des_key_int >= self.public_key[1]:
                raise ValueError(
                    f"RSA modulus ({self.public_key[1].bit_length()} bits) too small for DES key ({des_key_int.bit_length()} bits)")

            encrypted_des_key = pow(des_key_int, self.public_key[0], self.public_key[1])
            print(f"Encrypted DES key: {encrypted_des_key}")

            # Save encrypted key
            with open(encrypted_key_file, 'w') as f:
                f.write(str(encrypted_des_key))

            # Read and encrypt file
            with open(input_file, 'rb') as f:
                plaintext = f.read()
            print(f"Original text (hex): {plaintext.hex()}")

            # Pad the plaintext
            padded_plaintext = pad(plaintext, DES.block_size)
            print(f"Padded text (hex): {padded_plaintext.hex()}")

            # Create DES cipher and encrypt
            cipher = DES.new(des_key, DES.MODE_ECB)
            ciphertext = cipher.encrypt(padded_plaintext)
            print(f"Encrypted text (hex): {ciphertext.hex()}")

            # Save encrypted file
            with open(encrypted_file, 'wb') as f:
                f.write(ciphertext)

            return True

        except Exception as e:
            print(f"Encryption error: {str(e)}")
            raise

    def decrypt_file(self, encrypted_file, decrypted_file, encrypted_key_file):
        try:
            # Read encrypted DES key
            with open(encrypted_key_file, 'r') as f:
                encrypted_des_key = int(f.read())
            print(f"Read encrypted DES key: {encrypted_des_key}")

            # Decrypt DES key using RSA private key
            des_key_int = pow(encrypted_des_key, self.private_key[0], self.private_key[1])
            print(f"Decrypted DES key as integer: {des_key_int}")

            # Convert integer back to bytes, ensuring 8-byte length
            des_key = des_key_int.to_bytes(8, byteorder='big')
            print(f"Decrypted DES key (hex): {des_key.hex()}")

            # Read encrypted file
            with open(encrypted_file, 'rb') as f:
                ciphertext = f.read()
            print(f"Read encrypted text (hex): {ciphertext.hex()}")

            # Create DES cipher and decrypt
            cipher = DES.new(des_key, DES.MODE_ECB)
            padded_plaintext = cipher.decrypt(ciphertext)
            print(f"Decrypted padded text (hex): {padded_plaintext.hex()}")

            # Remove padding
            plaintext = unpad(padded_plaintext, DES.block_size)
            print(f"Decrypted text without padding (hex): {plaintext.hex()}")

            # Save decrypted file
            with open(decrypted_file, 'wb') as f:
                f.write(plaintext)

            return True

        except Exception as e:
            print(f"Decryption error: {str(e)}")
            raise

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