from typing import List


class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        m = len(conflictingPairs)

        # Bucket normalized pairs by their larger endpoint b.
        buckets = [[] for _ in range(n + 1)]
        for idx, (x, y) in enumerate(conflictingPairs):
            if x > y:
                x, y = y, x
            buckets[y].append((x, idx))

        gains = [0] * m

        # Active maximum and second maximum distinct smaller endpoints.
        max1 = 0
        max2 = 0
        cnt1 = 0
        unique_id = -1

        base = 0

        for r in range(1, n + 1):
            # Insert all pairs whose larger endpoint is r before evaluating r.
            for a, idx in buckets[r]:
                if a > max1:
                    max2 = max1
                    max1 = a
                    cnt1 = 1
                    unique_id = idx
                elif a == max1:
                    cnt1 += 1
                    unique_id = -1
                elif a > max2:
                    max2 = a

            # Valid subarrays ending at r.
            base += r - max1

            # If the current maximum is unique, deleting that pair improves
            # this right endpoint by max1 - max2.
            if cnt1 == 1 and unique_id != -1:
                gains[unique_id] += max1 - max2

        return base + (max(gains) if gains else 0)


# ----------------------------------------------------------------------
# Validation helpers. These are not needed by the judge unless this file
# is executed directly.
# ----------------------------------------------------------------------

def _normalize_pairs(pairs):
    return [(a if a < b else b, b if a < b else a) for a, b in pairs]


def _count_valid_brute(n, pairs):
    norm = _normalize_pairs(pairs)
    total = 0

    for l in range(1, n + 1):
        for r in range(l, n + 1):
            ok = True
            for a, b in norm:
                if l <= a and b <= r:
                    ok = False
                    break
            if ok:
                total += 1

    return total


def _brute_max(n, pairs):
    m = len(pairs)
    if m == 0:
        return _count_valid_brute(n, pairs)

    best = -1
    for i in range(m):
        best = max(best, _count_valid_brute(n, pairs[:i] + pairs[i + 1:]))
    return best


class _Rand:
    def __init__(self, seed: int = 123456789):
        self.state = seed & ((1 << 64) - 1)

    def _next(self) -> int:
        self.state = (
            self.state * 6364136223846793005 + 1442695040888963407
        ) & ((1 << 64) - 1)
        return self.state >> 32

    def randint(self, lo: int, hi: int) -> int:
        return lo + self._next() % (hi - lo + 1)


def validate() -> bool:
    sol = Solution()

    # Provided examples.
    assert sol.maxSubarrays(4, [[2, 3], [1, 4]]) == 9
    assert sol.maxSubarrays(5, [[1, 2], [2, 5], [3, 5]]) == 12

    # Targeted edge cases.
    cases = [
        # Duplicate pairs.
        (3, [[1, 2], [1, 2]]),
        (3, [[2, 1], [1, 2]]),

        # Equal smaller endpoint, different larger endpoint.
        (4, [[2, 3], [2, 4]]),

        # Equal larger endpoint, different smaller endpoint.
        (4, [[1, 4], [2, 4]]),
        (4, [[3, 4], [2, 4]]),

        # Single pair.
        (2, [[1, 2]]),

        # Removing the unique maximum reveals a lower second maximum.
        (5, [[4, 5], [3, 4], [2, 3]]),

        # Many pairs sharing one endpoint.
        (5, [[1, 5], [2, 5], [3, 5], [4, 5]]),
        (5, [[1, 2], [1, 3], [1, 4], [1, 5]]),

        # Nested and disjoint constraints.
        (6, [[1, 6], [2, 5], [3, 4]]),
        (6, [[1, 2], [3, 4], [5, 6]]),
        (6, [[2, 6], [3, 6], [4, 6], [5, 6]]),

        # Mixed interactions.
        (4, [[1, 3], [2, 4], [3, 4]]),
        (5, [[3, 5], [3, 4]]),
    ]

    for n, pairs in cases:
        assert sol.maxSubarrays(n, pairs) == _brute_max(n, pairs)

    # Large sanity checks for single and duplicate extreme pairs.
    total = 100000 * 100001 // 2
    assert sol.maxSubarrays(100000, [[1, 100000]]) == total
    assert sol.maxSubarrays(100000, [[1, 100000], [1, 100000]]) == total - 1

    # Deterministic random small tests against brute force.
    rng = _Rand(987654321)
    for _ in range(300):
        n = rng.randint(2, 6)
        m = rng.randint(1, 2 * n)

        pairs = []
        for _ in range(m):
            a = rng.randint(1, n)
            b = rng.randint(1, n)
            while a == b:
                b = rng.randint(1, n)
            pairs.append([a, b])

        # Force some duplicate pairs.
        for j in range(m):
            if rng.randint(1, 4) == 1:
                pairs[j] = pairs[rng.randint(0, len(pairs) - 1)][:]

        # Sometimes reverse input order to test bucket insertion order.
        if rng.randint(1, 2) == 1:
            pairs.reverse()

        assert sol.maxSubarrays(n, pairs) == _brute_max(n, pairs)

    return True


if __name__ == "__main__":
    validate()