from itertools import combinations_with_replacement


class Solution:
    _fact = None
    _pow9 = None
    _prefix_pow9 = None
    _beautiful_by_len = None
    _prefix_totals = None

    @classmethod
    def _precompute(cls):
        if cls._fact is not None:
            return

        fact = [1] * 11
        for i in range(1, 11):
            fact[i] = fact[i - 1] * i

        pow9 = [1] * 11
        for i in range(1, 11):
            pow9[i] = pow9[i - 1] * 9

        prefix_pow9 = [0] * 11
        for i in range(1, 11):
            prefix_pow9[i] = prefix_pow9[i - 1] + pow9[i]

        by_len = [[] for _ in range(11)]
        totals = [0] * 11
        digits = range(1, 10)

        for k in range(1, 11):
            for comb in combinations_with_replacement(digits, k):
                prod = 1
                sm = 0
                counts = [0] * 10

                for d in comb:
                    prod *= d
                    sm += d
                    counts[d] += 1

                if prod % sm == 0:
                    denom = 1
                    for c in counts:
                        denom *= fact[c]
                    total = fact[k] // denom

                    min_str = ''.join(str(d) * counts[d] for d in range(1, 10))
                    max_str = ''.join(str(d) * counts[d] for d in range(9, 0, -1))
                    minv = int(min_str)
                    maxv = int(max_str)

                    # Store counts compactly as a byte sequence.
                    by_len[k].append((bytes(counts), total, minv, maxv))
                    totals[k] += total

            by_len[k].sort(key=lambda x: x[2])

        prefix_totals = [0] * 11
        for i in range(1, 11):
            prefix_totals[i] = prefix_totals[i - 1] + totals[i]

        cls._fact = fact
        cls._pow9 = pow9
        cls._prefix_pow9 = prefix_pow9
        cls._beautiful_by_len = by_len
        cls._prefix_totals = prefix_totals

    def count_zero_free(self, n: int) -> int:
        if n <= 0:
            return 0

        if Solution._prefix_pow9 is None:
            Solution._precompute()

        s = str(n)
        m = len(s)

        # All zero-free numbers with fewer digits.
        ans = Solution._prefix_pow9[m - 1]
        pow9 = Solution._pow9

        # Zero-free numbers with the same length as n.
        for i, ch in enumerate(s):
            d = ord(ch) - 48
            rem = m - i - 1

            # Put a smaller non-zero digit here; remaining digits are arbitrary 1..9.
            if d > 1:
                ans += (d - 1) * pow9[rem]

            # Cannot continue matching a zero-free prefix through a zero digit.
            if d == 0:
                return ans

        # n itself is zero-free.
        return ans + 1

    def count_perm_leq(self, counts, total: int, k: int, n: int) -> int:
        if n <= 0:
            return 0

        s = str(n)
        m = len(s)

        if k > m:
            return 0
        if k < m:
            return total

        rem_counts = list(counts)
        rem_total = total
        ans = 0

        for pos, ch in enumerate(s):
            limit = ord(ch) - 48
            rem_len = k - pos

            # Choose a smaller non-zero digit at this position.
            for d in range(1, limit):
                c = rem_counts[d]
                if c:
                    ans += rem_total * c // rem_len

            # If the bound digit cannot be used, no exact-prefix continuation exists.
            if limit == 0 or rem_counts[limit] == 0:
                return ans

            # Fix the bound digit and update the number of permutations of the rest.
            rem_total = rem_total * rem_counts[limit] // rem_len
            rem_counts[limit] -= 1

        # The bound itself is one valid permutation.
        return ans + 1

    def count(self, n: int) -> int:
        if n <= 0:
            return 0

        if Solution._beautiful_by_len is None:
            Solution._precompute()

        zero_free = self.count_zero_free(n)

        # Every number containing digit 0 is beautiful because product = 0.
        res = n - zero_free
        m = len(str(n))

        # Fast path for 9, 99, 999, ...
        if m <= 10 and n == 10 ** m - 1:
            return res + Solution._prefix_totals[m]

        # Beautiful zero-free numbers with fewer digits are all <= n.
        res += Solution._prefix_totals[m - 1]

        # Beautiful zero-free numbers with the same digit length.
        for counts, total, minv, maxv in Solution._beautiful_by_len[m]:
            if minv > n:
                break
            if maxv <= n:
                res += total
            else:
                res += self.count_perm_leq(counts, total, m, n)

        return res

    def beautifulNumbers(self, l: int, r: int) -> int:
        if l > r:
            return 0
        return self.count(r) - self.count(l - 1)


if __name__ == "__main__":
    sol = Solution()

    # Provided samples.
    assert sol.beautifulNumbers(10, 20) == 2
    assert sol.beautifulNumbers(1, 15) == 10

    # Brute-force verification for small ranges.
    def is_beautiful(x: int) -> bool:
        prod = 1
        sm = 0
        y = x
        while y:
            d = y % 10
            prod *= d
            sm += d
            y //= 10
        return prod % sm == 0

    limit = 2000
    brute = [0] * (limit + 1)
    for x in range(1, limit + 1):
        brute[x] = brute[x - 1] + (1 if is_beautiful(x) else 0)

    for i in range(1, limit + 1):
        assert sol.count(i) == brute[i]

    assert sol.beautifulNumbers(1, limit) == brute[limit]