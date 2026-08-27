from typing import List


class Solution:
    def maxSubarraySum(self, nums: List[int]) -> int:
        n = len(nums)
        negative_positions = {}

        size = 1
        while size < n:
            size <<= 1

        NEG_INF = -10**30

        # (total_sum, has_retained,
        #  best_prefix_sum, prefix_has_retained,
        #  best_suffix_sum, suffix_has_retained,
        #  best_valid_subarray_sum)
        inactive_node = (0, False, 0, False, 0, False, NEG_INF)
        tree = [inactive_node] * (2 * size)

        def active_node(value: int):
            if value > 0:
                return (value, True, value, True, value, True, value)
            if value == 0:
                return (0, True, 0, True, 0, True, 0)
            # Empty prefix/suffix is numerically preferable, but invalid as a
            # retained non-empty subarray.
            return (value, True, 0, False, 0, False, value)

        def merge(left, right):
            lsum, lhas, lpre, lpre_valid, lsuf, lsuf_valid, lans = left
            rsum, rhas, rpre, rpre_valid, rsuf, rsuf_valid, rans = right

            total = lsum + rsum
            has = lhas or rhas

            # Prefix: either a prefix of left, or all of left plus a prefix
            # of right. Empty prefixes are allowed internally.
            p1_sum, p1_valid = lpre, lpre_valid
            p2_sum, p2_valid = lsum + rpre, lhas or rpre_valid
            if p1_sum > p2_sum:
                pre, pre_valid = p1_sum, p1_valid
            elif p2_sum > p1_sum:
                pre, pre_valid = p2_sum, p2_valid
            else:
                pre, pre_valid = p1_sum, p1_valid or p2_valid

            # Symmetric suffix computation.
            s1_sum, s1_valid = rsuf, rsuf_valid
            s2_sum, s2_valid = rsum + lsuf, rhas or lsuf_valid
            if s1_sum > s2_sum:
                suf, suf_valid = s1_sum, s1_valid
            elif s2_sum > s1_sum:
                suf, suf_valid = s2_sum, s2_valid
            else:
                suf, suf_valid = s1_sum, s1_valid or s2_valid

            best = max(lans, rans)
            cross = lsuf + rpre
            if (lsuf_valid or rpre_valid) and cross > best:
                best = cross

            return (total, has, pre, pre_valid, suf, suf_valid, best)

        for i, value in enumerate(nums):
            tree[size + i] = active_node(value)
            if value < 0:
                negative_positions.setdefault(value, []).append(i)

        for node in range(size - 1, 0, -1):
            tree[node] = merge(tree[node << 1], tree[node << 1 | 1])

        def set_leaf(index: int, node_value) -> None:
            pos = size + index
            tree[pos] = node_value
            pos >>= 1
            while pos:
                tree[pos] = merge(tree[pos << 1], tree[pos << 1 | 1])
                pos >>= 1

        answer = tree[1][6]

        # Removing zero or a positive value cannot increase a maximum subarray
        # sum, since retaining it never lowers the sum of a candidate subarray.
        for value, positions in negative_positions.items():
            if len(positions) == n:
                continue

            for index in positions:
                set_leaf(index, inactive_node)

            answer = max(answer, tree[1][6])

            original_node = active_node(value)
            for index in positions:
                set_leaf(index, original_node)

        return answer