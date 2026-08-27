import random
from typing import List


class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        m = len(conflictingPairs)
        # Group (left, pair_index) by the right endpoint.
        by_right = [[] for _ in range(n + 1)]
        for i, (a, b) in enumerate(conflictingPairs):
            l, r = (a, b) if a < b else (b, a)
            by_right[r].append((l, i))

        base = 0
        l1 = 0      # largest left endpoint among pairs with right <= current r
        l2 = 0      # second largest left endpoint among those pairs
        idx = -1    # index of the pair currently responsible for l1
        gain = [0] * m

        for r in range(1, n + 1):
            for l, i in by_right[r]:
                if l > l1:
                    l2 = l1
                    l1 = l
                    idx = i
                elif l > l2:
                    l2 = l
            # Subarrays ending at r must start > l1 -> (r - l1) choices.
            base += r - l1
            # If pair `idx` (the unique current max) were removed, the cap for
            # subarrays ending at r would drop from l1 to l2, adding (l1 - l2)
            # newly valid subarrays. Duplicates/ties force l2 == l1, giving 0.
            if idx != -1:
                gain[idx] += l1 - l2

        # Exactly one pair must be removed; removing one never hurts, so the
        # best gain is nonnegative and max(gain) >= 0 naturally.
        return base + max(gain)


# ---------------------------------------------------------------------------
# Validation harness: O(n^2 * m) brute-force enumerator vs. fast solution.
# ---------------------------------------------------------------------------

def brute_force(n: int, pairs: List[List[int]]) -> int:
    """Try removing each pair; count valid subarrays by enumeration."""
    m = len(pairs)
    norm = [tuple(sorted(p)) for p in pairs]
    best = 0
    for rem in range(m):
        remaining = [norm[j] for j in range(m) if j != rem]
        cnt = 0
        for s in range(1, n + 1):
            for e in range(s, n + 1):
                ok = True
                for (a, b) in remaining:
                    if s <= a and b <= e:  # subarray contains both endpoints
                        ok = False
                        break
                if ok:
                    cnt += 1
        if cnt > best:
            best = cnt
    return best


def run_tests() -> None:
    sol = Solution()

    def check(n, pairs, expected=None, label=""):
        got = sol.maxSubarrays(n, [list(p) for p in pairs])
        bf = brute_force(n, pairs)
        assert got == bf, f"FAIL {label}: n={n} pairs={pairs} got={got} brute={bf}"
        if expected is not None:
            assert got == expected, f"FAIL {label}: expected {expected}, got {got}"
        print(f"ok  {label or 'case'}: n={n} pairs={pairs} -> {got} (brute={bf})")

    # Provided samples.
    check(4, [[2, 3], [1, 4]], expected=9, label="sample1")
    check(5, [[1, 2], [2, 5], [3, 5]], expected=12, label="sample2")

    # m = 1: removing the only pair frees all subarrays.
    check(2, [[1, 2]], expected=3, label="m=1 minimal")
    check(5, [[2, 4]], label="m=1 middle")

    # Duplicates: removing one copy leaves the other active -> zero gain.
    check(3, [[1, 2], [1, 2]], label="exact duplicates")
    check(4, [[1, 3], [1, 3], [2, 4]], label="duplicates + other")

    # Ties on left endpoint across different right endpoints.
    check(5, [[2, 3], [2, 5]], label="same left, different right")
    check(5, [[1, 4], [3, 4], [3, 5]], label="same right tie")

    # Reversed orientation (a > b) must be normalized.
    check(4, [[3, 2], [4, 1]], expected=9, label="reversed orientation")

    # Zero-gain removals: one pair strictly dominates another.
    check(4, [[1, 4], [2, 3]], label="nested pairs")
    check(6, [[1, 6], [2, 3], [3, 4], [4, 5]], label="dominant + small")

    # All pairs disjoint-ish / chain structure.
    check(6, [[1, 2], [3, 4], [5, 6]], label="disjoint chain")

    # Random small fuzz, duplicates allowed, m >= 1.
    rng = random.Random(12345)
    trials = 0
    for _ in range(3000):
        n = rng.randint(2, 8)
        m = rng.randint(1, 10)
        pairs = []
        for _ in range(m):
            a = rng.randint(1, n)
            b = rng.randint(1, n)
            while b == a:
                b = rng.randint(1, n)
            pairs.append([a, b])
        got = sol.maxSubarrays(n, [list(p) for p in pairs])
        bf = brute_force(n, pairs)
        assert got == bf, f"FUZZ FAIL: n={n} pairs={pairs} got={got} brute={bf}"
        trials += 1
    print(f"ok  fuzz: {trials} random trials passed (duplicates/ties/m=1 included)")

    print("ALL TESTS PASSED")


if __name__ == "__main__":
    run_tests()