import sys
from PyQt5.QtWidgets import QApplication
from lab1.ui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


def LFSR():
    # Начальное состояние
    LFSR.ShiftRegister = getattr(LFSR, 'ShiftRegister', 0b1001111)
    initial = bin(LFSR.ShiftRegister)

    # Обратная связь и сдвиг
    print(f'Начальное значение: {initial}')
    print(f'Сдвиг на 6 позиций вправо: {bin(LFSR.ShiftRegister >> 6)}')
    print(f'Сдвиг на 2 позиций вправо: {bin(LFSR.ShiftRegister >> 2)}')
    print(f'XOR: {bin((LFSR.ShiftRegister >> 6) ^ (LFSR.ShiftRegister >> 2))}')
    print(f'Последний бит: {bin((LFSR.ShiftRegister >> 6) ^ (LFSR.ShiftRegister >> 2) & 0x01)}')
    new_bit = ((LFSR.ShiftRegister >> 6) ^ (LFSR.ShiftRegister >> 2)) & 0x01
    print(f'Сдвиг нового бита на 6 влево: {bin(new_bit << 6)}')
    print(f'Сдвиг начального значения на 2 вправо: {bin(LFSR.ShiftRegister >> 2)}')
    print(f'OR: {bin((new_bit << 6) | (LFSR.ShiftRegister >> 1))}')
    LFSR.ShiftRegister = (new_bit << 6) | (LFSR.ShiftRegister >> 1)

    # Возврат младшего бита
    return LFSR.ShiftRegister & 0x01




if __name__ == '__main__':
    # Пример использования
    for _ in range(10):
        LFSR()
    main()
