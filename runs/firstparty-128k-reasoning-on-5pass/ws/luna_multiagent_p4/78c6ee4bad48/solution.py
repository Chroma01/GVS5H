import sys


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n = data[0]
    x = data[1:]

    gaps = [x[i] - x[i - 1] for i in range(1, n)]

    answer = n * x[0]

    for parity in (0, 1):
        values = gaps[parity::2]
        coefficients = [n - (j + 1) for j in range(parity, n - 1, 2)]

        values.sort(reverse=True)
        coefficients.sort()

        answer += sum(v * c for v, c in zip(values, coefficients))

    print(answer)


if __name__ == "__main__":
    solve()