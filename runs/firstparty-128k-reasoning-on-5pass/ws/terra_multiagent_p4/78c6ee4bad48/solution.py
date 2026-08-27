import sys


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n = data[0]
    x = data[1:]

    gaps = [x[i + 1] - x[i] for i in range(n - 1)]

    odd_gaps = sorted(gaps[0::2])   # 1-indexed odd gap positions
    even_gaps = sorted(gaps[1::2])  # 1-indexed even gap positions

    ans = n * x[0]

    for k, gap in enumerate(odd_gaps):
        j = 2 * k + 1
        ans += (n - j) * gap

    for k, gap in enumerate(even_gaps):
        j = 2 * k + 2
        ans += (n - j) * gap

    print(ans)


if __name__ == "__main__":
    main()