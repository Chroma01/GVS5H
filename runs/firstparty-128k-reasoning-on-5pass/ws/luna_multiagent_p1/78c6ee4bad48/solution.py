import sys


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n = data[0]
    x = data[1:]

    gaps = [x[i + 1] - x[i] for i in range(n - 1)]

    odd_gaps = sorted(gaps[0::2])   # 1st, 3rd, ... gaps
    even_gaps = sorted(gaps[1::2])  # 2nd, 4th, ... gaps

    answer = n * x[0]

    for t, gap in enumerate(odd_gaps):
        j = 2 * t + 1  # 1-based gap index
        answer += (n - j) * gap

    for t, gap in enumerate(even_gaps):
        j = 2 * t + 2  # 1-based gap index
        answer += (n - j) * gap

    print(answer)


if __name__ == "__main__":
    solve()