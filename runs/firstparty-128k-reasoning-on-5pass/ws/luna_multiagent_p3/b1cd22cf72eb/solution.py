import sys


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n, x = data[0], data[1]

    u = [0] * n
    d = [0] * n
    total = 0
    p = 2
    upper_bound = 10**30

    for i in range(n):
        u[i] = data[p]
        d[i] = data[p + 1]
        p += 2
        total += u[i] + d[i]
        upper_bound = min(upper_bound, u[i] + d[i])

    def feasible(h):
        low = max(0, h - d[0])
        high = min(u[0], h)
        if low > high:
            return False

        for i in range(1, n):
            current_low = max(0, h - d[i])
            current_high = min(u[i], h)

            low = max(current_low, low - x)
            high = min(current_high, high + x)

            if low > high:
                return False

        return True

    left = 0
    right = upper_bound + 1

    while right - left > 1:
        mid = (left + right) // 2
        if feasible(mid):
            left = mid
        else:
            right = mid

    print(total - n * left)


if __name__ == "__main__":
    main()