from typing import List


class Solution:
    def maxSubarraySum(self, nums: List[int]) -> int:
        values = {v: i for i, v in enumerate(sorted(set(nums)))}
        m = len(values)

        NEG = -10**30
        INF = 10**30

        mn = [INF] * (4 * m)
        smn = [INF] * (4 * m)
        cnt = [0] * (4 * m)
        mx = [NEG] * (4 * m)
        add = [0] * (4 * m)
        floor_tag = [NEG] * (4 * m)

        def pull(p: int) -> None:
            left = p * 2
            right = left + 1

            mx[p] = max(mx[left], mx[right])

            if mn[left] < mn[right]:
                mn[p] = mn[left]
                cnt[p] = cnt[left]
                smn[p] = min(smn[left], mn[right])
            elif mn[left] > mn[right]:
                mn[p] = mn[right]
                cnt[p] = cnt[right]
                smn[p] = min(mn[left], smn[right])
            else:
                mn[p] = mn[left]
                cnt[p] = cnt[left] + cnt[right]
                smn[p] = min(smn[left], smn[right])

        def apply_add(p: int, value: int) -> None:
            if cnt[p] == 0:
                return

            mn[p] += value
            if smn[p] < INF:
                smn[p] += value
            mx[p] += value
            add[p] += value

            if floor_tag[p] > NEG:
                floor_tag[p] += value

        def apply_floor(p: int, value: int) -> None:
            if cnt[p] == 0 or value <= mn[p]:
                return

            mn[p] = value
            mx[p] = max(mx[p], value)
            floor_tag[p] = max(floor_tag[p], value)

        def push(p: int) -> None:
            left = p * 2
            right = left + 1

            if add[p]:
                apply_add(left, add[p])
                apply_add(right, add[p])
                add[p] = 0

            if floor_tag[p] > NEG:
                apply_floor(left, floor_tag[p])
                apply_floor(right, floor_tag[p])
                floor_tag[p] = NEG

        def build(p: int, lo: int, hi: int) -> None:
            if lo == hi:
                mn[p] = mx[p] = 0
                smn[p] = INF
                cnt[p] = 1
                return

            mid = (lo + hi) // 2
            build(p * 2, lo, mid)
            build(p * 2 + 1, mid + 1, hi)
            pull(p)

        def set_active(
            p: int,
            lo: int,
            hi: int,
            pos: int,
            value: int,
            active: bool,
        ) -> None:
            if lo == hi:
                if active:
                    mn[p] = mx[p] = value
                    smn[p] = INF
                    cnt[p] = 1
                else:
                    mn[p] = smn[p] = INF
                    mx[p] = NEG
                    cnt[p] = 0

                add[p] = 0
                floor_tag[p] = NEG
                return

            push(p)
            mid = (lo + hi) // 2

            if pos <= mid:
                set_active(p * 2, lo, mid, pos, value, active)
            else:
                set_active(p * 2 + 1, mid + 1, hi, pos, value, active)

            pull(p)

        def range_add(
            p: int,
            lo: int,
            hi: int,
            ql: int,
            qr: int,
            value: int,
        ) -> None:
            if ql > hi or qr < lo or cnt[p] == 0:
                return

            if ql <= lo and hi <= qr:
                apply_add(p, value)
                return

            push(p)
            mid = (lo + hi) // 2
            range_add(p * 2, lo, mid, ql, qr, value)
            range_add(p * 2 + 1, mid + 1, hi, ql, qr, value)
            pull(p)

        def range_floor(
            p: int,
            lo: int,
            hi: int,
            ql: int,
            qr: int,
            value: int,
        ) -> None:
            if ql > hi or qr < lo or cnt[p] == 0 or value <= mn[p]:
                return

            if ql <= lo and hi <= qr and value < smn[p]:
                apply_floor(p, value)
                return

            if lo == hi:
                apply_floor(p, value)
                return

            push(p)
            mid = (lo + hi) // 2
            range_floor(p * 2, lo, mid, ql, qr, value)
            range_floor(p * 2 + 1, mid + 1, hi, ql, qr, value)
            pull(p)

        build(1, 0, m - 1)

        best_no_delete = NEG
        ending = NEG
        inactive = None
        answer = NEG

        for i, y in enumerate(nums):
            idx = values[y]

            if i == 0:
                ending = y
                best_no_delete = y

                # Deleting the only value seen so far would leave an empty array.
                set_active(1, 0, m - 1, idx, 0, False)
                inactive = idx
            else:
                ending = max(y, ending + y)
                best_no_delete = max(best_no_delete, ending)

                # The first value becomes deletable once another distinct value exists.
                if inactive is not None and inactive != idx:
                    set_active(1, 0, m - 1, inactive, 0, True)
                    inactive = None

            # For every deletion value x != y:
            # dp[x] = max(dp[x] + y, y).
            if idx > 0:
                range_add(1, 0, m - 1, 0, idx - 1, y)
                range_floor(1, 0, m - 1, 0, idx - 1, y)

            if idx + 1 < m:
                range_add(1, 0, m - 1, idx + 1, m - 1, y)
                range_floor(1, 0, m - 1, idx + 1, m - 1, y)

            answer = max(answer, best_no_delete, mx[1])

        return answer