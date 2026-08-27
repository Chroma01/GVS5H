from typing import List


class Solution:
    def maxDistance(self, side: int, points: List[List[int]], k: int) -> int:
        perimeter = 4 * side
        positions = []

        # Clockwise perimeter coordinate:
        # bottom: (0, 0) -> (side, 0)
        # right:  (side, 0) -> (side, side)
        # top:    (side, side) -> (0, side)
        # left:   (0, side) -> (0, 0)
        for x, y in points:
            if y == 0:
                pos = x
            elif x == side:
                pos = side + y
            elif y == side:
                pos = 3 * side - x
            else:
                pos = perimeter - y
            positions.append(pos)

        positions.sort()
        n = len(positions)
        doubled = positions + [p + perimeter for p in positions]
        m = 2 * n

        def feasible(distance: int) -> bool:
            if distance == 0:
                return True

            # Compute the first point at least `distance` farther along
            # the doubled perimeter using a monotonic two-pointer scan.
            nxt = [m] * m
            j = 0
            for i in range(m):
                if j < i + 1:
                    j = i + 1
                target = doubled[i] + distance
                while j < m and doubled[j] < target:
                    j += 1
                nxt[i] = j

            # Binary lifting for repeated greedy transitions.
            steps = k - 1
            levels = steps.bit_length()
            jumps = [nxt]

            for _ in range(1, levels):
                prev = jumps[-1]
                cur = [m] * m
                for i in range(m):
                    mid = prev[i]
                    if mid < m:
                        cur[i] = prev[mid]
                jumps.append(cur)

            for start in range(n):
                current = start
                limit = start + n
                remaining = steps
                bit = 0

                while remaining:
                    if remaining & 1:
                        current = jumps[bit][current]
                        if current >= limit:
                            break
                    remaining >>= 1
                    bit += 1

                if current < limit:
                    # The final selected point must be at least `distance`
                    # from the first point across the perimeter wraparound.
                    if doubled[current] - doubled[start] <= perimeter - distance:
                        return True

            return False

        # Since k >= 4, the answer cannot exceed side.
        low, high = 0, side
        while low < high:
            mid = (low + high + 1) // 2
            if feasible(mid):
                low = mid
            else:
                high = mid - 1

        return low