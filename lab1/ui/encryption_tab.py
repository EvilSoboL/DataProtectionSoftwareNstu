from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QComboBox, QFileDialog, QMessageBox, QLabel, QLineEdit
from lab1.encryption import generate_key, encrypt, scramble_encrypt, scramble_decrypt
from lab1.scrambler_tests import (
    calculate_period, chi_squared_test, balance_test, correlation_test
)


class EncryptionTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.create_buttons(layout)
        self.create_scrambler_controls(layout)
        self.create_test_results_display(layout)

        self.setLayout(layout)

    def create_buttons(self, layout):
        self.encrypt_button = QPushButton('Шифровать файл однократным гаммированием')
        self.encrypt_button.clicked.connect(self.encrypt_file)
        layout.addWidget(self.encrypt_button)

        self.decrypt_button = QPushButton('Расшифровать файл однократным гаммированием')
        self.decrypt_button.clicked.connect(self.decrypt_file)
        layout.addWidget(self.decrypt_button)

        self.scramble_encrypt_button = QPushButton('Шифровать файл скремблером')
        self.scramble_encrypt_button.clicked.connect(self.scramble_encrypt_file)
        layout.addWidget(self.scramble_encrypt_button)

        self.scramble_decrypt_button = QPushButton('Расшифровать файл скремблером')
        self.scramble_decrypt_button.clicked.connect(self.scramble_decrypt_file)
        layout.addWidget(self.scramble_decrypt_button)

        self.test_scrambler_button = QPushButton('Тестировать скремблер')
        self.test_scrambler_button.clicked.connect(self.test_scrambler)
        layout.addWidget(self.test_scrambler_button)

    def create_scrambler_controls(self, layout):
        layout.addWidget(QLabel("Выберите скремблер"))
        self.scrambler_selector = QComboBox()
        self.scrambler_selector.addItems(["x^11 + x^5 + x^2 + 1", "x^11 + x^2 + 1"])
        layout.addWidget(self.scrambler_selector)

        layout.addWidget(QLabel("Начальное значение скремблера (IV):"))
        self.scrambler_iv_input = QLineEdit('00000000001')
        layout.addWidget(self.scrambler_iv_input)

    def create_test_results_display(self, layout):
        self.test_results = QLabel()
        layout.addWidget(self.test_results)

    def encrypt_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Выберите файл для шифрования', '', 'All Files (*)')
        if not file_path:
            return

        enc_file_path, _ = QFileDialog.getSaveFileName(self, 'Сохранить зашифрованный файл', '',
                                                       'Encrypted Files (*.enc)')
        if not enc_file_path:
            return

        key_file_path, _ = QFileDialog.getSaveFileName(self, 'Сохранить ключ', '', 'Key Files (*.key)')
        if not key_file_path:
            return

        data = self.read_file(file_path)
        key = generate_key(len(data))
        encrypted_data = encrypt(data, key)

        self.write_file(enc_file_path, encrypted_data)
        self.write_file(key_file_path, key)

        QMessageBox.information(self, "Успех", "Файл успешно зашифрован однократным гаммированием.")

    def decrypt_file(self):
        enc_file_path, _ = QFileDialog.getOpenFileName(self, 'Выберите зашифрованный файл', '',
                                                       'Encrypted Files (*.enc)')
        if not enc_file_path:
            return

        key_file_path, _ = QFileDialog.getOpenFileName(self, 'Выберите файл ключа', '', 'Key Files (*.key)')
        if not key_file_path:
            return

        dec_file_path, _ = QFileDialog.getSaveFileName(self, 'Сохранить расшифрованный файл', '', 'All Files (*)')
        if not dec_file_path:
            return

        encrypted_data = self.read_file(enc_file_path)
        key = self.read_file(key_file_path)

        if len(key) != len(encrypted_data):
            QMessageBox.warning(self, "Ошибка", "Длина ключа не соответствует длине зашифрованных данных.")
            return

        decrypted_data = encrypt(encrypted_data, key)
        self.write_file(dec_file_path, decrypted_data)

        QMessageBox.information(self, "Успех", "Файл успешно расшифрован.")

    def scramble_encrypt_file(self):
        scrambler_type = self.scrambler_selector.currentText()
        scrambler_iv = self.scrambler_iv_input.text()

        if not self.validate_iv(scrambler_iv):
            return

        file_path, _ = QFileDialog.getOpenFileName(self, 'Выберите файл для шифрования', '', 'All Files (*)')
        if not file_path:
            return

        enc_file_path, _ = QFileDialog.getSaveFileName(self, 'Сохранить зашифрованный файл', '',
                                                       'Encrypted Files (*.enc)')
        if not enc_file_path:
            return

        try:
            data = self.read_file(file_path)
            encrypted_data = scramble_encrypt(data, scrambler_type, scrambler_iv)
            self.write_file(enc_file_path, encrypted_data)
            QMessageBox.information(self, "Успех", "Файл успешно зашифрован скремблером.")
        except ValueError as e:
            QMessageBox.warning(self, "Ошибка", str(e))

    def scramble_decrypt_file(self):
        scrambler_type = self.scrambler_selector.currentText()
        scrambler_iv = self.scrambler_iv_input.text()

        if not self.validate_iv(scrambler_iv):
            return

        enc_file_path, _ = QFileDialog.getOpenFileName(self, 'Выберите зашифрованный файл', '',
                                                       'Encrypted Files (*.enc)')
        if not enc_file_path:
            return

        dec_file_path, _ = QFileDialog.getSaveFileName(self, 'Сохранить расшифрованный файл', '', 'All Files (*)')
        if not dec_file_path:
            return

        try:
            encrypted_data = self.read_file(enc_file_path)
            decrypted_data = scramble_decrypt(encrypted_data, scrambler_type, scrambler_iv)
            self.write_file(dec_file_path, decrypted_data)
            QMessageBox.information(self, "Успех", "Файл успешно расшифрован скремблером.")
        except ValueError as e:
            QMessageBox.warning(self, "Ошибка", str(e))

    def test_scrambler(self):
        scrambler_type = self.scrambler_selector.currentText()
        scrambler_iv = self.scrambler_iv_input.text()

        if not self.validate_iv(scrambler_iv):
            return

        test_length = 1000
        try:
            test_sequence = scramble_encrypt(b'\x00' * (test_length // 8), scrambler_type, scrambler_iv)
            test_sequence_bits = ''.join(f'{byte:08b}' for byte in test_sequence)

            period = calculate_period(test_sequence_bits)
            chi_squared = chi_squared_test(test_sequence_bits)
            balance = balance_test(test_sequence_bits)
            correlation = correlation_test(test_sequence_bits)

            results = (
                f"Период скремблера: {period}\n"
                f"Критерий хи^2: {chi_squared}\n"
                f"Сбалансированность: {balance}\n"
                f"Корреляция: {correlation}\n"
            )

            self.test_results.setText(results)
        except ValueError as e:
            QMessageBox.warning(self, "Ошибка", str(e))

    def read_file(self, file_path):
        with open(file_path, 'rb') as file:
            return file.read()

    def write_file(self, file_path, data):
        with open(file_path, 'wb') as file:
            file.write(data)

    def validate_iv(self, iv):
        required_iv_length = 11
        if len(iv) != required_iv_length:
            QMessageBox.warning(self, "Ошибка",
                                f"Начальное значение скремблера должно быть {required_iv_length} символов.")
            return False
        return True

