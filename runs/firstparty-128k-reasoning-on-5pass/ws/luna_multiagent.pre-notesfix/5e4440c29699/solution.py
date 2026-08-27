import sys

MOD = 998244353


def main():
    W, H, L, R, D, U = map(int, sys.stdin.buffer.readline().split())

    n = W + H + 4

    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % MOD

    invfact = [1] * (n + 1)
    invfact[n] = pow(fact[n], MOD - 2, MOD)
    for i in range(n, 0, -1):
        invfact[i - 1] = invfact[i] * i % MOD

    def comb(a, b):
        if b < 0 or b > a:
            return 0
        return fact[a] * invfact[b] % MOD * invfact[a - b] % MOD

    def all_to(x, y):
        if x < 0 or y < 0:
            return 0
        return (comb(x + y + 2, x + 1) - 1) % MOD

    def northeast_sum(x, y):
        a = W - x
        b = H - y
        return (comb(a + b + 2, a + 1) - 1) % MOD

    # Number of paths in the complete (W+1) by (H+1) grid.
    total = (
        comb(W + H + 4, W + 2)
        - (W + 1)
        - (H + 1)
        - 2
        - (W + 1) * (H + 1)
    ) % MOD

    # Paths whose first forbidden point lies on the lower or left boundary.
    bad_boundary = 0

    ways_to_corner = (
        1
        + all_to(L - 1, D)
        + all_to(L, D - 1)
    ) % MOD
    bad_boundary = ways_to_corner * northeast_sum(L, D) % MOD

    for y in range(D + 1, U + 1):
        ways_to_first = (1 + all_to(L - 1, y)) % MOD
        bad_boundary = (
            bad_boundary + ways_to_first * northeast_sum(L, y)
        ) % MOD

    for x in range(L + 1, R + 1):
        ways_to_first = (1 + all_to(x, D - 1)) % MOD
        bad_boundary = (
            bad_boundary + ways_to_first * northeast_sum(x, D)
        ) % MOD

    # Sum of C(a+b+2, a+1) over 0 <= a <= p, 0 <= b <= q.
    def prefix_binom_sum(p, q):
        if p < 0 or q < 0:
            return 0
        return (
            comb(p + q + 4, p + 2)
            - p
            - q
            - 4
        ) % MOD

    # Paths whose starting point is strictly beyond both the left and
    # lower boundaries of the forbidden rectangle:
    # L < x <= R and D < y <= U.
    bad_missing_start = 0
    if L < R and D < U:
        # a = W-x, b = H-y
        a_lo = W - R
        a_hi = W - L - 1
        b_lo = H - U
        b_hi = H - D - 1

        sum_binom = (
            prefix_binom_sum(a_hi, b_hi)
            - prefix_binom_sum(a_lo - 1, b_hi)
            - prefix_binom_sum(a_hi, b_lo - 1)
            + prefix_binom_sum(a_lo - 1, b_lo - 1)
        ) % MOD

        count_points = (R - L) * (U - D)
        bad_missing_start = (sum_binom - count_points) % MOD

    answer = (total - bad_boundary - bad_missing_start) % MOD
    print(answer)


if __name__ == "__main__":
    main()