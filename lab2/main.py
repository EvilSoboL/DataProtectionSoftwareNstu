import sys
from PyQt5.QtWidgets import QApplication

from lab2.feistel_cipher import FeistelCipher
from lab2.ui.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


# TODO Process finished with exit code -1073740791 (0xC0000409) при попытке изменения байта ключа
# TODO На вход поступают не байты а int