import sys
from PyQt5.QtWidgets import QApplication
from lab1.ui.main_window import MainWindow
from validators import validate_hexadecimal
from encryption import generate_key


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()