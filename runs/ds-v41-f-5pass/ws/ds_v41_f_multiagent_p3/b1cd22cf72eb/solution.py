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
    best_h = INF

    # Case j <= i: D_i + U_j + X * (i - j)
    # = (D_i + X * i) + (U_j - X * j)
    pref_min = INF
    for i in range(n):
        val = u[i] - x * i
        if val < pref_min:
            pref_min = val
        cand = d[i] + x * i + pref_min
        if cand < best_h:
            best_h = cand

    # Case j >= i: D_i + U_j + X * (j - i)
    # = (D_i - X * i) + (U_j + X * j)
    suff_min = INF
    for i in range(n - 1, -1, -1):
        val = u[i] + x * i
        if val < suff_min:
            suff_min = val
        cand = d[i] - x * i + suff_min
        if cand < best_h:
            best_h = cand

    answer = total - n * best_h
    print(answer)

if __name__ == "__main__":
    main()