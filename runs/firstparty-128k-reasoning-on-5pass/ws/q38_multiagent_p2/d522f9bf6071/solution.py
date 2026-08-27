from typing import List
from bisect import bisect_left

class Solution:
    def maximumWeight(self, intervals: List[List[int]]) -> List[int]:
        n = len(intervals)
        K = 4

        # Store as (right, left, original_index, weight) so sorting gives
        # right endpoint, then left endpoint, then original index.
        items = [(r, l, idx, w) for idx, (l, r, w) in enumerate(intervals)]
        items.sort()

        ends = [r for r, l, idx, w in items]
        # p[i] = number of intervals ending strictly before l_i.
        p = [bisect_left(ends, l) for r, l, idx, w in items]

        # Encode a sorted index tuple of fixed length in base `base`.
        # For the same length, integer order equals lexicographic order.
        base = max(2, n + 1)

        def decode(code: int, length: int, base: int = base) -> List[int]:
            vals = [0] * length
            for j in range(length - 1, -1, -1):
                vals[j], code = code % base, code // base
            return vals

        def insert_code(code: int, length: int, idx: int, base: int = base) -> int:
            if length == 0:
                return idx

            vals = [0] * length
            for j in range(length - 1, -1, -1):
                vals[j], code = code % base, code // base

            pos = 0
            while pos < length and vals[pos] < idx:
                pos += 1

            new_code = 0
            for j in range(length + 1):
                if j < pos:
                    v = vals[j]
                elif j == pos:
                    v = idx
                else:
                    v = vals[j - 1]
                new_code = new_code * base + v
            return new_code

        # weights[c][i] = best total weight using exactly c intervals
        # among the first i sorted intervals, or -1 if impossible.
        weights = [[0] * (n + 1) for _ in range(K + 1)]
        for c in range(1, K + 1):
            weights[c] = [-1] * (n + 1)

        # codes[c][i] encodes the lexicographically smallest sorted index tuple
        # achieving weights[c][i].
        codes = [[0] * (n + 1) for _ in range(K + 1)]

        for i, (r, l, idx, w) in enumerate(items):
            # Skip interval i.
            for c in range(K + 1):
                weights[c][i + 1] = weights[c][i]
                codes[c][i + 1] = codes[c][i]

            pi = p[i]

            # Take interval i after a compatible prefix.
            for c in range(1, min(K, i + 1) + 1):
                prev_w = weights[c - 1][pi]
                if prev_w < 0:
                    continue

                cand_w = prev_w + w
                cur_w = weights[c][i + 1]

                if cand_w > cur_w:
                    weights[c][i + 1] = cand_w
                    codes[c][i + 1] = insert_code(codes[c - 1][pi], c - 1, idx)
                elif cand_w == cur_w:
                    cand_code = insert_code(codes[c - 1][pi], c - 1, idx)
                    if cand_code < codes[c][i + 1]:
                        codes[c][i + 1] = cand_code

        best_w = -1
        best = []

        # Compare across exact counts 0..4 by weight, then lexicographic list.
        for c in range(K + 1):
            w = weights[c][n]
            if w < 0:
                continue
            cand = decode(codes[c][n], c)
            if w > best_w or (w == best_w and cand < best):
                best_w = w
                best = cand

        return best