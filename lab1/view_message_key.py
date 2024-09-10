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
            # Проверка на ключ или зашифрованный файл
            if file_path.endswith('_key.txt') or file_path.endswith('_crypted.txt'):
                self.read_binary_file(file_path)
            else:
                self.read_text_file(file_path)

    def read_text_file(self, file_path):
        """Чтение и отображение текстового файла."""
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            bin_content = ' '.join(format(ord(c), '08b') for c in content)
            hex_content = binascii.hexlify(content.encode()).decode('utf-8')

            self.label.setText(f"Символьный: {content}\n\nДвоичный: {bin_content}\n\nШестнадцатеричный: {hex_content}")

    def read_binary_file(self, file_path):
        """Чтение и отображение бинарного файла (ключа или зашифрованного сообщения)."""
        with open(file_path, 'rb') as file:
            content = file.read()
            bin_content = ' '.join(format(byte, '08b') for byte in content)
            hex_content = binascii.hexlify(content).decode('utf-8')

            # Символьное представление для бинарного файла не показываем
            char_content = "Символьное представление недоступно для бинарного файла."

            self.label.setText(f"{char_content}\n\nДвоичный: {bin_content}\n\nШестнадцатеричный: {hex_content}")
