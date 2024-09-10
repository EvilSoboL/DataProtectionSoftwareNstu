import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
from view_message_key import ViewMessageKeyWindow
from edit_message_key import EditMessageKeyWindow
from encrypt_message import EncryptMessageWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Главное меню")
        self.setGeometry(300, 300, 400, 200)

        layout = QVBoxLayout()

        self.view_btn = QPushButton("Просмотреть сообщение/ключ")
        self.view_btn.clicked.connect(self.open_view_window)
        layout.addWidget(self.view_btn)

        self.edit_btn = QPushButton("Изменить сообщение/ключ")
        self.edit_btn.clicked.connect(self.open_edit_window)
        layout.addWidget(self.edit_btn)

        self.encrypt_btn = QPushButton("Зашифровать сообщение")
        self.encrypt_btn.clicked.connect(self.open_encrypt_window)
        layout.addWidget(self.encrypt_btn)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def open_view_window(self):
        self.view_window = ViewMessageKeyWindow()
        self.view_window.show()

    def open_edit_window(self):
        self.edit_window = EditMessageKeyWindow()
        self.edit_window.show()

    def open_encrypt_window(self):
        self.encrypt_window = EncryptMessageWindow()
        self.encrypt_window.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
