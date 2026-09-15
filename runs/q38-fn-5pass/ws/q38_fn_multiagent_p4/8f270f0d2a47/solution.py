class Solution:
    def beautifulNumbers(self, l: int, r: int) -> int:
        # Maximum digit sum we may need to consider.
        # Under the constraints this is at most 81; using 9 * len(str(r))
        # also safely handles r == 10^9 if it appears in tests.
        max_sum_global = 9 * len(str(r))

        # For each possible digit sum s, store the exponents of 2, 3, 5, 7
        # required for a product to be divisible by s. If after removing
        # 2, 3, 5, 7 something remains, s has a prime factor > 7.
        req2 = [0] * (max_sum_global + 1)
        req3 = [0] * (max_sum_global + 1)
        req5 = [0] * (max_sum_global + 1)
        req7 = [0] * (max_sum_global + 1)
        large = [False] * (max_sum_global + 1)

        for s in range(1, max_sum_global + 1):
            x = s
            while x % 2 == 0:
                req2[s] += 1
                x //= 2
            while x % 3 == 0:
                req3[s] += 1
                x //= 3
            while x % 5 == 0:
                req5[s] += 1
                x //= 5
            while x % 7 == 0:
                req7[s] += 1
                x //= 7
            large[s] = (x != 1)

        cap2 = max(req2)
        cap3 = max(req3)
        cap5 = max(req5)
        cap7 = max(req7)

        # Prime-exponent contribution of each digit.
        raw2 = [0] * 10
        raw3 = [0] * 10
        raw5 = [0] * 10
        raw7 = [0] * 10

        for d in range(1, 10):
            x = d
            while x % 2 == 0:
                raw2[d] += 1
                x //= 2
            while x % 3 == 0:
                raw3[d] += 1
                x //= 3
            while x % 5 == 0:
                raw5[d] += 1
                x //= 5
            while x % 7 == 0:
                raw7[d] += 1
                x //= 7

        # Capped transition tables for exponents.
        next2 = [[0] * 10 for _ in range(cap2 + 1)]
        for e in range(cap2 + 1):
            row = next2[e]
            for d in range(10):
                v = e + raw2[d]
                row[d] = cap2 if v > cap2 else v

        next3 = [[0] * 10 for _ in range(cap3 + 1)]
        for e in range(cap3 + 1):
            row = next3[e]
            for d in range(10):
                v = e + raw3[d]
                row[d] = cap3 if v > cap3 else v

        next5 = [[0] * 10 for _ in range(cap5 + 1)]
        for e in range(cap5 + 1):
            row = next5[e]
            for d in range(10):
                v = e + raw5[d]
                row[d] = cap5 if v > cap5 else v

        next7 = [[0] * 10 for _ in range(cap7 + 1)]
        for e in range(cap7 + 1):
            row = next7[e]
            for d in range(10):
                v = e + raw7[d]
                row[d] = cap7 if v > cap7 else v

        # Capped transition table for digit sum.
        next_sum = [[-1] * 10 for _ in range(max_sum_global + 1)]
        for s in range(max_sum_global + 1):
            row = next_sum[s]
            for d in range(10):
                v = s + d
                if v <= max_sum_global:
                    row[d] = v

        SHIFT = 50
        MASK = (1 << SHIFT) - 1

        def count_up_to(n: int) -> int:
            if n <= 0:
                return 0

            digits = tuple(map(int, str(n)))
            L = len(digits)
            max_sum = 9 * L

            sum_dim = max_sum + 1
            dim2 = cap2 + 1
            dim3 = cap3 + 1
            dim5 = cap5 + 1
            dim7 = cap7 + 1

            memo = {}

            def dp(pos: int, tight: int, started: int, s: int,
                   e2: int, e3: int, e5: int, e7: int) -> int:
                key = (((((((pos * 2 + tight) * 2 + started) * sum_dim + s)
                          * dim2 + e2) * dim3 + e3) * dim5 + e5) * dim7 + e7)

                cached = memo.get(key)
                if cached is not None:
                    return cached

                if pos == L:
                    if started:
                        total = 1
                        if (not large[s] and
                            e2 >= req2[s] and
                            e3 >= req3[s] and
                            e5 >= req5[s] and
                            e7 >= req7[s]):
                            beautiful = 1
                        else:
                            beautiful = 0
                    else:
                        total = 0
                        beautiful = 0

                    res = (total << SHIFT) | beautiful
                    memo[key] = res
                    return res

                limit = digits[pos] if tight else 9
                total = 0
                beautiful = 0

                if not started:
                    # Keep using leading zeros.
                    ntight = 1 if (tight and limit == 0) else 0
                    res = dp(pos + 1, ntight, 0, 0, 0, 0, 0, 0)
                    total += res >> SHIFT
                    beautiful += res & MASK

                    # Start the number with a non-zero digit.
                    for d in range(1, limit + 1):
                        ns = next_sum[0][d]
                        ntight = 1 if (tight and d == limit) else 0
                        res = dp(
                            pos + 1,
                            ntight,
                            1,
                            ns,
                            next2[0][d],
                            next3[0][d],
                            next5[0][d],
                            next7[0][d],
                        )
                        total += res >> SHIFT
                        beautiful += res & MASK
                else:
                    # Count only zero-free numbers here; numbers containing
                    # digit 0 are handled outside this DP.
                    for d in range(1, limit + 1):
                        ns = next_sum[s][d]
                        if ns < 0:
                            continue

                        ntight = 1 if (tight and d == limit) else 0
                        res = dp(
                            pos + 1,
                            ntight,
                            1,
                            ns,
                            next2[e2][d],
                            next3[e3][d],
                            next5[e5][d],
                            next7[e7][d],
                        )
                        total += res >> SHIFT
                        beautiful += res & MASK

                res = (total << SHIFT) | beautiful
                memo[key] = res
                return res

            res = dp(0, 1, 0, 0, 0, 0, 0, 0)
            zero_free_total = res >> SHIFT
            zero_free_beautiful = res & MASK

            # Every positive number containing digit 0 is beautiful.
            return n - zero_free_total + zero_free_beautiful

        return count_up_to(r) - count_up_to(l - 1)