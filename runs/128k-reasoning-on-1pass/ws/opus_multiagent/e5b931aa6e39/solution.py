import sys
from math import isqrt

def icbrt(n):
    if n < 0:
        return 0
    c = int(round(n ** (1.0 / 3.0)))
    if c < 0:
        c = 0
    # correct downward
    while c > 0 and c * c * c > n:
        c -= 1
    # correct upward
    while (c + 1) * (c + 1) * (c + 1) <= n:
        c += 1
    return c

def main():
    data = sys.stdin.read().split()
    N = int(data[0])
    limit = icbrt(N)
    _isqrt = isqrt
    n = N
    for d in range(1, limit + 1):
        if n % d:
            continue
        M = n // d
        D = 12 * M - 3 * d * d
        if D < 0:
            continue
        s = _isqrt(D)
        if s * s != D:
            continue
        t = s - 3 * d
        if t > 0 and t % 6 == 0:
            y = t // 6
            sys.stdout.write(str(y + d) + " " + str(y) + "\n")
            return
    sys.stdout.write("-1\n")

main()