# random_math.py

def nCr(n, r):
    """Вычисляет биномиальный коэффициент (число сочетаний)."""
    if r < 0 or r > n:
        return 0
    if r == 0:
        return 1
    r = min(r, n - r)
    numerator = 1
    for i in range(1, r + 1):
        numerator = numerator * (n - i + 1) // i
    return numerator


def convert(n, k):
    """Преобразует число n в комбинацию для меню длины k."""
    if k < 1:
        raise ValueError("k must be at least 1")
    if k == 1:
        return [1] * n

    total = 0
    m = 1
    while True:
        c = nCr(k + m - 1, m)
        if n <= total + c:
            break
        total += c
        m += 1
    index_in_group = n - total - 1
    res = []
    a = 1
    cur = index_in_group
    n_remaining = m
    while n_remaining > 0:
        for digit in range(a, k + 1):
            if n_remaining == 1:
                count = 1
            else:
                count = nCr(k - digit + n_remaining - 1, n_remaining - 1)
            if cur < count:
                res.append(digit)
                a = digit
                n_remaining -= 1
                break
            else:
                cur -= count
    return res


def convert_signed(x, k):
    """
        Основная функция генерации заказа.
        x - seed (ключ), k - количество блюд в меню.
    """
    n = x + 1000000001
    if n < 1 or n > 2000000001:
        raise ValueError("x must be in [-1000000000, 1000000000]")
    return convert(n, k)
