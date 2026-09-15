from typing import List
from bisect import bisect_left

class Solution:
    def maximumWeight(self, intervals: List[List[int]]) -> List[int]:
        n = len(intervals)
        if n == 0:
            return []

        # Sort by right endpoint. Keep original 0-based index.
        arr = [(r, l, w, idx) for idx, (l, r, w) in enumerate(intervals)]
        arr.sort()

        ends = [item[0] for item in arr]

        # compat[pos] = number of previous intervals ending strictly before
        # this interval's start.
        compat = [
            bisect_left(ends, item[1], 0, pos)
            for pos, item in enumerate(arr)
        ]

        # Encode a sorted tuple of up to 4 original indices into one integer.
        # Digit = original_index + 1, padded with sentinel 0.
        # Numeric order of these fixed-base codes equals lexicographic order.
        B = n + 1
        P1 = B
        P2 = B * B
        P3 = B * B * B

        # dp for exact counts 1..4:
        # sX[i] = max score using exactly X intervals among first i sorted intervals
        # codeX[i] = lexicographically smallest encoded index tuple for that score
        s1 = [-1] * (n + 1)
        s2 = [-1] * (n + 1)
        s3 = [-1] * (n + 1)
        s4 = [-1] * (n + 1)

        code1 = [0] * (n + 1)
        code2 = [0] * (n + 1)
        code3 = [0] * (n + 1)
        code4 = [0] * (n + 1)

        for i in range(1, n + 1):
            _, l, w, idx = arr[i - 1]
            p = compat[i - 1]
            d = idx + 1

            # Exactly 1 interval.
            best_s = s1[i - 1]
            best_code = code1[i - 1]

            take_s = w
            take_code = d * P3

            if take_s > best_s or (take_s == best_s and take_code < best_code):
                best_s = take_s
                best_code = take_code

            s1[i] = best_s
            code1[i] = best_code

            # Exactly 2 intervals.
            best_s = s2[i - 1]
            best_code = code2[i - 1]

            prev_s = s1[p]
            if prev_s != -1:
                take_s = prev_s + w
                pc = code1[p]
                a = pc // P3

                if d < a:
                    take_code = d * P3 + a * P2
                else:
                    take_code = a * P3 + d * P2

                if take_s > best_s or (take_s == best_s and take_code < best_code):
                    best_s = take_s
                    best_code = take_code

            s2[i] = best_s
            code2[i] = best_code

            # Exactly 3 intervals.
            best_s = s3[i - 1]
            best_code = code3[i - 1]

            prev_s = s2[p]
            if prev_s != -1:
                take_s = prev_s + w
                pc = code2[p]
                a = pc // P3
                b = (pc // P2) % B

                if d < a:
                    take_code = d * P3 + a * P2 + b * P1
                elif d < b:
                    take_code = a * P3 + d * P2 + b * P1
                else:
                    take_code = a * P3 + b * P2 + d * P1

                if take_s > best_s or (take_s == best_s and take_code < best_code):
                    best_s = take_s
                    best_code = take_code

            s3[i] = best_s
            code3[i] = best_code

            # Exactly 4 intervals.
            best_s = s4[i - 1]
            best_code = code4[i - 1]

            prev_s = s3[p]
            if prev_s != -1:
                take_s = prev_s + w
                pc = code3[p]
                a = pc // P3
                b = (pc // P2) % B
                cc = (pc // P1) % B

                if d < a:
                    take_code = d * P3 + a * P2 + b * P1 + cc
                elif d < b:
                    take_code = a * P3 + d * P2 + b * P1 + cc
                elif d < cc:
                    take_code = a * P3 + b * P2 + d * P1 + cc
                else:
                    take_code = a * P3 + b * P2 + cc * P1 + d

                if take_s > best_s or (take_s == best_s and take_code < best_code):
                    best_s = take_s
                    best_code = take_code

            s4[i] = best_s
            code4[i] = best_code

        # Choose best among counts 0..4:
        # higher score first, then lexicographically smaller encoded tuple.
        best_s = -1
        best_code = 0

        for s, cd in (
            (0, 0),
            (s1[n], code1[n]),
            (s2[n], code2[n]),
            (s3[n], code3[n]),
            (s4[n], code4[n]),
        ):
            if s > best_s or (s == best_s and cd < best_code):
                best_s = s
                best_code = cd

        # Decode encoded tuple back to original 0-based indices.
        res = []
        code = best_code

        for P in (P3, P2, P1, 1):
            d = code // P
            code -= d * P
            if d:
                res.append(d - 1)

        return res