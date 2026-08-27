class Solution:
    def maxSubarraySum(self, nums: List[int]) -> int:
        n = len(nums)
        if n == 0:
            return 0
        
        # Build a segment tree for range max subarray sum queries
        # Each node stores: (max_sub, prefix_max, suffix_max, total_sum)
        size = 1
        while size < n:
            size *= 2
        
        # Initialize tree with identity values
        # For empty ranges, we use very small numbers for max_sub, prefix_max, suffix_max
        # and 0 for total_sum? Actually, for empty ranges, we should return a very small number.
        # But our queries will be on non-empty ranges only (since we skip empty segments).
        # We'll use a sentinel for "no valid subarray" which is -inf.
        INF = float('inf')
        
        tree = [None] * (2 * size)
        
        def merge(left, right):
            """Merge two nodes."""
            if left is None:
                return right
            if right is None:
                return left
            l_max_sub, l_prefix, l_suffix, l_total = left
            r_max_sub, r_prefix, r_suffix, r_total = right
            
            new_total = l_total + r_total
            new_prefix = max(l_prefix, l_total + r_prefix)
            new_suffix = max(r_suffix, r_total + l_suffix)
            new_max_sub = max(l_max_sub, r_max_sub, l_suffix + r_prefix)
            
            return (new_max_sub, new_prefix, new_suffix, new_total)
        
        # Build the tree
        # Leaves: for index i, the node is (nums[i], nums[i], nums[i], nums[i])
        for i in range(n):
            tree[size + i] = (nums[i], nums[i], nums[i], nums[i])
        for i in range(n, size):
            tree[size + i] = None  # empty
        
        for i in range(size - 1, 0, -1):
            tree[i] = merge(tree[2 * i], tree[2 * i + 1])
        
        def query(l, r):
            """Query max subarray sum in [l, r] (0-indexed, inclusive)."""
            if l > r:
                return None
            l += size
            r += size
            res_left = None
            res_right = None
            while l <= r:
                if l % 2 == 1:
                    res_left = merge(res_left, tree[l])
                    l += 1
                if r % 2 == 0:
                    res_right = merge(tree[r], res_right)
                    r -= 1
                l //= 2
                r //= 2
            return merge(res_left, res_right)
        
        # Original max subarray sum
        orig_result = query(0, n - 1)
        if orig_result is None:
            orig_result = -INF
        else:
            orig_result = orig_result[0]
        
        ans = orig_result
        
        # Group indices by value
        from collections import defaultdict
        pos = defaultdict(list)
        for i, x in enumerate(nums):
            pos[x].append(i)
        
        # For each unique x, compute max subarray sum after removing all x
        for x, indices in pos.items():
            # The segments are: [0, indices[0]-1], [indices[0]+1, indices[1]-1], ..., [indices[-1]+1, n-1]
            segments = []
            prev = -1
            for idx in indices:
                if prev + 1 <= idx - 1:
                    segments.append((prev + 1, idx - 1))
                prev = idx
            if prev + 1 <= n - 1:
                segments.append((prev + 1, n - 1))
            
            for l, r in segments:
                res = query(l, r)
                if res is not None:
                    ans = max(ans, res[0])
        
        return ans