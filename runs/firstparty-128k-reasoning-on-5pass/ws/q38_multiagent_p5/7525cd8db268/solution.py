from typing import List

class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        total = n * (n + 1) // 2
        m = len(conflictingPairs)
        if m == 0:
            return total

        by_r = [[] for _ in range(n + 1)]
        for idx, (a, b) in enumerate(conflictingPairs):
            if a > b:
                a, b = b, a
            by_r[b].append((a, idx))

        cnt = [0] * (n + 1)
        first_id = [-1] * (n + 1)
        gain = [0] * m

        top1 = 0
        top2 = 0
        bad = 0

        for r in range(1, n + 1):
            for l, idx in by_r[r]:
                cnt[l] += 1
                if cnt[l] == 1:
                    first_id[l] = idx

                if l > top1:
                    top2 = top1
                    top1 = l
                elif l < top1 and l > top2:
                    top2 = l

            bad += top1
            if top1 > 0 and cnt[top1] == 1:
                gain[first_id[top1]] += top1 - top2

        return total - bad + max(gain)