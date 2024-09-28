from PyQt5.QtWidgets import QMainWindow, QTabWidget
from lab1.ui.view_edit_tab import ViewEditTab
from lab2.ui.feistel_encryption_tab import FeistelEncryptionTab


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.tabs = QTabWidget()

        self.view_edit_tab = ViewEditTab()
        self.tabs.addTab(self.view_edit_tab, "Просмотр и изменение")

        self.feistel_encryption_tab = FeistelEncryptionTab()
        self.tabs.addTab(self.feistel_encryption_tab, "Шифрование при помощи сети Фейстеля")

        self.setCentralWidget(self.tabs)
        self.setWindowTitle('Шифрование и редактирование')
