import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(map(int, data))
    N = next(it)
    X = next(it)

    U = [0] * N
    D = [0] * N
    total = 0
    for i in range(N):
        u = next(it)
        d = next(it)
        U[i] = u
        D[i] = d
        total += u + d

    left = [0] * N
    left[0] = U[0]
    for i in range(1, N):
        v = left[i - 1] + X
        u = U[i]
        left[i] = u if u < v else v

    INF = 10 ** 30
    h = INF
    right = INF
    for i in range(N - 1, -1, -1):
        v = right + X
        u = U[i]
        right = u if u < v else v
        f = left[i] if left[i] < right else right
        val = D[i] + f
        if val < h:
            h = val

    print(total - N * h)

if __name__ == "__main__":
    main()