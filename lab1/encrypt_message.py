from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFileDialog, QMessageBox
import os
import random


class EncryptMessageWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Зашифровать сообщение")
        self.setGeometry(300, 300, 400, 200)

        self.layout = QVBoxLayout()
        self.label = QLabel("Выберите файл для шифрования")
        self.layout.addWidget(self.label)

        self.open_file_dialog()

        self.setLayout(self.layout)

    def open_file_dialog(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Выбор файла сообщения", "", "Text Files (*.txt)")

        if file_path:
            try:
                with open(file_path, 'rb') as f:
                    message_bytes = f.read()

                # Генерация случайного ключа
                key_bytes = bytearray([random.randint(0, 255) for _ in range(len(message_bytes))])

                # Шифрование сообщения методом однократного гаммирования
                encrypted_bytes = bytearray([mb ^ kb for mb, kb in zip(message_bytes, key_bytes)])

                # Подготовка имен файлов
                file_dir, file_name = os.path.split(file_path)
                file_base_name = os.path.splitext(file_name)[0]

                key_filename = os.path.join(file_dir, f"{file_base_name}_key.txt")
                encrypted_filename = os.path.join(file_dir, f"{file_base_name}_crypted.txt")

                # Сохранение ключа в файл
                with open(key_filename, 'wb') as key_file:
                    key_file.write(key_bytes)

                # Сохранение зашифрованного сообщения в файл
                with open(encrypted_filename, 'wb') as encrypted_file:
                    encrypted_file.write(encrypted_bytes)

                QMessageBox.information(self, "Успех",
                                        f"Сообщение успешно зашифровано.\n\nКлюч сохранен в: {key_filename}\nЗашифрованное сообщение сохранено в: {encrypted_filename}")
                self.close()
            except Exception as e:
                QMessageBox.warning(self, "Ошибка", f"Произошла ошибка при шифровании сообщения: {str(e)}")
        else:
            QMessageBox.information(self, "Отмена", "Вы не выбрали файл для шифрования.")
            self.close()
