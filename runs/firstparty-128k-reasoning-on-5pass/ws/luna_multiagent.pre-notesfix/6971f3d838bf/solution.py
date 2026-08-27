from typing import List


class Solution:
    def maxSubarraySum(self, nums: List[int]) -> int:
        n = len(nums)
        size = 1
        while size < n:
            size <<= 1

        NEG = -10**30

        total = [0] * (2 * size)
        pref = [NEG] * (2 * size)
        suff = [NEG] * (2 * size)
        best = [NEG] * (2 * size)

        # Build leaves. Leaves beyond n are the empty-sequence identity.
        for i, value in enumerate(nums):
            p = size + i
            total[p] = value
            pref[p] = value
            suff[p] = value
            best[p] = value

        def pull(p: int) -> None:
            left = p << 1
            right = left | 1

            total[p] = total[left] + total[right]
            pref[p] = max(pref[left], total[left] + pref[right])
            suff[p] = max(suff[right], total[right] + suff[left])
            best[p] = max(
                best[left],
                best[right],
                suff[left] + pref[right],
            )

        for p in range(size - 1, 0, -1):
            pull(p)

        def update(index: int, value: int, empty: bool) -> None:
            p = size + index
            if empty:
                total[p] = 0
                pref[p] = NEG
                suff[p] = NEG
                best[p] = NEG
            else:
                total[p] = value
                pref[p] = value
                suff[p] = value
                best[p] = value

            p >>= 1
            while p:
                pull(p)
                p >>= 1

        positions = {}
        for i, value in enumerate(nums):
            positions.setdefault(value, []).append(i)

        answer = best[1]  # No deletion.

        for value, indices in positions.items():
            # Removing this value must leave a non-empty array.
            if len(indices) == n:
                continue

            for index in indices:
                update(index, 0, True)

            answer = max(answer, best[1])

            for index in indices:
                update(index, nums[index], False)

        return answer