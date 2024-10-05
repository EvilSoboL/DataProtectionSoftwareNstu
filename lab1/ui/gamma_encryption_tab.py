from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFileDialog, QMessageBox
from lab1.gamma_encryption import generate_key, encrypt


class GammaEncryptionTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

        self.text_file_filter = 'Text Files (*.txt)'
        self.key_file_filter = 'Key Files (*.key)'
        self.encrypted_file_filter = 'Encrypted Files (*.enc)'

    def initUI(self):
        layout = QVBoxLayout()

        self.encrypt_button = QPushButton('Шифровать файл однократным гаммированием')
        self.encrypt_button.clicked.connect(self.encrypt_message)
        layout.addWidget(self.encrypt_button)

        self.encrypt_button = QPushButton('Расшифровать файл однократным гаммированием')
        self.encrypt_button.clicked.connect(self.decrypt_message)
        layout.addWidget(self.encrypt_button)

        self.setLayout(layout)

    def encrypt_message(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(self, 'Выберите файл для шифрования', '', self.text_file_filter)

        if file_path:
            with open(file_path, 'rb') as file:
                message = file.read()

            key = generate_key(len(message))

            key_file_path, _ = QFileDialog.getSaveFileName(self, 'Сохранить ключ', '', self.key_file_filter)
            if key_file_path:
                with open(key_file_path, 'wb') as key_file:
                    key_file.write(key)

            encrypted_data = encrypt(message, key)
            enc_file_path, _ = QFileDialog.getSaveFileName(self, 'Сохранить зашифрованный файл', '', self.encrypted_file_filter)

            if enc_file_path:
                with open(enc_file_path, 'wb') as enc_file:
                    enc_file.write(encrypted_data)

                QMessageBox.information(self, "Успех", "Файл успешно зашифрован однократным гаммированием.")

    def decrypt_message(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(self, 'Выберите файл для дешифрования', '', self.encrypted_file_filter)
        try:
            if file_path:
                with open(file_path, 'rb') as file:
                    encrypted_message = file.read()

                key_file_path, _ = QFileDialog.getOpenFileName(self, 'Выберите ключ для дешифрования', '', self.key_file_filter)
                if key_file_path:
                    with open(key_file_path, 'rb') as key_file:
                        key = key_file.read()

                    if len(encrypted_message) != len(key):
                        raise ValueError('Длина кюча не соответсвует длине сообщения!')

                    decrypted_message = encrypt(encrypted_message, key)
                    dec_file_path, _ = QFileDialog.getSaveFileName(self, 'Сохранить расшифрованный файл', '', self.text_file_filter)
                    if dec_file_path:
                        with open(dec_file_path, 'wb') as dec_file:
                            dec_file.write(decrypted_message)
                        QMessageBox.information(self, "Успех", "Файл успешно расшифрован.")

        except Exception as e:
            QMessageBox.warning(self, "Ошибка!", str(e))