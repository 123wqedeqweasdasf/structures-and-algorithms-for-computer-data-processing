import random
import unittest
from main import find


def max_checks(n, k):
    m = n + 1
    if m == 1:
        return 0

    h = 0
    power = 1
    while power < m:
        power *= k
        h += 1

    power //= k
    last = (m + power - 1) // power
    return (k - 1) * (h - 1) + last - 1


class CheckedArray:
    def __init__(self, n, border):
        self.n = n
        self.border = border
        self.reads = 0

    def __len__(self):
        return self.n

    def __getitem__(self, i):
        if not isinstance(i, int) or not 0 <= i < self.n:
            raise AssertionError("Выход за границы массива или срез")
        self.reads += 1
        return 1 if i < self.border else 0


class TestSearch(unittest.TestCase):
    def test_examples(self):
        examples = [
            ([], 0),
            ([0], 0),
            ([1], 1),
            ([0, 0, 0], 0),
            ([1, 1, 1], 3),
            ([1, 0], 1),
            ([1, 1, 0, 0], 2),
            ([1, 1, 1, 1, 0, 0, 0], 4)
        ]
        for a, answer in examples:
            for k in [2, 3, 4, 8, 100]:
                with self.subTest(a=a, k=k):
                    self.assertEqual(find(a, k)[0], answer)

    def test_all_borders(self):
        for n in range(101):
            for answer in range(n + 1):
                a = [1] * answer + [0] * (n - answer)
                for k in [2, 3, 4, 5, 8, 16, 200]:
                    with self.subTest(n=n, border=answer, k=k):
                        border, count = find(a, k)
                        self.assertEqual(border, answer)
                        self.assertIsInstance(count, int)
                        self.assertGreaterEqual(count, 0)
                        self.assertLessEqual(count, max_checks(n, k))

    def test_random_arrays(self):
        rnd = random.Random(19)
        for _ in range(300):
            n = rnd.randint(0, 10000)
            answer = rnd.randint(0, n)
            k = rnd.randint(2, 300)
            a = bytearray([1]) * answer + bytearray(n - answer)
            with self.subTest(n=n, border=answer, k=k):
                self.assertEqual(find(a, k)[0], answer)

    def test_array_not_changed(self):
        a = [1, 1, 1, 1, 0, 0, 0]
        saved = a.copy()
        for k in [2, 3, 8, 100]:
            find(a, k)
            self.assertEqual(a, saved)

    def test_checks_and_worst_case(self):
        for n in range(61):
            for k in [2, 3, 4, 5, 8, 16, 100]:
                biggest = 0
                for answer in range(n + 1):
                    a = CheckedArray(n, answer)
                    border, count = find(a, k)
                    with self.subTest(n=n, border=answer, k=k):
                        self.assertEqual(border, answer)
                        self.assertEqual(count, a.reads)
                    biggest = max(biggest, count)
                self.assertEqual(biggest, max_checks(n, k))
                a = CheckedArray(n, n)
                self.assertEqual(find(a, k)[1], biggest)

    def test_large_array(self):
        n = 10 ** 12
        for answer in [0, 1, n // 2, n - 1, n]:
            for k in [2, 3, 8, 32]:
                a = CheckedArray(n, answer)
                border, count = find(a, k)
                with self.subTest(border=answer, k=k):
                    self.assertEqual(border, answer)
                    self.assertEqual(count, a.reads)
                    self.assertLessEqual(count, max_checks(n, k))

    def test_default_k(self):
        a = [1, 1, 0, 0]
        self.assertEqual(find(a), find(a, 2))

    def test_wrong_k(self):
        for k in [-10, -1, 0, 1, 2.5, "3", None]:
            for a in [[], [1, 0]]:
                with self.subTest(a=a, k=k):
                    with self.assertRaises(ValueError):
                        find(a, k)


if __name__ == "__main__":
    unittest.main(verbosity=2)
