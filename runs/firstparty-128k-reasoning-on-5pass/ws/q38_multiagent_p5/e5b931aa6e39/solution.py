import sys
from math import isqrt


def icbrt(n: int) -> int:
    if n <= 0:
        return 0
    lo = 0
    hi = 1 << ((n.bit_length() + 2) // 3)
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if mid * mid * mid <= n:
            lo = mid
        else:
            hi = mid
    return lo


def main() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    N = int(data[0])
    limit = icbrt(N - 1)

    for d in range(1, limit + 1):
        if N % d != 0:
            continue

        m = N // d
        val = 3 * (4 * m - d * d)
        if val < 0:
            continue

        t = isqrt(val)
        if t * t != val:
            continue

        rem = t - 3 * d
        if rem > 0 and rem % 6 == 0:
            y = rem // 6
            print(y + d, y)
            return

    print(-1)


if __name__ == "__main__":
    main()