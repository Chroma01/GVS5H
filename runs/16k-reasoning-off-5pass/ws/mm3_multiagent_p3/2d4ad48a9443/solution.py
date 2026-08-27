import bisect
from typing import List

class Solution:
    def countNonDecreasingSubarrays(self, nums: List[int], k: int) -> int:
        n = len(nums)
        if n == 0:
            return 0
        
        # Build segment tree where each node stores a "profile" of the subarray.
        # Profile: list of (running_max_value, length, sum_of_originals) with strictly increasing values.
        # Cost of subarray = sum(v * len) - sum_of_originals
        # Merging two profiles: left profile's final max M absorbs the prefix of right profile with value <= M.
        
        size = 1
        while size < n:
            size *= 2
        
        # node: [segs, pref_len, pref_vlen, pref_sum, cost, total_len, total_sum]
        EMPTY = ([], [], [], [], 0, 0, 0)
        tree = [EMPTY] * (2 * size)
        
        for i in range(n):
            v = nums[i]
            tree[size + i] = ([(v, 1, v)], [1], [v], [v], 0, 1, v)
        
        def build_prefixes(segs):
            pl, pv, ps = [], [], []
            cl, cv, cs = 0, 0, 0
            for v, l, s in segs:
                cl += l
                cv += v * l
                cs += s
                pl.append(cl)
                pv.append(cv)
                ps.append(cs)
            return pl, pv, ps
        
        def merge_nodes(left, right):
            if not left[0]:
                return right
            if not right[0]:
                return left
            
            l_segs = left[0]
            r_segs = right[0]
            r_plen = right[1]
            r_pvlen = right[2]
            r_psum = right[3]
            M = l_segs[-1][0]  # max value of left profile
            
            # Binary search for first segment in right with value > M
            idx = bisect.bisect_right([s[0] for s in r_segs], M)
            
            sum_len = r_plen[idx - 1] if idx > 0 else 0
            sum_vlen = r_pvlen[idx - 1] if idx > 0 else 0
            sum_sum = r_psum[idx - 1] if idx > 0 else 0
            
            extra = M * sum_len - sum_vlen
            new_cost = left[4] + right[4] + extra
            
            # Build new segment list
            new_segs = list(l_segs[:-1])  # all except last
            last_v, last_l, last_s = l_segs[-1]
            new_last_l = last_l + sum_len
            new_last_s = last_s + sum_sum
            new_segs.append((last_v, new_last_l, new_last_s))
            if idx < len(r_segs):
                new_segs.extend(r_segs[idx:])
            
            pl, pv, ps = build_prefixes(new_segs)
            return (new_segs, pl, pv, ps, new_cost, pl[-1] if pl else 0, ps[-1] if ps else 0)
        
        # Build tree bottom-up
        for i in range(size - 1, 0, -1):
            tree[i] = merge_nodes(tree[2 * i], tree[2 * i + 1])
        
        def query_cost(l, r):
            """Compute cost of subarray nums[l..r]"""
            l += size
            r += size
            stack = []
            while l <= r:
                if l & 1:
                    stack.append(tree[l])
                    l += 1
                if not (r & 1):
                    stack.append(tree[r])
                    r -= 1
                l >>= 1
                r >>= 1
            result = EMPTY
            for node in reversed(stack):
                result = merge_nodes(result, node)
            return result[4]
        
        ans = 0
        for r in range(n):
            # Find leftmost l such that cost(l, r) <= k
            # cost is non-increasing as l increases
            if query_cost(0, r) <= k:
                ans += r + 1
                continue
            
            lo, hi = 0, r
            leftmost = r + 1  # sentinel: no valid l found
            while lo <= hi:
                mid = (lo + hi) >> 1
                if query_cost(mid, r) <= k:
                    leftmost = mid
                    hi = mid - 1
                else:
                    lo = mid + 1
            
            if leftmost <= r:
                ans += r - leftmost + 1
        
        return ans