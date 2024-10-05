from PyQt5.QtWidgets import QMainWindow, QTabWidget
from lab1.ui.view_edit_tab import ViewEditTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.tabs = QTabWidget()

        self.view_edit_tab = ViewEditTab()
        self.tabs.addTab(self.view_edit_tab, "Просмотр и редактирование")

        self.setCentralWidget(self.tabs)
        self.setWindowTitle('Лабораторная работа №1')



