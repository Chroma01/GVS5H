class Solution:
    MOD = 10**9 + 7

    def _comb(self, n: int, r: int) -> int:
        if r < 0 or r > n:
            return 0
        r = min(r, n - r)
        if r == 0:
            return 1

        num = 1
        den = 1
        start = n - r + 1

        for i in range(1, r + 1):
            num = (num * (start + i - 1)) % self.MOD
            den = (den * i) % self.MOD

        return (num * pow(den, self.MOD - 2, self.MOD)) % self.MOD

    def countGoodArrays(self, n: int, m: int, k: int) -> int:
        if k < 0 or k > n - 1:
            return 0

        gaps = n - 1
        ans = self._comb(gaps, k)
        ans = (ans * (m % self.MOD)) % self.MOD
        ans = (ans * pow((m - 1) % self.MOD, gaps - k, self.MOD)) % self.MOD
        return ans


if __name__ == "__main__":
    from itertools import product

    sol = Solution()

    assert sol.countGoodArrays(3, 2, 1) == 4
    assert sol.countGoodArrays(4, 2, 2) == 6
    assert sol.countGoodArrays(5, 2, 0) == 2

    for n in range(1, 6):
        for m in range(1, 4):
            for k in range(n):
                expected = 0
                for arr in product(range(1, m + 1), repeat=n):
                    if sum(arr[i] == arr[i + 1] for i in range(n - 1)) == k:
                        expected += 1
                assert sol.countGoodArrays(n, m, k) == expected

    assert sol.countGoodArrays(1, 1, 0) == 1
    assert sol.countGoodArrays(1, 100000, 0) == 100000
    assert sol.countGoodArrays(5, 1, 4) == 1
    assert sol.countGoodArrays(5, 1, 3) == 0
    assert sol.countGoodArrays(100000, 1, 99999) == 1
    assert sol.countGoodArrays(100000, 1, 99998) == 0

    print("All tests passed")