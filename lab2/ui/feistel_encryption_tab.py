from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QComboBox, QFileDialog, QMessageBox, QLabel, QLineEdit


class FeistelEncryptionTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()


        self.test_results = QLabel()
        layout.addWidget(self.test_results)

        self.setLayout(layout)
