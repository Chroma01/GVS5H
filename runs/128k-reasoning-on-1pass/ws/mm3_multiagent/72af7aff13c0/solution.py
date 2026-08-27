import sys

def main():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    MOD = 998244353
    H = int(next(it))
    W = int(next(it))
    A = [[int(next(it)) for _ in range(W)] for _ in range(H)]

    if H == 1 or W == 1:
        # Special case: product of all elements
        prod = 1
        for i in range(H):
            for j in range(W):
                prod = prod * A[i][j] % MOD
        Q = int(next(it))
        sh = int(next(it)) - 1
        sw = int(next(it)) - 1
        cur_h, cur_w = sh, sw
        out = []
        for _ in range(Q):
            d = next(it).decode()
            a = int(next(it))
            if d == 'L':
                cur_w -= 1
            elif d == 'R':
                cur_w += 1
            elif d == 'U':
                cur_h -= 1
            else:  # 'D'
                cur_h += 1
            old = A[cur_h][cur_w]
            if old != 0:
                prod = prod * pow(old, MOD - 2, MOD) % MOD
            else:
                prod = 0
            A[cur_h][cur_w] = a
            prod = prod * a % MOD
            out.append(str(prod))
        sys.stdout.write("\n".join(out))
        return

    # DP initialization
    dp = [[0] * W for _ in range(H)]
    dp[0][0] = A[0][0] % MOD
    for i in range(1, H):
        dp[i][0] = A[i][0] * dp[i - 1][0] % MOD
    for j in range(1, W):
        dp[0][j] = A[0][j] * dp[0][j - 1] % MOD
    for i in range(1, H):
        row_A = A[i]
        dp_i = dp[i]
        dp_i_1 = dp[i - 1]
        for j in range(1, W):
            dp_i[j] = row_A[j] * (dp_i_1[j] + dp_i[j - 1]) % MOD

    Q = int(next(it))
    sh = int(next(it)) - 1
    sw = int(next(it)) - 1
    cur_h, cur_w = sh, sw
    out = []
    for _ in range(Q):
        d = next(it).decode()
        a = int(next(it))
        if d == 'L':
            cur_w -= 1
        elif d == 'R':
            cur_w += 1
        elif d == 'U':
            cur_h -= 1
        else:  # 'D'
            cur_h += 1
        h, w = cur_h, cur_w
        A[h][w] = a
        # Recompute suffix DP starting from (h, w)
        for i in range(h, H):
            row_A = A[i]
            dp_i = dp[i]
            if i == 0:
                for j in range(w, W):
                    if j == 0:
                        dp_i[0] = row_A[0] % MOD
                    else:
                        dp_i[j] = row_A[j] * dp_i[j - 1] % MOD
            else:
                dp_i_1 = dp[i - 1]
                for j in range(w, W):
                    if j == 0:
                        dp_i[0] = row_A[0] * dp_i_1[0] % MOD
                    else:
                        up = dp_i_1[j]
                        left = dp_i[j - 1]
                        dp_i[j] = row_A[j] * (up + left) % MOD
        out.append(str(dp[H - 1][W - 1]))
    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()