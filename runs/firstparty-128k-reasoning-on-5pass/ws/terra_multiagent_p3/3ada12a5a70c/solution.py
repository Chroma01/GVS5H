from typing import List


class Solution:
    def maxDistance(self, side: int, points: List[List[int]], k: int) -> int:
        perimeter = 4 * side

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
        doubled = pos + [x + perimeter for x in pos]
        m = 2 * n

        def feasible(dist: int) -> bool:
            nxt = [m] * m
            j = 0

            for i in range(m):
                if j <= i:
                    j = i + 1
                while j < m and doubled[j] - doubled[i] < dist:
                    j += 1
                nxt[i] = j

            for start in range(n):
                cur = start

                for _ in range(k - 1):
                    cur = nxt[cur]
                    if cur >= m:
                        break

                if cur < m and doubled[cur] <= doubled[start] + perimeter - dist:
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