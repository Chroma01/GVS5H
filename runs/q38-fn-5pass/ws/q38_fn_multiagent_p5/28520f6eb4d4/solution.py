import sys


def solve() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    it = iter(data)
    n = int(next(it))

    if n == 1:
        print(-1)
        return

    x_prev = int(next(it))
    h_prev = int(next(it))

    best_num = None
    best_den = 1

    for _ in range(n - 1):
        x = int(next(it))
        h = int(next(it))

        # y-intercept of the line through (x_prev, h_prev) and (x, h):
        # (x * h_prev - x_prev * h) / (x - x_prev)
        num = x * h_prev - x_prev * h
        den = x - x_prev

        if best_num is None or num * best_den > best_num * den:
            best_num = num
            best_den = den

        x_prev, h_prev = x, h

    if best_num is None or best_num < 0:
        print(-1)
    else:
        print(f"{best_num / best_den:.18f}")


if __name__ == "__main__":
    solve()