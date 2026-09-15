import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n, x = data[0], data[1]
    U = [0] * n
    D = [0] * n

    total = 0
    idx = 2
    for i in range(n):
        u = data[idx]
        d = data[idx + 1]
        idx += 2
        U[i] = u
        D[i] = d
        total += u + d

    INF = 10**30
    H = INF

    # i <= j: U_i + D_j + X * (j - i)
    best = INF
    for j in range(n):
        val = U[j] - x * j
        if val < best:
            best = val
        cand = best + D[j] + x * j
        if cand < H:
            H = cand

    # i >= j: U_i + D_j + X * (i - j)
    best = INF
    for i in range(n):
        val = D[i] - x * i
        if val < best:
            best = val
        cand = U[i] + x * i + best
        if cand < H:
            H = cand

    print(total - n * H)

if __name__ == "__main__":
    main()