from typing import List

class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        m = len(conflictingPairs)
        # bucket by right endpoint b: store (a, id) for each normalized pair
        bucket = [[] for _ in range(n + 1)]
        for idx, (x, y) in enumerate(conflictingPairs):
            a, b = (x, y) if x < y else (y, x)
            bucket[b].append((a, idx))

        # Fenwick tree over a-values in [1, n], storing counts of active pairs per a
        tree = [0] * (n + 1)
        top_bit = 1 << (n.bit_length() - 1)

        def add(i, d):
            while i <= n:
                tree[i] += d
                i += i & (-i)

        def kth(k):
            # smallest index whose prefix sum >= k (k >= 1)
            idx = 0
            bit = top_bit
            while bit:
                nxt = idx + bit
                if nxt <= n and tree[nxt] < k:
                    idx = nxt
                    k -= tree[nxt]
                bit >>= 1
            return idx + 1

        cnt = [0] * (n + 1)
        owner = [0] * (n + 1)   # id+1 of the unique active pair with this a; -1 if ambiguous
        gain = [0] * m

        base = 0
        total = 0
        for R in range(1, n + 1):
            for a, idx in bucket[R]:
                if cnt[a] == 0:
                    owner[a] = idx + 1
                else:
                    owner[a] = -1
                cnt[a] += 1
                add(a, 1)
                total += 1

            if total == 0:
                base += R
                continue

            top = kth(total)
            base += R - top

            if cnt[top] == 1:
                rem = total - 1  # total - cnt[top]
                second = kth(rem) if rem > 0 else 0
                oid = owner[top] - 1
                gain[oid] += top - second

        return base + max(gain)