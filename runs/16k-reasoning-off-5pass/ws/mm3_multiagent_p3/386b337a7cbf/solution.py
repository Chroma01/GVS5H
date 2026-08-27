class Solution:
    def maxProduct(self, nums: List[int], k: int, limit: int) -> int:
        n = len(nums)
        total = sum(nums)
        if abs(k) > total:
            return -1
        
        OFFSET = total
        size = 2 * OFFSET + 1
        mask = (1 << size) - 1
        
        # dp_reach[par][prod] = bitset of reachable sums (offset)
        # dp_nonempty[par][prod] = bitset of sums reachable via non-empty subsequences
        dp_reach = [[0] * (limit + 1) for _ in range(2)]
        dp_nonempty = [[0] * (limit + 1) for _ in range(2)]
        
        # empty subsequence: parity 0, product 1, sum 0
        dp_reach[0][1] = 1 << OFFSET
        
        for x in nums:
            # copy current states for "skip" case
            next_reach = [row[:] for row in dp_reach]
            next_nonempty = [row[:] for row in dp_nonempty]
            
            # start a new subsequence with this element as the only element
            if x <= limit:
                bit = 1 << (x + OFFSET)
                next_reach[1][x] |= bit
                next_nonempty[1][x] |= bit
            
            # transition from existing states
            for par in (0, 1):
                for prod in range(limit + 1):
                    bs = dp_reach[par][prod]
                    if bs == 0:
                        continue
                    new_par = 1 - par
                    new_prod = prod * x
                    if new_prod > limit:
                        continue
                    # shift bitset according to parity
                    if par == 0:
                        new_bs = (bs << x) & mask
                    else:
                        new_bs = (bs >> x) & mask
                    next_reach[new_par][new_prod] |= new_bs
                    
                    # also propagate non-emptiness
                    nbs = dp_nonempty[par][prod]
                    if nbs:
                        if par == 0:
                            new_nbs = (nbs << x) & mask
                        else:
                            new_nbs = (nbs >> x) & mask
                        next_nonempty[new_par][new_prod] |= new_nbs
            
            dp_reach = next_reach
            dp_nonempty = next_nonempty
        
        target_bit = 1 << (k + OFFSET)
        ans = -1
        for par in (0, 1):
            for prod in range(limit + 1):
                if dp_nonempty[par][prod] & target_bit:
                    if prod > ans:
                        ans = prod
        return ans