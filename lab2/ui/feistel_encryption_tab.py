from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QComboBox, QFileDialog, QMessageBox, QLineEdit
from lab2.utils.file_operations import FileOperations
from lab2.utils.key_operations import KeyOperations
from lab2.feistel_cipher import FeistelCipher
import os


class FeistelEncryptionTab(QWidget):
    def __init__(self):
        super().__init__()
        self.file_ops = FileOperations()
        self.key_ops = KeyOperations()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.bit_position_input = QLineEdit(self)
        self.bit_position_input.setPlaceholderText("Введите позицию изменяемого бита")
        layout.addWidget(self.bit_position_input)

        self.change_target_combo = QComboBox()
        self.change_target_combo.addItem("Изменить бит в открытом тексте", 0)
        self.change_target_combo.addItem("Изменить бит в ключе", 1)
        layout.addWidget(self.change_target_combo)

        # Описание методов получения подключей
        description_label = QLabel(
            "Выберите способ получения подключей для каждого раунда шифрования:\n"
            "Способ A: Цепочка из 32 бит, которая начинается с i-го бита ключа и циклически повторяется.\n"
            "Способ B: Цепочка из 8 бит используется как начальное значение для скремблера, который генерирует 32-битный подключ.")
        layout.addWidget(description_label)

        # Комбобокс для выбора способа получения подключей
        self.subkey_method_combo = QComboBox()
        self.subkey_method_combo.addItem("Способ A: Циклическая цепочка из 32 бит", 0)
        self.subkey_method_combo.addItem("Способ B: Скремблер из 8 бит", 1)
        layout.addWidget(self.subkey_method_combo)

        # Комбобокс для выбора функции F
        self.function_combo = QComboBox()
        self.function_combo.addItem("Единичная функция F(Vi) = Vi", 0)
        self.function_combo.addItem("Функция F(Vi, X) = S(X) XOR Vi", 1)
        layout.addWidget(self.function_combo)

        self.test_results = QLabel()
        layout.addWidget(self.test_results)

        # Кнопка для шифрования файла
        self.encrypt_button = QPushButton('Зашифровать файл')
        self.encrypt_button.clicked.connect(self.encrypt)
        layout.addWidget(self.encrypt_button)

        # Кнопка для расшифровки файла
        self.decrypt_button = QPushButton('Расшифровать файл')
        self.decrypt_button.clicked.connect(self.decrypt)
        layout.addWidget(self.decrypt_button)

        self.setLayout(layout)

    def encrypt(self):
        options = QFileDialog.Options()
        method = self.subkey_method_combo.currentIndex()  # 0 для метода A, 1 для метода B
        function_type = self.function_combo.currentIndex()  # 0 для единичной функции, 1 для функции F с X
        key = self.key_ops.generate_random_key()

        cipher = FeistelCipher(subkey_method=method, key=key, function_type=function_type)

        file_path, _ = QFileDialog.getOpenFileName(
            self, "Выберите файл для шифрования", "", "Файлы сообщений (*.txt)", options=options
        )
        if not file_path:
            return

        try:
            with open(file_path, 'rb') as f:
                plaintext = f.read()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка чтения файла: {str(e)}")
            return

        bit_position = int(self.bit_position_input.text())  # Получаем позицию бита
        change_target = self.change_target_combo.currentIndex()  # 0 - текст, 1 - ключ

        # Изменяем бит в ключе или тексте
        if change_target == 0:
            # Проверяем, что позиция бита находится в допустимых пределах для текста
            if bit_position >= len(plaintext) * 8:
                QMessageBox.warning(self, "Ошибка", "Позиция бита выходит за пределы длины текста.")
            plaintext = self._change_bit(plaintext, bit_position)

        if change_target == 1:
            if bit_position >= len(key):
                QMessageBox.warning(self, "Ошибка", "Позиция бита выходит за пределы длины ключа.")
            key = self._change_bit(key, bit_position)

        save_path, _ = QFileDialog.getSaveFileName(
            self, "Сохранить зашифрованный файл", file_path + ".enc", "Зашифрованные файлы (*.enc)", options=options
        )
        if not save_path:
            return

        key_save_path, _ = QFileDialog.getSaveFileName(
            self, "Сохранить ключ", os.path.join(os.path.dirname(save_path), "encryption.key"), "Key files (*.key)",
            options=options
        )
        if not key_save_path:
            return

        try:
            self.key_ops.save_key_to_file(key, key_save_path)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ключ не сохранен: {str(e)}")

        try:
            encrypted_data = cipher.encrypt(plaintext)
            with open(save_path, 'wb') as f:
                f.write(encrypted_data)

            self.test_results.setText(
                f"Шифрование завершено. Файл сохранен как: {save_path}. Ключ сохранен как: {key_save_path}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка шифрования: {str(e)}")

    def decrypt(self):
        method = self.subkey_method_combo.currentIndex()  # 0 для метода A, 1 для метода B
        function_type = self.function_combo.currentIndex()  # 0 для единичной функции, 1 для функции F с X

        key_path = self.file_ops.get_open_file("Выберите ключевой файл")
        if not key_path:
            return

        key = self.key_ops.read_key_file(key_path)
        if key is None:
            return

        cipher = FeistelCipher(subkey_method=method, key=key, function_type=function_type)

        file_path = self.file_ops.get_open_file("Выберите файл для дешифрования")
        if not file_path:
            return

        encrypted_data = self.file_ops.read_file(file_path)
        if encrypted_data is None:
            return

        save_path = self.file_ops.get_save_file("Сохранить расшифрованный файл", file_path.replace(".enc", "_decrypted"))
        if not save_path:
            return

        try:
            decrypted_data = cipher.decrypt(encrypted_data)
            self.file_ops.write_file(save_path, decrypted_data)

            self.test_results.setText(f"Дешифрование завершено. Файл сохранен как: {save_path}")
        except Exception as e:
            self.file_ops.show_error("Ошибка дешифрования", str(e))

    def _change_bit(self, data: bytes, bit_position: int) -> bytes:
        # Преобразуем данные в целое число
        data_as_int = int.from_bytes(data, byteorder='big')

        data_as_int ^= (1 << bit_position)

        # Преобразуем данные обратно в байты, длина должна остаться прежней
        return data_as_int.to_bytes(len(data), byteorder='big')
