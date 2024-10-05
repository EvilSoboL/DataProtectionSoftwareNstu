from PyQt5.QtWidgets import QMainWindow, QTabWidget
from lab1.ui.view_edit_tab import ViewEditTab
from lab1.ui.gamma_encryption_tab import GammaEncryptionTab


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.tabs = QTabWidget()

        self.view_edit_tab = ViewEditTab()
        self.tabs.addTab(self.view_edit_tab, "Просмотр и редактирование")

        self.gamma_encryption_tab = GammaEncryptionTab()
        self.tabs.addTab(self.gamma_encryption_tab, "Шифрование гаммированием")

        self.setCentralWidget(self.tabs)
        self.setWindowTitle('Лабораторная работа №1')



