import sys

MOD = 998244353


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return
    W, H, L, R, D, U = data
    m = MOD

    N = W + H + 4

    fact = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = fact[i - 1] * i % m

    invfact = [1] * (N + 1)
    invfact[N] = pow(fact[N], m - 2, m)
    for i in range(N, 0, -1):
        invfact[i - 1] = invfact[i] * i % m

    def comb(n, k):
        return fact[n] * invfact[k] % m * invfact[n - k] % m

    # Total number of monotone paths in a full (a+1) x (b+1) grid,
    # i.e. sum_{x=0..a} sum_{y=0..b} (C(x+y+2, x+1) - 1).
    def total(a, b):
        if a < 0 or b < 0:
            return 0
        n = a + b + 4
        k = a + 2
        c = fact[n] * invfact[k] % m * invfact[n - k] % m
        return (c - (a + 1) * (b + 1) - a - b - 4) % m

    # All full-grid paths.
    S_total = total(W, H)

    # J1: paths whose first forbidden point is q, counted by "start at q".
    # Sum over q in [L,R] x [D,U] of G(W-qx, H-qy), as a rectangle prefix sum.
    J1 = (
        total(W - L, H - D)
        - total(W - R - 1, H - D)
        - total(W - L, H - U - 1)
        + total(W - R - 1, H - U - 1)
    ) % m

    # Prepare boundary-sum values using H(a,b) = G(a,b) + 1 = C(a+b+2, a+1).
    J2 = 0
    if L > 0:
        a2 = L - 1
        c2 = W - L
        HA2 = comb(a2 + D + 2, a2 + 1)       # H(L-1, D)
        b2 = H - D
        HB2 = comb(c2 + b2 + 2, c2 + 1)      # H(W-L, H-D)

    J3 = 0
    if D > 0:
        b3 = D - 1
        e3 = H - D
        HF3 = comb(L + b3 + 2, L + 1)        # H(L, D-1)
        a3 = W - L
        HB3 = comb(a3 + e3 + 2, a3 + 1)      # H(W-L, H-D)

    # Inverses only up to the largest denominator actually used in recurrences.
    max_inv = 0
    if L > 0 and U > D:
        max_inv = max(max_inv, U + 1, W - L + H - D + 2)
    if D > 0 and R > L:
        max_inv = max(max_inv, R + 1, W - L + H - D + 2)
    if max_inv > N:
        max_inv = N

    if max_inv > 0:
        inv = [0] * (max_inv + 1)
        for i in range(1, max_inv + 1):
            inv[i] = fact[i - 1] * invfact[i] % m
    else:
        inv = [0]

    del fact, invfact

    # J2: entry from the left side of the forbidden rectangle.
    # Sum_{y=D..U} G(L-1, y) * G(W-L, H-y)
    if L > 0:
        numA = a2 + D + 3
        denA = D + 2
        numB = b2 + 1
        denB = c2 + b2 + 2

        total2 = 0
        inv_local = inv
        mm = m

        for _ in range(U - D):
            total2 = (total2 + (HA2 - 1) * (HB2 - 1)) % mm
            HA2 = (HA2 * numA * inv_local[denA]) % mm
            HB2 = (HB2 * numB * inv_local[denB]) % mm
            numA += 1
            denA += 1
            numB -= 1
            denB -= 1

        total2 = (total2 + (HA2 - 1) * (HB2 - 1)) % mm
        J2 = total2

    # J3: entry from the bottom side of the forbidden rectangle.
    # Sum_{x=L..R} G(x, D-1) * G(W-x, H-D)
    if D > 0:
        numF = L + b3 + 3
        denF = L + 2
        numA = a3 + 1
        denA = a3 + e3 + 2

        total3 = 0
        inv_local = inv
        mm = m

        for _ in range(R - L):
            total3 = (total3 + (HF3 - 1) * (HB3 - 1)) % mm
            HF3 = (HF3 * numF * inv_local[denF]) % mm
            HB3 = (HB3 * numA * inv_local[denA]) % mm
            numF += 1
            denF += 1
            numA -= 1
            denA -= 1

        total3 = (total3 + (HF3 - 1) * (HB3 - 1)) % mm
        J3 = total3

    ans = (S_total - J1 - J2 - J3) % m
    print(ans)


if __name__ == "__main__":
    main()