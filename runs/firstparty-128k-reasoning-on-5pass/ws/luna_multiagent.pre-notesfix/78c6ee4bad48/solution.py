import sys


def solve() -> None:
    input = sys.stdin.readline

    n = int(input())
    x = list(map(int, input().split()))

    gaps = [x[i + 1] - x[i] for i in range(n - 1)]

    odd_gaps = sorted(gaps[0::2])   # 1-based gap indices: 1, 3, 5, ...
    even_gaps = sorted(gaps[1::2])  # 1-based gap indices: 2, 4, 6, ...

    answer = n * x[0]

    oi = 0
    ei = 0
    for j in range(1, n):
        if j % 2 == 1:
            gap = odd_gaps[oi]
            oi += 1
        else:
            gap = even_gaps[ei]
            ei += 1
        answer += gap * (n - j)

    print(answer)


if __name__ == "__main__":
    solve()