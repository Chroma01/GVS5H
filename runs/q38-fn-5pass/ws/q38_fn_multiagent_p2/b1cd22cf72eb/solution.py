import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    x = data[1]

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

    # suff[i] = min_{j >= i} (U_j + X * j), 0-based
    suff = [0] * n
    cur = INF
    for i in range(n - 1, -1, -1):
        val = u[i] + x * i
        if val < cur:
            cur = val
        suff[i] = cur

    # For each i, compute min_j (U_j + X * |i - j|)
    # using prefix minimum of U_j - X*j and suffix minimum of U_j + X*j.
    best_h = INF
    cur = INF
    for i in range(n):
        val = u[i] - x * i
        if val < cur:
            cur = val

        left = x * i + cur
        right = -x * i + suff[i]
        min_u_plus_dist = left if left < right else right

        h = d[i] + min_u_plus_dist
        if h < best_h:
            best_h = h

    print(total - n * best_h)

if __name__ == "__main__":
    main()