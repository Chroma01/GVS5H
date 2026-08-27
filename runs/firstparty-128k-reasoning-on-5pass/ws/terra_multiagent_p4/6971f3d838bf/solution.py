from typing import List


class Solution:
    def maxSubarraySum(self, nums: List[int]) -> int:
        n = len(nums)

        size = 1
        while size < n:
            size <<= 1

        cnt = [0] * (2 * size)
        total = [0] * (2 * size)
        pref = [0] * (2 * size)
        suff = [0] * (2 * size)
        best = [0] * (2 * size)

        positions = {}

        for i, value in enumerate(nums):
            p = size + i
            cnt[p] = 1
            total[p] = pref[p] = suff[p] = best[p] = value
            if value < 0:
                positions.setdefault(value, []).append(i)

        def pull(p: int) -> None:
            left = p << 1
            right = left | 1

            if cnt[left] == 0:
                cnt[p] = cnt[right]
                total[p] = total[right]
                pref[p] = pref[right]
                suff[p] = suff[right]
                best[p] = best[right]
                return

            if cnt[right] == 0:
                cnt[p] = cnt[left]
                total[p] = total[left]
                pref[p] = pref[left]
                suff[p] = suff[left]
                best[p] = best[left]
                return

            cnt[p] = cnt[left] + cnt[right]
            total[p] = total[left] + total[right]
            pref[p] = max(pref[left], total[left] + pref[right])
            suff[p] = max(suff[right], total[right] + suff[left])
            best[p] = max(best[left], best[right], suff[left] + pref[right])

        for p in range(size - 1, 0, -1):
            pull(p)

        def set_active(index: int, active: bool) -> None:
            p = size + index
            if active:
                value = nums[index]
                cnt[p] = 1
                total[p] = pref[p] = suff[p] = best[p] = value
            else:
                cnt[p] = 0
                total[p] = pref[p] = suff[p] = best[p] = 0

            p >>= 1
            while p:
                pull(p)
                p >>= 1

        answer = best[1]

        for indices in positions.values():
            if len(indices) == n:
                continue

            for index in indices:
                set_active(index, False)

            answer = max(answer, best[1])

            for index in indices:
                set_active(index, True)

        return answer