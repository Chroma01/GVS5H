import bisect
from typing import List, Tuple


class BIT:
    """Fenwick tree (Binary Indexed Tree) for prefix maximum of (weight, list) pairs."""

    __slots__ = ("n", "tree")

    def __init__(self, n: int):
        self.n = n
        self.tree = [(0, ())] * (n + 1)          # 1‑based indexing

    def _better(self, a: Tuple[int, Tuple[int, ...]],
                b: Tuple[int, Tuple[int, ...]]) -> Tuple[int, Tuple[int, ...]]:
        """Return the better of two states (weight, list)."""
        if a[0] != b[0]:
            return a if a[0] > b[0] else b
        # equal weight → lexicographically smaller sorted list wins
        return a if a[1] < b[1] else b

    def update(self, idx: int, val: Tuple[int, Tuple[int, ...]]) -> None:
        """Set position idx (1‑based) to the better of its current value and val."""
        n = self.n
        tree = self.tree
        while idx <= n:
            tree[idx] = self._better(tree[idx], val)
            idx += idx & -idx

    def query(self, idx: int) -> Tuple[int, Tuple[int, ...]]:
        """Return the best value in the prefix [1 .. idx] (inclusive)."""
        res = (0, ())
        tree = self.tree
        while idx:
            res = self._better(res, tree[idx])
            idx -= idx & -idx
        return res


class Solution:
    def maximumWeight(self, intervals: List[List[int]]) -> List[int]:
        """Select up to 4 non‑overlapping intervals with maximum total weight.
        Returns the lexicographically smallest list of original indices (sorted)."""
        if not intervals:
            return []

        n = len(intervals)
        # 1. sort intervals by right endpoint, then left endpoint
        indexed = list(enumerate(intervals))                # (original_index, [l, r, w])
        indexed.sort(key=lambda x: (x[1][1], x[1][0]))      # sort by r, then l

        starts = [0] * n
        ends = [0] * n
        weights = [0] * n
        orig_idx = [0] * n

        for i, (orig, iv) in enumerate(indexed):
            l, r, w = iv
            starts[i] = l
            ends[i] = r
            weights[i] = w
            orig_idx[i] = orig

        # 2. compute predecessor for each interval (last interval that ends before start[i])
        prev = [-1] * n
        for i in range(n):
            # bisect_left gives first r >= l[i]; we need r < l[i]
            pos = bisect.bisect_left(ends, starts[i]) - 1
            prev[i] = pos

        # 3. DP for k = 0..4 using Fenwick trees
        MAXK = 4
        bits = [BIT(n) for _ in range(MAXK + 1)]   # bits[0] stays (0, ())
        dpPrev = [(0, ())] * (MAXK + 1)            # best (weight, list) up to previous i

        for i in range(n):
            w = weights[i]
            idx = orig_idx[i]
            p = prev[i]

            for k in range(1, MAXK + 1):
                # best result with k-1 intervals that end before start[i]
                if p >= 0:
                    bestPrevW, bestPrevL = bits[k - 1].query(p + 1)
                else:
                    bestPrevW, bestPrevL = 0, ()

                candW = bestPrevW + w
                # new list = sorted(bestPrevL ∪ {idx})
                candL = tuple(sorted(bestPrevL + (idx,)))

                # previous best without using interval i
                prevW, prevL = dpPrev[k]

                # choose the better one
                if candW > prevW:
                    cur = (candW, candL)
                elif candW < prevW:
                    cur = (prevW, prevL)
                else:                               # equal weight → smaller list wins
                    cur = (candW, candL) if candL < prevL else (prevW, prevL)

                dpPrev[k] = cur
                bits[k].update(i + 1, cur)          # i+1 because BIT is 1‑based

        # 4. pick the overall best among k = 0..4
        best = (0, ())
        for k in range(MAXK + 1):
            w, lst = dpPrev[k]
            if w > best[0] or (w == best[0] and lst < best[1]):
                best = (w, lst)

        return list(best[1])                         # already sorted increasingly