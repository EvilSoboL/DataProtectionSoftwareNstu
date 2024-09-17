import math

def calculate_period(seq: str) -> int:
    """Расчет периода последовательности."""
    n = len(seq)
    for i in range(1, n // 2 + 1):
        if seq[:i] == seq[i:2 * i]:
            return i
    return n  # Если период не найден, возвращаем длину последовательности

def chi_squared_test(seq: str) -> float:
    """Критерий хи-квадрат для последовательности."""
    n = len(seq)
    zeros = seq.count('0')
    ones = seq.count('1')

    expected = n / 2
    chi_squared = ((zeros - expected) ** 2 + (ones - expected) ** 2) / expected
    return chi_squared

def balance_test(seq: str, interval: int = 1000) -> tuple[bool, float]:
    """Тест на сбалансированность."""
    n = len(seq)
    for start in range(0, n, interval):
        end = min(start + interval, n)
        segment = seq[start:end]
        zeros = segment.count('0')
        ones = segment.count('1')
        balance_ratio = abs(zeros - ones) / interval

        if balance_ratio > 0.05:
            return False, balance_ratio

    return True, balance_ratio

def correlation_test(seq: str, shift: int = 5) -> tuple[bool, float]:
    """Тест на корреляцию."""
    n = len(seq)
    if n <= shift * 2:
        raise ValueError("Длина последовательности должна быть больше, чем дважды величина сдвига.")

    pl = sum(seq[i] == seq[i + shift] for i in range(shift, n - shift))
    mi = (n - shift * 2) - pl

    correlation_ratio = abs(pl - mi) / (n - shift * 2)

    if correlation_ratio > 0.05:
        return False, correlation_ratio

    return True, correlation_ratio
