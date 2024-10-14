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
        description_label = QLabel("Выберите способ получения подключей для каждого раунда шифрования:\n"
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
        key_bytes = int.to_bytes(key, length=(key.bit_length() + 7) // 8, byteorder='big')  # Преобразуем ключ в байты
        cipher = FeistelCipher(subkey_method=method, key=key, function_type=function_type)

        file_path, _ = QFileDialog.getOpenFileName(
            self, "Выберите файл для шифрования", "", "Все файлы (*)", options=options
        )
        try:
            if file_path:
                with open(file_path, 'rb') as f:
                    plaintext = f.read()

                bit_position = int(self.bit_position_input.text())  # Получаем позицию бита
                change_target = self.change_target_combo.currentIndex()  # 0 - текст, 1 - ключ

                # Изменяем бит в ключе или тексте
                if change_target == 0:
                    plaintext = self._change_bit(plaintext, bit_position)
                elif change_target == 1:
                    key_bytes = self._change_bit(key_bytes, bit_position)

                save_path, _ = QFileDialog.getSaveFileName(
                    self, "Сохранить зашифрованный файл", file_path + ".enc", "Зашифрованные файлы (*.enc)", options=options
                )
                if save_path:
                    key_save_path, _ = QFileDialog.getSaveFileName(
                        self, "Сохранить ключ", os.path.join(os.path.dirname(save_path), "encryption.key"), "Key files (*.key)",
                        options=options
                    )
                    key_as_int = int.from_bytes(key_bytes, byteorder='big')  # Преобразуем байты обратно в int
                    self.key_ops.save_key_to_file(key_as_int, key_save_path)

                    encrypted_data = cipher.encrypt(plaintext)
                    with open(save_path, 'wb') as f:
                        f.write(encrypted_data)

                    self.test_results.setText(
                        f"Шифрование завершено. Файл сохранен как: {save_path}. Ключ сохранен как: {key_save_path}")

        except Exception as e:
            QMessageBox.warning(self, "Ошибка!", str(e))

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
        byte_index = bit_position // 8
        bit_index = bit_position % 8
        modified_data = bytearray(data)
        modified_data[byte_index] ^= (1 << (7 - bit_index))  # Инвертируем указанный бит
        return bytes(modified_data)
