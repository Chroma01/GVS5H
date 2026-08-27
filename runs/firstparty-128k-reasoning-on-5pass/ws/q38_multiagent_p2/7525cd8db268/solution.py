from typing import List
import heapq
import random


class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        m = len(conflictingPairs)
        if m == 0:
            return n * (n + 1) // 2

        buckets = [[] for _ in range(n + 1)]
        for idx, (x, y) in enumerate(conflictingPairs):
            if x < y:
                a, b = x, y
            else:
                a, b = y, x
            buckets[b].append((a, idx))

        heap = []
        cnt = [0] * (n + 1)
        uid = [-1] * (n + 1)
        gain = [0] * m
        base = 0

        heappush = heapq.heappush
        heappop = heapq.heappop

        for r in range(1, n + 1):
            for a, idx in buckets[r]:
                if cnt[a] == 0:
                    heappush(heap, -a)
                    cnt[a] = 1
                    uid[a] = idx
                else:
                    cnt[a] += 1
                    uid[a] = -1

            if heap:
                top1 = heappop(heap)
                max_a = -top1
                second_a = -heap[0] if heap else 0
                heappush(heap, top1)

                base += r - max_a
                if cnt[max_a] == 1:
                    u = uid[max_a]
                    if u != -1:
                        gain[u] += max_a - second_a
            else:
                base += r

        return base + max(gain)


def _brute_max(n: int, pairs: List[List[int]]) -> int:
    norm = []
    for x, y in pairs:
        if x < y:
            norm.append((x, y))
        else:
            norm.append((y, x))

    m = len(norm)
    masks = [[0] * (n + 1) for _ in range(n + 1)]

    for l in range(1, n + 1):
        for r in range(l, n + 1):
            mask = 0
            for i, (a, b) in enumerate(norm):
                if a >= l and b <= r:
                    mask |= 1 << i
            masks[l][r] = mask

    best = 0
    for skip in range(m):
        keep = ((1 << m) - 1) ^ (1 << skip)
        valid = 0
        for l in range(1, n + 1):
            for r in range(l, n + 1):
                if (masks[l][r] & keep) == 0:
                    valid += 1
        if valid > best:
            best = valid

    return best


if __name__ == "__main__":
    sol = Solution()

    assert sol.maxSubarrays(4, [[2, 3], [1, 4]]) == 9
    assert sol.maxSubarrays(5, [[1, 2], [2, 5], [3, 5]]) == 12
    assert sol.maxSubarrays(2, [[1, 2]]) == 3
    assert sol.maxSubarrays(2, [[1, 2], [1, 2]]) == 2
    assert sol.maxSubarrays(3, [[1, 2], [2, 3]]) == 4
    assert sol.maxSubarrays(3, [[1, 3], [2, 3]]) == 5
    assert sol.maxSubarrays(3, [[1, 2], [1, 3]]) == 5
    assert sol.maxSubarrays(4, [[1, 4], [2, 3], [3, 4]]) == 7
    assert sol.maxSubarrays(4, [[1, 2], [3, 4]]) == 7
    assert sol.maxSubarrays(5, [[1, 5] for _ in range(10)]) == 14

    rng = random.Random(12345)
    for _ in range(2000):
        n = rng.randint(2, 8)
        m = rng.randint(1, min(10, 2 * n))
        pairs = []
        for _ in range(m):
            x = rng.randint(1, n)
            y = rng.randint(1, n)
            while y == x:
                y = rng.randint(1, n)
            pairs.append([x, y])

        if m > 1 and rng.random() < 0.3:
            pairs[-1] = pairs[rng.randrange(m - 1)].copy()

        expected = _brute_max(n, pairs)
        actual = sol.maxSubarrays(n, pairs)
        if actual != expected:
            raise AssertionError(f"n={n} pairs={pairs} expected={expected} actual={actual}")