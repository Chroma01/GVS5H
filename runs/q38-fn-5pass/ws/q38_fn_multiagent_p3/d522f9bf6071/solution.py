from typing import List
from bisect import bisect_left

class Solution:
    def maximumWeight(self, intervals: List[List[int]]) -> List[int]:
        n = len(intervals)
        if n == 0:
            return []

        # Sort original indices by interval right endpoint.
        order = list(range(n))
        order.sort(key=lambda i: intervals[i][1])
        rights = [intervals[i][1] for i in order]

        NEG = -1
        size = (n + 1) * 5

        # Flat DP arrays:
        # row i stores states for the first i sorted intervals.
        # column k stores exactly k chosen intervals.
        score = [NEG] * size
        packed = [0] * size
        score[0] = 0

        # Pack a sorted tuple of up to 4 original indices into fixed-width fields.
        # Stored value is index + 1; 0 is a sentinel. This makes integer order
        # equal to lexicographic order of the padded index arrays.
        shift = max(1, n.bit_length())
        mask = (1 << shift) - 1
        s1 = shift
        s2 = shift << 1
        s3 = shift << 2

        bisect = bisect_left

        for i, idx in enumerate(order, 1):
            l, _, w = intervals[idx]

            # Number of previous intervals ending strictly before l.
            pref = bisect(rights, l, 0, i - 1)

            base = i * 5
            prev = base - 5
            pbase = pref * 5

            # Skip current interval: copy previous prefix states.
            score[base] = score[prev]
            packed[base] = packed[prev]
            score[base + 1] = score[prev + 1]
            packed[base + 1] = packed[prev + 1]
            score[base + 2] = score[prev + 2]
            packed[base + 2] = packed[prev + 2]
            score[base + 3] = score[prev + 3]
            packed[base + 3] = packed[prev + 3]
            score[base + 4] = score[prev + 4]
            packed[base + 4] = packed[prev + 4]

            x = idx + 1

            # Take current interval as the 1st chosen interval.
            ps = score[pbase]
            if ps != NEG:
                cand_s = ps + w
                cand_p = x << s3
                if cand_s > score[base + 1] or (
                    cand_s == score[base + 1] and cand_p < packed[base + 1]
                ):
                    score[base + 1] = cand_s
                    packed[base + 1] = cand_p

            # Take current interval as the 2nd chosen interval.
            ps = score[pbase + 1]
            if ps != NEG:
                cand_s = ps + w
                v0 = (packed[pbase + 1] >> s3) & mask
                if x < v0:
                    cand_p = (x << s3) | (v0 << s2)
                else:
                    cand_p = (v0 << s3) | (x << s2)

                if cand_s > score[base + 2] or (
                    cand_s == score[base + 2] and cand_p < packed[base + 2]
                ):
                    score[base + 2] = cand_s
                    packed[base + 2] = cand_p

            # Take current interval as the 3rd chosen interval.
            ps = score[pbase + 2]
            if ps != NEG:
                cand_s = ps + w
                pv = packed[pbase + 2]
                v0 = (pv >> s3) & mask
                v1 = (pv >> s2) & mask

                if x < v0:
                    cand_p = (x << s3) | (v0 << s2) | (v1 << s1)
                elif x < v1:
                    cand_p = (v0 << s3) | (x << s2) | (v1 << s1)
                else:
                    cand_p = (v0 << s3) | (v1 << s2) | (x << s1)

                if cand_s > score[base + 3] or (
                    cand_s == score[base + 3] and cand_p < packed[base + 3]
                ):
                    score[base + 3] = cand_s
                    packed[base + 3] = cand_p

            # Take current interval as the 4th chosen interval.
            ps = score[pbase + 3]
            if ps != NEG:
                cand_s = ps + w
                pv = packed[pbase + 3]
                v0 = (pv >> s3) & mask
                v1 = (pv >> s2) & mask
                v2 = (pv >> s1) & mask

                if x < v0:
                    cand_p = (x << s3) | (v0 << s2) | (v1 << s1) | v2
                elif x < v1:
                    cand_p = (v0 << s3) | (x << s2) | (v1 << s1) | v2
                elif x < v2:
                    cand_p = (v0 << s3) | (v1 << s2) | (x << s1) | v2
                else:
                    cand_p = (v0 << s3) | (v1 << s2) | (v2 << s1) | x

                if cand_s > score[base + 4] or (
                    cand_s == score[base + 4] and cand_p < packed[base + 4]
                ):
                    score[base + 4] = cand_s
                    packed[base + 4] = cand_p

        final_base = n * 5
        best_s = NEG
        best_p = 0

        # Choose the best state among k = 0..4.
        for k in range(5):
            s = score[final_base + k]
            if s == NEG:
                continue
            pv = packed[final_base + k]
            if best_s == NEG or s > best_s or (s == best_s and pv < best_p):
                best_s = s
                best_p = pv

        # Decode packed indices.
        ans = []
        for sh in (s3, s2, s1, 0):
            v = (best_p >> sh) & mask
            if v == 0:
                break
            ans.append(v - 1)

        return ans