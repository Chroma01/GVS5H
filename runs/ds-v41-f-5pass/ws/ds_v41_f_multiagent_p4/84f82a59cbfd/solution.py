import sys
import math
import bisect


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    LIMIT = 10 ** 6

    # omega[i] = number of distinct prime factors of i
    omega = [0] * (LIMIT + 1)
    for i in range(2, LIMIT + 1):
        if omega[i] == 0:          # i is prime
            for j in range(i, LIMIT + 1, i):
                omega[j] += 1

    # m must have exactly 2 distinct prime factors
    valid = [i for i in range(2, LIMIT + 1) if omega[i] == 2]
    valid_sq = [m * m for m in valid]

    q = int(data[0])
    out = []
    idx = 1
    isqrt = math.isqrt
    br = bisect.bisect_right

    for _ in range(q):
        a = int(data[idx])
        idx += 1
        m = isqrt(a)                   # m = floor(sqrt(a))
        pos = br(valid, m) - 1         # largest valid m <= isqrt(a)
        out.append(str(valid_sq[pos]))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()