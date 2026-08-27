import sys

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    x0 = data[1]

    odd = []
    even = []

    # data[1] is X_1, data[2] is X_2, ..., data[n] is X_n.
    # The gap between data[idx-1] and data[idx] is gap number idx-1 (1-based).
    for idx in range(2, n + 1):
        g = data[idx] - data[idx - 1]
        if (idx - 1) % 2 == 1:
            odd.append(g)
        else:
            even.append(g)

    odd.sort()
    even.sort()

    ans = n * x0

    # Odd gap positions: 1, 3, 5, ...
    # Their weights are n-1, n-3, n-5, ...
    w = n - 1
    for g in odd:
        ans += g * w
        w -= 2

    # Even gap positions: 2, 4, 6, ...
    # Their weights are n-2, n-4, n-6, ...
    w = n - 2
    for g in even:
        ans += g * w
        w -= 2

    print(ans)

if __name__ == "__main__":
    solve()