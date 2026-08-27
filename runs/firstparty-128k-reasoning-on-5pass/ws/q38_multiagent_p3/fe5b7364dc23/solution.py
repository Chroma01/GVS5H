import sys

MOD = 998244353

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N = data[0]
    K = data[1]
    k1 = K + 1

    # signed[p] = C(K, p) * (-1)^p mod MOD
    signed = [0] * k1
    c = 1
    for p in range(k1):
        if p:
            c = c * (K - p + 1) // p
        v = c % MOD
        if p & 1:
            v = (-v) % MOD
        signed[p] = v

    # M[p] = sum of previous prefix sums^p, initially only S_0 = 0
    M = [0] * k1
    M[0] = 1

    # pw[p] = current prefix sum^p
    pw = [1] * k1

    ans = 0
    S = 0
    mod = MOD

    rng = range(k1)
    rng_pow = range(1, k1)
    sg = signed

    for a in data[2:2 + N]:
        S += a
        if S >= mod:
            S -= mod

        for i in rng_pow:
            pw[i] = (pw[i - 1] * S) % mod

        total = 0
        for p in rng:
            total += sg[p] * pw[K - p] * M[p]

        ans += total % mod
        if ans >= mod:
            ans -= mod

        for p in rng:
            v = M[p] + pw[p]
            if v >= mod:
                v -= mod
            M[p] = v

    print(ans)

if __name__ == "__main__":
    main()