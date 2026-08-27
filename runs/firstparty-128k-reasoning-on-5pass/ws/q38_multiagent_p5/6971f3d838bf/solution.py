from typing import List

class Solution:
    def maxSubarraySum(self, nums: List[int]) -> int:
        if not nums:
            return 0

        # Non-empty maximum subarray sum of the original array.
        cur = best_orig = nums[0]
        for v in nums[1:]:
            cur = max(v, cur + v)
            if cur > best_orig:
                best_orig = cur

        # If there is no positive element, deletion cannot improve the answer.
        if best_orig <= 0:
            return best_orig

        # Lazy simultaneous Kadane over all negative deleted values.
        g = 0          # current original prefix sum
        h = 0          # -min original prefix sum seen so far
        max_raw = 0    # max stored raw value over seen negative values
        best = 0       # best candidate from deleting a negative value
        raw = {}       # negative value -> stored lazy R value

        for y in nums:
            if y > 0:
                g += y
                m = max_raw if max_raw > h else h
                val = g + m
                if val > best:
                    best = val

            elif y < 0:
                # Actual R for y before this occurrence is max(raw[y], h).
                old = raw.get(y, 0)
                if h > old:
                    old = h

                # At an occurrence of y, R_y increases by -y.
                r = old - y
                raw[y] = r
                if r > max_raw:
                    max_raw = r

                g += y
                neg_g = -g
                if neg_g > h:
                    h = neg_g

                m = max_raw if max_raw > h else h
                val = g + m
                if val > best:
                    best = val

            # y == 0 changes neither prefix sum, h, nor any raw value.

        return best_orig if best_orig > best else best