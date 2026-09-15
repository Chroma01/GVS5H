import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n, x = data[0], data[1]
    u = [0] * n
    d = [0] * n
    total = 0

    idx = 2
    for i in range(n):
        ui = data[idx]
        di = data[idx + 1]
        idx += 2
        u[i] = ui
        d[i] = di
        total += ui + di

    INF = 10**30
    h = INF

    # Pairs with j <= i:
    # U_j + X * (i - j) = (U_j - X * j) + X * i
    cur = INF
    for i in range(n):
        v = u[i] - x * i
        if v < cur:
            cur = v
        cand = d[i] + cur + x * i
        if cand < h:
            h = cand

    # Pairs with j >= i:
    # U_j + X * (j - i) = (U_j + X * j) - X * i
    cur = INF
    for i in range(n - 1, -1, -1):
        v = u[i] + x * i
        if v < cur:
            cur = v
        cand = d[i] + cur - x * i
        if cand < h:
            h = cand

    print(total - n * h)

if __name__ == "__main__":
    main()