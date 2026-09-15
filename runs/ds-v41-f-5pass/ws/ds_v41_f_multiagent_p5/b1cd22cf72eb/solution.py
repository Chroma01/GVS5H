import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    N = int(data[0])
    X = int(data[1])
    U = [0] * N
    D = [0] * N
    S = 0
    idx = 2
    for i in range(N):
        u = int(data[idx])
        d = int(data[idx + 1])
        idx += 2
        U[i] = u
        D[i] = d
        S += u + d

    # suff[i] = min_{j >= i} (D[j] + X*j)
    suff = [0] * N
    cur = None
    for j in range(N - 1, -1, -1):
        val = D[j] + X * j
        if cur is None or val < cur:
            cur = val
        suff[j] = cur

    # prefix min of D[j] - X*j while scanning i
    Hmax = None
    cur = None
    for i in range(N):
        val = D[i] - X * i
        if cur is None or val < cur:
            cur = val
        v1 = U[i] + X * i + cur
        v2 = U[i] - X * i + suff[i]
        if Hmax is None or v1 < Hmax:
            Hmax = v1
        if v2 < Hmax:
            Hmax = v2

    ans = S - N * Hmax
    sys.stdout.write(str(ans) + "\n")

if __name__ == "__main__":
    main()