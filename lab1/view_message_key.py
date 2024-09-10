from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFileDialog
import binascii


class ViewMessageKeyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Просмотр сообщения/ключа")
        self.setGeometry(300, 300, 400, 300)

        layout = QVBoxLayout()

        self.label = QLabel("Выберите файл для просмотра")
        layout.addWidget(self.label)

        self.open_file_dialog()
        self.setLayout(layout)

    def open_file_dialog(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Выбор файла", "", "Text Files (*.txt)")

        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                bin_content = ' '.join(format(ord(c), '08b') for c in content)
                hex_content = binascii.hexlify(content.encode()).decode('utf-8')

                self.label.setText(
                    f"Символьный: {content}\n\nДвоичный: {bin_content}\n\nШестнадцатеричный: {hex_content}")
