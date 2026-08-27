import sys

def solve():
    input = sys.stdin.readline

    N = int(input())
    X = list(map(int, input().split()))

    gaps = [X[i + 1] - X[i] for i in range(N - 1)]

    odd_gaps = sorted(gaps[0::2])   # gap indices 1, 3, 5, ... in 1-based indexing
    even_gaps = sorted(gaps[1::2])  # gap indices 2, 4, 6, ... in 1-based indexing

    ans = N * X[0]
    oi = 0
    ei = 0

    for j in range(1, N):
        weight = N - j
        if j % 2 == 1:
            ans += weight * odd_gaps[oi]
            oi += 1
        else:
            ans += weight * even_gaps[ei]
            ei += 1

    print(ans)

if __name__ == "__main__":
    solve()