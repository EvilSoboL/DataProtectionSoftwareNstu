from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFileDialog, QMessageBox
from lab1.gamma_encryption import generate_key, encrypt


class GammaEncryptionTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.encrypt_button = QPushButton('Шифровать файл однократным гаммированием')
        self.encrypt_button.clicked.connect(self.encrypt_message)
        layout.addWidget(self.encrypt_button)

        self.setLayout(layout)

    def encrypt_message(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(self, 'Выберите файл для шифрования', '', 'Text Files (*.txt)')

        if file_path:
            with open(file_path, 'rb') as file:
                data = file.read()

            key = generate_key(len(data))

            key_file_path, _ = QFileDialog.getSaveFileName(self, 'Сохранить ключ', '', 'Key Files (*.key)')
            if key_file_path:
                with open(key_file_path, 'wb') as key_file:
                    key_file.write(key)

            encrypted_data = encrypt(data, key)
            enc_file_path, _ = QFileDialog.getSaveFileName(self, 'Сохранить зашифрованный файл', '', 'Encrypted Files (*.enc)')

            if enc_file_path:
                with open(enc_file_path, 'wb') as enc_file:
                    enc_file.write(encrypted_data)

                QMessageBox.information(self, "Успех", "Файл успешно зашифрован однократным гаммированием.")
