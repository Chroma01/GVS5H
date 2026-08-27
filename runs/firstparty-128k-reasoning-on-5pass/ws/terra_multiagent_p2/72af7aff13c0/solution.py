import sys

MOD = 998244353


def solve_small_height(H, W, A, Q, r, c, transposed):
    d = H
    size = d * d

    nbase = 1
    while nbase < W:
        nbase <<= 1

    identity = [0] * size
    for i in range(d):
        identity[i * d + i] = 1

    def make_column(col):
        mat = [0] * size
        for top in range(d):
            prod = 1
            for bottom in range(top, d):
                prod = prod * A[bottom][col] % MOD
                mat[bottom * d + top] = prod
        return mat

    def mul(right, left):
        out = [0] * size
        for i in range(d):
            ib = i * d
            for j in range(i + 1):
                total = 0
                for k in range(j, i + 1):
                    total += right[ib + k] * left[k * d + j]
                out[ib + j] = total % MOD
        return out

    seg = [identity[:] for _ in range(2 * nbase)]
    for col in range(W):
        seg[nbase + col] = make_column(col)

    for p in range(nbase - 1, 0, -1):
        seg[p] = mul(seg[p * 2 + 1], seg[p * 2])

    directions = {
        b"L": (0, -1),
        b"R": (0, 1),
        b"U": (-1, 0),
        b"D": (1, 0),
    }

    read = sys.stdin.buffer.readline
    ans = []

    for _ in range(Q):
        dch, value = read().split()
        value = int(value)

        dr, dc = directions[dch]
        if transposed:
            dr, dc = dc, dr

        r += dr
        c += dc
        A[r][c] = value

        p = nbase + c
        seg[p] = make_column(c)
        p >>= 1

        while p:
            seg[p] = mul(seg[p * 2 + 1], seg[p * 2])
            p >>= 1

        ans.append(str(seg[1][(d - 1) * d]))

    sys.stdout.write("\n".join(ans))


def solve_recompute(H, W, A, Q, r, c, transposed):
    directions = {
        b"L": (0, -1),
        b"R": (0, 1),
        b"U": (-1, 0),
        b"D": (1, 0),
    }

    read = sys.stdin.buffer.readline
    dp = [0] * W
    ans = []

    for _ in range(Q):
        dch, value = read().split()
        value = int(value)

        dr, dc = directions[dch]
        if transposed:
            dr, dc = dc, dr

        r += dr
        c += dc
        A[r][c] = value

        cur = A[0][0]
        dp[0] = cur
        for j in range(1, W):
            cur = cur * A[0][j] % MOD
            dp[j] = cur

        for i in range(1, H):
            row = A[i]
            dp[0] = dp[0] * row[0] % MOD
            left = dp[0]
            for j in range(1, W):
                left = (left + dp[j]) * row[j] % MOD
                dp[j] = left

        ans.append(str(dp[-1]))

    sys.stdout.write("\n".join(ans))


def main():
    read = sys.stdin.buffer.readline

    H, W = map(int, read().split())
    A = [list(map(int, read().split())) for _ in range(H)]

    Q, r, c = map(int, read().split())
    r -= 1
    c -= 1

    if H <= 3:
        solve_small_height(H, W, A, Q, r, c, False)
    elif W <= 3:
        AT = [[A[i][j] for i in range(H)] for j in range(W)]
        solve_small_height(W, H, AT, Q, c, r, True)
    else:
        solve_recompute(H, W, A, Q, r, c, False)


if __name__ == "__main__":
    main()