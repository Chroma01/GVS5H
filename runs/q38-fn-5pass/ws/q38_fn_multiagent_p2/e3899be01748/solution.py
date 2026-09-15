_TRANS = [[None] * 10 for _ in range(10)]
for _d in range(1, 10):
    for _c in range(10):
        _TRANS[_d][_c] = tuple((_r * 10 + _c) % _d for _r in range(_d))


class Solution:
    def countSubstrings(self, s: str) -> int:
        digits = [ord(ch) - 48 for ch in s]
        present = [False] * 10
        for c in digits:
            present[c] = True

        ans = 0
        trans_all = _TRANS

        for d in range(1, 10):
            if not present[d]:
                continue

            cnt = [0] * d
            trans_d = trans_all[d]

            for c in digits:
                nxt = [0] * d
                mapping = trans_d[c]

                # Extend all substrings that ended at the previous position.
                for r, target in enumerate(mapping):
                    nxt[target] += cnt[r]

                # Add the new one-digit substring.
                nxt[c % d] += 1

                # If the current digit is the divisor, count divisible endings.
                if c == d:
                    ans += nxt[0]

                cnt = nxt

        return ans


def _brute_count(s: str) -> int:
    n = len(s)
    ans = 0
    for i in range(n):
        value = 0
        for j in range(i, n):
            digit = ord(s[j]) - 48
            value = value * 10 + digit
            if digit != 0 and value % digit == 0:
                ans += 1
    return ans


def _run_tests() -> bool:
    sol = Solution()
    n = 100000

    long_ones = "1" * n
    long_nines = "9" * n
    long_alternating = "10" * (n // 2)

    tests = [
        # Provided examples.
        ("12936", 11),
        ("5701283", 18),
        ("1010101010", 25),

        # Edge cases.
        ("0", 0),
        ("000", 0),
        ("1", 1),
        ("9", 1),
        ("0001", 4),
        ("10", 1),
        ("01", 2),
        ("12", 3),
        ("111", 6),
        ("999", 6),
        ("0" * 100, 0),

        # Long repeated patterns.
        (long_ones, n * (n + 1) // 2),
        (long_nines, n * (n + 1) // 2),
        (long_alternating, (n // 2) * (n // 2)),
    ]

    for s, expected in tests:
        got = sol.countSubstrings(s)
        if got != expected:
            label = s if len(s) <= 20 else f"{s[:10]}...{s[-10:]} (len={len(s)})"
            print(f"FAIL: {label} expected={expected} got={got}")
            return False

    # Exhaustive small validation against brute force.
    from itertools import product
    for length in range(1, 5):
        for tup in product("0123456789", repeat=length):
            s = "".join(tup)
            expected = _brute_count(s)
            got = sol.countSubstrings(s)
            if got != expected:
                print(f"FAIL brute: {s} expected={expected} got={got}")
                return False

    print("Sample tests: pass")
    print("Edge tests: pass")
    print("Brute-force small tests: pass")
    return True


if __name__ == "__main__":
    _run_tests()