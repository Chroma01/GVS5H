MOD = 10**9 + 7


class Solution:
    def countGoodArrays(self, n: int, m: int, k: int) -> int:
        if k < 0 or k > n - 1:
            return 0
        N = n  # need factorials up to n-1
        fact = [1] * (N + 1)
        for i in range(1, N + 1):
            fact[i] = fact[i - 1] * i % MOD
        inv_fact = [1] * (N + 1)
        inv_fact[N] = pow(fact[N], MOD - 2, MOD)
        for i in range(N, 0, -1):
            inv_fact[i - 1] = inv_fact[i] * i % MOD

        comb = fact[n - 1] * inv_fact[k] % MOD * inv_fact[n - 1 - k] % MOD
        return m % MOD * comb % MOD * pow((m - 1) % MOD, n - 1 - k, MOD) % MOD


if __name__ == "__main__":
    s = Solution()
    assert s.countGoodArrays(3, 2, 1) == 4
    assert s.countGoodArrays(4, 2, 2) == 6
    assert s.countGoodArrays(5, 2, 0) == 2

    # brute force validation
    from itertools import product

    def brute(n, m, k):
        c = 0
        for arr in product(range(1, m + 1), repeat=n):
            if sum(1 for i in range(1, n) if arr[i - 1] == arr[i]) == k:
                c += 1
        return c

    for n in range(1, 7):
        for m in range(1, 5):
            for k in range(0, n):
                assert brute(n, m, k) == s.countGoodArrays(n, m, k), (n, m, k)
    print("ok")