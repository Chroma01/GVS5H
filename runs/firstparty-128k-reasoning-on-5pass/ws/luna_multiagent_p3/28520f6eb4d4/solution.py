import sys


def solve() -> None:
    input = sys.stdin.readline
    n = int(input())

    x_prev, h_prev = map(int, input().split())

    best_num = None
    best_den = 1

    for _ in range(n - 1):
        x_cur, h_cur = map(int, input().split())

        num = x_cur * h_prev - x_prev * h_cur
        den = x_cur - x_prev

        if best_num is None or num * best_den > best_num * den:
            best_num = num
            best_den = den

        x_prev, h_prev = x_cur, h_cur

    if best_num is None or best_num < 0:
        print(-1)
    else:
        print("{:.18f}".format(best_num / best_den))


if __name__ == "__main__":
    solve()