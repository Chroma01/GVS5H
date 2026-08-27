import bisect
from typing import List, Tuple, Optional

class Fenwick:
    """
    Fenwick tree (Binary Indexed Tree) that supports:
      - update(pos, k, state): merge the best state for count k at position pos.
      - query(pos): return, for each k = 0..3, the best state among all positions <= pos.
    State = (score, indices_tuple) with indices_tuple sorted ascending.
    Better = higher score, or if equal, lexicographically smaller indices tuple.
    """
    def __init__(self, size: int):
        self.n = size
        # tree[k] is a list of length self.n+1 (1-indexed) storing best state for count k.
        self.tree = [[None] * (self.n + 1) for _ in range(4)]  # k = 0..3

    @staticmethod
    def _better(a: Optional[Tuple[int, Tuple[int, ...]]],
                b: Optional[Tuple[int, Tuple[int, ...]]]) -> Optional[Tuple[int, Tuple[int, ...]]]:
        if a is None:
            return b
        if b is None:
            return a
        sa, idx_a = a
        sb, idx_b = b
        if sa != sb:
            return a if sa > sb else b
        return a if idx_a < idx_b else b

    def update(self, pos: int, k: int, state: Tuple[int, Tuple[int, ...]]):
        n = self.n
        t = self.tree[k]
        i = pos
        while i <= n:
            t[i] = self._better(t[i], state)
            i += i & -i

    def query(self, pos: int) -> List[Optional[Tuple[int, Tuple[int, ...]]]]:
        res = [None] * 4
        i = pos
        while i > 0:
            for k in range(4):
                res[k] = self._better(res[k], self.tree[k][i])
            i -= i & -i
        return res


class Solution:
    def maximumWeight(self, intervals: List[List[int]]) -> List[int]:
        if not intervals:
            return []

        n = len(intervals)
        # Attach original indices
        indexed = [(l, r, w, i) for i, (l, r, w) in enumerate(intervals)]
        # Sort by start l, then by end r, then by original index for determinism
        indexed.sort(key=lambda x: (x[0], x[1], x[2]))

        # Coordinate compression of end positions
        ends = [e[1] for e in indexed]
        uniq_ends = sorted(set(ends))
        comp = {v: i + 1 for i, v in enumerate(uniq_ends)}  # 1-indexed

        ft = Fenwick(len(uniq_ends))
        empty_state = (0, ())

        # Best state for exactly k intervals (k = 0..4).
        # k = 0 is always empty_state.
        # k = 1..3 are stored in Fenwick, k = 4 tracked separately.
        best_k4: Optional[Tuple[int, Tuple[int, ...]]] = None

        for l, r, w, orig_idx in indexed:
            end_pos = comp[r]

            # Find largest compressed end that is < l
            pos = bisect.bisect_left(uniq_ends, l)
            if pos == 0:
                prev = [None] * 4
                prev[0] = empty_state
            else:
                prev = ft.query(pos)
                if prev[0] is None:
                    prev[0] = empty_state

            # Extend states with k-1 intervals to k intervals (k = 1..4)
            for k in range(1, 5):
                base = prev[k - 1]
                if base is None:
                    continue
                base_score, base_idx = base
                new_score = base_score + w
                new_idx = tuple(sorted(base_idx + (orig_idx,)))
                new_state = (new_score, new_idx)

                if k <= 3:
                    ft.update(end_pos, k, new_state)
                else:  # k == 4
                    best_k4 = Fenwick._better(best_k4, new_state)

        # Final best among all counts 0..4
        final = ft.query(len(uniq_ends))
        if final[0] is None:
            final[0] = empty_state

        best = None
        for k in range(4):
            if final[k] is not None:
                best = Fenwick._better(best, final[k])
        if best_k4 is not None:
            best = Fenwick._better(best, best_k4)

        if best is None:
            return []
        return list(best[1])


# ----------------- Test harness -----------------
if __name__ == "__main__":
    sol = Solution()

    # Example 1
    iv1 = [[1,3,2],[4,5,2],[1,5,5],[6,9,3],[6,7,1],[8,9,1]]
    print("Ex1:", sol.maximumWeight(iv1), "expected [2,3]")

    # Example 2
    iv2 = [[5,8,1],[6,7,7],[4,7,3],[9,10,6],[7,8,2],[11,14,3],[3,5,5]]
    print("Ex2:", sol.maximumWeight(iv2), "expected [1,3,5,6]")

    # Edge: single interval
    print("Single:", sol.maximumWeight([[1,2,5]]), "expected [0]")

    # Edge: all overlapping (pick max weight)
    iv3 = [[1,10,1],[1,10,2],[1,10,3],[1,10,4]]
    print("All overlap:", sol.maximumWeight(iv3), "expected [3]")

    # Edge: identical intervals (same l,r, different w)
    iv4 = [[1,5,1],[1,5,2],[1,5,3]]
    print("Identical:", sol.maximumWeight(iv4), "expected [2]")

    # Edge: touching boundaries are overlapping
    iv5 = [[1,2,10],[2,3,20]]
    print("Touching:", sol.maximumWeight(iv5), "expected [1]")

    # Edge: can pick 4 non-overlapping
    iv6 = [[1,2,1],[3,4,2],[5,6,3],[7,8,4]]
    print("Four non-overlap:", sol.maximumWeight(iv6), "expected [0,1,2,3]")

    # Edge: large coordinates
    iv7 = [[1,1000000000,1],[1000000001,2000000000,2]]
    print("Large coords:", sol.maximumWeight(iv7), "expected [0,1]")

    # Edge: ties in score - lex smallest
    # Two ways to get score 10: pick [0,2] (weights 5+5) or [1] (weight 10)
    # Lex smallest among max-score solutions: [1] (shorter) vs [0,2] - shorter is smaller
    iv8 = [[1,2,5],[1,2,10],[3,4,5]]
    print("Tie shorter:", sol.maximumWeight(iv8), "expected [1]")

    # Lex tie: [0,1] vs [0,2] both score 6? Let's craft:
    # iv9: [1,2,3], [3,4,3], [1,2,2], [3,4,4] -> picking [2,3] gives 6, [0,1] gives 6
    # Lex smaller: [0,1] (since 0<2)
    iv9 = [[1,2,3],[3,4,3],[1,2,2],[3,4,4]]
    print("Lex tie:", sol.maximumWeight(iv9), "expected [0,1]")

    # More than 4 available but we cap at 4
    iv10 = [[1,2,1],[3,4,2],[5,6,3],[7,8,4],[9,10,5]]
    print("Cap at 4:", sol.maximumWeight(iv10), "expected [0,1,2,3] (score 10 < [1,2,3,4] score 14)")
    # Actually best is [1,2,3,4] with weight 14
    print("Cap at 4 correct:", sol.maximumWeight(iv10), "expected [1,2,3,4]")