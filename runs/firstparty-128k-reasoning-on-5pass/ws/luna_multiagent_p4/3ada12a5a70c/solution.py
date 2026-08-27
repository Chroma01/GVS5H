from bisect import bisect_left
from typing import List


class Solution:
    def maxDistance(self, side: int, points: List[List[int]], k: int) -> int:
        perimeter = 4 * side
        positions = []

        for x, y in points:
            if y == 0:
                pos = x
            elif x == side:
                pos = side + y
            elif y == side:
                pos = 3 * side - x
            else:
                pos = 4 * side - y
            positions.append(pos)

        positions.sort()
        n = len(positions)
        doubled = positions + [p + perimeter for p in positions]
        total = 2 * n

        def feasible(distance: int) -> bool:
            if distance == 0:
                return True

            successor = [total] * total
            for i in range(total):
                successor[i] = bisect_left(
                    doubled,
                    doubled[i] + distance,
                    i + 1,
                    total,
                )

            for start in range(n):
                current = start
                limit = start + n

                for _ in range(k - 1):
                    current = successor[current]
                    if current >= limit:
                        break
                else:
                    if doubled[start] + perimeter - doubled[current] >= distance:
                        return True

            return False

        low, high = 0, side
        while low < high:
            mid = (low + high + 1) // 2
            if feasible(mid):
                low = mid
            else:
                high = mid - 1

        return low