import sys


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n, x = data[0], data[1]

    u = [0] * n
    d = [0] * n
    total = 0
    p = 2
    upper_h = 10**30

    for i in range(n):
        u[i] = data[p]
        d[i] = data[p + 1]
        p += 2
        total += u[i] + d[i]
        upper_h = min(upper_h, u[i] + d[i])

    def feasible(h):
        low = max(0, h - d[0])
        high = min(u[0], h)
        if low > high:
            return False

        for i in range(1, n):
            left = max(0, h - d[i])
            right = min(u[i], h)

            low = max(left, low - x)
            high = min(right, high + x)

            if low > high:
                return False

        return True

    lo, hi = 0, upper_h + 1
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid

    print(total - n * lo)


if __name__ == "__main__":
    main()