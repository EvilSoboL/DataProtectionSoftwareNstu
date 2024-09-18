from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel,
    QComboBox, QTextEdit, QMessageBox
)
from lab1.validators import validate_binary, validate_hexadecimal
from lab1.utils import (
    bytes_to_binary, bytes_to_hex, bytes_to_text,
    binary_to_bytes, hex_to_bytes, text_to_bytes
)
import os


class ViewEditTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        self.original_lengths = {
            'key': 0,
            'message.txt': 0,
            'encrypted': 0
        }

    def initUI(self):
        layout = QVBoxLayout()

        # Ключ
        layout.addWidget(QLabel("Ключ"))
        self.load_key_button = QPushButton('Открыть и редактировать ключ')
        self.load_key_button.clicked.connect(self.load_key)
        layout.addWidget(self.load_key_button)

        self.key_format_selector = QComboBox()
        self.key_format_selector.addItems(["Двоичный", "Шестнадцатеричный", "Символьный"])
        layout.addWidget(self.key_format_selector)

        self.key_editor = QTextEdit()
        layout.addWidget(self.key_editor)

        self.save_key_button = QPushButton('Сохранить ключ')
        self.save_key_button.clicked.connect(self.save_key)
        layout.addWidget(self.save_key_button)

        # Исходное сообщение
        layout.addWidget(QLabel("Исходное сообщение"))
        self.load_message_button = QPushButton('Открыть и редактировать исходное сообщение')
        self.load_message_button.clicked.connect(self.load_message)
        layout.addWidget(self.load_message_button)

        self.message_format_selector = QComboBox()
        self.message_format_selector.addItems(["Двоичный", "Шестнадцатеричный", "Символьный"])
        layout.addWidget(self.message_format_selector)

        self.message_editor = QTextEdit()
        layout.addWidget(self.message_editor)

        self.save_message_button = QPushButton('Сохранить исходное сообщение')
        self.save_message_button.clicked.connect(self.save_message)
        layout.addWidget(self.save_message_button)

        # Зашифрованное сообщение
        layout.addWidget(QLabel("Зашифрованное сообщение"))
        self.load_encrypted_button = QPushButton('Открыть и редактировать зашифрованное сообщение')
        self.load_encrypted_button.clicked.connect(self.load_encrypted_message)
        layout.addWidget(self.load_encrypted_button)

        self.encrypted_format_selector = QComboBox()
        self.encrypted_format_selector.addItems(["Двоичный", "Шестнадцатеричный", "Символьный"])
        layout.addWidget(self.encrypted_format_selector)

        self.encrypted_editor = QTextEdit()
        layout.addWidget(self.encrypted_editor)

        self.save_encrypted_button = QPushButton('Сохранить зашифрованное сообщение')
        self.save_encrypted_button.clicked.connect(self.save_encrypted_message)
        layout.addWidget(self.save_encrypted_button)

        self.setLayout(layout)

    def display_data_in_editor(self, data, format_type, editor):
        if format_type == "Двоичный":
            editor.setPlainText(bytes_to_binary(data))
        elif format_type == "Шестнадцатеричный":
            editor.setPlainText(bytes_to_hex(data))
        elif format_type == "Символьный":
            editor.setPlainText(bytes_to_text(data))

    def load_key(self):
        key_file_path, _ = QFileDialog.getOpenFileName(self, 'Открыть файл ключа', '', 'Key Files (*.key)')
        if key_file_path:
            with open(key_file_path, 'rb') as key_file:
                self.key_data = key_file.read()
            format_type = self.key_format_selector.currentText()
            self.display_data_in_editor(self.key_data, format_type, self.key_editor)
            self.original_lengths['key'] = len(self.key_data)

    def save_key(self):
        if self.check_length(self.key_editor.toPlainText().strip(), 'key'):
            self.save_data_from_editor(self.key_editor, self.key_format_selector.currentText(), 'Key Files (*.key)')

    def load_message(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Открыть исходное сообщение', '', 'Text Files (*.txt)')
        if file_path:
            with open(file_path, 'rb') as file:
                self.message_data = file.read()
            format_type = self.message_format_selector.currentText()
            self.display_data_in_editor(self.message_data, format_type, self.message_editor)
            self.original_lengths['message.txt'] = len(self.message_data)

    def save_message(self):
        self.save_data_from_editor(self.message_editor, self.message_format_selector.currentText(),
                                   'Text Files (*.txt)')

    def load_encrypted_message(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Открыть зашифрованное сообщение', '',
                                                   'Encrypted Files (*.enc)')
        if file_path:
            with open(file_path, 'rb') as file:
                self.encrypted_data = file.read()
            format_type = self.encrypted_format_selector.currentText()
            self.display_data_in_editor(self.encrypted_data, format_type, self.encrypted_editor)
            self.original_lengths['encrypted'] = len(self.encrypted_data)

    def save_encrypted_message(self):
        if self.check_length(self.encrypted_editor.toPlainText().strip(), 'encrypted'):
            self.save_data_from_editor(self.encrypted_editor, self.encrypted_format_selector.currentText(),
                                       'Encrypted Files (*.enc)')

    def check_length(self, data, data_type):
        try:
            if data_type == 'key':
                expected_length = self.original_lengths['key']
                if self.key_format_selector.currentText() == "Двоичный":
                    data_length = len(binary_to_bytes(data))
                elif self.key_format_selector.currentText() == "Шестнадцатеричный":
                    data_length = len(hex_to_bytes(data))
                else:
                    data_length = len(data.encode('windows-1251'))
            elif data_type == 'encrypted':
                expected_length = self.original_lengths['encrypted']
                if self.encrypted_format_selector.currentText() == "Двоичный":
                    data_length = len(binary_to_bytes(data))
                elif self.encrypted_format_selector.currentText() == "Шестнадцатеричный":
                    data_length = len(hex_to_bytes(data))
                else:
                    data_length = len(data.encode('windows-1251'))
            else:
                return True  # Исходное сообщение не проверяется

            # Проверка длины данных
            if data_length != expected_length:
                raise ValueError(f"Длина данных ({data_length}) не соответствует исходной длине ({expected_length}).")
            return True
        except ValueError as ve:
            QMessageBox.warning(self, "Ошибка", str(ve))
            return False

    def save_data_from_editor(self, editor, format_type, file_filter):
        data = editor.toPlainText().strip()
        try:
            if format_type == "Двоичный":
                if not validate_binary(data):
                    raise ValueError("Некорректный двоичный формат.")
                data_bytes = binary_to_bytes(data)
            elif format_type == "Шестнадцатеричный":
                if not validate_hexadecimal(data):
                    raise ValueError("Некорректный шестнадцатеричный формат.")
                data_bytes = hex_to_bytes(data)
            elif format_type == "Символьный":
                data_bytes = text_to_bytes(data)  # Преобразование символьного представления в байты
            else:
                raise ValueError("Неизвестный формат.")

            file_path, _ = QFileDialog.getSaveFileName(self, f'Сохранить {file_filter}', '', file_filter)
            if file_path:
                with open(file_path, 'wb') as file:
                    file.write(data_bytes)
                QMessageBox.information(self, "Успех", "Файл успешно сохранён.")
        except ValueError as ve:
            QMessageBox.warning(self, "Ошибка", str(ve))

            file_path, _ = QFileDialog.getSaveFileName(self, f'Сохранить {file_filter}', '', file_filter)
            if file_path:
                with open(file_path, 'wb') as file:
                    file.write(data_bytes)
                QMessageBox.information(self, "Успех", "Файл успешно сохранён.")
        except ValueError as ve:
            QMessageBox.warning(self, "Ошибка", str(ve))
