from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFileDialog, QMessageBox, QLabel, QLineEdit
from lab2.feistel_cipher import FeistelCipher  # Импортируем класс из модуля FeistelCipher

class FeistelEncryptionTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Поле для ввода ключа
        self.key_input = QLineEdit(self)
        self.key_input.setPlaceholderText("Введите ключ (целое число)")
        layout.addWidget(self.key_input)

        # Кнопка для шифрования
        self.encrypt_button = QPushButton("Зашифровать файл", self)
        self.encrypt_button.clicked.connect(self.encrypt)
        layout.addWidget(self.encrypt_button)

        # Кнопка для дешифрования
        self.decrypt_button = QPushButton("Расшифровать файл", self)
        self.decrypt_button.clicked.connect(self.decrypt)
        layout.addWidget(self.decrypt_button)

        # Поле для отображения статуса
        self.test_results = QLabel()
        layout.addWidget(self.test_results)

        self.setLayout(layout)

    def encrypt(self):
        key_text = self.key_input.text()
        if not key_text.isdigit():
            QMessageBox.warning(self, "Ошибка", "Введите целочисленный ключ.")
            return

        key = int(key_text)
        cipher = FeistelCipher()

        # Выбор файла для шифрования
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите файл для шифрования", "", "Все файлы (*)", options=options)
        if not file_path:
            return

        # Чтение исходного файла
        try:
            with open(file_path, 'rb') as f:
                plaintext = f.read()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка чтения файла: {str(e)}")
            return

        # Выбор места и имени для сохранения зашифрованного файла
        save_path, _ = QFileDialog.getSaveFileName(self, "Сохранить зашифрованный файл", file_path + ".enc", "Зашифрованные файлы (*.enc)", options=options)
        if not save_path:
            return

        # Шифрование и сохранение данных
        try:
            encrypted_data = cipher.encrypt(plaintext, key)
            with open(save_path, 'wb') as f:
                f.write(encrypted_data)

            self.test_results.setText(f"Шифрование завершено. Файл сохранен как: {save_path}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка шифрования: {str(e)}")

    def decrypt(self):
        key_text = self.key_input.text()
        if not key_text.isdigit():
            QMessageBox.warning(self, "Ошибка", "Введите целочисленный ключ.")
            return

        key = int(key_text)
        cipher = FeistelCipher()

        # Выбор зашифрованного файла
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите файл для дешифрования", "", "Зашифрованные файлы (*.enc)", options=options)
        if not file_path:
            return

        # Чтение зашифрованного файла
        try:
            with open(file_path, 'rb') as f:
                encrypted_data = f.read()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка чтения файла: {str(e)}")
            return

        # Выбор места и имени для сохранения расшифрованного файла
        save_path, _ = QFileDialog.getSaveFileName(self, "Сохранить расшифрованный файл", file_path.replace(".enc", "_decrypted"), "Все файлы (*)", options=options)
        if not save_path:
            return

        # Дешифрование и сохранение данных
        try:
            decrypted_data = cipher.decrypt(encrypted_data, key)
            with open(save_path, 'wb') as f:
                f.write(decrypted_data)

            self.test_results.setText(f"Дешифрование завершено. Файл сохранен как: {save_path}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка дешифрования: {str(e)}")
