import sys


class Solution:
    def beautifulNumbers(self, l: int, r: int) -> int:
        def count_upto(n: int) -> int:
            if n <= 0:
                return 0

            bound = str(n)
            L = len(bound)

            fact = [1] * (L + 1)
            for i in range(1, L + 1):
                fact[i] = fact[i - 1] * i

            powers = [[1] * (L + 1) for _ in range(10)]
            for d in range(1, 10):
                for c in range(1, L + 1):
                    powers[d][c] = powers[d][c - 1] * d

            def count_leq(counts, initial_denom):
                rem = counts[:]
                cur_denom = initial_denom
                ans = 0
                total = L

                for i, ch in enumerate(bound):
                    limit = ord(ch) - 48
                    rem_total = total - i

                    # Put a smaller non-zero digit here.
                    for d in range(1, limit):
                        c = rem[d]
                        if c:
                            ans += fact[rem_total - 1] * c // cur_denom

                    # Continue with the equal digit if possible.
                    if 1 <= limit <= 9:
                        c = rem[limit]
                        if c:
                            cur_denom //= c
                            rem[limit] = c - 1
                            continue

                    return ans

                return ans + 1

            counts = [0] * 10
            bad = 0

            def dfs(idx, remaining, length, digit_sum, product, denom):
                nonlocal bad

                if idx == 9:
                    if length > 0 and product % digit_sum != 0:
                        if length < L:
                            bad += fact[length] // denom
                        else:
                            bad += count_leq(counts, denom)
                    return

                d = idx + 1
                for c in range(remaining + 1):
                    counts[d] = c
                    dfs(
                        idx + 1,
                        remaining - c,
                        length + c,
                        digit_sum + c * d,
                        product * powers[d][c],
                        denom * fact[c],
                    )
                counts[d] = 0

            dfs(0, L, 0, 0, 1, 1)
            return n - bad

        return count_upto(r) - count_upto(l - 1)


def is_beautiful(x: int) -> bool:
    s = 0
    p = 1
    while x > 0:
        d = x % 10
        s += d
        p *= d
        x //= 10
    return p % s == 0


def run_checks() -> bool:
    sol = Solution()
    failures = []

    def check(name, actual, expected):
        if actual != expected:
            failures.append(f"{name}: actual={actual} expected={expected}")

    check("example1", sol.beautifulNumbers(10, 20), 2)
    check("example2", sol.beautifulNumbers(1, 15), 10)
    check("edge_1", sol.beautifulNumbers(1, 1), 1)
    check("edge_11", sol.beautifulNumbers(11, 11), 0)
    check("edge_10_20", sol.beautifulNumbers(10, 20), 2)
    check("edge_1_15", sol.beautifulNumbers(1, 15), 10)

    large = 999999999
    check("edge_large", sol.beautifulNumbers(large, large), 1 if is_beautiful(large) else 0)

    N = 2000
    brute_pref = [0] * (N + 1)
    for x in range(1, N + 1):
        y = x
        s = 0
        p = 1
        while y > 0:
            d = y % 10
            s += d
            p *= d
            y //= 10
        brute_pref[x] = brute_pref[x - 1] + (1 if p % s == 0 else 0)

    sol_pref = [0] * (N + 1)
    bn = sol.beautifulNumbers
    for n in range(1, N + 1):
        sol_pref[n] = bn(1, n)

    for n in range(1, N + 1):
        if sol_pref[n] != brute_pref[n]:
            failures.append(f"prefix n={n}: sol={sol_pref[n]} brute={brute_pref[n]}")
            break

    if not failures:
        M = 50
        for l in range(1, M + 1):
            for r in range(l, M + 1):
                expected = brute_pref[r] - brute_pref[l - 1]
                actual = bn(l, r)
                if actual != expected:
                    failures.append(f"direct l={l} r={r}: sol={actual} brute={expected}")
                    break
            if failures:
                break

    if not failures:
        sp = sol_pref
        bp = brute_pref
        expected_total = N * (N + 1) // 2

        for l in range(1, N + 1):
            sol_l = sp[l - 1]
            brute_l = bp[l - 1]
            for r in range(l, N + 1):
                if sp[r] - sol_l != bp[r] - brute_l:
                    failures.append(
                        f"range l={l} r={r}: sol={sp[r] - sol_l} brute={bp[r] - brute_l}"
                    )
                    break
            if failures:
                break

        if not failures:
            print("examples and edge cases: pass")
            print("direct small ranges 1..50: pass")
            print(f"all range differences 1..2000: pass ({expected_total}/{expected_total})")
            print("overall: pass")
            return True

    print("FAIL")
    for f in failures[:10]:
        print(f)
    return False


if __name__ == "__main__":
    sys.exit(0 if run_checks() else 1)