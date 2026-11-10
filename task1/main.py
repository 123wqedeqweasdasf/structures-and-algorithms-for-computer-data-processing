def search(a, left, right):
    if left == right:
        return left

    mid = (left + right) // 2

    if a[mid] == 1:
        return search(a, mid + 1, right)
    else:
        return search(a, left, mid)


def find(a):
    return search(a, 0, len(a))


if __name__ == "__main__":
    a = [1, 1, 1, 1, 0, 0, 0]
    print("Граница:", find(a))
