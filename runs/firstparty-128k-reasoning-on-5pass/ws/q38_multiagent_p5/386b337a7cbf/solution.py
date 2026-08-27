from typing import List

class Solution:
    def maxProduct(self, nums: List[int], k: int, limit: int) -> int:
        total = sum(nums)
        if abs(k) > total:
            return -1

        offset = total
        target_bit = 1 << (k + offset)

        zero_ok = False
        if 0 in nums:
            # st[0]: even length, no zero selected
            # st[1]: odd length, no zero selected
            # st[2]: even length, zero selected
            # st[3]: odd length, zero selected
            st = [1 << offset, 0, 0, 0]
            for x in nums:
                old = st[:]
                if x > 0:
                    st[1] |= old[0] << x
                    st[0] |= old[1] >> x
                    st[3] |= old[2] << x
                    st[2] |= old[3] >> x
                else:
                    st[3] |= old[0] | old[2]
                    st[2] |= old[1] | old[3]
            zero_ok = bool((st[2] | st[3]) & target_bit)

        dp0 = [0] * (limit + 1)
        dp1 = [0] * (limit + 1)

        for x in nums:
            if x == 0 or x > limit:
                continue

            old0 = dp0[:]
            old1 = dp1[:]

            dp1[x] |= 1 << (x + offset)

            for p in range(1, limit // x + 1):
                q = p * x
                if old0[p]:
                    dp1[q] |= old0[p] << x
                if old1[p]:
                    dp0[q] |= old1[p] >> x

        for p in range(limit, 0, -1):
            if (dp0[p] | dp1[p]) & target_bit:
                return p

        return 0 if zero_ok else -1