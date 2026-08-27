from typing import List


class Solution:
    def maxSubarraySum(self, nums: List[int]) -> int:
        best_no_delete = nums[0]
        current = nums[0]
        for value in nums[1:]:
            current = max(value, current + value)
            best_no_delete = max(best_no_delete, current)

        values = list(dict.fromkeys(nums))
        m = len(values)

        # Deleting the only distinct value would empty the array.
        if m == 1:
            return best_no_delete

        index = {value: i for i, value in enumerate(values)}
        neg_inf = -(10**30)
        inf = 10**30

        min1 = [neg_inf] * (4 * m)
        min2 = [inf] * (4 * m)
        maximum = [neg_inf] * (4 * m)
        lazy_add = [0] * (4 * m)

        def pull(node: int) -> None:
            left = node * 2
            right = left + 1

            maximum[node] = max(maximum[left], maximum[right])

            if min1[left] < min1[right]:
                min1[node] = min1[left]
                min2[node] = min(min2[left], min1[right])
            elif min1[left] > min1[right]:
                min1[node] = min1[right]
                min2[node] = min(min1[left], min2[right])
            else:
                min1[node] = min1[left]
                min2[node] = min(min2[left], min2[right])

        def apply_add(node: int, value: int) -> None:
            min1[node] += value
            if min2[node] < inf:
                min2[node] += value
            maximum[node] += value
            lazy_add[node] += value

        def apply_chmax(node: int, value: int) -> None:
            if value <= min1[node]:
                return

            old_min = min1[node]
            min1[node] = value
            if maximum[node] == old_min:
                maximum[node] = value

        def push(node: int) -> None:
            left = node * 2
            right = left + 1

            if lazy_add[node]:
                value = lazy_add[node]
                apply_add(left, value)
                apply_add(right, value)
                lazy_add[node] = 0

            parent_min = min1[node]
            if min1[left] < parent_min:
                apply_chmax(left, parent_min)
            if min1[right] < parent_min:
                apply_chmax(right, parent_min)

        def range_chmax(node: int, left: int, right: int, value: int) -> None:
            if value <= min1[node]:
                return

            if value < min2[node]:
                apply_chmax(node, value)
                return

            push(node)
            mid = (left + right) // 2
            range_chmax(node * 2, left, mid, value)
            range_chmax(node * 2 + 1, mid + 1, right, value)
            pull(node)

        def point_query(
            node: int, left: int, right: int, position: int
        ) -> int:
            if left == right:
                return min1[node]

            push(node)
            mid = (left + right) // 2
            if position <= mid:
                return point_query(node * 2, left, mid, position)
            return point_query(node * 2 + 1, mid + 1, right, position)

        def point_set(
            node: int,
            left: int,
            right: int,
            position: int,
            value: int,
        ) -> None:
            if left == right:
                min1[node] = value
                min2[node] = inf
                maximum[node] = value
                lazy_add[node] = 0
                return

            push(node)
            mid = (left + right) // 2
            if position <= mid:
                point_set(node * 2, left, mid, position, value)
            else:
                point_set(node * 2 + 1, mid + 1, right, position, value)
            pull(node)

        for value in nums:
            position = index[value]

            # The current occurrence is deleted for this state.
            unchanged = point_query(1, 0, m - 1, position)

            # For all other states:
            # dp = max(previous_dp + value, value).
            apply_add(1, value)
            range_chmax(1, 0, m - 1, value)

            # Restore the exceptional state.
            point_set(1, 0, m - 1, position, unchanged)

        return max(best_no_delete, maximum[1])