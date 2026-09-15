from typing import List
from bisect import bisect_left


class Solution:
    def maximumWeight(self, intervals: List[List[int]]) -> List[int]:
        if not intervals:
            return []

        n = len(intervals)

        # Sort by right endpoint, keeping the original index.
        arr = sorted((r, l, idx, w) for idx, (l, r, w) in enumerate(intervals))
        ends = [item[0] for item in arr]

        # p[i] = number of intervals ending strictly before interval i starts.
        bl = bisect_left
        p = [bl(ends, item[1]) for item in arr]
        del ends

        # Insert x into a sorted tuple of length at most 3.
        def add_idx(t, x):
            ln = len(t)
            if ln == 0:
                return (x,)
            if ln == 1:
                a = t[0]
                if x < a:
                    return (x, a)
                return (a, x)
            if ln == 2:
                a, b = t
                if x < a:
                    return (x, a, b)
                if x < b:
                    return (a, x, b)
                return (a, b, x)

            a, b, d = t
            if x < a:
                return (x, a, b, d)
            if x < b:
                return (a, x, b, d)
            if x < d:
                return (a, b, x, d)
            return (a, b, d, x)

        # DP for exact counts. prev_* is for count c-1, curr_* for count c.
        prev_w = [0] * (n + 1)
        prev_t = [()] * (n + 1)

        best_w = 0
        best_t = ()

        for _ in range(1, 5):
            curr_w = [-1] * (n + 1)
            curr_t = [None] * (n + 1)

            cw = curr_w
            ct = curr_t
            pw = prev_w
            pt = prev_t
            pp = p
            aa = arr
            add = add_idx

            for i in range(1, n + 1):
                # Skip interval i-1.
                bw = cw[i - 1]
                bt = ct[i - 1]

                # Take interval i-1.
                pi = pp[i - 1]
                base_w = pw[pi]
                if base_w != -1:
                    item = aa[i - 1]
                    tw = base_w + item[3]

                    if tw > bw:
                        bw = tw
                        bt = add(pt[pi], item[2])
                    elif tw == bw:
                        tt = add(pt[pi], item[2])
                        if bt is None or tt < bt:
                            bt = tt

                cw[i] = bw
                ct[i] = bt

            if cw[n] != -1:
                if cw[n] > best_w or (
                    cw[n] == best_w and (best_t is None or ct[n] < best_t)
                ):
                    best_w = cw[n]
                    best_t = ct[n]

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

    # Touching boundaries overlap; separated points do not.
    assert sol.maximumWeight([[1, 2, 10], [2, 3, 10]]) == [0]
    assert sol.maximumWeight([[1, 1, 5], [2, 2, 5]]) == [0, 1]

    # All overlapping, equal and unequal weights.
    assert sol.maximumWeight([[1, 5, 5], [2, 4, 5], [3, 6, 5]]) == [0]
    assert sol.maximumWeight([[1, 5, 1], [2, 4, 2], [3, 6, 3]]) == [2]

    # Ties across different chosen counts.
    assert sol.maximumWeight([[1, 10, 10], [1, 1, 5], [2, 2, 5]]) == [0]
    assert sol.maximumWeight([[1, 1, 5], [2, 2, 5], [3, 10, 10]]) == [0, 1]

    # Large coordinates and boundary at 1e9.
    assert sol.maximumWeight(
        [[1, 1000000000, 1000000000], [1000000000, 1000000000, 1000000000]]
    ) == [0]
    assert sol.maximumWeight(
        [[1, 999999999, 1], [1000000000, 1000000000, 1]]
    ) == [0, 1]

    # More than four compatible intervals: choose the lexicographically smallest four.
    assert sol.maximumWeight([[i, i, 1] for i in range(1, 10)]) == [0, 1, 2, 3]

    # A single heavy interval beats several lighter compatible intervals.
    assert sol.maximumWeight(
        [[1, 1, 1], [2, 2, 1], [3, 3, 1], [4, 4, 1], [5, 5, 100]]
    ) == [4]

    # Duplicate overlapping intervals choose the smallest index.
    assert sol.maximumWeight([[1, 2, 5], [1, 2, 5], [3, 4, 5]]) == [0, 2]

    # Empty input is handled even though constraints have n >= 1.
    assert sol.maximumWeight([]) == []