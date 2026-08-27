import sys


def solve() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    n = data[0]

    if n == 1:
        print(-1)
        return

    xs = [0] * n
    hs = [0] * n
    p = 1
    for i in range(n):
        xs[i] = data[p]
        hs[i] = data[p + 1]
        p += 2

    best_num = None
    best_den = 1

    for i in range(n - 1):
        # Y-intercept of the line through:
        # (X_i, H_i), (X_{i+1}, H_{i+1})
        num = hs[i] * xs[i + 1] - hs[i + 1] * xs[i]
        den = xs[i + 1] - xs[i]

        if best_num is None or num * best_den > best_num * den:
            best_num = num
            best_den = den

    if best_num < 0:
        print(-1)
    else:
        print("{:.18f}".format(best_num / best_den))


if __name__ == "__main__":
    solve()