from typing import List


class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        # Bucket each conflict by its larger endpoint b, normalized so a < b.
        buckets = [[] for _ in range(n + 1)]
        m = len(conflictingPairs)
        for idx, (x, y) in enumerate(conflictingPairs):
            if x < y:
                a, b = x, y
            else:
                a, b = y, x
            buckets[b].append((a, idx))

        gain = [0] * m           # extra valid subarrays obtained by deleting pair idx
        owner_of_a = {}          # a-value -> a pair index carrying that a
        cnt = {}                 # a-value -> number of active pairs with that a
        M = 0                    # largest active a (0 if none)
        S = 0                    # second-largest distinct active a
        base = 0

        for r in range(1, n + 1):
            # Activate every conflict whose larger endpoint equals r.
            for a, idx in buckets[r]:
                c = cnt.get(a, 0) + 1
                cnt[a] = c
                if c == 1:
                    owner_of_a[a] = idx
                if a > M:
                    S = M
                    M = a
                elif a < M and a > S:
                    S = a

            # Subarrays [l, r] are valid iff l > M, i.e. l in (M, r].
            base += r - M

            # Deleting the unique pair supplying M lowers the limit to S.
            if M > 0 and cnt[M] == 1:
                gain[owner_of_a[M]] += M - S

        return base + max(gain)


if __name__ == "__main__":
    sol = Solution()
    # Example 1 -> expected 9
    print(sol.maxSubarrays(4, [[2, 3], [1, 4]]))
    # Example 2 -> expected 12
    print(sol.maxSubarrays(5, [[1, 2], [2, 5], [3, 5]]))