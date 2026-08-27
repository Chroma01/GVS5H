import sys


def main():
    input = sys.stdin.buffer.readline
    N, X = map(int, input().split())

    U = [0] * N
    D = [0] * N
    total = 0

    for i in range(N):
        u, d = map(int, input().split())
        U[i] = u
        D[i] = d
        total += u + d

    best_upper = U[:]

    for i in range(1, N):
        best_upper[i] = min(best_upper[i], best_upper[i - 1] + X)

    for i in range(N - 2, -1, -1):
        best_upper[i] = min(best_upper[i], best_upper[i + 1] + X)

    H = min(D[i] + best_upper[i] for i in range(N))

    print(total - N * H)


if __name__ == "__main__":
    main()