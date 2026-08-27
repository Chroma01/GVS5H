import sys

MOD = 998244353


def main():
    input = sys.stdin.buffer.readline

    H, W = map(int, input().split())
    n = H * W
    A = [0] * n

    for i in range(H):
        row = list(map(int, input().split()))
        base = i * W
        A[base:base + W] = row

    dp = [0] * n
    for i in range(H):
        base = i * W
        for j in range(W):
            p = base + j
            if p == 0:
                dp[p] = A[p]
            else:
                s = 0
                if i:
                    s += dp[p - W]
                if j:
                    s += dp[p - 1]
                dp[p] = A[p] * s % MOD

    Q, sh, sw = map(int, input().split())
    r = sh - 1
    c = sw - 1
    out = []

    for _ in range(Q):
        d, x = input().split()
        x = int(x)

        if d == b"L":
            c -= 1
        elif d == b"R":
            c += 1
        elif d == b"U":
            r -= 1
        else:
            r += 1

        start = r * W + c
        if A[start] != x:
            A[start] = x

            for i in range(r, H):
                base = i * W
                begin = c if i == r else c

                for j in range(begin, W):
                    p = base + j
                    if p == 0:
                        nv = A[p]
                    else:
                        s = 0
                        if i:
                            s += dp[p - W]
                        if j:
                            s += dp[p - 1]
                        nv = A[p] * s % MOD
                    dp[p] = nv

        out.append(str(dp[-1]))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()