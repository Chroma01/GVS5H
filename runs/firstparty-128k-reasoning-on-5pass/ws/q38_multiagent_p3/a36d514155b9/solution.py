MOD = 1_000_000_007


class Solution:
    def distanceSum(self, m: int, n: int, k: int) -> int:
        total_cells = m * n

        fact = [1] * (total_cells + 1)
        for i in range(1, total_cells + 1):
            fact[i] = fact[i - 1] * i % MOD

        invfact = [1] * (total_cells + 1)
        invfact[total_cells] = pow(fact[total_cells], MOD - 2, MOD)
        for i in range(total_cells, 0, -1):
            invfact[i - 1] = invfact[i] * i % MOD

        ways_to_include_pair = (
            fact[total_cells - 2]
            * invfact[k - 2]
            % MOD
            * invfact[total_cells - k]
            % MOD
        )

        inv6 = pow(6, MOD - 2, MOD)
        mm = m % MOD
        nn = n % MOD

        row_pair_distance_sum = mm * ((mm * mm - 1) % MOD) % MOD * inv6 % MOD
        col_pair_distance_sum = nn * ((nn * nn - 1) % MOD) % MOD * inv6 % MOD

        all_pair_distance_sum = (
            nn * nn % MOD * row_pair_distance_sum
            + mm * mm % MOD * col_pair_distance_sum
        ) % MOD

        return ways_to_include_pair * all_pair_distance_sum % MOD


if __name__ == "__main__":
    import itertools

    def brute_force(m: int, n: int, k: int) -> int:
        cells = [(i, j) for i in range(m) for j in range(n)]
        total = 0
        for chosen in itertools.combinations(cells, k):
            for a in range(k):
                x1, y1 = chosen[a]
                for b in range(a + 1, k):
                    x2, y2 = chosen[b]
                    total += abs(x1 - x2) + abs(y1 - y2)
        return total % MOD

    sol = Solution()
    assert sol.distanceSum(2, 2, 2) == 8
    assert sol.distanceSum(1, 4, 3) == 20

    for m in range(1, 4):
        for n in range(1, 4):
            total_cells = m * n
            for k in range(2, total_cells + 1):
                expected = brute_force(m, n, k)
                got = sol.distanceSum(m, n, k)
                assert got == expected, (m, n, k, got, expected)

    import random
    random.seed(1)
    for _ in range(100):
        m = random.randint(1, 5)
        n = random.randint(1, 5)
        total_cells = m * n
        if total_cells < 2 or total_cells > 12:
            continue
        k = random.randint(2, total_cells)
        expected = brute_force(m, n, k)
        got = sol.distanceSum(m, n, k)
        assert got == expected, (m, n, k, got, expected)

    print("All tests passed")