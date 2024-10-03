from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel,
    QComboBox, QTextEdit, QMessageBox
)
from lab1.validators import validate_binary, validate_hexadecimal, validate_text
from lab1.converter import (
    bytes_to_binary, bytes_to_hex, bytes_to_text,
    binary_to_bytes, hex_to_bytes, text_to_bytes,
    text_to_binary, text_to_hex
)


class ViewEditTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        self.original_byte_lengths = {
            'key': 0,
            'message.txt': 0,
            'encrypted': 0
        }

    def initUI(self):
        layout = QVBoxLayout()

        format_selector = ["Двоичный", "Шестнадцатеричный", "Символьный"]

        # Редактирование и просмотр ключа
        layout.addWidget(QLabel("Ключ"))
        self.load_key_button = QPushButton('Открыть и редактировать ключ')
        self.load_key_button.clicked.connect(self.load_key)
        layout.addWidget(self.load_key_button)

        self.key_format_selector = QComboBox()
        self.key_format_selector.addItems(format_selector)
        layout.addWidget(self.key_format_selector)

        self.key_editor = QTextEdit()
        layout.addWidget(self.key_editor)

        self.save_key_button = QPushButton('Сохранить ключ')
        self.save_key_button.clicked.connect(self.save_key)
        layout.addWidget(self.save_key_button)

        # Редактирование и просмотр исходного сообщения
        layout.addWidget(QLabel("Исходное сообщение"))
        self.load_message_button = QPushButton('Открыть и редактировать исходное сообщение')
        self.load_message_button.clicked.connect(self.load_message)
        layout.addWidget(self.load_message_button)

        self.message_format_selector = QComboBox()
        self.message_format_selector.addItems(format_selector)
        layout.addWidget(self.message_format_selector)

        self.message_editor = QTextEdit()
        layout.addWidget(self.message_editor)

        self.save_message_button = QPushButton('Сохранить исходное сообщение')
        self.save_message_button.clicked.connect(self.save_message)
        layout.addWidget(self.save_message_button)

        # Редактирование и просмотр зашифрованного сообщения
        layout.addWidget(QLabel("Зашифрованное сообщение"))
        self.load_encrypted_button = QPushButton('Открыть и редактировать зашифрованное сообщение')
        self.load_encrypted_button.clicked.connect(self.load_encrypted_message)
        layout.addWidget(self.load_encrypted_button)

        self.encrypted_format_selector = QComboBox()
        self.encrypted_format_selector.addItems(format_selector)
        layout.addWidget(self.encrypted_format_selector)

        self.encrypted_editor = QTextEdit()
        layout.addWidget(self.encrypted_editor)

        self.save_encrypted_button = QPushButton('Сохранить зашифрованное сообщение')
        self.save_encrypted_button.clicked.connect(self.save_encrypted_message)
        layout.addWidget(self.save_encrypted_button)

        self.setLayout(layout)

    # Открытие ключа, сообщения, зашифрованного сообщения в окне редактирования
    @staticmethod
    def display_data_in_editor(data, format_type, editor):
        if format_type == "Двоичный":
            editor.setPlainText(bytes_to_binary(data))
        elif format_type == "Шестнадцатеричный":
            editor.setPlainText(bytes_to_hex(data))
        elif format_type == "Символьный":
            editor.setPlainText(bytes_to_text(data))

    def load_key(self):
        key_file_path, _ = QFileDialog.getOpenFileName(self, 'Открыть файл ключа', '', 'Key Files (*.key)')
        with open(key_file_path, 'rb') as key_file:
            key = key_file.read()

        format_type = self.key_format_selector.currentText()
        self.display_data_in_editor(key, format_type, self.key_editor)

    def load_message(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Открыть исходное сообщение', '', 'Text Files (*.txt)')
        with open(file_path, 'rb') as file:
            message = file.read()

        format_type = self.message_format_selector.currentText()
        self.display_data_in_editor(message, format_type, self.message_editor)

    def load_encrypted_message(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Открыть зашифрованное сообщение', '', 'Encrypted Files (*.enc)')
        with open(file_path, 'rb') as file:
            encrypted_message = file.read()

        format_type = self.encrypted_format_selector.currentText()
        self.save_original_length(encrypted_message, 'encrypted', format_type)
        self.display_data_in_editor(encrypted_message, format_type, self.encrypted_editor)

    def save_original_length(self, data: bytes | str, data_type: str, format_type: str) -> None:
        if data_type == 'key' and format_type == 'Двоичный':
            self.original_byte_lengths['key'] = len(binary_to_bytes(data))

        elif data_type == 'key' and format_type == 'Шестнадцатеричный':
            self.original_byte_lengths['key'] = len(hex_to_bytes(data))

        elif data_type == 'encrypted' and format_type == 'Двоичный':
            self.original_byte_lengths['encrypted'] = len(binary_to_bytes(data))

        elif data_type == 'encrypted' and format_type == 'Шестнадцатеричный':
            self.original_byte_lengths['encrypted'] = len(hex_to_bytes(data))

    # Сохранение отредактированного ключа, сообщения и зашифрованного сообщения
    def save_data_from_editor(self, editor, format_type, file_filter):
        data = editor.toPlainText().strip()

        if format_type == "Двоичный":
            if validate_binary(data):
                data_bytes = binary_to_bytes(data)
            else:
                raise ValueError("Некорректный двоичный формат.")

        elif format_type == "Шестнадцатеричный":
            if validate_hexadecimal(data):
                data_bytes = hex_to_bytes(data)
            else:
                raise ValueError("Некорректный шестнадцатеричный формат.")

        elif format_type == "Символьный":
            if validate_text(data):
                data_bytes = text_to_bytes(data)
            else:
                raise ValueError("Некорректный формат windows-1251.")

        file_path, _ = QFileDialog.getSaveFileName(self, f'Сохранить {file_filter}', '', file_filter)
        with open(file_path, 'wb') as file:
            file.write(data_bytes)
        QMessageBox.information(self, "Успех", "Файл успешно сохранён.")

    # Сохранение ключа, сообщения и зашифрованного сообщения
    def check_length(self, data, data_type) -> bool:
        if data_type == 'key':
            expected_length = self.original_byte_lengths['key']
            if self.key_format_selector.currentText() == "Двоичный":
                data_length = len(binary_to_bytes(data))
            elif self.key_format_selector.currentText() == "Шестнадцатеричный":
                data_length = len(hex_to_bytes(data))
            else:
                data_length = len(data.encode('windows-1251'))

        elif data_type == 'encrypted':
            expected_length = self.original_byte_lengths['encrypted']

            if self.encrypted_format_selector.currentText() == "Двоичный":
                data_length = len(binary_to_bytes(data))

            elif self.encrypted_format_selector.currentText() == "Шестнадцатеричный":
                data_length = len(hex_to_bytes(data))

            else:
                data_length = len(data.encode('windows-1251'))

        # Проверка длины данных
        if data_length != expected_length:
            raise ValueError(f"Длина данных ({data_length}) не соответствует исходной длине ({expected_length}).")
        else:
            return True

    def save_key(self):
        data = self.key_editor.toPlainText().strip()
        if self.check_length(data, data_type='key'):
            self.save_data_from_editor(self.key_editor, self.key_format_selector.currentText(), 'Key Files (*.key)')
        else:
            QMessageBox.warning(self, "Ошибка")
            raise ValueError(f"Длина данных!")

    def save_message(self):
        self.save_data_from_editor(self.message_editor, self.message_format_selector.currentText(), 'Text Files (*.txt)')

    def save_encrypted_message(self):
        data = self.encrypted_editor.toPlainText().strip()
        if self.check_length(data, 'encrypted'):
            self.save_data_from_editor(self.encrypted_editor, self.encrypted_format_selector.currentText(), 'Encrypted Files (*.enc)')


