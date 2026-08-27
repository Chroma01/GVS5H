import sys
from bisect import bisect_right

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    q = data[0]
    queries = data[1:q + 1]

    limit = 1_000_000
    distinct_factor_count = bytearray(limit + 1)

    for p in range(2, limit + 1):
        if distinct_factor_count[p] == 0:
            for multiple in range(p, limit + 1, p):
                distinct_factor_count[multiple] += 1

    squares = [
        x * x
        for x in range(2, limit + 1)
        if distinct_factor_count[x] == 2
    ]

    out = []
    for a in queries:
        index = bisect_right(squares, a) - 1
        out.append(str(squares[index]))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()