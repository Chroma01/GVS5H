from typing import List

class Solution:
    def subsequencesWithMiddleMode(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        n = len(nums)
        if n < 5:
            return 0

        # left contains indices < current pivot, right contains indices > current pivot.
        # Start with pivot index 2.
        left = {}
        left_dup = 0  # sum over values of C(count, 2) in left
        for v in nums[:2]:
            c = left.get(v, 0)
            left[v] = c + 1
            left_dup += c

        right = {}
        right_dup = 0  # sum over values of C(count, 2) in right
        for v in nums[3:]:
            c = right.get(v, 0)
            right[v] = c + 1
            right_dup += c

        left_total = 2
        right_total = n - 3
        ans = 0

        for k in range(2, n - 2):
            x = nums[k]

            lx = left.get(x, 0)
            rx = right.get(x, 0)
            lnon = left_total - lx
            rnon = right_total - rx

            # Pair types on each side:
            # 2 copies of x, exactly 1 copy of x, 0 copies of x.
            l2 = lx * (lx - 1) // 2
            l1 = lx * lnon
            l0 = lnon * (lnon - 1) // 2

            r2 = rx * (rx - 1) // 2
            r1 = rx * rnon
            r0 = rnon * (rnon - 1) // 2

            # If at least two extra copies of x are chosen, x appears at least 3 times.
            # The other three selected values can contribute at most 2 occurrences,
            # so x is automatically the unique mode.
            ans = (
                ans
                + l2 * (r2 + r1 + r0)
                + l1 * (r2 + r1)
                + l0 * r2
            ) % MOD

            # If exactly one extra copy of x is chosen, x appears exactly twice.
            # Then the three non-x chosen values must be pairwise distinct.
            if lx or rx:
                # Number of unordered pairs of non-x indices with distinct values.
                dl = lnon * (lnon - 1) // 2 - (left_dup - l2)
                dr = rnon * (rnon - 1) // 2 - (right_dup - r2)

                # Extra x is on the left:
                # choose one left x, one left non-x value y,
                # and a right pair of distinct non-x values not equal to y.
                if lx and dr and lnon:
                    s = 0
                    rget = right.get
                    for y, c in left.items():
                        if y == x:
                            continue
                        ry = rget(y, 0)
                        s += c * (dr - ry * (rnon - ry))
                    ans = (ans + lx * s) % MOD

                # Extra x is on the right, symmetric.
                if rx and dl and rnon:
                    s = 0
                    lget = left.get
                    for y, c in right.items():
                        if y == x:
                            continue
                        ly = lget(y, 0)
                        s += c * (dl - ly * (lnon - ly))
                    ans = (ans + rx * s) % MOD

            # Move pivot from k to k + 1.
            v = nums[k]
            c = left.get(v, 0)
            left[v] = c + 1
            left_dup += c
            left_total += 1

            v = nums[k + 1]
            c = right.get(v, 0)
            if c == 1:
                del right[v]
            elif c > 1:
                right[v] = c - 1
            right_dup -= c - 1
            right_total -= 1

        return ans