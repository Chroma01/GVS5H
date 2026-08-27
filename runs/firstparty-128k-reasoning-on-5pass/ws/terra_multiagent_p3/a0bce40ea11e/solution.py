import sys


def mat_mul(a, b, mod):
    n = len(a)
    c = [[0] * n for _ in range(n)]
    for i in range(n):
        row_a = a[i]
        row_c = c[i]
        for k, x in enumerate(row_a):
            if x:
                row_b = b[k]
                for j in range(n):
                    row_c[j] += x * row_b[j]
        c[i] = [x % mod for x in row_c]
    return c


def mat_pow(a, e, mod):
    n = len(a)
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        result[i][i] = 1

    while e:
        if e & 1:
            result = mat_mul(result, a, mod)
        e >>= 1
        if e:
            a = mat_mul(a, a, mod)
    return result


def main():
    input = sys.stdin.buffer.readline
    n, p = map(int, input().split())
    a = [list(map(int, input().split())) for _ in range(n)]

    if p == 1:
        print(*(["0"] * n), sep="\n")
        return

    # For p = 2, every zero has exactly one possible replacement: 1.
    # Thus every resulting matrix is the all-ones matrix.
    if p == 2:
        v = n & 1
        line = " ".join([str(v)] * n)
        print("\n".join([line] * n))
        return

    fixed = [[0] * n for _ in range(n)]
    zero = [[0] * n for _ in range(n)]
    diag_zero = [0] * n
    k_zero = 0

    for i in range(n):
        for j in range(n):
            if a[i][j] == 0:
                zero[i][j] = 1
                k_zero += 1
                if i == j:
                    diag_zero[i] = 1
            else:
                fixed[i][j] = a[i][j]

    if p == 3:
        f2 = mat_mul(fixed, fixed, p)
        ans = mat_mul(f2, fixed, p)

        # D F + F D, where D has 1 at originally-zero diagonal entries.
        for i in range(n):
            if diag_zero[i]:
                for j in range(n):
                    ans[i][j] += fixed[i][j]
                    ans[j][i] += fixed[j][i]

        # Walk pattern: zero edge, reverse fixed edge, same zero edge.
        for i in range(n):
            for j in range(n):
                if zero[i][j]:
                    ans[i][j] += fixed[j][i]

        for i in range(n):
            for j in range(n):
                ans[i][j] %= p
    else:
        ans = mat_pow(fixed, p, p)

        # For p >= 5, a surviving zero edge occurring p-1 times
        # must be a loop. The sole fixed edge is before or after it.
        for i in range(n):
            if diag_zero[i]:
                for j in range(n):
                    ans[i][j] += fixed[i][j]      # D F
                    ans[j][i] += fixed[j][i]      # F D

        for i in range(n):
            for j in range(n):
                ans[i][j] %= p

    # Every variable, whether unused or used p-1 times, contributes -1
    # after summation over F_p^*.
    if k_zero & 1:
        for i in range(n):
            for j in range(n):
                ans[i][j] = (-ans[i][j]) % p

    print("\n".join(" ".join(map(str, row)) for row in ans))


if __name__ == "__main__":
    main()