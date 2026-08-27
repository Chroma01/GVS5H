import sys
import bisect

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    q = int(data[0])
    queries = list(map(int, data[1:1 + q]))

    LIMIT = 10**6  # sqrt(10^12)

    # Sieve: count distinct prime factors for each number up to LIMIT
    distinct_pf = [0] * (LIMIT + 1)
    for i in range(2, LIMIT + 1):
        if distinct_pf[i] == 0:  # i is prime
            for j in range(i, LIMIT + 1, i):
                distinct_pf[j] += 1

    # Collect squares of numbers with exactly 2 distinct prime factors
    good_squares = []
    for m in range(2, LIMIT + 1):
        if distinct_pf[m] == 2:
            good_squares.append(m * m)
    # good_squares is already sorted since m increases

    out = []
    for a in queries:
        idx = bisect.bisect_right(good_squares, a) - 1
        out.append(str(good_squares[idx]))

    sys.stdout.write("\n".join(out) + "\n")

main()