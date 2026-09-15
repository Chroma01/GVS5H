from typing import List

class Solution:
    def maxProduct(self, nums: List[int], k: int, limit: int) -> int:
        S = sum(nums)
        off = S
        target = k + off
        if target < 0 or target > 2 * S:
            return -1
        
        # Zero-product DP: states (hasZero, parity) -> bitset of alternating sums
        zero = {(False, 0): 1 << off}
        for v in nums:
            items = list(zero.items())
            for (hz, par), bits in items:
                if bits == 0:
                    continue
                nhz = hz or (v == 0)
                if par == 0:
                    npar = 1
                    shifted = bits << v
                else:
                    npar = 0
                    shifted = bits >> v
                key = (nhz, npar)
                zero[key] = zero.get(key, 0) | shifted
        
        zero_reach = False
        if (True, 0) in zero and ((zero[(True, 0)] >> target) & 1):
            zero_reach = True
        elif (True, 1) in zero and ((zero[(True, 1)] >> target) & 1):
            zero_reach = True
        
        # Positive-product DP: even[p], odd[p] are bitsets of alternating sums
        even = [0] * (limit + 1)
        odd = [0] * (limit + 1)
        for v in nums:
            if v == 0:
                continue
            # snapshot before using v, so v is used at most once
            items = [(p, even[p], odd[p]) for p in range(1, limit + 1) if even[p] or odd[p]]
            # start a new subsequence with v
            if v <= limit:
                odd[v] |= 1 << (v + off)
            # append v to existing subsequences
            for p, be, bo in items:
                np = p * v
                if np > limit:
                    continue
                if be:
                    odd[np] |= be << v
                if bo:
                    even[np] |= bo >> v
        
        for p in range(limit, 0, -1):
            if ((even[p] | odd[p]) >> target) & 1:
                return p
        
        if zero_reach:
            return 0
        return -1