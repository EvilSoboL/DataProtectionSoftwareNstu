from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTabWidget, QLabel, QPushButton, QFileDialog, QMessageBox
)
from lab1.ui.view_edit_tab import ViewEditTab
from lab1.encryption import generate_key, encrypt
import os


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Создание вкладок
        self.tabs = QTabWidget()

        # Первая вкладка: Просмотр и изменение
        self.view_edit_tab = ViewEditTab()
        self.tabs.addTab(self.view_edit_tab, "Просмотр и изменение")

        # Вторая вкладка: шифрование/расшифрование
        self.other_tab = QWidget()
        other_layout = QVBoxLayout()

        self.encrypt_button = QPushButton('Шифровать файл однократным гаммированием')
        self.encrypt_button.clicked.connect(self.encrypt_file)
        other_layout.addWidget(self.encrypt_button)

        self.decrypt_button = QPushButton('Расшифровать файл однократным гаммированием')
        self.decrypt_button.clicked.connect(self.decrypt_file)
        other_layout.addWidget(self.decrypt_button)

        self.other_tab.setLayout(other_layout)
        self.tabs.addTab(self.other_tab, "Шифрование/Расшифрование")

        layout.addWidget(self.tabs)
        self.setLayout(layout)
        self.setWindowTitle('Шифрование')

    def encrypt_file(self):
        # Выбор файла для шифрования
        file_path, _ = QFileDialog.getOpenFileName(self, 'Выберите файл для шифрования', '', 'All Files (*)')
        if not file_path:
            return

        # Выбор места сохранения зашифрованного файла
        enc_file_path, _ = QFileDialog.getSaveFileName(self, 'Сохранить зашифрованный файл', '', 'Encrypted Files (*.enc)')
        if not enc_file_path:
            return

        # Выбор места сохранения ключа
        key_file_path, _ = QFileDialog.getSaveFileName(self, 'Сохранить ключ', '', 'Key Files (*.key)')
        if not key_file_path:
            return

        # Чтение исходных данных
        with open(file_path, 'rb') as f:
            data = f.read()

        # Генерация ключа
        key = generate_key(len(data))

        # Шифрование данных
        encrypted_data = encrypt(data, key)

        # Сохранение зашифрованных данных и ключа
        with open(enc_file_path, 'wb') as enc_file:
            enc_file.write(encrypted_data)
        with open(key_file_path, 'wb') as key_file:
            key_file.write(key)

        QMessageBox.information(self, "Успех", "Файл успешно зашифрован.")

    def decrypt_file(self):
        # Выбор зашифрованного файла
        enc_file_path, _ = QFileDialog.getOpenFileName(self, 'Выберите зашифрованный файл', '', 'Encrypted Files (*.enc)')
        if not enc_file_path:
            return

        # Выбор ключа
        key_file_path, _ = QFileDialog.getOpenFileName(self, 'Выберите файл ключа', '', 'Key Files (*.key)')
        if not key_file_path:
            return

        # Выбор места сохранения расшифрованного файла
        dec_file_path, _ = QFileDialog.getSaveFileName(self, 'Сохранить расшифрованный файл', '', 'All Files (*)')
        if not dec_file_path:
            return

        # Чтение зашифрованных данных и ключа
        with open(enc_file_path, 'rb') as enc_file:
            encrypted_data = enc_file.read()
        with open(key_file_path, 'rb') as key_file:
            key = key_file.read()

        # Проверка длины ключа
        if len(key) != len(encrypted_data):
            QMessageBox.warning(self, "Ошибка", "Длина ключа не соответствует длине зашифрованных данных.")
            return

        # Расшифровка данных
        decrypted_data = encrypt(encrypted_data, key)

        # Сохранение расшифрованных данных
        with open(dec_file_path, 'wb') as dec_file:
            dec_file.write(decrypted_data)

        QMessageBox.information(self, "Успех", "Файл успешно расшифрован.")
