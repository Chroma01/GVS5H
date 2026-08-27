import sys

def main():
    tokens = sys.stdin.buffer.read().split()
    if not tokens:
        return

    it = iter(tokens)
    N = int(next(it))
    X = int(next(it))

    U = [0] * N
    D = [0] * N
    total = 0

    for i in range(N):
        u = int(next(it))
        d = int(next(it))
        U[i] = u
        D[i] = d
        total += u + d

    # f[i] = min_j (U[j] + X * abs(i - j))
    f = U

    # Left-to-right pass: considers j <= i
    for i in range(1, N):
        v = f[i - 1] + X
        if v < f[i]:
            f[i] = v

    # Right-to-left pass: considers j >= i
    for i in range(N - 2, -1, -1):
        v = f[i + 1] + X
        if v < f[i]:
            f[i] = v

    H = min(D[i] + f[i] for i in range(N))
    print(total - N * H)

if __name__ == "__main__":
    main()