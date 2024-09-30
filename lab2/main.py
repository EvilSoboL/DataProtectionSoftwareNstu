import sys
from PyQt5.QtWidgets import QApplication
from lab2.ui.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


#TODO A_2, B_2 шифрование неверно расшифровывает сообщение