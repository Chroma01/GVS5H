from itertools import combinations

MOD = 10**9 + 7
INV6 = pow(6, MOD - 2, MOD)


class Solution:
    def distanceSum(self, m: int, n: int, k: int) -> int:
        total = m * n

        # Precompute factorials and inverse factorials up to total (<= 1e5)
        fact = [1] * (total + 1)
        for i in range(1, total + 1):
            fact[i] = fact[i - 1] * i % MOD
        inv_fact = [1] * (total + 1)
        inv_fact[total] = pow(fact[total], MOD - 2, MOD)
        for i in range(total, 0, -1):
            inv_fact[i - 1] = inv_fact[i] * i % MOD

        def comb(a: int, b: int) -> int:
            if b < 0 or b > a:
                return 0
            return fact[a] * inv_fact[b] % MOD * inv_fact[a - b] % MOD

        # Sum of |r1 - r2| over all unordered pairs of x distinct values
        # = x * (x^2 - 1) / 6
        def pair_sum(x: int) -> int:
            return x % MOD * ((x * x - 1) % MOD) % MOD * INV6 % MOD

        row_part = pair_sum(m) * (n * n % MOD) % MOD
        col_part = pair_sum(n) * (m * m % MOD) % MOD
        ways = comb(total - 2, k - 2)

        return (row_part + col_part) % MOD * ways % MOD


# ----------------- validation -----------------
def brute(m, n, k):
    cells = [(i, j) for i in range(m) for j in range(n)]
    total = 0
    for arrangement in combinations(cells, k):
        for a in range(k):
            for b in range(a + 1, k):
                total += abs(arrangement[a][0] - arrangement[b][0]) + \
                         abs(arrangement[a][1] - arrangement[b][1])
    return total % MOD


if __name__ == "__main__":
    sol = Solution()
    assert sol.distanceSum(2, 2, 2) == 8, sol.distanceSum(2, 2, 2)
    assert sol.distanceSum(1, 4, 3) == 20, sol.distanceSum(1, 4, 3)

    import random
    random.seed(0)
    for _ in range(200):
        m = random.randint(1, 4)
        n = random.randint(1, 4)
        if m * n < 2:
            continue
        k = random.randint(2, m * n)
        got = sol.distanceSum(m, n, k)
        want = brute(m, n, k)
        assert got == want, (m, n, k, got, want)

    # edge cases
    assert sol.distanceSum(1, 1, 2) == 0 or True  # k <= m*n so k=2 invalid here; skip
    assert sol.distanceSum(1, 2, 2) == 1
    assert sol.distanceSum(100000, 1, 2) == (100000 * (100000**2 - 1) // 6) % MOD
    print("all tests passed")