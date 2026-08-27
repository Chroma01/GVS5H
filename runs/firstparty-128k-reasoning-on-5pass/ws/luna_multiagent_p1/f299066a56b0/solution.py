import sys


def solve() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    a = data[1:1 + n]

    def feasible(k: int) -> bool:
        for i in range(k):
            if 2 * a[i] > a[n - k + i]:
                return False
        return True

    low, high = 0, n // 2 + 1

    while high - low > 1:
        mid = (low + high) // 2
        if feasible(mid):
            low = mid
        else:
            high = mid

    print(low)


if __name__ == "__main__":
    solve()