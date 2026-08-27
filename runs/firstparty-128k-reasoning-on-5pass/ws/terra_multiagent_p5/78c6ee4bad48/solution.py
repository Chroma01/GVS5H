import sys

def solve():
    input = sys.stdin.readline

    n = int(input())
    x = list(map(int, input().split()))

    gaps = [x[i + 1] - x[i] for i in range(n - 1)]

    odd_gaps = sorted(gaps[0::2])   # 1-indexed odd gap positions
    even_gaps = sorted(gaps[1::2])  # 1-indexed even gap positions

    ans = n * x[0]
    oi = 0
    ei = 0

    for j in range(n - 1):
        if j % 2 == 0:
            gap = odd_gaps[oi]
            oi += 1
        else:
            gap = even_gaps[ei]
            ei += 1

        ans += gap * (n - j - 1)

    print(ans)

if __name__ == "__main__":
    solve()