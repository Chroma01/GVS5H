class Solution:
    def countSubstrings(self, s: str) -> int:
        ans = 0

        # Counters for normalized prefix residues.
        # Index 0 starts with 1 to represent the empty prefix.
        cnt3 = [1, 0, 0]
        cnt9 = [1] + [0] * 8
        cnt7 = [1] + [0] * 6

        pref3 = pref9 = pref7 = 0
        inv10 = 1  # 10^(-processed_length) modulo 7; 10^(-1) == 5 mod 7

        # Last two digits, used for divisibility rules for 4 and 8.
        last1 = 0
        last2 = 0

        for i, ch in enumerate(s):
            d = ord(ch) - 48

            # Update all prefix state before counting substrings ending here.
            pref3 = (pref3 + d) % 3
            pref9 = (pref9 + d) % 9
            pref7 = (pref7 * 10 + d) % 7
            inv10 = (inv10 * 5) % 7
            q7 = (pref7 * inv10) % 7

            if d == 1 or d == 2 or d == 5:
                # Every substring ending here is divisible by 1, 2, or 5.
                ans += i + 1
            elif d == 4:
                # Single digit "4" is valid.
                ans += 1
                # For length >= 2, 10*p + 4 is divisible by 4 iff p is even.
                if i > 0 and (last1 & 1) == 0:
                    ans += i
            elif d == 8:
                # Single digit "8" is valid.
                ans += 1
                # Length 2: check the actual two-digit suffix.
                if i > 0 and (last1 * 10 + 8) % 8 == 0:
                    ans += 1
                # Length >= 3: if the last three digits are divisible by 8,
                # all longer substrings ending here are also divisible by 8.
                if i > 1 and (last2 * 100 + last1 * 10 + 8) % 8 == 0:
                    ans += i - 1
            elif d == 3 or d == 6:
                # Divisibility by 3 via digit-sum prefix residues.
                # Last digit 6 is automatically even, so modulo 3 is enough.
                ans += cnt3[pref3]
            elif d == 9:
                # Divisibility by 9 via digit-sum prefix residues.
                ans += cnt9[pref9]
            elif d == 7:
                # Divisibility by 7 via normalized prefix residues.
                ans += cnt7[q7]

            # Insert the current prefix for future substrings.
            cnt3[pref3] += 1
            cnt9[pref9] += 1
            cnt7[q7] += 1

            last2 = last1
            last1 = d

        return ans


def _brute(s: str) -> int:
    n = len(s)
    ans = 0
    for i in range(n):
        d = ord(s[i]) - 48
        if d == 0:
            continue

        val = 0
        mul = 1
        for j in range(i, -1, -1):
            val = (ord(s[j]) - 48) * mul + val
            if val % d == 0:
                ans += 1
            mul *= 10
    return ans


def _run_tests() -> None:
    sol = Solution()

    # Given examples.
    assert sol.countSubstrings("12936") == 11
    assert sol.countSubstrings("5701283") == 18
    assert sol.countSubstrings("1010101010") == 25

    # All single digits.
    for ch in "0123456789":
        assert sol.countSubstrings(ch) == _brute(ch)

    # All-zero strings.
    for n in range(1, 13):
        s = "0" * n
        assert sol.countSubstrings(s) == 0

    # Exhaustive small strings, including leading zeros.
    from itertools import product
    for n in range(1, 5):
        for tup in product("0123456789", repeat=n):
            s = "".join(tup)
            assert sol.countSubstrings(s) == _brute(s)

    # Random small strings, including leading zeros.
    import random
    rng = random.Random(12345)
    for _ in range(20000):
        n = rng.randint(1, 12)
        s = "".join(rng.choice("0123456789") for _ in range(n))
        assert sol.countSubstrings(s) == _brute(s)

    # Large-answer sanity check: every substring of all '1's is valid.
    n = 100000
    s = "1" * n
    assert sol.countSubstrings(s) == n * (n + 1) // 2


if __name__ == "__main__":
    _run_tests()