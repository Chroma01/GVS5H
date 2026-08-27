from typing import List
from bisect import bisect_left


class Solution:
    def maximumWeight(self, intervals: List[List[int]]) -> List[int]:
        n = len(intervals)

        # Sort by right endpoint, then left endpoint. Keep original index.
        data = [(r, l, w, i) for i, (l, r, w) in enumerate(intervals)]
        data.sort()

        ends = [x[0] for x in data]
        lefts = [x[1] for x in data]
        weights = [x[2] for x in data]
        orig = [x[3] for x in data]

        # p[j] = number of intervals ending strictly before lefts[j].
        # Strictness enforces that touching endpoints overlap.
        p = [bisect_left(ends, l) for l in lefts]

        # DP for exact count 0:
        # every prefix can choose 0 intervals with weight 0 and empty tuple.
        prev_w = [0] * (n + 1)
        prev_t = [()] * (n + 1)

        best_w = 0
        best_t = ()

        # Build exact counts 1..4.
        for _ in range(1, 5):
            curr_w = [-1] * (n + 1)
            curr_t = [None] * (n + 1)

            for i in range(1, n + 1):
                j = i - 1

                # Option 1: skip interval j.
                bw = curr_w[i - 1]
                bt = curr_t[i - 1]

                # Option 2: take interval j, combined with best exact
                # previous count among intervals ending before lefts[j].
                pw = prev_w[p[j]]
                if pw >= 0:
                    tw = pw + weights[j]
                    pt = prev_t[p[j]]
                    x = orig[j]

                    # Insert original index x into the sorted tuple.
                    if not pt:
                        nt = (x,)
                    else:
                        lst = list(pt)
                        pos = 0
                        while pos < len(lst) and lst[pos] < x:
                            pos += 1
                        lst.insert(pos, x)
                        nt = tuple(lst)

                    # Larger weight wins; ties go to lexicographically smaller tuple.
                    if tw > bw or (tw == bw and (bt is None or nt < bt)):
                        bw = tw
                        bt = nt

                curr_w[i] = bw
                curr_t[i] = bt

            # Record best exact count for this layer.
            fw = curr_w[n]
            ft = curr_t[n]
            if fw > best_w or (fw == best_w and ft is not None and (best_t is None or ft < best_t)):
                best_w = fw
                best_t = ft

            # This layer becomes the previous layer for the next count.
            prev_w, prev_t = curr_w, curr_t

        return list(best_t)


if __name__ == "__main__":
    sol = Solution()
    assert sol.maximumWeight(
        [[1, 3, 2], [4, 5, 2], [1, 5, 5], [6, 9, 3], [6, 7, 1], [8, 9, 1]]
    ) == [2, 3]
    assert sol.maximumWeight(
        [[5, 8, 1], [6, 7, 7], [4, 7, 3], [9, 10, 6], [7, 8, 2], [11, 14, 3], [3, 5, 5]]
    ) == [1, 3, 5, 6]