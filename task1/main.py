def search(a, k, left, right):
    if left == right:
        return left, 0

    m = right - left + 1
    parts = min(k, m)

    for i in range(1, parts):
        pos = left + i * m // parts - 1

        if a[pos] == 0:
            start = left + (i - 1) * m // parts
            border, count = search(a, k, start, pos)
            return border, count + i

    start = left + (parts - 1) * m // parts
    border, count = search(a, k, start, right)
    return border, count + parts - 1


def find(a, k=2):
    if not isinstance(k, int) or k < 2:
        raise ValueError("k должно быть целым числом не меньше 2")

    return search(a, k, 0, len(a))


if __name__ == "__main__":
    a = [1, 1, 1, 1, 0, 0, 0]
    k = int(input("Введите k: "))

    border, count = find(a, k)

    print("Массив:", a)
    print("Граница:", border)
    print("Количество проверок:", count)
