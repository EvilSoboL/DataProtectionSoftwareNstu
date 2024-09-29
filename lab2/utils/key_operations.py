import random
from PyQt5.QtWidgets import QMessageBox


class KeyOperations:
    @staticmethod
    def generate_random_key():
        return random.getrandbits(64)

    @staticmethod
    def save_key_to_file(key, save_path):
        if not save_path.endswith('.key'):
            save_path += '.key'  # Добавляем расширение .key, если его нет
        try:
            with open(save_path, 'w') as f:
                f.write(f"{key}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка сохранения ключа: {str(e)}")

    @staticmethod
    def read_key_file(key_path):
        try:
            with open(key_path, 'r') as f:
                return int(f.read().strip())
        except Exception as e:
            QMessageBox.critical(None, "Ошибка", f"Ошибка чтения ключевого файла: {str(e)}")
            return None
