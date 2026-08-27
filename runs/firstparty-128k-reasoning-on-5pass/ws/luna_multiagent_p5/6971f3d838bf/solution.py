from typing import List


class SegmentTreeBeats:
    def __init__(self, n: int, neg_inf: int):
        self.n = n
        self.neg_inf = neg_inf
        size = 4 * max(1, n)
        self.mn = [neg_inf] * size
        self.se = [10**30] * size
        self.mx = [neg_inf] * size
        self.lazy = [neg_inf] * size

    def _apply_chmax(self, p: int, x: int) -> None:
        if x <= self.mn[p]:
            return
        old_min = self.mn[p]
        if self.mx[p] == old_min:
            self.mx[p] = x
        self.mn[p] = x
        if self.lazy[p] < x:
            self.lazy[p] = x

    def _pull(self, p: int) -> None:
        left = p * 2
        right = left + 1

        self.mx[p] = max(self.mx[left], self.mx[right])

        if self.mn[left] < self.mn[right]:
            self.mn[p] = self.mn[left]
            self.se[p] = min(self.se[left], self.mn[right])
        elif self.mn[left] > self.mn[right]:
            self.mn[p] = self.mn[right]
            self.se[p] = min(self.mn[left], self.se[right])
        else:
            self.mn[p] = self.mn[left]
            self.se[p] = min(self.se[left], self.se[right])

    def _push(self, p: int) -> None:
        if self.lazy[p] != self.neg_inf:
            value = self.lazy[p]
            self._apply_chmax(p * 2, value)
            self._apply_chmax(p * 2 + 1, value)
            self.lazy[p] = self.neg_inf

    def _set(self, p: int, left: int, right: int,
             index: int, value: int) -> None:
        if right - left == 1:
            self.mn[p] = value
            self.mx[p] = value
            self.se[p] = 10**30
            self.lazy[p] = self.neg_inf
            return

        self._push(p)
        middle = (left + right) // 2

        if index < middle:
            self._set(p * 2, left, middle, index, value)
        else:
            self._set(p * 2 + 1, middle, right, index, value)

        self._pull(p)

    def set_point(self, index: int, value: int) -> None:
        self._set(1, 0, self.n, index, value)

    def _add(self, p: int, left: int, right: int,
             index: int, delta: int) -> None:
        if right - left == 1:
            self.mn[p] += delta
            self.mx[p] += delta
            return

        self._push(p)
        middle = (left + right) // 2

        if index < middle:
            self._add(p * 2, left, middle, index, delta)
        else:
            self._add(p * 2 + 1, middle, right, index, delta)

        self._pull(p)

    def add_point(self, index: int, delta: int) -> None:
        self._add(1, 0, self.n, index, delta)

    def _chmax(self, p: int, left: int, right: int,
               qleft: int, qright: int, value: int) -> None:
        if qright <= left or right <= qleft or value <= self.mn[p]:
            return

        if qleft <= left and right <= qright and value < self.se[p]:
            self._apply_chmax(p, value)
            return

        self._push(p)
        middle = (left + right) // 2

        self._chmax(p * 2, left, middle, qleft, qright, value)
        self._chmax(p * 2 + 1, middle, right, qleft, qright, value)

        self._pull(p)

    def range_chmax(self, left: int, right: int, value: int) -> None:
        if left < right:
            self._chmax(1, 0, self.n, left, right, value)

    def maximum(self) -> int:
        return self.mx[1]


class Solution:
    def maxSubarraySum(self, nums: List[int]) -> int:
        n = len(nums)
        neg_inf = -10**30
        tree = SegmentTreeBeats(n, neg_inf)

        cumulative = nums[0]
        best_end = nums[0]
        answer = nums[0]

        value_to_id = {nums[0]: 0}
        active = [False] * n
        active_count = 0

        for value in nums[1:]:
            old_sum = cumulative

            first_value = nums[0]
            first_id = value_to_id[first_value]

            # The first value may only be deleted once a different value
            # appears. Before that point, every possible subarray consists
            # entirely of the value being deleted, so its deletion state
            # must start fresh at the current position.
            if value != first_value and not active[first_id]:
                tree.set_point(first_id, -old_sum)
                active[first_id] = True
                active_count += 1

            if value not in value_to_id:
                value_id = len(value_to_id)
                value_to_id[value] = value_id

                # This value has not appeared in the preceding prefix, so
                # the ordinary Kadane state is valid before deleting it.
                tree.set_point(value_id, best_end - old_sum)
                active[value_id] = True
                active_count += 1
            else:
                value_id = value_to_id[value]

            # For the candidate deleting the current value, skip it.
            if active[value_id]:
                tree.add_point(value_id, -value)

            # Every other deletion candidate keeps the current value.
            threshold = -old_sum
            tree.range_chmax(0, value_id, threshold)
            tree.range_chmax(value_id + 1, active_count, threshold)

            cumulative += value
            best_end = max(value, best_end + value)

            answer = max(answer, best_end)

            if active_count:
                answer = max(answer, cumulative + tree.maximum())

        return answer