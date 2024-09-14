import os
import random
import re
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QPushButton, QFileDialog, QWidget, QLabel, QComboBox, QTextEdit, \
    QMessageBox, QTabWidget, QHBoxLayout


class EncryptionApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Создание табов
        self.tabs = QTabWidget()

        # Первая вкладка: Просмотр и изменение
        self.tab_view_edit = QWidget()
        self.tab_view_edit_layout = QVBoxLayout()

        # Ключ
        self.load_key_button = QPushButton('Открыть и редактировать ключ', self)
        self.load_key_button.clicked.connect(self.load_key)
        self.tab_view_edit_layout.addWidget(self.load_key_button)

        self.key_format_selector = QComboBox(self)
        self.key_format_selector.addItems(["Двоичный", "Шестнадцатеричный", "Символьный"])
        self.tab_view_edit_layout.addWidget(self.key_format_selector)

        self.key_editor = QTextEdit(self)
        self.tab_view_edit_layout.addWidget(self.key_editor)

        self.save_key_button = QPushButton('Сохранить ключ', self)
        self.save_key_button.clicked.connect(self.save_key)
        self.tab_view_edit_layout.addWidget(self.save_key_button)

        # Исходное сообщение
        self.load_message_button = QPushButton('Открыть и редактировать исходное сообщение', self)
        self.load_message_button.clicked.connect(self.load_message)
        self.tab_view_edit_layout.addWidget(self.load_message_button)

        self.message_format_selector = QComboBox(self)
        self.message_format_selector.addItems(["Двоичный", "Шестнадцатеричный", "Символьный"])
        self.tab_view_edit_layout.addWidget(self.message_format_selector)

        self.message_editor = QTextEdit(self)
        self.tab_view_edit_layout.addWidget(self.message_editor)

        self.save_message_button = QPushButton('Сохранить исходное сообщение', self)
        self.save_message_button.clicked.connect(self.save_message)
        self.tab_view_edit_layout.addWidget(self.save_message_button)

        # Зашифрованное сообщение
        self.load_encrypted_button = QPushButton('Открыть и редактировать зашифрованное сообщение', self)
        self.load_encrypted_button.clicked.connect(self.load_encrypted_message)
        self.tab_view_edit_layout.addWidget(self.load_encrypted_button)

        self.encrypted_format_selector = QComboBox(self)
        self.encrypted_format_selector.addItems(["Двоичный", "Шестнадцатеричный", "Символьный"])
        self.tab_view_edit_layout.addWidget(self.encrypted_format_selector)

        self.encrypted_editor = QTextEdit(self)
        self.tab_view_edit_layout.addWidget(self.encrypted_editor)

        self.save_encrypted_button = QPushButton('Сохранить зашифрованное сообщение', self)
        self.save_encrypted_button.clicked.connect(self.save_encrypted_message)
        self.tab_view_edit_layout.addWidget(self.save_encrypted_button)

        self.tab_view_edit.setLayout(self.tab_view_edit_layout)

        # Вторая вкладка: Другой функционал (пока пустая)
        self.tab_other_functionality = QWidget()
        self.tab_other_functionality_layout = QVBoxLayout()
        self.tab_other_functionality_label = QLabel('Другой функционал будет здесь')
        self.tab_other_functionality_layout.addWidget(self.tab_other_functionality_label)
        self.tab_other_functionality.setLayout(self.tab_other_functionality_layout)

        # Добавляем вкладки
        self.tabs.addTab(self.tab_view_edit, "Просмотр и изменение")
        self.tabs.addTab(self.tab_other_functionality, "Другой функционал")

        # Основной компоновщик
        layout.addWidget(self.tabs)
        self.setLayout(layout)
        self.setWindowTitle('Шифрование')

    # Методы работы с файлами: загрузка и сохранение
    def load_key(self):
        key_file_path, _ = QFileDialog.getOpenFileName(self, 'Открыть файл ключа', '', 'Key Files (*.key)')
        if key_file_path:
            with open(key_file_path, 'rb') as key_file:
                self.key_data = key_file.read()

            self.display_data_in_editor(self.key_data, self.key_format_selector.currentText(), self.key_editor)

    def save_key(self):
        self.save_data_from_editor(self.key_editor, self.key_format_selector.currentText(), 'Key Files (*.key)')

    def load_message(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Открыть исходное сообщение', '', 'Text Files (*.txt)')
        if file_path:
            with open(file_path, 'rb') as file:
                self.message_data = file.read()

            self.display_data_in_editor(self.message_data, self.message_format_selector.currentText(),
                                        self.message_editor)

    def save_message(self):
        self.save_data_from_editor(self.message_editor, self.message_format_selector.currentText(),
                                   'Text Files (*.txt)')

    def load_encrypted_message(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Открыть зашифрованное сообщение', '',
                                                   'Encrypted Files (*.enc)')
        if file_path:
            with open(file_path, 'rb') as file:
                self.encrypted_data = file.read()

            self.display_data_in_editor(self.encrypted_data, self.encrypted_format_selector.currentText(),
                                        self.encrypted_editor)

    def save_encrypted_message(self):
        self.save_data_from_editor(self.encrypted_editor, self.encrypted_format_selector.currentText(),
                                   'Encrypted Files (*.enc)')

    def display_data_in_editor(self, data, format_type, editor):
        if format_type == "Двоичный":
            editor.setPlainText(' '.join(format(byte, '08b') for byte in data))
        elif format_type == "Шестнадцатеричный":
            editor.setPlainText(data.hex())
        elif format_type == "Символьный":
            try:
                editor.setPlainText(data.decode('utf-8'))
            except UnicodeDecodeError:
                editor.setPlainText('<Некорректные символы для UTF-8>')

    def save_data_from_editor(self, editor, format_type, file_type):
        data = editor.toPlainText().strip()

        if self.validate_data(data, format_type):
            file_path, _ = QFileDialog.getSaveFileName(self, f'Сохранить {file_type}', '', file_type)
            if file_path:
                try:
                    if format_type == "Двоичный":
                        data = bytearray(int(b, 2) for b in data.split())
                    elif format_type == "Шестнадцатеричный":
                        data = bytearray.fromhex(data)
                    elif format_type == "Символьный":
                        data = data.encode('utf-8')

                    with open(file_path, 'wb') as file:
                        file.write(data)
                    self.label.setText(f'Файл успешно сохранен')
                except ValueError:
                    self.label.setText('Ошибка при сохранении файла')

    def validate_data(self, data, format_type):
        if format_type == "Двоичный":
            if re.fullmatch(r'([01]{8} )*[01]{8}', data):
                return True
            else:
                self.show_error("Сообщение должно содержать только 0 и 1 в виде байтов (8 бит), разделенных пробелами.")
                return False
        elif format_type == "Шестнадцатеричный":
            if re.fullmatch(r'[0-9a-fA-F]+', data):
                return True
            else:
                self.show_error("Сообщение должно содержать только шестнадцатеричные символы (0-9, a-f).")
                return False
        return True

    def show_error(self, message):
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Warning)
        error_dialog.setText(message)
        error_dialog.setWindowTitle("Ошибка валидации")
        error_dialog.exec_()


if __name__ == '__main__':
    app = QApplication([])
    window = EncryptionApp()
    window.show()
    app.exec_()


