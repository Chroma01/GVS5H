import sys

def mat_mul(a, b, mod):
    n = len(a)
    res = [[0] * n for _ in range(n)]
    for i in range(n):
        ri = res[i]
        ai = a[i]
        for k, x in enumerate(ai):
            if x:
                bk = b[k]
                for j in range(n):
                    ri[j] += x * bk[j]
        for j in range(n):
            ri[j] %= mod
    return res

def mat_pow(a, e, mod):
    n = len(a)
    res = [[0] * n for _ in range(n)]
    for i in range(n):
        res[i][i] = 1

    while e:
        if e & 1:
            res = mat_mul(res, a, mod)
        e >>= 1
        if e:
            a = mat_mul(a, a, mod)
    return res

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n, p = data[0], data[1]
    a = []
    pos = 2
    for _ in range(n):
        a.append(data[pos:pos + n])
        pos += n

    if p == 2:
        b = [[1 if a[i][j] == 0 else a[i][j] for j in range(n)] for i in range(n)]
        ans = mat_mul(b, b, p)
        print("\n".join(" ".join(map(str, row)) for row in ans))
        return

    c = [[0] * n for _ in range(n)]
    zero_mask = [[False] * n for _ in range(n)]
    diagonal_zero = [False] * n
    k_zeros = 0

    for i in range(n):
        for j in range(n):
            if a[i][j] == 0:
                zero_mask[i][j] = True
                k_zeros += 1
                if i == j:
                    diagonal_zero[i] = True
            else:
                c[i][j] = a[i][j]

    ans = mat_pow(c, p, p)

    # Contributions from one zero diagonal edge used p-1 times.
    # The sole fixed nonzero edge is at the beginning or at the end.
    for i in range(n):
        for j in range(n):
            extra = 0
            if diagonal_zero[j]:
                extra += c[i][j]
            if diagonal_zero[i]:
                extra += c[i][j]
            ans[i][j] = (ans[i][j] + extra) % p

    # For p = 3 only, a non-diagonal zero edge can occur twice,
    # separated by one fixed edge in the reverse direction.
    if p == 3:
        for i in range(n):
            for j in range(n):
                if zero_mask[i][j]:
                    ans[i][j] = (ans[i][j] + c[j][i]) % p

    if k_zeros & 1:
        for i in range(n):
            for j in range(n):
                ans[i][j] = (-ans[i][j]) % p

    print("\n".join(" ".join(map(str, row)) for row in ans))

if __name__ == "__main__":
    main()