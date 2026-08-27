import sys

MOD = 998244353


def main():
    W, H, L, R, D, U = map(int, sys.stdin.buffer.read().split())

    max_n = W + H + 4
    fact = [1] * (max_n + 1)
    for i in range(1, max_n + 1):
        fact[i] = fact[i - 1] * i % MOD

    ifact = [1] * (max_n + 1)
    ifact[max_n] = pow(fact[max_n], MOD - 2, MOD)
    for i in range(max_n, 0, -1):
        ifact[i - 1] = ifact[i] * i % MOD

    def comb(n, r):
        if r < 0 or r > n:
            return 0
        return fact[n] * ifact[r] % MOD * ifact[n - r] % MOD

    # Number of monotone paths from any point in [0..x]x[0..y] to (x,y).
    def prefix_paths(x, y):
        if x < 0 or y < 0:
            return 0
        return (comb(x + y + 2, y + 1) - 1) % MOD

    # Number of monotone paths from (x,y) to any point in [x..W]x[y..H].
    def suffix_paths(x, y):
        if x > W or y > H:
            return 0
        a = W - x
        b = H - y
        return (comb(a + b + 2, a + 1) - 1) % MOD

    # Sum of suffix_paths(x,y) over 0<=x<=A, 0<=y<=B.
    def rectangle_prefix(A, B):
        if A < 0 or B < 0:
            return 0
        # Sum C(a+b+2,a+1)-1 over 0<=a<=A, 0<=b<=B.
        value = comb(A + B + 4, B + 2)
        value -= B + 3
        value -= A + 1
        value -= (A + 1) * (B + 1)
        return value % MOD

    # Total number of unrestricted paths over all start/end pairs.
    total = rectangle_prefix(W, H)

    # Sum suffix_paths over the forbidden rectangle.
    # Reverse x,y: a=W-x, b=H-y.
    forbidden = (
        rectangle_prefix(W - L, H - D)
        - rectangle_prefix(W - R - 1, H - D)
        - rectangle_prefix(W - L, H - U - 1)
        + rectangle_prefix(W - R - 1, H - U - 1)
    ) % MOD

    # For a forbidden point p, count paths whose first forbidden point is p.
    # Every such path is obtained from a valid prefix to p, followed by
    # an arbitrary suffix from p.
    invalid = forbidden

    # Entry through the bottom side: only possible when y == D and D > 0.
    if D > 0:
        for x in range(L, R + 1):
            invalid += prefix_paths(x, D - 1) * suffix_paths(x, D)
        invalid %= MOD

    # Entry through the left side: only possible when x == L and L > 0.
    if L > 0:
        for y in range(D, U + 1):
            invalid += prefix_paths(L - 1, y) * suffix_paths(L, y)
        invalid %= MOD

    answer = (total - invalid) % MOD
    print(answer)


if __name__ == "__main__":
    main()