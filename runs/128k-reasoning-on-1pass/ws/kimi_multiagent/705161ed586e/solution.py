import random
import string
import time
from array import array


class Solution:
    def minCostGoodCaption(self, caption: str) -> str:
        n = len(caption)
        if n < 3:
            return ""

        INF = 1 << 60
        # State encoding (79 states):
        #   0                -> boundary: no open run (only occurs at position 0)
        #   1 + c*3 + (l-1)  -> open run of letter c (0..25) with capped length l in {1,2,3};
        #                       l == 3 means "length >= 3", i.e. the run may be closed.
        S = 79
        src = [ord(ch) - 97 for ch in caption]
        DIST = [[abs(x - c) for c in range(26)] for x in range(26)]

        # g[i*S + s] = minimum extra cost to process caption[i:] while starting in
        # state s (the state describes the open run coming from the prefix).
        g = array('q', [INF]) * ((n + 1) * S)

        # Terminal row i == n: boundary and capped-length-3 states are valid (cost 0);
        # open runs of capped length 1 or 2 can never be closed -> INF.
        base = n * S
        g[base] = 0
        for c in range(26):
            g[base + 3 + c * 3] = 0  # state (c, l=3)

        # Backward suffix DP.
        for i in range(n - 1, -1, -1):
            x = src[i]
            dx = DIST[x]
            cur = i * S
            nxt = cur + S

            # h[t] = cost of writing letter t at position i and opening a fresh
            # run (t, 1). Track the two smallest values so that each (c, 3) state
            # can take the minimum over t != c in O(1).
            best1 = INF
            best2 = INF
            arg1 = -1
            for t in range(26):
                v = dx[t] + g[nxt + 1 + t * 3]
                if v < best1:
                    best2 = best1
                    best1 = v
                    arg1 = t
                elif v < best2:
                    best2 = v

            g[cur] = best1  # boundary: start the first run with any letter

            b = cur + 1
            nb = nxt + 1
            for c in range(26):
                d = dx[c]
                g[b] = d + g[nb + 1]      # (c,1): must continue -> (c,2)
                g[b + 1] = d + g[nb + 2]  # (c,2): must continue -> (c,3)
                cont = d + g[nb + 2]      # (c,3): continue      -> (c,3)
                switch = best1 if arg1 != c else best2  # close, start (t,1), t != c
                g[b + 2] = cont if cont < switch else switch
                b += 3
                nb += 3

        if g[0] >= INF:
            return ""  # unreachable for n >= 3, kept for safety

        # Greedy reconstruction of the lexicographically smallest optimal caption:
        # at each position take the smallest letter whose transition can still
        # attain the suffix optimum.
        res = []
        s = 0
        rem = g[0]
        for i in range(n):
            x = src[i]
            dx = DIST[x]
            nxt = (i + 1) * S
            c = (s - 1) // 3 if s else -1
            l = (s - 1) % 3 + 1 if s else 0
            for t in range(26):
                if s == 0:
                    ns = 1 + t * 3                          # open first run (t,1)
                elif t == c:
                    ns = 1 + c * 3 + (l if l < 3 else 2)    # continue -> (c, min(l+1,3))
                elif l == 3:
                    ns = 1 + t * 3                          # close run, open (t,1)
                else:
                    continue                                # run of length 1/2 cannot close
                if dx[t] + g[nxt + ns] == rem:
                    res.append(chr(97 + t))
                    s = ns
                    rem = g[nxt + ns]
                    break

        return "".join(res)


# ============================== TESTS ==============================

def is_good(s: str) -> bool:
    """Every maximal run has length >= 3."""
    if not s:
        return False
    run = 1
    for i in range(1, len(s)):
        if s[i] == s[i - 1]:
            run += 1
        else:
            if run < 3:
                return False
            run = 1
    return run >= 3


def brute_force(caption: str) -> str:
    """Enumerate ALL good target strings (run compositions of n into parts >= 3,
    adjacent parts with distinct letters), compute exact cost for each, and return
    the lexicographically smallest among minimum-cost ones. Feasible for tiny n."""
    n = len(caption)
    if n < 3:
        return ""
    src = [ord(c) - 97 for c in caption]
    best = [None, None]  # [cost, string]

    def comps(rem):
        if rem == 0:
            yield []
            return
        for first in range(3, rem + 1):
            for rest in comps(rem - first):
                yield [first] + rest

    for comp in comps(n):
        letters = []
        k = len(comp)

        def assign(idx, prev):
            if idx == k:
                cost = 0
                p = 0
                parts = []
                for j, c in enumerate(letters):
                    parts.append(chr(97 + c) * comp[j])
                    for _ in range(comp[j]):
                        cost += abs(src[p] - c)
                        p += 1
                    if best[0] is not None and cost > best[0]:
                        return  # costs are non-negative: safe to prune
                s = "".join(parts)
                if (best[0] is None or cost < best[0]
                        or (cost == best[0] and s < best[1])):
                    best[0] = cost
                    best[1] = s
                return
            for c in range(26):
                if c != prev:
                    letters.append(c)
                    assign(idx + 1, c)
                    letters.pop()

        assign(0, -1)
    return best[1]


def run_tests():
    sol = Solution()
    check_count = 0

    def check(caption, expected=None):
        nonlocal check_count
        got = sol.minCostGoodCaption(caption)
        if expected is None:
            expected = brute_force(caption)
        assert got == expected, f"caption={caption!r}: got {got!r}, expected {expected!r}"
        if got:
            assert len(got) == len(caption) and is_good(got)
        check_count += 1

    # ---- the three examples from the statement ----
    check("cdcd", "cccc")
    check("aca", "aaa")
    check("bc", "")

    # ---- n = 1 / 2 (impossible), n = 3 / 4 / 5 ----
    check("a", "")
    check("z", "")
    check("ab", "")
    check("zz", "")
    for s in ["abc", "aaa", "aza", "abcd", "aabb", "zzza",
              "abcde", "aaabb", "azaza", "zyxwv", "eeeee"]:
        check(s)

    # ---- already-good strings must be returned unchanged (cost 0) ----
    for s in ["aaa", "zzz", "aaabbb", "aaaaccc", "zzzyyyxxx",
              "aaabbbcccdddeee", "aaazzzz", "mmmmmmm"]:
        check(s, s)

    # ---- all-same / all-alternating ----
    for ch in "abcdefghijklmnopqrstuvwxyz":
        check(ch * 3, ch * 3)
        check(ch * 10, ch * 10)
    for s in ["ababab", "ababababab", "azazaz", "zazaza",
              "abababa", "cdcdcd", "cdcdcdcd"]:
        check(s)

    # ---- all 'a' / all 'z' (alphabet boundaries) ----
    check("a" * 7, "a" * 7)
    check("z" * 7, "z" * 7)
    check("aaaz", brute_force("aaaz"))
    check("azzz", brute_force("azzz"))
    check("zaaz", brute_force("zaaz"))

    # ---- tricky: total frequency fine but maximal runs invalid ----
    check("aaabaa")          # trailing 'aa' run can never stay
    check("aabaa", brute_force("aabaa"))
    check("bbaabb", brute_force("bbaabb"))

    # ---- exhaustive: every caption over {'a','b','c'} of length 3..6 ----
    def gen(alphabet, length):
        if length == 0:
            yield ""
            return
        for ch in alphabet:
            for rest in gen(alphabet, length - 1):
                yield ch + rest

    for length in range(3, 7):
        for s in gen("abc", length):
            check(s)

    # ---- randomized brute-force comparison, tiny n, small alphabet ----
    random.seed(12345)
    for n, iters in [(3, 150), (4, 150), (5, 150), (6, 150),
                     (7, 120), (8, 100), (9, 25), (10, 10)]:
        for _ in range(iters):
            s = "".join(random.choice("abcdez") for _ in range(n))
            check(s)

    # ---- randomized brute-force comparison, tiny n, full alphabet ----
    for n in range(3, 8):
        for _ in range(25):
            s = "".join(random.choice(string.ascii_lowercase) for _ in range(n))
            check(s)

    # ---- large-n smoke / performance test (no brute force) ----
    for trial in range(5):
        n = 50000
        s = "".join(random.choice(string.ascii_lowercase) for _ in range(n))
        t0 = time.time()
        got = sol.minCostGoodCaption(s)
        dt = time.time() - t0
        assert len(got) == n and is_good(got)
        cost = sum(abs(ord(a) - ord(b)) for a, b in zip(s, got))
        # lower bound sanity: cost >= sum of per-position min distances is 0;
        # and cost <= best single-run cost (always achievable)
        single = min(sum(abs(ord(ch) - 97 - c) for ch in s) for c in range(26))
        assert 0 <= cost <= single
        print(f"  large test {trial}: n={n}, cost={cost}, time={dt:.2f}s")

    big = "a" * 50000
    assert sol.minCostGoodCaption(big) == big
    big = "z" * 50000
    assert sol.minCostGoodCaption(big) == big
    alt = "ab" * 25000
    got = sol.minCostGoodCaption(alt)
    assert len(got) == 50000 and is_good(got)

    print(f"ALL TESTS PASSED ({check_count} exact checks + large-n smoke tests)")


if __name__ == "__main__":
    run_tests()