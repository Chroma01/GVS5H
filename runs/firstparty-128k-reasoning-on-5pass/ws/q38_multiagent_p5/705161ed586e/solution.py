import itertools
import random
import time


class Solution:
    def minCostGoodCaption(self, caption: str) -> str:
        n = len(caption)
        if n < 3:
            return ""

        INF = 10 ** 9
        A = 26
        S = A * 3

        codes = [ord(ch) - 97 for ch in caption]
        cost_rows = [[abs(i - j) for j in range(A)] for i in range(A)]
        bases = [c * 3 for c in range(A)]
        letters = [chr(97 + i) for i in range(A)]

        # row represents G[i+1] while computing G[i].
        # Index c*3 + (k-1) is state (previous char c, current run length k capped at 3).
        row = [INF] * S
        for c in range(A):
            row[bases[c] + 2] = 0

        # Only k == 3 states need a stored decision; k == 1 or 2 are forced to repeat.
        choices = bytearray(n * A)

        for i in range(n - 1, 0, -1):
            cost = cost_rows[codes[i]]

            # Top two values for starting a new run at i:
            # value[d] = cost(i, d) + G[i+1][d][1].
            # We need the best value for each previous char c, excluding d == c.
            b1v = INF
            b1c = 255
            b2v = INF
            b2c = 255

            for d in range(A):
                v = row[bases[d]] + cost[d]
                if v >= INF:
                    v = INF

                if v < b1v:
                    b2v, b2c = b1v, b1c
                    b1v, b1c = v, d
                elif v == b1v:
                    if v < b2v:
                        b2v, b2c = v, d
                elif v < b2v:
                    b2v, b2c = v, d

            cur = [INF] * S
            off = i * A

            for c in range(A):
                base = bases[c]
                cc = cost[c]

                # State k = 1: must repeat c, next k = 2.
                v1 = row[base + 1] + cc
                if v1 >= INF:
                    v1 = INF
                cur[base] = v1

                # State k = 2: must repeat c, next k = 3.
                v2 = row[base + 2] + cc
                if v2 >= INF:
                    v2 = INF
                cur[base + 1] = v2

                # State k = 3: may repeat c, or switch to a different char.
                same = v2

                if c != b1c:
                    sw = b1v
                    swc = b1c
                else:
                    sw = b2v
                    swc = b2c

                if same < sw:
                    v3 = same
                    ch = c
                elif sw < same:
                    v3 = sw
                    ch = swc
                else:
                    v3 = same
                    if v3 >= INF:
                        ch = 255
                    else:
                        ch = c if c < swc else swc

                cur[base + 2] = v3
                choices[off + c] = ch

            row = cur

        # Choose the first character. After choosing c, state is (1, c, 1).
        cost0 = cost_rows[codes[0]]
        total = INF
        first = 255
        for c in range(A):
            v = row[bases[c]] + cost0[c]
            if v >= INF:
                v = INF
            if v < total:
                total = v
                first = c

        if total >= INF:
            return ""

        res = [letters[first]]
        prev = first
        k = 1

        for i in range(1, n):
            if k == 3:
                ch = choices[i * A + prev]
                if ch >= A:
                    return ""
            else:
                ch = prev

            res.append(letters[ch])

            if ch == prev:
                if k < 3:
                    k += 1
            else:
                k = 1
            prev = ch

        return ''.join(res)


_GOOD_CACHE = {}


def _good_data(n: int):
    if n in _GOOD_CACHE:
        return _GOOD_CACHE[n]

    strs = []

    def rec(pos: int, prev: int, cur: list) -> None:
        if pos == n:
            strs.append(''.join(cur))
            return
        for length in range(3, n - pos + 1):
            for ch in range(26):
                if ch == prev:
                    continue
                cur.append(chr(97 + ch) * length)
                rec(pos + length, ch, cur)
                cur.pop()

    rec(0, -1, [])
    strs.sort()
    codes = [[ord(ch) - 97 for ch in s] for s in strs]
    _GOOD_CACHE[n] = (strs, codes)
    return _GOOD_CACHE[n]


def brute_force(caption: str) -> str:
    n = len(caption)
    if n < 3:
        return ""

    codes = [ord(ch) - 97 for ch in caption]
    strs, gcs = _good_data(n)

    best_cost = 10 ** 9
    best = ""
    abs_ = abs

    for s, g in zip(strs, gcs):
        cost = 0
        for j in range(n):
            cost += abs_(codes[j] - g[j])
            if cost >= best_cost:
                break
        if cost < best_cost:
            best_cost = cost
            best = s

    return best


def run_tests() -> None:
    sol = Solution()

    fixed = {
        "cdcd": "cccc",
        "aca": "aaa",
        "bc": "",

        "a": "",
        "z": "",
        "aa": "",
        "zz": "",
        "az": "",
        "za": "",

        "aaa": "aaa",
        "bbb": "bbb",
        "zzz": "zzz",
        "aba": "aaa",
        "bab": "bbb",

        "aaaa": "aaaa",
        "bbbb": "bbbb",
        "aabb": "aaaa",
        "bbaa": "aaaa",
        "azaz": "aaaa",
        "yyzz": "yyyy",

        "abcde": "ccccc",
        "azaza": "aaaaa",
        "zzazz": "zzzzz",

        "aaaaaa": "aaaaaa",
        "zzzzzz": "zzzzzz",
        "aaabbb": "aaabbb",
        "bbbaaa": "bbbaaa",
        "aaazzz": "aaazzz",
        "zzzaaa": "zzzaaa",
        "ababab": "aaabbb",
        "bababa": "bbbaaa",
        "azazaz": "aaazzz",

        "aaabbbb": "aaabbbb",
        "aaaabbb": "aaaabbb",

        "aaabbbbb": "aaabbbbb",
        "aaaaabbb": "aaaaabbb",
        "aaaabbbb": "aaaabbbb",

        "aaabbbccc": "aaabbbccc",
    }

    for s, expected in fixed.items():
        got = sol.minCostGoodCaption(s)
        if got != expected:
            raise AssertionError(f"fixed mismatch for {s}: got {got}, expected {expected}")

    # Exhaustive small-alphabet checks.
    for n in range(1, 9):
        for tup in itertools.product("ab", repeat=n):
            s = ''.join(tup)
            expected = brute_force(s)
            got = sol.minCostGoodCaption(s)
            if got != expected:
                raise AssertionError(f"binary mismatch for {s}: got {got}, expected {expected}")

    for n in range(3, 7):
        for tup in itertools.product("abc", repeat=n):
            s = ''.join(tup)
            expected = brute_force(s)
            got = sol.minCostGoodCaption(s)
            if got != expected:
                raise AssertionError(f"ternary mismatch for {s}: got {got}, expected {expected}")

    # Random full-alphabet small checks.
    rng = random.Random(12345)
    alphabet = "abcdefghijklmnopqrstuvwxyz"

    for _ in range(200):
        n = rng.randint(3, 8)
        s = ''.join(rng.choice(alphabet) for _ in range(n))
        expected = brute_force(s)
        got = sol.minCostGoodCaption(s)
        if got != expected:
            raise AssertionError(f"random mismatch for {s}: got {got}, expected {expected}")

    for _ in range(10):
        s = ''.join(rng.choice(alphabet) for _ in range(9))
        expected = brute_force(s)
        got = sol.minCostGoodCaption(s)
        if got != expected:
            raise AssertionError(f"random length-9 mismatch for {s}: got {got}, expected {expected}")

    print("pass")


def run_performance() -> None:
    sol = Solution()
    n = 50000

    # Tie-heavy deterministic large input.
    s = "az" * (n // 2)

    t0 = time.perf_counter()
    res = sol.minCostGoodCaption(s)
    t1 = time.perf_counter()

    if len(res) != n:
        raise AssertionError("performance result length mismatch")

    # Verify the result is a good caption.
    i = 0
    while i < n:
        j = i + 1
        while j < n and res[j] == res[i]:
            j += 1
        if j - i < 3:
            raise AssertionError("performance result is not a good caption")
        i = j

    cost = 0
    for a, b in zip(s, res):
        cost += abs(ord(a) - ord(b))

    print(f"performance n={n} time={t1 - t0:.3f}s cost={cost}")


if __name__ == "__main__":
    run_tests()
    run_performance()