import matplotlib.pyplot as plt


def plot_changed_bits_histogram(file_path):
    rounds = []
    changed_bits = []

    # Чтение первых 16 записей из файла
    with open(file_path, 'r') as file:
        for _ in range(16):
            line = file.readline()
            if "Round" in line:
                parts = line.strip().split(':')
                round_number = int(parts[0].split()[1])
                bits_changed = int(parts[1].split()[0])
                rounds.append(round_number)
                changed_bits.append(bits_changed)

    # Построение гистограммы
    plt.figure(figsize=(10, 6))
    plt.bar(rounds, changed_bits, color='blue', edgecolor='black')
    plt.title('Зависимость числа изменившихся бит от раунда шифрования')
    plt.xlabel('Раунд шифрования')
    plt.ylabel('Изменившиеся биты')
    plt.grid(True)
    plt.show()


# Пример использования
plot_changed_bits_histogram('round_data.txt')
