from typing import List
from collections import defaultdict


class Solution:
    def maxSubarraySum(self, nums: List[int]) -> int:
        neg_inf = -10**30
        n = len(nums)

        # (total sum, maximum non-empty prefix, maximum non-empty suffix,
        #  maximum non-empty subarray)
        identity = (0, neg_inf, neg_inf, neg_inf)

        def merge(a, b):
            total = a[0] + b[0]
            prefix = max(a[1], a[0] + b[1])
            suffix = max(b[2], b[0] + a[2])
            best = max(a[3], b[3], a[2] + b[1])
            return total, prefix, suffix, best

        size = 1
        while size < n:
            size <<= 1

        tree = [identity] * (2 * size)
        positions = defaultdict(list)

        for i, value in enumerate(nums):
            tree[size + i] = (value, value, value, value)
            if value < 0:
                positions[value].append(i)

        for i in range(size - 1, 0, -1):
            tree[i] = merge(tree[i << 1], tree[i << 1 | 1])

        def update(index, summary):
            node = size + index
            tree[node] = summary
            node >>= 1
            while node:
                tree[node] = merge(tree[node << 1], tree[node << 1 | 1])
                node >>= 1

        answer = tree[1][3]

        # Deleting a nonnegative value cannot improve the answer: reinserting
        # it into a corresponding interval only preserves or increases sum.
        for value, indices in positions.items():
            # Removing all elements is forbidden.
            if len(indices) == n:
                continue

            for index in indices:
                update(index, identity)

            answer = max(answer, tree[1][3])

            original = (value, value, value, value)
            for index in indices:
                update(index, original)

        return answer