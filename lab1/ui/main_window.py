from PyQt5.QtWidgets import QMainWindow, QTabWidget
from lab1.ui.view_edit_tab import ViewEditTab
from lab1.ui.encryption_tab import EncryptionTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.tabs = QTabWidget()

        self.view_edit_tab = ViewEditTab()
        self.tabs.addTab(self.view_edit_tab, "Просмотр и изменение")

        self.encryption_tab = EncryptionTab()
        self.tabs.addTab(self.encryption_tab, "Шифрование/Расшифрование")

        self.setCentralWidget(self.tabs)
        self.setWindowTitle('Шифрование и редактирование')

