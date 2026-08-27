import sys
from bisect import bisect_right

def main():
    data = sys.stdin.buffer.read().split()
    q = int(data[0])
    queries = list(map(int, data[1:1 + q]))

    LIMIT = 10**6  # sqrt(10^12)

    # Count distinct prime factors for every m up to LIMIT
    omega = bytearray(LIMIT + 1)
    is_comp = bytearray(LIMIT + 1)
    for p in range(2, LIMIT + 1):
        if not is_comp[p]:
            # p is prime; add 1 to distinct-prime-factor count of all multiples
            for m in range(p, LIMIT + 1, p):
                omega[m] += 1
                is_comp[m] = 1

    # 400 numbers are squares of m with exactly 2 distinct prime factors
    squares = [m * m for m in range(2, LIMIT + 1) if omega[m] == 2]
    squares.sort()

    out = []
    for a in queries:
        idx = bisect_right(squares, a) - 1
        out.append(str(squares[idx]))
    sys.stdout.write("\n".join(out) + "\n")

main()