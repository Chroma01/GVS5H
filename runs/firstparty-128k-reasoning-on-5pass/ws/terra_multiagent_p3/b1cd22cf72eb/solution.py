import sys


def main():
    input = sys.stdin.buffer.readline

    N, X = map(int, input().split())
    U = [0] * N
    D = [0] * N

    total = 0
    hi = 10**30

    for i in range(N):
        u, d = map(int, input().split())
        U[i] = u
        D[i] = d
        total += u + d
        if u + d < hi:
            hi = u + d

    def feasible(h):
        left = max(0, h - D[0])
        right = min(U[0], h)
        if left > right:
            return False

        for i in range(1, N):
            left = max(max(0, h - D[i]), left - X)
            right = min(min(U[i], h), right + X)
            if left > right:
                return False

        return True

    lo = 0
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid - 1

    print(total - N * lo)


if __name__ == "__main__":
    main()