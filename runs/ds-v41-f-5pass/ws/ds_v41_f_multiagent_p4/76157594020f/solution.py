from itertools import product


class Solution:
    def minLength(self, s: str, numOps: int) -> int:
        n = len(s)

        def feasible(L: int) -> bool:
            if L == 1:
                # Only alternating strings have all runs of length 1.
                # The two patterns are complements, so mismatches sum to n.
                m1 = 0
                for i, ch in enumerate(s):
                    a = '0' if (i & 1) == 0 else '1'
                    if ch != a:
                        m1 += 1
                return min(m1, n - m1) <= numOps

            # For L >= 2, each maximal run of length `len` costs
            # exactly len // (L+1) interior flips, and runs are independent.
            total = 0
            i = 0
            while i < n:
                j = i
                while j < n and s[j] == s[i]:
                    j += 1
                total += (j - i) // (L + 1)
                if total > numOps:
                    return False
                i = j
            return True

        lo, hi = 1, n
        while lo < hi:
            mid = (lo + hi) // 2
            if feasible(mid):
                hi = mid
            else:
                lo = mid + 1
        return lo


def brute_all(s):
    """Return best[k] = min possible longest-run using at most k flips."""
    n = len(s)
    INF = n + 1
    exact = [INF] * (n + 1)
    for mask in range(1 << n):
        f = bin(mask).count('1')
        chars = list(s)
        for i in range(n):
            if (mask >> i) & 1:
                chars[i] = '1' if chars[i] == '0' else '0'
        mr = 1
        cur = 1
        for i in range(1, n):
            if chars[i] == chars[i - 1]:
                cur += 1
            else:
                cur = 1
            if cur > mr:
                mr = cur
        if mr < exact[f]:
            exact[f] = mr
    res = [INF] * (n + 1)
    best = INF
    for k in range(n + 1):
        if exact[k] < best:
            best = exact[k]
        res[k] = best
    return res


def main():
    sol = Solution()

    # Official examples
    official = [("000001", 1, 2), ("0000", 2, 1), ("0101", 0, 1)]
    all_ok = True
    for s, k, exp in official:
        got = sol.minLength(s, k)
        ok = got == exp
        all_ok &= ok
        print(f"official  s={s!r} numOps={k} got={got} exp={exp} {'OK' if ok else 'FAIL'}")

    # Extra hand-checked cases (corrected expectations)
    extra = [
        ("0", 0, 1),            # n = 1
        ("0011", 0, 2),         # numOps = 0 -> original max run
        ("0000", 4, 1),         # numOps = n -> forced alternating
        ("0110", 1, 2),         # L=1 needs 2 flips -> answer 2
        ("0000000000", 3, 2),   # 10 zeros, 3 flips -> L=2
    ]
    for s, k, exp in extra:
        got = sol.minLength(s, k)
        ok = got == exp
        all_ok &= ok
        print(f"explicit  s={s!r} numOps={k} got={got} exp={exp} {'OK' if ok else 'FAIL'}")

    # Brute-force validation: all binary strings length 1..9, all numOps in [0, n]
    comparisons = 0
    mismatches = []
    for n in range(1, 10):
        for tup in product("01", repeat=n):
            s = "".join(tup)
            exp_list = brute_all(s)
            for k in range(n + 1):
                got = sol.minLength(s, k)
                exp = exp_list[k]
                comparisons += 1
                if got != exp:
                    mismatches.append((s, k, got, exp))

    print(f"brute-force comparisons={comparisons} mismatches={len(mismatches)}")
    for m in mismatches[:20]:
        print("MISMATCH", m)

    verdict = "PASS" if (all_ok and not mismatches) else "FAIL"
    print("VERDICT:", verdict)


if __name__ == "__main__":
    main()