# ui/encryption_tab.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QComboBox, QFileDialog, QMessageBox
from lab1.encryption import generate_key, encrypt, scramble_encrypt
import os

class EncryptionTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Кнопки для шифрования и расшифрования
        self.encrypt_button = QPushButton('Шифровать файл однократным гаммированием')
        self.encrypt_button.clicked.connect(self.encrypt_file)
        layout.addWidget(self.encrypt_button)

        self.decrypt_button = QPushButton('Расшифровать файл однократным гаммированием')
        self.decrypt_button.clicked.connect(self.decrypt_file)
        layout.addWidget(self.decrypt_button)

        # Выбор скремблера
        self.scrambler_selector = QComboBox()
        self.scrambler_selector.addItems(["x^11 + x^5 + x^2 + 1", "x^11 + x^2 + 1"])
        layout.addWidget(self.scrambler_selector)

        self.scramble_encrypt_button = QPushButton('Шифровать скремблером')
        self.scramble_encrypt_button.clicked.connect(self.scramble_encrypt_file)
        layout.addWidget(self.scramble_encrypt_button)

        self.setLayout(layout)

    def encrypt_file(self):
        # Логика для шифрования файла гаммированием
        pass  # Код аналогичен текущему

    def decrypt_file(self):
        # Логика для расшифрования файла гаммированием
        pass  # Код аналогичен текущему

    def scramble_encrypt_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Выберите файл для шифрования', '', 'All Files (*)')
        if not file_path:
            return

        enc_file_path, _ = QFileDialog.getSaveFileName(self, 'Сохранить зашифрованный файл', '', 'Encrypted Files (*.enc)')
        if not enc_file_path:
            return

        scrambler_type = self.scrambler_selector.currentText()

        with open(file_path, 'rb') as f:
            data = f.read()

        encrypted_data = scramble_encrypt(data, scrambler_type)

        with open(enc_file_path, 'wb') as enc_file:
            enc_file.write(encrypted_data)

        QMessageBox.information(self, "Успех", "Файл успешно зашифрован скремблером.")

