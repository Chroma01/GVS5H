import sys
from math import isqrt

def main():
    nums = list(map(int, sys.stdin.buffer.read().split()))
    if not nums:
        return

    q = nums[0]
    queries = nums[1:1 + q]
    if not queries:
        return

    max_r = isqrt(max(queries))
    if max_r < 6:
        max_r = 6
    end = max_r + 1

    # omega[x] = number of distinct prime factors of x
    omega = bytearray(end)
    for p in range(2, end):
        if omega[p] == 0:  # p is prime
            for multiple in range(p, end, p):
                omega[multiple] += 1

    # best[r] = largest integer <= r with exactly two distinct prime factors
    best = [0] * end
    last = 0
    for i in range(2, end):
        if omega[i] == 2:
            last = i
        best[i] = last

    out = []
    append = out.append
    for a in queries:
        m = best[isqrt(a)]
        append(str(m * m))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()