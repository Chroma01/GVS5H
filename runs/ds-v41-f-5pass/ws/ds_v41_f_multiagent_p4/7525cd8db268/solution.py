from typing import List

class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        m = len(conflictingPairs)
        if m == 0:
            return n * (n + 1) // 2

        # Bucket each pair by its larger endpoint b.
        buckets = [[] for _ in range(n + 1)]
        for idx, pair in enumerate(conflictingPairs):
            a, b = pair
            if a > b:
                a, b = b, a
            buckets[b].append((a, idx))

        cnt = [0] * (n + 2)      # multiplicity of each active smaller endpoint a
        owner = [-1] * (n + 2)   # pair id that first activated a
        gain = [0] * m           # total extra valid subarrays from removing pair i

        M = 0   # largest active smaller endpoint
        S = 0   # second-largest distinct active smaller endpoint
        base = 0

        for r in range(1, n + 1):
            # Activate all pairs whose larger endpoint equals r.
            for a, idx in buckets[r]:
                if cnt[a] == 0:
                    owner[a] = idx
                    if a > M:
                        S = M
                        M = a
                    elif a > S:
                        S = a
                cnt[a] += 1

            # Subarrays ending at r that avoid every active pair: r - M.
            base += r - M

            # Removing the unique pair attaining M drops the bound to S.
            if M > 0 and cnt[M] == 1:
                gain[owner[M]] += M - S

        return base + max(gain)