from typing import List


class Solution:
    def maxDistance(self, side: int, points: List[List[int]], k: int) -> int:
        perimeter = 4 * side
        positions = []

        # Clockwise perimeter coordinate, with each corner assigned once.
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

        def feasible(distance: int) -> bool:
            if distance == 0:
                return True

            if k * distance > perimeter:
                return False

            doubled = positions + [p + perimeter for p in positions]
            m = 2 * n

            # next_index[i] is the first index j with
            # doubled[j] - doubled[i] >= distance.
            next_index = [m] * m
            j = 0

            for i in range(m):
                if j < i + 1:
                    j = i + 1
                target = doubled[i] + distance
                while j < m and doubled[j] < target:
                    j += 1
                next_index[i] = j

            # Fix each possible first point and greedily take the earliest
            # possible next point.
            for start in range(n):
                current = start

                for _ in range(k - 1):
                    current = next_index[current]
                    if current >= start + n:
                        break
                else:
                    closing_gap = doubled[start] + perimeter - doubled[current]
                    if closing_gap >= distance:
                        return True

            return False

        low, high = 0, side + 1

        while low + 1 < high:
            mid = (low + high) // 2
            if feasible(mid):
                low = mid
            else:
                high = mid

        return low