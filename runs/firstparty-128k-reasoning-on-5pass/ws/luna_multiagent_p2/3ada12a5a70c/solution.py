from typing import List


class Solution:
    def maxDistance(self, side: int, points: List[List[int]], k: int) -> int:
        perimeter = 4 * side
        positions = []

        # Assign each boundary point a unique position on the perimeter.
        # The order is counterclockwise starting from (0, 0):
        # bottom -> right -> top -> left.
        for x, y in points:
            if y == 0:
                t = x
            elif x == side:
                t = side + y
            elif y == side:
                t = 3 * side - x
            else:
                t = 4 * side - y
            positions.append(t)

        positions.sort()
        n = len(positions)

        def feasible(distance: int) -> bool:
            if distance == 0:
                return True

            doubled = positions + [x + perimeter for x in positions]
            total = 2 * n

            # nxt[i] is the first index j such that
            # doubled[j] - doubled[i] >= distance.
            nxt = [total] * total
            j = 1

            for i in range(total):
                if j < i + 1:
                    j = i + 1

                target = doubled[i] + distance
                while j < total and doubled[j] < target:
                    j += 1
                nxt[i] = j

            # Try every point as the first selected point.
            for start in range(n):
                current = start
                valid = True

                for _ in range(k - 1):
                    current = nxt[current]
                    if current >= start + n:
                        valid = False
                        break

                if valid:
                    # Check the final circular gap back to the start.
                    if doubled[current] + distance <= doubled[start] + perimeter:
                        return True

            return False

        # Since k >= 4, the minimum cyclic gap cannot exceed perimeter / 4 = side.
        low, high = 0, side

        while low < high:
            mid = (low + high + 1) // 2
            if feasible(mid):
                low = mid
            else:
                high = mid - 1

        return low