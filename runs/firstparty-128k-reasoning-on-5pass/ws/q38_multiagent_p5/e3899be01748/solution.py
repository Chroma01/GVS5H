import random
from itertools import product


class Solution:
    def countSubstrings(self, s: str) -> int:
        ans = 0

        cnt3 = [1, 0, 0]
        cnt9 = [1, 0, 0, 0, 0, 0, 0, 0, 0]
        cnt7 = [1, 0, 0, 0, 0, 0, 0]

        prefix3 = 0
        prefix9 = 0

        # Normalized prefix for divisibility by 7.
        # invpow is 5^(i+1) mod 7, where 5 is the inverse of 10 modulo 7.
        norm7 = 0
        invpow = 1
        inv10 = 5

        prev1 = -1
        prev2 = -1

        for i, ch in enumerate(s):
            d = ord(ch) - 48

            prefix3 = (prefix3 + d) % 3
            prefix9 = (prefix9 + d) % 9
            invpow = (invpow * inv10) % 7
            norm7 = (norm7 + d * invpow) % 7

            if d == 1 or d == 2 or d == 5:
                ans += i + 1
            elif d == 3 or d == 6:
                ans += cnt3[prefix3]
            elif d == 9:
                ans += cnt9[prefix9]
            elif d == 4:
                ans += 1
                if i >= 1 and (prev1 * 10 + 4) % 4 == 0:
                    ans += i
            elif d == 8:
                ans += 1
                if i >= 1 and (prev1 * 10 + 8) % 8 == 0:
                    ans += 1
                if i >= 2 and (prev2 * 100 + prev1 * 10 + 8) % 8 == 0:
                    ans += i - 1
            elif d == 7:
                ans += cnt7[norm7]

            cnt3[prefix3] += 1
            cnt9[prefix9] += 1
            cnt7[norm7] += 1

            prev2 = prev1
            prev1 = d

        return ans


def brute_count(s: str) -> int:
    digits = [ord(c) - 48 for c in s]
    n = len(digits)
    ans = 0

    for i in range(n):
        val = 0
        for j in range(i, n):
            val = val * 10 + digits[j]
            last = digits[j]
            if last != 0 and val % last == 0:
                ans += 1

    return ans


def run_tests() -> None:
    sol = Solution()
    mismatches = 0
    max_report = 20

    examples = [
        ("12936", 11),
        ("5701283", 18),
        ("1010101010", 25),
    ]

    for s, expected in examples:
        got = sol.countSubstrings(s)
        if got == expected:
            print(f"example s={s!r} expected={expected} got={got} ok")
        else:
            mismatches += 1
            if mismatches <= max_report:
                print(f"MISMATCH example s={s!r} expected={expected} got={got}")

    digits = "0123456789"

    # Exhaustive check for all short strings.
    for length in range(1, 6):
        for tup in product(digits, repeat=length):
            s = "".join(tup)
            expected = brute_count(s)
            got = sol.countSubstrings(s)
            if expected != got:
                mismatches += 1
                if mismatches <= max_report:
                    print(f"MISMATCH s={s!r} expected={expected} got={got}")
                if mismatches > max_report:
                    print(f"Too many mismatches; stopping after {max_report} reports.")
                    return

    # Random small strings.
    random.seed(12345)
    for _ in range(5000):
        length = random.randint(1, 8)
        s = "".join(random.choice(digits) for _ in range(length))
        expected = brute_count(s)
        got = sol.countSubstrings(s)
        if expected != got:
            mismatches += 1
            if mismatches <= max_report:
                print(f"MISMATCH s={s!r} expected={expected} got={got}")
            if mismatches > max_report:
                print(f"Too many mismatches; stopping after {max_report} reports.")
                return

    # Targeted edge cases.
    edge_cases = [
        "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
        "00", "000", "01", "04", "07", "08",
        "10", "100", "1000",
        "1234567890", "9876543210",
        "7777777777", "8888888888", "4444444444",
        "3333333333", "6666666666", "9999999999",
        "1010101010", "12345678901234567890",
    ]

    for s in edge_cases:
        expected = brute_count(s)
        got = sol.countSubstrings(s)
        if expected != got:
            mismatches += 1
            if mismatches <= max_report:
                print(f"MISMATCH s={s!r} expected={expected} got={got}")

    if mismatches == 0:
        print("All tests passed: examples, exhaustive length <= 5, random length <= 8, and edge cases matched.")
    else:
        print(f"Total mismatches: {mismatches}")


if __name__ == "__main__":
    run_tests()