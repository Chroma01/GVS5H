import sys

MOD = 998244353

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    # N = int(data[0])
    s = data[1]

    # DP over the 13 reachable relations.
    # State 0 is the identity relation.
    a0 = 1
    a1 = a2 = a3 = a4 = a5 = a6 = a7 = a8 = a9 = a10 = a11 = a12 = 0

    cnt = 0
    mod = MOD

    for c in s:
        if c == 48:  # '0'
            b0 = a0
            b1 = a0 + a1 + a4 + a6 + a8
            b2 = a0 + a2 + a5 + a7 + a9
            b3 = a1 + a2 + 3 * a3 + a4 + a5 + a10 + a12
            b4 = a1 + a4 + a8
            b5 = a2 + a5 + a9
            b6 = a6
            b7 = a7
            b8 = a8
            b9 = a9
            b10 = a7 + a10 + a11 + a12
            b11 = a11
            b12 = a6 + a10 + a11 + a12
        else:        # '1'
            b0 = 0
            b1 = a0 + a1 + a4 + a6 + a8
            b2 = a0 + a2 + a5 + a7 + a9
            b3 = a1 + a2 + 4 * a3 + a4 + a5 + a10 + a12
            b4 = a1 + a4 + a8
            b5 = a2 + a5 + a9
            b6 = a0 + a6
            b7 = a0 + a7
            b8 = a1 + a4 + 2 * a8
            b9 = a2 + a5 + 2 * a9
            b10 = a7 + a10 + a11 + a12
            b11 = a6 + a7 + a10 + 2 * a11 + a12
            b12 = a6 + a10 + a11 + a12

        a0, a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12 = (
            b0, b1, b2, b3, b4, b5, b6, b7, b8, b9, b10, b11, b12
        )

        cnt += 1
        if cnt == 14:
            a0 %= mod
            a1 %= mod
            a2 %= mod
            a3 %= mod
            a4 %= mod
            a5 %= mod
            a6 %= mod
            a7 %= mod
            a8 %= mod
            a9 %= mod
            a10 %= mod
            a11 %= mod
            a12 %= mod
            cnt = 0

    # Accepted states are all except states 1, 2, 3.
    ans = (a0 + a4 + a5 + a6 + a7 + a8 + a9 + a10 + a11 + a12) % mod
    print(ans)

if __name__ == "__main__":
    solve()