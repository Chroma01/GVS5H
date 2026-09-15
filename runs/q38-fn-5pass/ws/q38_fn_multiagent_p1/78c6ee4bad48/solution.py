import sys

def solve() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    x = data[1:1 + n]

    gaps = [x[i + 1] - x[i] for i in range(n - 1)]

    odd_gaps = sorted(gaps[0::2])   # 1-indexed odd positions
    even_gaps = sorted(gaps[1::2])  # 1-indexed even positions

    ans = n * x[0]
    oi = 0
    ei = 0

    for j in range(1, n):
        if j & 1:
            ans += (n - j) * odd_gaps[oi]
            oi += 1
        else:
            ans += (n - j) * even_gaps[ei]
            ei += 1

    print(ans)

if __name__ == "__main__":
    solve()