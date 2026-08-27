import sys


def solve() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    n = data[0]
    x = data[1:]

    odd_gaps = []
    even_gaps = []

    for i in range(n - 1):
        gap = x[i + 1] - x[i]
        if i % 2 == 0:
            odd_gaps.append(gap)
        else:
            even_gaps.append(gap)

    odd_gaps.sort()
    even_gaps.sort()

    ans = n * x[0]
    oi = ei = 0

    for i in range(n - 1):
        if i % 2 == 0:
            gap = odd_gaps[oi]
            oi += 1
        else:
            gap = even_gaps[ei]
            ei += 1
        ans += (n - 1 - i) * gap

    print(ans)


if __name__ == "__main__":
    solve()