from typing import List

class Solution:
    def maxSubarraySum(self, nums: List[int]) -> int:
        # Coordinate compression
        vals = sorted(set(nums))
        idx = {v: i for i, v in enumerate(vals)}
        m = len(vals)
        
        # Segment tree for range chmax and range max query
        size = 1
        while size < m:
            size *= 2
        tree = [0] * (2 * size)
        lazy = [0] * (2 * size)  # lazy value for chmax
        
        def apply_chmax(node, val):
            if tree[node] < val:
                tree[node] = val
            if lazy[node] < val:
                lazy[node] = val
        
        def push(node):
            if lazy[node]:
                apply_chmax(node*2, lazy[node])
                apply_chmax(node*2+1, lazy[node])
                lazy[node] = 0
        
        def range_chmax(l, r, val, node, node_l, node_r):
            if r < node_l or node_r < l:
                return
            if l <= node_l and node_r <= r:
                apply_chmax(node, val)
                return
            push(node)
            mid = (node_l + node_r) // 2
            range_chmax(l, r, val, node*2, node_l, mid)
            range_chmax(l, r, val, node*2+1, mid+1, node_r)
            tree[node] = max(tree[node*2], tree[node*2+1])
        
        def range_max(l, r, node, node_l, node_r):
            if r < node_l or node_r < l:
                return -10**18
            if l <= node_l and node_r <= r:
                return tree[node]
            push(node)
            mid = (node_l + node_r) // 2
            return max(range_max(l, r, node*2, node_l, mid),
                       range_max(l, r, node*2+1, mid+1, node_r))
        
        def point_set(pos, val, node, node_l, node_r):
            if node_l == node_r:
                if tree[node] < val:
                    tree[node] = val
                return
            push(node)
            mid = (node_l + node_r) // 2
            if pos <= mid:
                point_set(pos, val, node*2, node_l, mid)
            else:
                point_set(pos, val, node*2+1, mid+1, node_r)
            tree[node] = max(tree[node*2], tree[node*2+1])
        
        # Compute original max subarray sum via Kadane
        orig_max = nums[0]
        cur = nums[0]
        for x in nums[1:]:
            cur = max(x, cur + x)
            orig_max = max(orig_max, cur)
        
        ans = orig_max
        add = 0
        
        for a in nums:
            ai = idx[a]
            # Update all v != a: cur[v] = max(cur[v], a - add)
            target = a - add
            if target > 0:
                if ai > 0:
                    range_chmax(0, ai-1, target, 1, 0, size-1)
                if ai < m-1:
                    range_chmax(ai+1, m-1, target, 1, 0, size-1)
            # Update v == a: cur[a] = max(cur[a], 0)
            point_set(ai, 0, 1, 0, size-1)
            add += a
            # Query max over v != a
            best = -10**18
            if ai > 0:
                best = max(best, range_max(0, ai-1, 1, 0, size-1) + add)
            if ai < m-1:
                best = max(best, range_max(ai+1, m-1, 1, 0, size-1) + add)
            # Also consider v == a (actual value is cur[a], no add)
            cur_a = range_max(ai, ai, 1, 0, size-1)
            best = max(best, cur_a)
            ans = max(ans, best)
        
        return ans