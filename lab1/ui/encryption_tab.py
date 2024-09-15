from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QComboBox, QFileDialog, QMessageBox, QLabel, QLineEdit
from lab1.encryption import generate_key, encrypt, scramble_encrypt, scramble_decrypt
import os

class EncryptionTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Кнопки для шифрования и расшифрования однократным гаммированием
        self.encrypt_button = QPushButton('Шифровать файл однократным гаммированием')
        self.encrypt_button.clicked.connect(self.encrypt_file)
        layout.addWidget(self.encrypt_button)

        self.decrypt_button = QPushButton('Расшифровать файл однократным гаммированием')
        self.decrypt_button.clicked.connect(self.decrypt_file)
        layout.addWidget(self.decrypt_button)

        # Выбор скремблера
        layout.addWidget(QLabel("Выберите скремблер"))
        self.scrambler_selector = QComboBox()
        self.scrambler_selector.addItems(["x^11 + x^5 + x^2 + 1", "x^11 + x^2 + 1"])
        layout.addWidget(self.scrambler_selector)

        # Поле для ввода начального значения скремблера
        layout.addWidget(QLabel("Начальное значение скремблера (IV):"))
        self.scrambler_iv_input = QLineEdit()
        self.scrambler_iv_input.setText('00000000001')  # Значение по умолчанию
        layout.addWidget(self.scrambler_iv_input)

        # Кнопка для шифрования скремблером
        self.scramble_encrypt_button = QPushButton('Шифровать файл скремблером')
        self.scramble_encrypt_button.clicked.connect(self.scramble_encrypt_file)
        layout.addWidget(self.scramble_encrypt_button)

        # Кнопка для расшифровки скремблером
        self.scramble_decrypt_button = QPushButton('Расшифровать файл скремблером')
        self.scramble_decrypt_button.clicked.connect(self.scramble_decrypt_file)
        layout.addWidget(self.scramble_decrypt_button)

        self.setLayout(layout)

    def encrypt_file(self):
        # Логика для шифрования файла однократным гаммированием
        file_path, _ = QFileDialog.getOpenFileName(self, 'Выберите файл для шифрования', '', 'All Files (*)')
        if not file_path:
            return

        enc_file_path, _ = QFileDialog.getSaveFileName(self, 'Сохранить зашифрованный файл', '', 'Encrypted Files (*.enc)')
        if not enc_file_path:
            return

        key_file_path, _ = QFileDialog.getSaveFileName(self, 'Сохранить ключ', '', 'Key Files (*.key)')
        if not key_file_path:
            return

        # Чтение данных
        with open(file_path, 'rb') as f:
            data = f.read()

        key = generate_key(len(data))
        encrypted_data = encrypt(data, key)

        with open(enc_file_path, 'wb') as enc_file:
            enc_file.write(encrypted_data)
        with open(key_file_path, 'wb') as key_file:
            key_file.write(key)

        QMessageBox.information(self, "Успех", "Файл успешно зашифрован однократным гаммированием.")

    def decrypt_file(self):
        # Логика для расшифрования файла однократным гаммированием
        enc_file_path, _ = QFileDialog.getOpenFileName(self, 'Выберите зашифрованный файл', '', 'Encrypted Files (*.enc)')
        if not enc_file_path:
            return

        key_file_path, _ = QFileDialog.getOpenFileName(self, 'Выберите файл ключа', '', 'Key Files (*.key)')
        if not key_file_path:
            return

        dec_file_path, _ = QFileDialog.getSaveFileName(self, 'Сохранить расшифрованный файл', '', 'All Files (*)')
        if not dec_file_path:
            return

        with open(enc_file_path, 'rb') as enc_file:
            encrypted_data = enc_file.read()
        with open(key_file_path, 'rb') as key_file:
            key = key_file.read()

        if len(key) != len(encrypted_data):
            QMessageBox.warning(self, "Ошибка", "Длина ключа не соответствует длине зашифрованных данных.")
            return

        decrypted_data = encrypt(encrypted_data, key)

        with open(dec_file_path, 'wb') as dec_file:
            dec_file.write(decrypted_data)

        QMessageBox.information(self, "Успех", "Файл успешно расшифрован.")

    def scramble_encrypt_file(self):
        scrambler_type = self.scrambler_selector.currentText()
        scrambler_iv = self.scrambler_iv_input.text()

        # Проверка длины начального значения (IV) в битах
        required_iv_length = 11  # Ожидаем 11 бит для обоих полиномов
        if len(scrambler_iv) != required_iv_length:
            QMessageBox.warning(self, "Ошибка", f"Начальное значение скремблера должно быть {required_iv_length} символов.")
            return

        file_path, _ = QFileDialog.getOpenFileName(self, 'Выберите файл для шифрования', '', 'All Files (*)')
        if not file_path:
            return

        enc_file_path, _ = QFileDialog.getSaveFileName(self, 'Сохранить зашифрованный файл', '', 'Encrypted Files (*.enc)')
        if not enc_file_path:
            return

        try:
            with open(file_path, 'rb') as f:
                data = f.read()

            encrypted_data = scramble_encrypt(data, scrambler_type, scrambler_iv)

            with open(enc_file_path, 'wb') as enc_file:
                enc_file.write(encrypted_data)

            QMessageBox.information(self, "Успех", "Файл успешно зашифрован скремблером.")
        except ValueError as e:
            QMessageBox.warning(self, "Ошибка", str(e))

    def scramble_decrypt_file(self):
        scrambler_type = self.scrambler_selector.currentText()
        scrambler_iv = self.scrambler_iv_input.text()

        # Проверка длины начального значения (IV) в битах
        required_iv_length = 11  # Ожидаем 11 бит для обоих полиномов
        if len(scrambler_iv) != required_iv_length:
            QMessageBox.warning(self, "Ошибка", f"Начальное значение скремблера должно быть {required_iv_length} символов.")
            return

        enc_file_path, _ = QFileDialog.getOpenFileName(self, 'Выберите зашифрованный файл', '', 'Encrypted Files (*.enc)')
        if not enc_file_path:
            return

        dec_file_path, _ = QFileDialog.getSaveFileName(self, 'Сохранить расшифрованный файл', '', 'All Files (*)')
        if not dec_file_path:
            return

        try:
            with open(enc_file_path, 'rb') as enc_file:
                encrypted_data = enc_file.read()

            decrypted_data = scramble_decrypt(encrypted_data, scrambler_type, scrambler_iv)

            with open(dec_file_path, 'wb') as dec_file:
                dec_file.write(decrypted_data)

            QMessageBox.information(self, "Успех", "Файл успешно расшифрован скремблером.")
        except ValueError as e:
            QMessageBox.warning(self, "Ошибка", str(e))


