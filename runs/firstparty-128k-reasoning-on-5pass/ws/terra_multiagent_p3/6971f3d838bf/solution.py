from typing import List


class Solution:
    def maxSubarraySum(self, nums: List[int]) -> int:
        NEG = -10**30
        n = len(nums)

        size = 1
        while size < n:
            size <<= 1

        total = [0] * (2 * size)
        pref = [NEG] * (2 * size)
        suff = [NEG] * (2 * size)
        best = [NEG] * (2 * size)

        def pull(i: int) -> None:
            left = i << 1
            right = left | 1

            total[i] = total[left] + total[right]
            pref[i] = max(pref[left], total[left] + pref[right])
            suff[i] = max(suff[right], total[right] + suff[left])
            best[i] = max(best[left], best[right], suff[left] + pref[right])

        def set_leaf(pos: int, value: int, deleted: bool) -> None:
            i = size + pos
            if deleted:
                total[i] = 0
                pref[i] = suff[i] = best[i] = NEG
            else:
                total[i] = pref[i] = suff[i] = best[i] = value

            i >>= 1
            while i:
                pull(i)
                i >>= 1

        positions = {}
        for i, value in enumerate(nums):
            positions.setdefault(value, []).append(i)
            leaf = size + i
            total[leaf] = pref[leaf] = suff[leaf] = best[leaf] = value

        # Unused padding leaves remain deleted: sum 0 and no valid subarray.
        for i in range(size - 1, 0, -1):
            pull(i)

        answer = best[1]

        # Removing a nonnegative value cannot improve the result: reinserting
        # removed values into a chosen resulting subarray only increases its sum.
        for value, indices in positions.items():
            if value >= 0:
                continue

            for pos in indices:
                set_leaf(pos, value, True)

            if best[1] != NEG:  # Do not allow deletion leaving an empty array.
                answer = max(answer, best[1])

            for pos in indices:
                set_leaf(pos, value, False)

        return answer