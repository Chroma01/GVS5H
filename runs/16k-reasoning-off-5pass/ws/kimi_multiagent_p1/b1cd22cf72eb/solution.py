import sys

def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    N = int(data[idx]); idx += 1
    X = int(data[idx]); idx += 1
    U = [0] * N
    D = [0] * N
    total = 0
    for i in range(N):
        u = int(data[idx]); idx += 1
        d = int(data[idx]); idx += 1
        U[i] = u
        D[i] = d
        total += u + d

    # B_k = min_j (D_j + X * |j - k|)
    B = D[:]
    for k in range(1, N):
        v = B[k - 1] + X
        if v < B[k]:
            B[k] = v
    for k in range(N - 2, -1, -1):
        v = B[k + 1] + X
        if v < B[k]:
            B[k] = v

    H = min(U[k] + B[k] for k in range(N))
    print(total - N * H)

main()