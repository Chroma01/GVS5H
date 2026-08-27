import sys
from bisect import bisect_right

def main():
    data = sys.stdin.buffer.read().split()
    q = int(data[0])
    queries = list(map(int, data[1:1 + q]))

    LIMIT = 10**6  # sqrt(10^12)

    # Count distinct prime factors for every m up to LIMIT
    cnt = bytearray(LIMIT + 1)
    for p in range(2, LIMIT + 1):
        if cnt[p] == 0:  # p is prime
            for j in range(p, LIMIT + 1, p):
                cnt[j] += 1

    # 400 numbers are squares of m with exactly 2 distinct prime factors
    squares = []
    append = squares.append
    for m in range(2, LIMIT + 1):
        if cnt[m] == 2:
            append(m * m)
    # squares is already sorted since m increases

    out = []
    for a in queries:
        out.append(str(squares[bisect_right(squares, a) - 1]))
    sys.stdout.write("\n".join(out) + "\n")

main()