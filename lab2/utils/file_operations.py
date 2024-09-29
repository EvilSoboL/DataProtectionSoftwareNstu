import os
from PyQt5.QtWidgets import QFileDialog, QMessageBox


class FileOperations:
    @staticmethod
    def get_open_file(title):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(None, title, "", "Все файлы (*)", options=options)
        return file_path

    @staticmethod
    def get_save_file(title, default_name):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(None, title, default_name, "Все файлы (*)", options=options)
        return file_path

    @staticmethod
    def read_file(file_path):
        try:
            with open(file_path, 'rb') as f:
                return f.read()
        except Exception as e:
            QMessageBox.critical(None, "Ошибка", f"Ошибка чтения файла: {str(e)}")
            return None

    @staticmethod
    def write_file(file_path, data):
        try:
            with open(file_path, 'wb') as f:
                f.write(data)
        except Exception as e:
            QMessageBox.critical(None, "Ошибка", f"Ошибка записи файла: {str(e)}")

    @staticmethod
    def show_error(title, message):
        QMessageBox.critical(None, title, message)
