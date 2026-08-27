from typing import List


class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        n = len(nums)

        prefix_nums = [0] * (n + 1)
        prefix_cost = [0] * (n + 1)
        for i in range(n):
            prefix_nums[i + 1] = prefix_nums[i] + nums[i]
            prefix_cost[i + 1] = prefix_cost[i] + cost[i]

        inf = 10**30
        previous = [inf] * (n + 1)
        previous[0] = 0
        answer = inf

        for segments in range(1, n + 1):
            current = [inf] * (n + 1)

            slopes = []
            intercepts = []
            pointer = 0

            def add_line(m: int, b: int) -> None:
                nonlocal pointer

                while len(slopes) >= 2:
                    m1, b1 = slopes[-2], intercepts[-2]
                    m2, b2 = slopes[-1], intercepts[-1]

                    # Remove the middle line if its optimal interval is empty.
                    if (b2 - b1) * (m2 - m) >= (b - b2) * (m1 - m2):
                        slopes.pop()
                        intercepts.pop()
                        if pointer >= len(slopes):
                            pointer = len(slopes) - 1
                    else:
                        break

                slopes.append(m)
                intercepts.append(b)

            def query(x: int) -> int:
                nonlocal pointer

                while (
                    pointer + 1 < len(slopes)
                    and slopes[pointer + 1] * x + intercepts[pointer + 1]
                    <= slopes[pointer] * x + intercepts[pointer]
                ):
                    pointer += 1

                return slopes[pointer] * x + intercepts[pointer]

            for right in range(segments, n + 1):
                left = right - 1

                if previous[left] < inf:
                    add_line(-prefix_cost[left], previous[left])

                if slopes:
                    x = prefix_nums[right] + k * segments
                    current[right] = prefix_cost[right] * x + query(x)

            answer = min(answer, current[n])
            previous = current

        return answer