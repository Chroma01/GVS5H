from typing import List


class Solution:
    def maxSubarraySum(self, nums: List[int]) -> int:
        values = list(set(nums))
        index = {value: i for i, value in enumerate(values)}
        m = len(values)

        size = 1
        while size < m:
            size <<= 1

        total = size << 1
        NEG = -10**30
        INF = 10**30

        mn = [NEG] * total
        smn = [INF] * total
        mx = [NEG] * total
        cnt = [1] * total
        lazy = [0] * total

        for i in range(size - 1, 0, -1):
            left = i << 1
            right = left | 1
            cnt[i] = cnt[left] + cnt[right]

        def pull(i: int) -> None:
            left = i << 1
            right = left | 1

            mx[i] = max(mx[left], mx[right])

            if mn[left] < mn[right]:
                mn[i] = mn[left]
                cnt[i] = cnt[left]
                smn[i] = min(smn[left], mn[right])
            elif mn[left] > mn[right]:
                mn[i] = mn[right]
                cnt[i] = cnt[right]
                smn[i] = min(mn[left], smn[right])
            else:
                mn[i] = mn[left]
                cnt[i] = cnt[left] + cnt[right]
                smn[i] = min(smn[left], smn[right])

        def apply_add(i: int, value: int) -> None:
            mn[i] += value
            mx[i] += value
            if smn[i] < INF // 2:
                smn[i] += value
            lazy[i] += value

        def apply_chmax(i: int, value: int) -> None:
            if value <= mn[i]:
                return
            old_min = mn[i]
            mn[i] = value
            if mx[i] == old_min:
                mx[i] = value

        def push(i: int) -> None:
            left = i << 1
            right = left | 1

            if lazy[i]:
                value = lazy[i]
                apply_add(left, value)
                apply_add(right, value)
                lazy[i] = 0

            if mn[left] < mn[i]:
                apply_chmax(left, mn[i])
            if mn[right] < mn[i]:
                apply_chmax(right, mn[i])

        def range_add(
            i: int, lo: int, hi: int,
            qlo: int, qhi: int, value: int
        ) -> None:
            if qlo >= hi or qhi <= lo:
                return

            if qlo <= lo and hi <= qhi:
                apply_add(i, value)
                return

            push(i)
            mid = (lo + hi) >> 1
            range_add(i << 1, lo, mid, qlo, qhi, value)
            range_add(i << 1 | 1, mid, hi, qlo, qhi, value)
            pull(i)

        def range_chmax(
            i: int, lo: int, hi: int,
            qlo: int, qhi: int, value: int
        ) -> None:
            if qlo >= hi or qhi <= lo or value <= mn[i]:
                return

            if qlo <= lo and hi <= qhi and value < smn[i]:
                apply_chmax(i, value)
                return

            if hi - lo == 1:
                apply_chmax(i, value)
                return

            push(i)
            mid = (lo + hi) >> 1
            range_chmax(i << 1, lo, mid, qlo, qhi, value)
            range_chmax(i << 1 | 1, mid, hi, qlo, qhi, value)
            pull(i)

        def replace_point(
            i: int, lo: int, hi: int,
            pos: int, value: int
        ) -> int:
            if hi - lo == 1:
                old = mn[i]
                mn[i] = value
                smn[i] = INF
                mx[i] = value
                cnt[i] = 1
                lazy[i] = 0
                return old

            push(i)
            mid = (lo + hi) >> 1
            if pos < mid:
                old = replace_point(i << 1, lo, mid, pos, value)
            else:
                old = replace_point(i << 1 | 1, mid, hi, pos, value)
            pull(i)
            return old

        answer = NEG
        kadane = NEG

        for value in nums:
            kadane = max(value, kadane + value)
            answer = max(answer, kadane)

            pos = index[value]

            # Temporarily remove the state for deleting `value`.
            old = replace_point(1, 0, size, pos, NEG)

            # Apply dp = max(dp + value, value) to every other state.
            # The skipped state must be excluded from both updates.
            range_add(1, 0, size, 0, pos, value)
            range_add(1, 0, size, pos + 1, m, value)

            range_chmax(1, 0, size, 0, pos, value)
            range_chmax(1, 0, size, pos + 1, m, value)

            # Restore the skipped state unchanged.
            replace_point(1, 0, size, pos, old)

            answer = max(answer, mx[1])

        return answer