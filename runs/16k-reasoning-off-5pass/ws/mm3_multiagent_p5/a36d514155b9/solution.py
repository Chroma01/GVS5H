class Solution:
    MOD = 10**9 + 7
    _fact = {}
    _inv_fact = {}

    def _precompute(self, N):
        if N in self._fact:
            return
        fact = [1] * (N + 1)
        for i in range(1, N + 1):
            fact[i] = fact[i - 1] * i % self.MOD
        inv_fact = [1] * (N + 1)
        inv_fact[N] = pow(fact[N], self.MOD - 2, self.MOD)
        for i in range(N, 0, -1):
            inv_fact[i - 1] = inv_fact[i] * i % self.MOD
        self._fact[N] = fact
        self._inv_fact[N] = inv_fact

    def _nCr(self, n, r, fact, inv_fact):
        if r < 0 or r > n:
            return 0
        return fact[n] * inv_fact[r] % self.MOD * inv_fact[n - r] % self.MOD

    def distanceSum(self, m: int, n: int, k: int) -> int:
        S = m * n
        self._precompute(S)
        fact = self._fact[S]
        inv_fact = self._inv_fact[S]

        # Number of arrangements containing a specific pair of cells
        comb = self._nCr(S - 2, k - 2, fact, inv_fact)

        # Row contribution: n^2 * m(m^2-1)/6
        # Col contribution: m^2 * n(n^2-1)/6
        inv6 = pow(6, self.MOD - 2, self.MOD)
        row_part = n * n % self.MOD
        row_part = row_part * m % self.MOD
        row_part = row_part * (m * m - 1) % self.MOD
        row_part = row_part * inv6 % self.MOD

        col_part = m * m % self.MOD
        col_part = col_part * n % self.MOD
        col_part = col_part * (n * n - 1) % self.MOD
        col_part = col_part * inv6 % self.MOD

        pair_sum = (row_part + col_part) % self.MOD
        return comb * pair_sum % self.MOD


# ---- self-check ----
if __name__ == "__main__":
    s = Solution()
    # Example 1
    assert s.distanceSum(2, 2, 2) == 8, f"got {s.distanceSum(2,2,2)}"
    # Example 2
    assert s.distanceSum(1, 4, 3) == 20, f"got {s.distanceSum(1,4,3)}"
    # Edge: k == mn => only one arrangement, all pairs in it, sum of distances of all cells
    # For m=2,n=2,k=4: C(2,2)=1, row_part+col_part = 4+4 = 8
    assert s.distanceSum(2, 2, 4) == 8, f"got {s.distanceSum(2,2,4)}"
    # k=2 case: m=3,n=3,k=2
    # Row: 9 * 3*8/6 = 9*4 = 36; Col: same = 36; total = 72
    assert s.distanceSum(3, 3, 2) == 72, f"got {s.distanceSum(3,3,2)}"
    print("All self-checks passed.")