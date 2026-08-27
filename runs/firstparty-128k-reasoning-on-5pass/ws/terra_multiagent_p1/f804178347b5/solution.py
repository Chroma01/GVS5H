import sys


def main():
    data = sys.stdin.read().split()
    if not data:
        return

    n = int(data[0])
    a = data[1]

    dp = [(0, 1) if ch == '0' else (1, 0) for ch in a]

    for _ in range(n):
        nxt = []
        for i in range(0, len(dp), 3):
            x, y, z = dp[i], dp[i + 1], dp[i + 2]

            cost0 = min(
                x[0] + y[0] + min(z[0], z[1]),
                x[0] + z[0] + min(y[0], y[1]),
                y[0] + z[0] + min(x[0], x[1]),
            )
            cost1 = min(
                x[1] + y[1] + min(z[0], z[1]),
                x[1] + z[1] + min(y[0], y[1]),
                y[1] + z[1] + min(x[0], x[1]),
            )

            nxt.append((cost0, cost1))
        dp = nxt

    cost0, cost1 = dp[0]
    print(cost1 if cost0 == 0 else cost0)


if __name__ == "__main__":
    main()