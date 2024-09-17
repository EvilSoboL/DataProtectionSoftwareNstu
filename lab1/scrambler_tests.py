import math


def calculate_period(seq):
    """Расчет периода скремблера"""
    n = len(seq)
    for i in range(1, n // 2 + 1):
        if seq[:i] == seq[i:2 * i]:
            return i
    return n  # Если период не найден, возвращаем длину последовательности


def chi_squared_test(seq):
    """Критерий хи-квадрат для последовательности"""
    n = len(seq)
    zeros = seq.count('0')
    ones = seq.count('1')

    s = 2.0 * n
    s *= (math.pow(zeros / n - 0.5, 2.0) + math.pow(ones / n - 0.5, 2.0))
    return s


def balance_test(seq):
    """Тест на сбалансированность"""
    interval = 1000
    index = 0
    n = len(seq)

    for j in range(0, n, interval):
        z = seq[j:j + interval].count('0')
        o = seq[j:j + interval].count('1')
        balance_ratio = abs(z - o) / interval

        if balance_ratio > 0.05:
            return False, balance_ratio

    return True, balance_ratio


def correlation_test(seq):
    """Тест на корреляцию"""
    pl = 0
    mi = 0
    n = len(seq)
    shift = 5

    for i in range(shift, n - shift):
        if seq[i] == seq[i + shift]:
            pl += 1
        else:
            mi += 1

    correlation_ratio = abs(pl - mi) / (n - shift - shift)

    if correlation_ratio > 0.05:
        return False, correlation_ratio

    return True, correlation_ratio
