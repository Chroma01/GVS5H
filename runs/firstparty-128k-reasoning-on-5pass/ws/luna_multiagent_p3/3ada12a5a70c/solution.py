from typing import List


class Solution:
    def maxDistance(self, side: int, points: List[List[int]], k: int) -> int:
        perimeter = 4 * side

        # Map each boundary point to a unique counter-clockwise perimeter
        # coordinate in [0, perimeter).
        positions = []
        for x, y in points:
            if y == 0:
                t = x
            elif x == side:
                t = side + y
            elif y == side:
                t = 2 * side + (side - x)
            else:
                t = 3 * side + (side - y)
            positions.append(t)

        positions.sort()
        n = len(positions)
        doubled = positions + [p + perimeter for p in positions]
        m = 2 * n

        def feasible(distance: int) -> bool:
            if distance == 0:
                return True

            # next_index[i] is the first point at least `distance` farther
            # along the doubled perimeter.
            next_index = [m] * m
            right = 1

            for i in range(m):
                if right <= i:
                    right = i + 1

                target = doubled[i] + distance
                while right < m and doubled[right] < target:
                    right += 1

                next_index[i] = right

            # Binary lifting for applying k - 1 greedy transitions.
            jumps = k - 1
            levels = [next_index + [m]]

            for _ in range(1, jumps.bit_length()):
                previous = levels[-1]
                levels.append([previous[previous[i]] for i in range(m + 1)])

            # Try every point as the first selected point.
            for start in range(n):
                index = start
                remaining = jumps
                bit = 0

                while remaining:
                    if remaining & 1:
                        index = levels[bit][index]
                        if index >= start + n:
                            break
                    remaining >>= 1
                    bit += 1

                if index < start + n:
                    # The final selected point must also be far enough from
                    # the first point across the cyclic boundary.
                    if doubled[start] + perimeter - doubled[index] >= distance:
                        return True

            return False

        low, high = 0, side + 1

        while low + 1 < high:
            middle = (low + high) // 2
            if feasible(middle):
                low = middle
            else:
                high = middle

        return low