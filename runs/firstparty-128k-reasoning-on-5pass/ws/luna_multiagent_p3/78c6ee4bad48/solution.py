import sys


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n = data[0]
    x = data[1:]

    gaps = [x[i + 1] - x[i] for i in range(n - 1)]

    odd_gaps = sorted(gaps[0::2])
    even_gaps = sorted(gaps[1::2])

    oi = ei = 0
    total = n * x[0]

    for j, _ in enumerate(gaps, start=1):
        if j % 2 == 1:
            g = odd_gaps[oi]
            oi += 1
        else:
            g = even_gaps[ei]
            ei += 1
        total += (n - j) * g

    print(total)


if __name__ == "__main__":
    solve()