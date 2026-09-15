from functools import lru_cache

class Solution:
    def beautifulNumbers(self, l: int, r: int) -> int:
        M = len(str(r))

        def max_digit_sum(n: int) -> int:
            if n <= 0:
                return 0
            s = str(n)
            m = len(s)
            best = 0
            prefix = 0
            for i, ch in enumerate(s):
                d = ord(ch) - 48
                if d > 0:
                    cand = prefix + (d - 1) + 9 * (m - i - 1)
                    if cand > best:
                        best = cand
                prefix += d
            if prefix > best:
                best = prefix
            return best

        max_sum = max_digit_sum(r)
        if max_sum == 0:
            return 0

        pow9 = [1] * (M + 1)
        for i in range(1, M + 1):
            pow9[i] = pow9[i - 1] * 9

        def count_no_zero(n: int) -> int:
            if n <= 0:
                return 0
            s = str(n)
            m = len(s)
            total = 0
            for length in range(1, m):
                total += pow9[length]
            for i, ch in enumerate(s):
                d = ord(ch) - 48
                choices = d - 1
                if choices > 0:
                    total += choices * pow9[m - i - 1]
                if d == 0:
                    return total
            return total + 1

        def count_with_zero(n: int) -> int:
            if n <= 0:
                return 0
            return n - count_no_zero(n)

        smooth = []
        for s in range(1, max_sum + 1):
            x = s
            for p in (2, 3, 5, 7):
                while x % p == 0:
                    x //= p
            if x == 1:
                smooth.append(s)

        rem_max = [9 * (M - pos) for pos in range(M + 1)]
        min_rem = [M - pos for pos in range(M + 1)]
        digits19 = range(1, 10)

        zero_free_total = 0

        for S in smooth:
            first_mod = [d % S for d in range(10)]
            mul_mod = [[(p * d) % S for d in range(10)] for p in range(S)]

            @lru_cache(maxsize=None)
            def free(pos, sum_so_far, prod_mod, started,
                     S=S, rem_max=rem_max, min_rem=min_rem,
                     first_mod=first_mod, mul_mod=mul_mod,
                     M=M, digits19=digits19):
                if sum_so_far > S:
                    return 0
                if sum_so_far + rem_max[pos] < S:
                    return 0
                if started and sum_so_far + min_rem[pos] > S:
                    return 0
                if pos == M:
                    return 1 if started and sum_so_far == S and prod_mod == 0 else 0

                res = 0
                rem_after = rem_max[pos + 1]
                min_after = min_rem[pos + 1]

                if not started:
                    if sum_so_far + rem_after >= S:
                        res += free(pos + 1, sum_so_far, 0, False)
                    for d in digits19:
                        ns = sum_so_far + d
                        if ns + min_after <= S and ns + rem_after >= S:
                            res += free(pos + 1, ns, first_mod[d], True)
                else:
                    for d in digits19:
                        ns = sum_so_far + d
                        if ns + min_after <= S and ns + rem_after >= S:
                            res += free(pos + 1, ns, mul_mod[prod_mod][d], True)
                return res

            def count_bound(n: int) -> int:
                if n <= 0:
                    return 0
                digits = tuple(int(c) for c in str(n).zfill(M))

                def dfs(pos, sum_so_far, prod_mod, tight, started,
                        digits=digits, S=S, rem_max=rem_max, min_rem=min_rem,
                        first_mod=first_mod, mul_mod=mul_mod, M=M,
                        free=free):
                    if not tight:
                        return free(pos, sum_so_far, prod_mod, started)
                    if sum_so_far > S:
                        return 0
                    if sum_so_far + rem_max[pos] < S:
                        return 0
                    if started and sum_so_far + min_rem[pos] > S:
                        return 0
                    if pos == M:
                        return 1 if started and sum_so_far == S and prod_mod == 0 else 0

                    limit = digits[pos]
                    res = 0
                    rem_after = rem_max[pos + 1]
                    min_after = min_rem[pos + 1]

                    if not started:
                        if sum_so_far + rem_after >= S:
                            if limit == 0:
                                res += dfs(pos + 1, sum_so_far, 0, True, False)
                            else:
                                res += free(pos + 1, sum_so_far, 0, False)

                        for d in range(1, limit + 1):
                            ns = sum_so_far + d
                            if ns + min_after <= S and ns + rem_after >= S:
                                if d == limit:
                                    res += dfs(pos + 1, ns, first_mod[d], True, True)
                                else:
                                    res += free(pos + 1, ns, first_mod[d], True)
                    else:
                        for d in range(1, limit + 1):
                            ns = sum_so_far + d
                            if ns + min_after <= S and ns + rem_after >= S:
                                np = mul_mod[prod_mod][d]
                                if d == limit:
                                    res += dfs(pos + 1, ns, np, True, True)
                                else:
                                    res += free(pos + 1, ns, np, True)
                    return res

                return dfs(0, 0, 0, True, False)

            zero_free_total += count_bound(r) - count_bound(l - 1)
            free.cache_clear()

        zero_total = count_with_zero(r) - count_with_zero(l - 1)
        return zero_total + zero_free_total