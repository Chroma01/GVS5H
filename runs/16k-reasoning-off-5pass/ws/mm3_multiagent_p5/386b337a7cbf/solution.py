class Solution:
    def maxProduct(self, nums: List[int], k: int, limit: int) -> int:
        n = len(nums)
        MAX_SUM = n * 12
        SHIFT = MAX_SUM
        BITS = 2 * SHIFT + 1
        MASK = (1 << BITS) - 1
        size = limit + 1

        # reachable states (including empty subsequence)
        dp0 = [0] * size  # even length
        dp1 = [0] * size  # odd length
        # non‑empty reachable states
        ndp0 = [0] * size
        ndp1 = [0] * size

        # empty subsequence: product 1, sum 0, even length
        dp0[1] = 1 << SHIFT

        for x in nums:
            # copy current arrays to serve as the "skip" transition
            new0 = dp0[:]
            new1 = dp1[:]
            new_ndp0 = ndp0[:]
            new_ndp1 = ndp1[:]

            for p in range(size):
                if dp0[p] == 0 and dp1[p] == 0:
                    continue
                newp = p * x
                if newp > limit:
                    continue
                if x == 0:
                    # even -> odd, sum unchanged
                    new1[newp] |= dp0[p]
                    new_ndp1[newp] |= dp0[p]
                    # odd -> even, sum unchanged
                    new0[newp] |= dp1[p]
                    new_ndp0[newp] |= dp1[p]
                else:
                    # even -> odd (contribute +x)
                    shifted = (dp0[p] << x) & MASK
                    if shifted:
                        new1[newp] |= shifted
                        new_ndp1[newp] |= shifted
                    # odd -> even (contribute -x)
                    shifted = dp1[p] >> x
                    if shifted:
                        new0[newp] |= shifted
                        new_ndp0[newp] |= shifted

            dp0, dp1 = new0, new1
            ndp0, ndp1 = new_ndp0, new_ndp1

        # target sum k
        target_index = k + SHIFT
        if not (0 <= target_index < BITS):
            return -1
        target_bit = 1 << target_index

        # scan from largest product downwards
        for p in range(limit, -1, -1):
            if (ndp0[p] | ndp1[p]) & target_bit:
                return p
        return -1