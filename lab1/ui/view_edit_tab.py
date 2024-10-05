from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel,
    QComboBox, QTextEdit, QMessageBox
)
from lab1.binary_converter import bytes_to_binary, binary_to_bytes
from lab1.validators import validate_binary, validate_hexadecimal


class ViewEditTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        format_selector = ["Двоичный", "Шестнадцатеричный", "Символьный"]

        # Окно редактирование ключа
        layout.addWidget(QLabel("Редактирование ключа"))
        self.load_key_button = QPushButton('Открыть и редактировать ключ')
        self.load_key_button.clicked.connect(lambda: None)
        layout.addWidget(self.load_key_button)

        self.key_format_selector = QComboBox()
        self.key_format_selector.addItems(format_selector)
        layout.addWidget(self.key_format_selector)

        self.key_editor = QTextEdit()
        layout.addWidget(self.key_editor)

        self.save_key_button = QPushButton('Сохранить ключ')
        self.save_key_button.clicked.connect(lambda: None)
        layout.addWidget(self.save_key_button)

        # Окно редактирования исходного сообщения
        layout.addWidget(QLabel("Редактирование исходного сообщения"))
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

        # Окно редактирования зашифрованного сообщения
        layout.addWidget(QLabel("Редактирование зашифрованного сообщения"))
        self.load_encrypted_button = QPushButton('Открыть и редактировать зашифрованное сообщение')
        self.load_encrypted_button.clicked.connect(lambda: None)
        layout.addWidget(self.load_encrypted_button)

        self.encrypted_format_selector = QComboBox()
        self.encrypted_format_selector.addItems(format_selector)
        layout.addWidget(self.encrypted_format_selector)

        self.encrypted_editor = QTextEdit()
        layout.addWidget(self.encrypted_editor)

        self.save_encrypted_button = QPushButton('Сохранить зашифрованное сообщение')
        self.save_encrypted_button.clicked.connect(lambda: None)
        layout.addWidget(self.save_encrypted_button)

        self.setLayout(layout)

    def load_message(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(self, 'Открыть исходное сообщение', '', 'Text Files (*.txt)')
        if file_path:
            with open(file_path, 'rb') as file:
                message = file.read()

            format_type = self.message_format_selector.currentText()
            self.display_data_in_editor(message, format_type, self.message_editor)

    @staticmethod
    def display_data_in_editor(data: bytes, format_type: str, editor: QTextEdit) -> None:
        if format_type == "Двоичный":
            editor.setPlainText(bytes_to_binary(data))

        elif format_type == "Шестнадцатеричный":
            editor.setPlainText(data.hex())

        elif format_type == "Символьный":
            editor.setPlainText(data.decode('windows-1251'))

    def save_message(self) -> None:
        format_type = self.message_format_selector.currentText()
        self.save_data_from_editor(self.message_editor, format_type, 'Text Files (*.txt)')

    def save_data_from_editor(self, editor: QTextEdit, format_type: str, file_filter: str) -> None:
        data = editor.toPlainText().strip()

        if format_type == "Двоичный":
            if not validate_binary(data):
                raise ValueError("Некорректный двоичный формат!")
            data_in_bytes = binary_to_bytes(data)

        elif format_type == "Шестнадцатеричный":
            if not validate_hexadecimal(data):
                raise ValueError('Некорректный шестнадцатеричный формат!')
            data_in_bytes = bytes.fromhex(data)

        elif format_type == "Символьный":
            data_in_bytes = bytes(data, 'windows-1251')

        file_path, _ = QFileDialog.getSaveFileName(self, f'Сохранить {file_filter}', '', file_filter)
        if file_path:
            with open(file_path, 'wb') as file:
                file.write(data_in_bytes)
                QMessageBox.information(self, "Успех", "Файл успешно сохранён.")
