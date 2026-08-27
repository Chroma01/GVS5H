import sys


def solve() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    n, m = data[0], data[1]
    prices = data[2:2 + n]

    def feasible(threshold: int) -> bool:
        total = 0
        for p in prices:
            q = (threshold // p + 1) // 2
            total += p * q * q
            if total > m:
                return False
        return True

    lo = 0
    hi = 1
    while feasible(hi):
        hi *= 2

    while hi - lo > 1:
        mid = (lo + hi) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid

    answer = 0
    for p in prices:
        answer += (lo // p + 1) // 2

    print(answer)


if __name__ == "__main__":
    solve()