from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFileDialog, QComboBox, QTextEdit, QPushButton
import binascii


class EditMessageKeyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Изменить сообщение/ключ")
        self.setGeometry(300, 300, 400, 300)

        self.layout = QVBoxLayout()
        self.label = QLabel("Выберите файл для изменения")
        self.layout.addWidget(self.label)

        self.open_file_dialog()

        self.setLayout(self.layout)

    def open_file_dialog(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Выбор файла", "", "Text Files (*.txt)")

        if file_path:
            file_name = file_path.split("/")[-1]
            self.format_selector = QComboBox()
            self.format_selector.addItems(["Символьный", "Двоичный", "Шестнадцатеричный"])
            self.layout.addWidget(self.format_selector)

            self.text_edit = QTextEdit()
            self.layout.addWidget(self.text_edit)

            self.save_button = QPushButton("Сохранить изменения")
            self.save_button.clicked.connect(lambda: self.save_file(file_path, file_name))
            self.layout.addWidget(self.save_button)

            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                if '_key' in file_name:
                    self.text_edit.setText(binascii.hexlify(content.encode()).decode('utf-8'))
                else:
                    self.text_edit.setText(content)

    def save_file(self, file_path, file_name):
        selected_format = self.format_selector.currentText()
        edited_content = self.text_edit.toPlainText()

        if selected_format == "Двоичный":
            edited_content = ' '.join(format(ord(c), '08b') for c in edited_content)
        elif selected_format == "Шестнадцатеричный":
            edited_content = binascii.hexlify(edited_content.encode()).decode('utf-8')

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(edited_content)
