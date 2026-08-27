from heapq import heappush, heappop
import random
import time


class Solution:
    def makeStringGood(self, s: str) -> int:
        cnt = [0] * 26
        for ch in s:
            cnt[ord(ch) - 97] += 1
        return _min_ops_dp(cnt)


def _min_ops_dp(cnt) -> int:
    """
    Exact DP for an alphabet of size len(cnt).

    For a fixed final nonzero frequency T, every final count is either 0 or T.
    The no-change cost is sum |cnt[i] - final[i]|.  A change can beat
    delete+insert only on an adjacent edge i -> i+1: it costs 1 instead of 2,
    saving exactly 1 per unit.  Distance-2 changes only tie delete+insert and
    longer changes are worse, so maximal adjacent carry is sufficient.
    """
    m = len(cnt)
    n = sum(cnt)
    ans = n  # safe fallback; for n > 0, keeping one character is even better
    maxcnt = max(cnt) if cnt else 0

    # Any T > maxcnt is dominated by T = maxcnt with the same kept set:
    # all kept letters only need fewer/equal inserts, deleted letters unchanged.
    for T in range(1, maxcnt + 1):
        c0 = cnt[0]
        dp0 = c0                 # previous final count is 0
        d0 = c0 - T
        dp1 = d0 if d0 >= 0 else -d0  # previous final count is T

        for i in range(1, m):
            c = cnt[i]
            pc = cnt[i - 1]

            sup0 = pc            # surplus at i-1 when final[i-1] = 0
            sup1 = pc - T        # surplus at i-1 when final[i-1] = T
            if sup1 < 0:
                sup1 = 0

            def1 = T - c         # deficit at i when final[i] = T
            if def1 < 0:
                def1 = 0
            # deficit at i when final[i] = 0 is always 0, so no carry into state 0

            base0 = c            # |c - 0|
            base1 = c - T        # |c - T|
            if base1 < 0:
                base1 = -base1

            # End at final[i] = 0: no deficit, hence no saving on edge i-1 -> i.
            ndp0 = (dp0 if dp0 < dp1 else dp1) + base0

            # End at final[i] = T: carry min(previous surplus, current deficit).
            save0 = sup0 if sup0 < def1 else def1
            save1 = sup1 if sup1 < def1 else def1
            cand0 = dp0 - save0
            cand1 = dp1 - save1
            ndp1 = (cand0 if cand0 < cand1 else cand1) + base1

            dp0, dp1 = ndp0, ndp1

        cur = dp0 if dp0 < dp1 else dp1
        if cur < ans:
            ans = cur

    return ans


# ------------------------- independent brute validator -------------------------

def _is_good(state) -> bool:
    nonzero = [x for x in state if x != 0]
    return len(set(nonzero)) <= 1  # empty is treated as good; only used as a bound


def _min_ops_brute(cnt) -> int:
    """
    Dijkstra over count vectors for small alphabets.

    Delete-all gives an upper bound of n, so states reachable only after more
    than n operations cannot improve the answer.  Total length therefore never
    needs to exceed 2n in the search.
    """
    m = len(cnt)
    n = sum(cnt)
    if n == 0:
        return 0

    limit = 2 * n
    start = tuple(cnt)
    dist = {start: 0}
    pq = [(0, start)]

    while pq:
        d, st = heappop(pq)
        if d != dist[st]:
            continue
        if _is_good(st):
            return d
        if d >= n:
            continue

        def relax(ns, nd):
            old = dist.get(ns)
            if old is None or nd < old:
                dist[ns] = nd
                heappush(pq, (nd, ns))

        # delete
        for i, x in enumerate(st):
            if x:
                ns = list(st)
                ns[i] -= 1
                relax(tuple(ns), d + 1)

        # insert, bounded by the delete-all fallback
        if sum(st) < limit:
            for i in range(m):
                ns = list(st)
                ns[i] += 1
                relax(tuple(ns), d + 1)

        # change i -> i+1; no wrap from the last letter
        for i in range(m - 1):
            if st[i]:
                ns = list(st)
                ns[i] -= 1
                ns[i + 1] += 1
                relax(tuple(ns), d + 1)

    return n  # unreachable: delete-all is always reachable at cost n


def _compositions(total, m):
    if m == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for rest in _compositions(total - first, m - 1):
            yield (first,) + rest


def _validate() -> None:
    def check(cnt):
        cnt = list(cnt)
        got = _min_ops_dp(cnt)
        want = _min_ops_brute(cnt)
        assert got == want, f"mismatch cnt={cnt}: dp={got}, brute={want}"

    # Exhaustive small alphabet/small length coverage, including zero counts.
    for m in range(1, 5):
        for total in range(0, 9):
            for cnt in _compositions(total, m):
                check(cnt)

    # Targeted adjacent carries, distance-2 ties, cnt == T/2 ties, and gaps.
    targeted = [
        [0, 0, 0, 0],
        [1, 0, 1, 0],
        [2, 0, 0, 2],
        [3, 0, 1, 0],
        [2, 2, 0, 0],
        [1, 2, 1, 2],
        [4, 2, 0, 1],
        [0, 5, 0, 1],
        [2, 0, 2, 0],
        [1, 0, 0, 1],
        [3, 1, 1, 3],
        [2, 4, 2, 4],
        [5, 0, 5, 0],
        [0, 3, 0, 3],
        [4, 0, 1, 4],
    ]
    for cnt in targeted:
        check(cnt)

    # Biased random small cases: zeros, adjacent-heavy masses, and ties.
    rng = random.Random(0)
    for _ in range(1000):
        m = 4
        while True:
            cnt = [rng.randint(0, 5) for _ in range(m)]
            if 3 <= sum(cnt) <= 8:
                break
        if rng.random() < 0.5:
            cnt[rng.randrange(m)] = 0
        if rng.random() < 0.3:
            i = rng.randrange(m - 1)
            cnt[i + 1] = max(0, cnt[i] + rng.choice([-1, 0, 1]))
        if 3 <= sum(cnt) <= 8:
            check(cnt)


def _run_requested_tests() -> None:
    sol = Solution()

    # Provided examples.
    assert sol.makeStringGood("acab") == 1
    assert sol.makeStringGood("wddw") == 0
    assert sol.makeStringGood("aaabc") == 2

    # All identical characters / all 'z'.
    assert sol.makeStringGood("aaaaaa") == 0
    assert sol.makeStringGood("zzzzzz") == 0
    assert sol.makeStringGood("zyxwv") == 4  # five distinct letters -> keep one

    # Strictly increasing / decreasing count patterns, checked against brute force.
    small_count_cases = [
        [1, 2, 3, 4],        # increasing over a..d
        [4, 3, 2, 1],        # decreasing over a..d
        [1, 2, 2],           # insert-only is optimal: insert one 'a'
        [1, 1, 3],           # delete-only is optimal: delete two 'c'
        [3, 0, 0, 0, 0, 1],  # many zero-frequency gaps between a and f
        [0, 0, 5, 0, 0, 5],  # zeros plus already-equal nonzero counts
        [6, 0, 0, 0, 0, 6],  # equal nonzero counts separated by zeros
    ]
    for cnt in small_count_cases:
        assert _min_ops_dp(cnt) == _min_ops_brute(cnt), cnt

    # Explicit insert-only / delete-only optimal scenarios on real strings.
    assert sol.makeStringGood("abbcc") == 1   # insert one 'a'
    assert sol.makeStringGood("abccc") == 2   # delete two 'c'
    assert sol.makeStringGood("aaaz") == 2    # far apart: delete two 'a' or insert two 'z'

    # Many zero frequencies in the full 26-letter alphabet.
    cnt = [0] * 26
    cnt[0] = 3
    cnt[25] = 3
    assert _min_ops_dp(cnt) == 0  # a^3 z^3 is already good despite 24 zeros
    cnt[25] = 1
    assert _min_ops_dp(cnt) == 2  # equalize a^3 and z^1

    # Timing / robustness on random maximum-size inputs.
    rng = random.Random(12345)
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    for trial in range(3):
        s = "".join(rng.choice(alphabet) for _ in range(2 * 10**4))
        t0 = time.perf_counter()
        res = sol.makeStringGood(s)
        elapsed = time.perf_counter() - t0
        assert 0 <= res <= len(s)
        assert elapsed < 5.0, f"too slow: {elapsed:.3f}s"
        print(f"perf trial {trial}: n={len(s)} ans={res} time={elapsed:.4f}s")


if __name__ == "__main__":
    _validate()
    _run_requested_tests()
    print("all tests passed")