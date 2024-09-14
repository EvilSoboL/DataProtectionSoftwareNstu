from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFileDialog, QTextEdit, QPushButton
import binascii


class EditMessageKeyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Изменить сообщение/ключ")
        self.setGeometry(300, 300, 400, 400)

        layout = QVBoxLayout()

        self.label = QLabel("Выберите файл для редактирования")
        layout.addWidget(self.label)

        self.text_edit = QTextEdit()
        layout.addWidget(self.text_edit)

        self.save_button = QPushButton("Сохранить изменения")
        self.save_button.clicked.connect(self.save_changes)
        layout.addWidget(self.save_button)

        self.open_file_dialog()
        self.setLayout(layout)

        self.file_path = None
        self.original_data = None

    def open_file_dialog(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Выбор файла", "", "Text Files (*.txt)")

        if file_path:
            self.file_path = file_path
            if file_path.endswith('_key.txt') or file_path.endswith('_crypted.txt'):
                self.read_binary_file(file_path)
            else:
                self.read_text_file(file_path)

    def read_text_file(self, file_path):
        """Чтение текстового файла."""
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            self.text_edit.setPlainText(content)

    def read_binary_file(self, file_path):
        """Чтение бинарного файла и отображение в шестнадцатеричном виде."""
        with open(file_path, 'rb') as file:
            content = file.read()
            self.original_data = content

            # Отображаем данные в шестнадцатеричном формате для редактирования
            hex_content = binascii.hexlify(content).decode('utf-8')
            self.text_edit.setPlainText(hex_content)

    def save_changes(self):
        """Сохранение изменений."""
        if self.file_path.endswith('_key.txt') or self.file_path.endswith('_crypted.txt'):
            self.save_binary_file(self.file_path)
        else:
            self.save_text_file(self.file_path)

    def save_text_file(self, file_path):
        """Сохранение текстового файла."""
        content = self.text_edit.toPlainText()
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)

    def save_binary_file(self, file_path):
        """Сохранение бинарного файла после редактирования в шестнадцатеричном виде."""
        hex_content = self.text_edit.toPlainText().strip()

        # Проверка на чётность длины строки
        if len(hex_content) % 2 != 0:
            self.label.setText("Ошибка: шестнадцатеричная строка должна содержать чётное количество символов.")
            return

        # Проверка на допустимые шестнадцатеричные символы
        valid_chars = "0123456789abcdefABCDEF"
        if not all(c in valid_chars for c in hex_content):
            self.label.setText("Ошибка: шестнадцатеричная строка содержит недопустимые символы.")
            return

        try:
            # Преобразуем шестнадцатеричные данные обратно в байты
            new_content = binascii.unhexlify(hex_content)

            with open(file_path, 'wb') as file:
                file.write(new_content)
            self.label.setText("Файл успешно сохранён.")
        except binascii.Error:
            self.label.setText("Ошибка: некорректный шестнадцатеричный формат.")
