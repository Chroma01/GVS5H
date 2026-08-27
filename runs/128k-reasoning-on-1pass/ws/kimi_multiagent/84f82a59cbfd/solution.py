import sys
from bisect import bisect_right

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    q = int(data[0])
    queries = list(map(int, data[1:1 + q]))

    LIMIT = 10**6  # sqrt(10^12)

    # Sieve the number of distinct prime factors omega(n) for all n <= LIMIT
    omega = bytearray(LIMIT + 1)
    for p in range(2, LIMIT + 1):
        if omega[p] == 0:  # p is prime
            for m in range(p, LIMIT + 1, p):
                omega[m] += 1

    # 400 numbers are squares of integers with exactly two distinct prime factors
    candidates = [i * i for i in range(2, LIMIT + 1) if omega[i] == 2]
    # candidates is already sorted because i is increasing

    out = []
    for a in queries:
        idx = bisect_right(candidates, a) - 1
        out.append(str(candidates[idx]))
    sys.stdout.write("\n".join(out) + "\n")

main()