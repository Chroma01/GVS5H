import sys

MOD = 998244353

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    s = data[1] if len(data) > 1 else b""
    if not s:
        print(0)
        return

    # one = 0 before the first '1', and 1 afterwards.
    one = 1 if s[0] == 49 else 0

    # Reduced 6-variable DP derived from the 16-state mask DP.
    a = b = c = d = e = f = 0

    mod = MOD
    cnt = 1  # the first character has already been consumed

    for ch in s[1:]:
        if ch == 48:  # '0'
            a, b, c, d, e, f = (
                2 * a + b + 1,
                b,
                2 * c + e + 1,
                2 * d + one + f,
                e,
                f,
            )
        else:         # '1'
            a, b, c, d, e, f = (
                2 * a + b + 1,
                2 * a + 2 * b + 1,
                2 * c + e + 1,
                2 * d + one + f,
                2 * c + 1 + 2 * e,
                2 * d + 2 * one + 2 * f,
            )
            one = 1

        cnt += 1
        if cnt == 16:
            cnt = 0
            a %= mod
            b %= mod
            c %= mod
            d %= mod
            e %= mod
            f %= mod

    ans = (a + b + c + 2 * d + e + f + 1 + one) % mod
    print(ans)

if __name__ == "__main__":
    main()