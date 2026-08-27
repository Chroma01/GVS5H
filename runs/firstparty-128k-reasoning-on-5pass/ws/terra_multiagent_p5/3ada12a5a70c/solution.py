from typing import List


class Solution:
    def maxDistance(self, side: int, points: List[List[int]], k: int) -> int:
        # Clockwise perimeter coordinates:
        # bottom: [0, side], right: [side, 2*side],
        # top: [2*side, 3*side], left: [3*side, 4*side].
        pos = []
        for x, y in points:
            if y == 0:
                pos.append(x)
            elif x == side:
                pos.append(side + y)
            elif y == side:
                pos.append(3 * side - x)
            else:
                pos.append(4 * side - y)

        pos.sort()
        n = len(pos)
        perimeter = 4 * side

        def feasible(d: int) -> bool:
            arr = pos + [p + perimeter for p in pos]
            m = 2 * n

            # Earliest later point whose forward perimeter gap is at least d.
            nxt = [m] * (m + 1)
            j = 0
            for i in range(m):
                if j < i + 1:
                    j = i + 1
                target = arr[i] + d
                while j < m and arr[j] < target:
                    j += 1
                nxt[i] = j

            # Binary lifting over greedy successor choices.
            jumps = [nxt]
            steps = k - 1
            while (1 << len(jumps)) <= steps:
                prev = jumps[-1]
                cur_jump = [m] * (m + 1)
                for i in range(m):
                    mid = prev[i]
                    if mid < m:
                        cur_jump[i] = prev[mid]
                jumps.append(cur_jump)

            for start in range(n):
                cur = start
                remaining = steps
                bit = 0

                while remaining:
                    if remaining & 1:
                        cur = jumps[bit][cur]
                        if cur >= m:
                            break
                    remaining >>= 1
                    bit += 1

                # Ensure all k points occur in one circuit and the final
                # gap back to the starting point also satisfies d.
                if cur < start + n and arr[start] + perimeter - arr[cur] >= d:
                    return True

            return False

        # For k >= 4, a minimum pairwise Manhattan distance greater than
        # side is impossible on the boundary of a square.
        lo, hi = 0, side
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if feasible(mid):
                lo = mid
            else:
                hi = mid - 1

        return lo