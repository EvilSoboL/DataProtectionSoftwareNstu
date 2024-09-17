from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel,
    QComboBox, QTextEdit, QMessageBox
)
from lab1.validators import validate_binary, validate_hexadecimal
from lab1.utils import (
    bytes_to_binary, bytes_to_hex, bytes_to_text,
    binary_to_bytes, hex_to_bytes, text_to_bytes
)


class ViewEditTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        self.original_lengths = {'key': 0, 'message': 0, 'encrypted': 0}

    def initUI(self):
        layout = QVBoxLayout()

        # Ключ
        layout.addWidget(QLabel("Ключ"))
        self.key_editor = self.create_editor('Открыть и редактировать ключ', 'Сохранить ключ')
        layout.addWidget(self.key_editor)

        # Исходное сообщение
        layout.addWidget(QLabel("Исходное сообщение"))
        self.message_editor = self.create_editor('Открыть и редактировать исходное сообщение', 'Сохранить исходное сообщение')
        layout.addWidget(self.message_editor)

        # Зашифрованное сообщение
        layout.addWidget(QLabel("Зашифрованное сообщение"))
        self.encrypted_editor = self.create_editor('Открыть и редактировать зашифрованное сообщение', 'Сохранить зашифрованное сообщение')
        layout.addWidget(self.encrypted_editor)

        self.setLayout(layout)

    def create_editor(self, load_text, save_text):
        button_layout = QVBoxLayout()
        load_button = QPushButton(load_text)
        load_button.clicked.connect(lambda: self.load_data(load_button.text(), self.get_editor(load_text)))
        button_layout.addWidget(load_button)

        format_selector = QComboBox()
        format_selector.addItems(["Двоичный", "Шестнадцатеричный", "Символьный"])
        button_layout.addWidget(format_selector)

        editor = QTextEdit()
        button_layout.addWidget(editor)

        save_button = QPushButton(save_text)
        save_button.clicked.connect(lambda: self.save_data(editor, format_selector.currentText(), save_text))
        button_layout.addWidget(save_button)

        container = QWidget()
        container.setLayout(button_layout)
        return container

    def get_editor(self, text):
        if "ключ" in text:
            return self.key_editor
        elif "исходное сообщение" in text:
            return self.message_editor
        elif "зашифрованное сообщение" in text:
            return self.encrypted_editor

    def load_data(self, button_text, editor):
        file_filters = {
            'Открыть и редактировать ключ': 'Key Files (*.key)',
            'Открыть и редактировать исходное сообщение': 'Text Files (*.txt)',
            'Открыть и редактировать зашифрованное сообщение': 'Encrypted Files (*.enc)'
        }
        file_path, _ = QFileDialog.getOpenFileName(self, f'Открыть {button_text}', '', file_filters[button_text])
        if file_path:
            with open(file_path, 'rb') as file:
                data = file.read()
            format_type = self.get_format_selector(editor).currentText()
            self.display_data_in_editor(data, format_type, editor)
            self.original_lengths[self.get_data_type(button_text)] = len(data)

    def save_data(self, editor, format_type, save_text):
        data_type = self.get_data_type(save_text)
        if not self.check_length(editor.toPlainText().strip(), data_type):
            return

        file_filters = {
            'Сохранить ключ': 'Key Files (*.key)',
            'Сохранить исходное сообщение': 'Text Files (*.txt)',
            'Сохранить зашифрованное сообщение': 'Encrypted Files (*.enc)'
        }
        file_path, _ = QFileDialog.getSaveFileName(self, f'Сохранить {save_text}', '', file_filters[save_text])
        if file_path:
            self.save_data_from_editor(editor, format_type, file_path)

    def get_format_selector(self, editor):
        return editor.findChild(QComboBox)

    def get_data_type(self, text):
        if "ключ" in text:
            return 'key'
        elif "исходное сообщение" in text:
            return 'message'
        elif "зашифрованное сообщение" in text:
            return 'encrypted'

    def display_data_in_editor(self, data, format_type, editor):
        converters = {
            "Двоичный": bytes_to_binary,
            "Шестнадцатеричный": bytes_to_hex,
            "Символьный": bytes_to_text
        }
        editor.setPlainText(converters[format_type](data))

    def check_length(self, data, data_type):
        try:
            format_type = {
                'key': self.key_format_selector.currentText(),
                'encrypted': self.encrypted_format_selector.currentText()
            }.get(data_type, None)
            if format_type:
                data_length = len(self.convert_to_bytes(data, format_type))
                if data_length != self.original_lengths[data_type]:
                    raise ValueError("Длина данных не соответствует исходной длине.")
            return True
        except ValueError as ve:
            QMessageBox.warning(self, "Ошибка", str(ve))
            return False

    def convert_to_bytes(self, data, format_type):
        converters = {
            "Двоичный": binary_to_bytes,
            "Шестнадцатеричный": hex_to_bytes,
            "Символьный": lambda d: d.encode('utf-8')
        }
        return converters[format_type](data)

    def save_data_from_editor(self, editor, format_type, file_path):
        data = editor.toPlainText().strip()
        try:
            data_bytes = self.convert_to_bytes(data, format_type)
            with open(file_path, 'wb') as file:
                file.write(data_bytes)
            QMessageBox.information(self, "Успех", "Файл успешно сохранён.")
        except ValueError as ve:
            QMessageBox.warning(self, "Ошибка", str(ve))
