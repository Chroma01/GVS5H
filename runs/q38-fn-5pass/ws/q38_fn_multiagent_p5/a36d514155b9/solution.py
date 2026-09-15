class Solution:
    MOD = 10**9 + 7
    INV6 = pow(6, MOD - 2, MOD)

    # Cached factorials and inverse factorials across calls.
    _fact = [1]
    _invfact = [1]

    def _ensure_fact(self, n: int) -> None:
        """Ensure _fact and _invfact are valid up to n."""
        old = len(self._fact) - 1
        if n <= old:
            return

        self._fact.extend([1] * (n - old))
        for i in range(old + 1, n + 1):
            self._fact[i] = self._fact[i - 1] * i % self.MOD

        self._invfact.extend([1] * (n - old))
        self._invfact[n] = pow(self._fact[n], self.MOD - 2, self.MOD)
        for i in range(n, old, -1):
            self._invfact[i - 1] = self._invfact[i] * i % self.MOD

    def _comb(self, n: int, r: int) -> int:
        """Return C(n, r) modulo MOD."""
        if r < 0 or r > n:
            return 0
        self._ensure_fact(n)
        return self._fact[n] * self._invfact[r] % self.MOD * self._invfact[n - r] % self.MOD

    def _line_sum(self, length: int) -> int:
        """
        Sum_{d=1}^{length-1} d * (length - d)
        = length * (length - 1) * (length + 1) / 6.
        """
        mod = self.MOD
        return (
            (length % mod)
            * ((length - 1) % mod)
            % mod
            * ((length + 1) % mod)
            % mod
            * self.INV6
            % mod
        )

    def distanceSum(self, m: int, n: int, k: int) -> int:
        mod = self.MOD
        total_cells = m * n

        if k < 2 or k > total_cells:
            return 0

        # Sum of Manhattan distances over all unordered pairs of cells.
        # Row contribution: for each pair of rows at distance d, there are n^2 cell pairs.
        # Column contribution: for each pair of columns at distance d, there are m^2 cell pairs.
        row_part = (n % mod) * (n % mod) % mod * self._line_sum(m) % mod
        col_part = (m % mod) * (m % mod) % mod * self._line_sum(n) % mod
        total_pairwise_distance = (row_part + col_part) % mod

        # Each fixed unordered pair of cells appears in exactly C(total_cells - 2, k - 2)
        # valid arrangements.
        ways = self._comb(total_cells - 2, k - 2)

        return total_pairwise_distance * ways % mod