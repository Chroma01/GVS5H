class Solution:
    MOD = 10**9 + 7
    fact = [1]
    invfact = [1]

    def _ensure_fact(self, size: int) -> None:
        cur = len(self.fact) - 1
        if size <= cur:
            return

        self.fact.extend([1] * (size - cur))
        for i in range(cur + 1, size + 1):
            self.fact[i] = self.fact[i - 1] * i % self.MOD

        self.invfact.extend([1] * (size - cur))
        self.invfact[size] = pow(self.fact[size], self.MOD - 2, self.MOD)
        for i in range(size, cur, -1):
            self.invfact[i - 1] = self.invfact[i] * i % self.MOD

    def _comb(self, a: int, b: int) -> int:
        if b < 0 or b > a:
            return 0
        self._ensure_fact(a)
        return self.fact[a] * self.invfact[b] % self.MOD * self.invfact[a - b] % self.MOD

    def distanceSum(self, m: int, n: int, k: int) -> int:
        total_cells = m * n
        if k < 2 or total_cells < 2:
            return 0

        mod = self.MOD

        def line_pair_sum(length: int) -> int:
            # Sum of |i - j| over all unordered pairs 1 <= i < j <= length.
            return (length * (length - 1) * (length + 1) // 6) % mod

        row_part = (n % mod) * (n % mod) % mod * line_pair_sum(m) % mod
        col_part = (m % mod) * (m % mod) % mod * line_pair_sum(n) % mod
        total_distance = (row_part + col_part) % mod

        arrangements_per_pair = self._comb(total_cells - 2, k - 2)
        return total_distance * arrangements_per_pair % mod