import csv
import random
import statistics
import time
from pathlib import Path
from main import find

def measure(a, k, answer):
    times = []

    for _ in range(5):
        start = time.perf_counter_ns()
        for _ in range(100):
            border, count = find(a, k)
        end = time.perf_counter_ns()

        if border != answer:
            raise RuntimeError("Граница найдена неправильно")

        times.append((end - start) / 100)

    return times, count


def main():
    rnd = random.Random(19)
    sizes = [16, 64, 256, 1023, 1024, 1025, 4096, 16384,
             65536, 262144, 1048575, 1048576, 1048577, 4194304]
    values = list(range(2, 33))
    path = Path(__file__).resolve().parent / "results.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["n", "bytes", "k", "mode", "time_ns", "checks"])
        for n in sizes:
            times = {k: [] for k in values}
            counts = {k: [] for k in values}
            for _ in range(10):
                answer = rnd.randint(0, n)
                a = bytearray([1]) * answer + bytearray(n - answer)

                order = values.copy()
                rnd.shuffle(order)
                for k in order:
                    ts, count = measure(a, k, answer)
                    times[k].extend(ts)
                    counts[k].append(count)

            for k in values:
                writer.writerow([n, n, k, "random",
                                 statistics.median(times[k]),
                                 statistics.mean(counts[k])])
            a = bytearray([1]) * n
            order = values.copy()
            rnd.shuffle(order)
            for k in order:
                ts, count = measure(a, k, n)
                writer.writerow([n, n, k, "worst",
                                 statistics.median(ts), count])

            f.flush()
            print("Готов размер:", n, "байт", flush=True)
    print("Результаты сохранены в", path)


if __name__ == "__main__":
    main()
