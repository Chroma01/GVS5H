class Solution:
    def makeStringGood(self, s: str) -> int:
        cnt = [0] * 26
        for ch in s:
            cnt[ord(ch) - 97] += 1

        n = len(s)
        if n == 0:
            return 0

        INF = 10**18
        ans = INF

        for k in range(1, n + 1):
            c0 = cnt[0]

            # dp00: previous letter choice 0, no letter chosen yet
            # dp01: previous letter choice 0, some earlier letter chosen
            # dp11: previous letter choice 1, some letter chosen
            dp00 = c0
            dp01 = INF
            dp11 = c0 - k if c0 < k else k - c0

            for i in range(1, 26):
                ci = cnt[i]
                cp = cnt[i - 1]

                if ci < k:
                    u1 = k - ci
                    d = u1

                    # prev choice 0, current choice 1
                    save01 = cp if cp < d else d

                    # prev choice 1, current choice 1
                    left = cp - k if cp > k else 0
                    save11 = left if left < d else d
                else:
                    u1 = ci - k
                    save01 = 0
                    save11 = 0

                add01 = u1 - save01
                add11 = u1 - save11

                # Choose current letter absent.
                ndp00 = dp00 + ci
                m01 = dp01 if dp01 < dp11 else dp11
                ndp01 = m01 + ci

                # Choose current letter present.
                m0 = dp00 if dp00 < dp01 else dp01
                v0 = m0 + add01
                v1 = dp11 + add11
                ndp11 = v0 if v0 < v1 else v1

                dp00, dp01, dp11 = ndp00, ndp01, ndp11

            cost = dp01 if dp01 < dp11 else dp11
            if cost < ans:
                ans = cost
                if ans == 0:
                    break

        return ans


def _exact_fixed_cost(c, f, A):
    """Exact min cost to transform counts c into fixed target counts f."""
    n = sum(c)
    INF = 10**18
    dp = [INF] * (n + 1)
    dp[0] = 0

    for i in range(A):
        ci = c[i]
        fi = f[i]
        ndp = [INF] * (n + 1)
        last = (i == A - 1)

        for carry in range(n + 1):
            val = dp[carry]
            if val >= INF:
                continue

            avail = ci + carry
            max_y = 0 if last else min(avail, n)

            for y in range(max_y + 1):
                cost = val + y + abs(avail - fi - y)
                if cost < ndp[y]:
                    ndp[y] = cost

        dp = ndp

    return dp[0]


def _brute_force(s: str) -> int:
    """Small-string cross-check using exact fixed-target DP and enumeration."""
    cnt26 = [0] * 26
    for ch in s:
        cnt26[ord(ch) - 97] += 1

    n = len(s)
    if n == 0:
        return 0

    max_idx = max(i for i, v in enumerate(cnt26) if v)

    # Absent letters cannot strictly improve the optimum. For small alphabets,
    # allow one extra letter to the right as a safety margin.
    if max_idx <= 5:
        A = max_idx + 2
        candidates = list(range(A))
        cnt = cnt26[:A]
    else:
        A = 26
        candidates = [i for i, v in enumerate(cnt26) if v]
        cnt = cnt26

    INF = 10**18
    best = INF

    for k in range(1, 2 * n + 1):
        for mask in range(1, 1 << len(candidates)):
            f = [0] * A
            for idx, i in enumerate(candidates):
                if mask & (1 << idx):
                    f[i] = k

            cost = _exact_fixed_cost(cnt, f, A)
            if cost < best:
                best = cost

    return best


def _run_checks():
    sol = Solution()

    examples = [
        ("acab", 1),
        ("wddw", 0),
        ("aaabc", 2),
    ]

    for s, expected in examples:
        got = sol.makeStringGood(s)
        if got != expected:
            raise AssertionError(f"example {s}: got {got}, expected {expected}")

    import itertools

    for length in range(1, 6):
        for tup in itertools.product("abc", repeat=length):
            s = "".join(tup)
            expected = _brute_force(s)
            got = sol.makeStringGood(s)
            if got != expected:
                raise AssertionError(f"mismatch for {s}: got {got}, brute {expected}")

    for s in ["zzz", "azzz", "zzza", "yyzz", "yzz", "zzzy", "zzzz", "az", "za", "yz"]:
        expected = _brute_force(s)
        got = sol.makeStringGood(s)
        if got != expected:
            raise AssertionError(f"mismatch for {s}: got {got}, brute {expected}")

    print("All checks passed")


def _verify() -> bool:
    sol = Solution()

    examples = [
        ("acab", 1),
        ("wddw", 0),
        ("aaabc", 2),
    ]

    for s, expected in examples:
        got = sol.makeStringGood(s)
        if got != expected:
            print(f"VERDICT: FAIL example {s!r}: got {got}, expected {expected}")
            return False

    import io
    import contextlib

    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            _run_checks()
    except Exception as e:
        print(f"VERDICT: FAIL _run_checks: {e}")
        return False

    if buf.getvalue().strip() != "All checks passed":
        print(f"VERDICT: FAIL _run_checks output: {buf.getvalue()!r}")
        return False

    import itertools

    memo = {}
    total = 0

    for length in range(1, 6):
        for tup in itertools.product("abcd", repeat=length):
            s = "".join(tup)
            total += 1

            cnt = [0] * 4
            for ch in s:
                cnt[ord(ch) - 97] += 1

            key = tuple(cnt)
            if key not in memo:
                n = sum(key)
                best = 10**18
                for k in range(0, 2 * n + 1):
                    for mask in range(16):
                        f = [0] * 4
                        for i in range(4):
                            if (mask >> i) & 1:
                                f[i] = k
                        cost = _exact_fixed_cost(cnt, f, 4)
                        if cost < best:
                            best = cost
                memo[key] = best

            expected = memo[key]
            got = sol.makeStringGood(s)
            if got != expected:
                print(f"VERDICT: FAIL exhaustive {s!r}: got {got}, expected {expected}")
                return False

    print(f"VERDICT: PASS examples, _run_checks, and {total} strings over 'a'..'d' length 1..5 all match")
    return True


if __name__ == "__main__":
    import sys
    sys.exit(0 if _verify() else 1)