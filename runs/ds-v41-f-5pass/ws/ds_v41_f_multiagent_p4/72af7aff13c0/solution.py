import sys

def main():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    MOD = 998244353
    H = int(next(it))
    W = int(next(it))
    N = H * W
    A = [0] * N
    for i in range(N):
        A[i] = int(next(it)) % MOD
    Q = int(next(it))
    sh = int(next(it)) - 1
    sw = int(next(it)) - 1

    dp = [0] * N
    # initial DP
    dp[0] = A[0]
    for w in range(1, W):
        dp[w] = A[w] * dp[w - 1] % MOD
    for h in range(1, H):
        idx = h * W
        dp[idx] = A[idx] * dp[idx - W] % MOD
        for w in range(1, W):
            idx = h * W + w
            dp[idx] = A[idx] * (dp[idx - 1] + dp[idx - W]) % MOD

    out = []
    for _ in range(Q):
        d = next(it)
        a = int(next(it)) % MOD
        if d == b'L':
            sw -= 1
        elif d == b'R':
            sw += 1
        elif d == b'U':
            sh -= 1
        else:  # b'D'
            sh += 1
        idx = sh * W + sw
        if A[idx] != a:
            A[idx] = a
            if sh == 0 and sw == 0:
                dp[0] = A[0]
                for w in range(1, W):
                    dp[w] = A[w] * dp[w - 1] % MOD
                for h in range(1, H):
                    row = h * W
                    dp[row] = A[row] * dp[row - W] % MOD
                    for w in range(1, W):
                        cur = row + w
                        dp[cur] = A[cur] * (dp[cur - 1] + dp[cur - W]) % MOD
            else:
                for h in range(sh, H):
                    row = h * W
                    for w in range(sw, W):
                        cur = row + w
                        up = dp[cur - W] if h > 0 else 0
                        left = dp[cur - 1] if w > 0 else 0
                        dp[cur] = A[cur] * (up + left) % MOD
        out.append(str(dp[N - 1]))
    sys.stdout.write('\n'.join(out))

if __name__ == '__main__':
    main()