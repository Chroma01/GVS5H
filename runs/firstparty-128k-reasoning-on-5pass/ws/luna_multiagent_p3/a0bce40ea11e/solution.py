import sys


def mat_mul(a, b, mod):
    n = len(a)
    c = [[0] * n for _ in range(n)]
    for i in range(n):
        ci = c[i]
        ai = a[i]
        for k, aik in enumerate(ai):
            if aik:
                bk = b[k]
                for j in range(n):
                    ci[j] += aik * bk[j]
        for j in range(n):
            ci[j] %= mod
    return c


def mat_pow(a, exp, mod):
    n = len(a)
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        result[i][i] = 1
    base = a
    while exp:
        if exp & 1:
            result = mat_mul(result, base, mod)
        base = mat_mul(base, base, mod)
        exp >>= 1
    return result


def main():
    input = sys.stdin.readline
    n, p = map(int, input().split())
    a = [list(map(int, input().split())) for _ in range(n)]

    if p == 2:
        b = [[1 if a[i][j] == 0 else a[i][j] for j in range(n)]
             for i in range(n)]
        ans = mat_mul(b, b, p)
        print("\n".join(" ".join(map(str, row)) for row in ans))
        return

    k = sum(a[i][j] == 0 for i in range(n) for j in range(n))
    ans = mat_pow(a, p, p)

    correction = [[0] * n for _ in range(n)]

    # A zero diagonal entry may be used p-1 times, with one fixed
    # incoming or outgoing edge as the remaining edge.
    for u in range(n):
        if a[u][u] == 0:
            for x in range(n):
                if x != u:
                    correction[x][u] += a[x][u]
                    correction[u][x] += a[u][x]

    # For p=3, a non-loop zero edge may be used twice, with its
    # fixed reverse edge as the third edge.
    if p == 3:
        for u in range(n):
            for v in range(n):
                if u != v and a[u][v] == 0:
                    correction[u][v] += a[v][u]

    sign = 1 if k % 2 == 0 else p - 1
    for i in range(n):
        for j in range(n):
            ans[i][j] = sign * (ans[i][j] + correction[i][j]) % p

    print("\n".join(" ".join(map(str, row)) for row in ans))


if __name__ == "__main__":
    main()