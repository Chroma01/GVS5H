import sys
from bisect import bisect_right


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    q = data[0]
    queries = data[1:1 + q]

    limit = 1_000_000

    # Smallest prime factor sieve.
    spf = list(range(limit + 1))
    for p in range(2, 1001):
        if spf[p] == p:
            for x in range(p * p, limit + 1, p):
                if spf[x] == x:
                    spf[x] = p

    # Number of distinct prime factors for every integer.
    distinct = bytearray(limit + 1)
    squares = []

    for x in range(2, limit + 1):
        p = spf[x]
        y = x // p
        distinct[x] = distinct[y] + (spf[y] != p)

        if distinct[x] == 2:
            squares.append(x * x)

    answers = []
    for a in queries:
        answers.append(str(squares[bisect_right(squares, a) - 1]))

    sys.stdout.write("\n".join(answers))


if __name__ == "__main__":
    solve()