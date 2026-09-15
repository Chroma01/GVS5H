import sys

def solve():
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

    inf = 10**30
    best_h = inf

    # Pairs with i <= j:
    # D_i + U_j + X * (j - i)
    # = (D_i - X * i) + (U_j + X * j)
    pref = inf
    for j in range(n):
        v = d[j] - x * j
        if v < pref:
            pref = v
        cand = pref + u[j] + x * j
        if cand < best_h:
            best_h = cand

    # Pairs with i >= j:
    # D_i + U_j + X * (i - j)
    # = (D_i + X * i) + (U_j - X * j)
    suff = inf
    for j in range(n - 1, -1, -1):
        v = d[j] + x * j
        if v < suff:
            suff = v
        cand = suff + u[j] - x * j
        if cand < best_h:
            best_h = cand

    print(total - n * best_h)

if __name__ == "__main__":
    solve()