class Solution:
    def maxSubarraySum(self, nums: List[int]) -> int:
        n = len(nums)
        if n == 0:
            return 0
        if n == 1:
            return nums[0]
        
        # Segment tree for range max subarray sum
        # Each node stores: (max_prefix, max_suffix, max_subarray, total_sum)
        size = 1
        while size < n:
            size *= 2
        tree = [None] * (2 * size)
        
        # Build the tree
        # Initialize leaves
        for i in range(n):
            val = nums[i]
            tree[size + i] = (val, val, val, val)
        for i in range(n, size):
            # For positions beyond n, we use a neutral element that doesn't affect results
            # But since we only query valid ranges, we can set to very small numbers
            # However, to be safe, we'll use a value that represents an empty segment
            # But max subarray sum requires non-empty, so we handle queries carefully.
            # Actually, for positions >= n, we can set to (-inf, -inf, -inf, 0) but that's tricky.
            # Instead, we'll just not query those. We'll set them to a safe default.
            tree[size + i] = (-10**18, -10**18, -10**18, 0)
        
        # Build internal nodes
        for i in range(size - 1, 0, -1):
            left = tree[2 * i]
            right = tree[2 * i + 1]
            total = left[3] + right[3]
            max_pref = max(left[0], left[3] + right[0])
            max_suff = max(right[1], right[3] + left[1])
            max_sub = max(left[2], right[2], left[1] + right[0])
            tree[i] = (max_pref, max_suff, max_sub, total)
        
        # Query function for range [l, r] (0-indexed, inclusive)
        def query(l, r):
            # Convert to leaf indices
            l += size
            r += size
            # We need to collect nodes that cover [l, r]
            # Standard segment tree query
            res_left = None
            res_right = None
            
            # We'll collect left and right parts separately
            # Actually, we can do iterative query and merge results
            # But merging is associative, so we can do it in order.
            # We'll use a list to store nodes from left and right sides.
            left_nodes = []
            right_nodes = []
            
            L, R = l, r
            while L <= R:
                if L % 2 == 1:
                    left_nodes.append(tree[L])
                    L += 1
                if R % 2 == 0:
                    right_nodes.append(tree[R])
                    R -= 1
                L //= 2
                R //= 2
            
            # Merge left_nodes in order
            def merge(a, b):
                if a is None:
                    return b
                if b is None:
                    return a
                total = a[3] + b[3]
                max_pref = max(a[0], a[3] + b[0])
                max_suff = max(b[1], b[3] + a[1])
                max_sub = max(a[2], b[2], a[1] + b[0])
                return (max_pref, max_suff, max_sub, total)
            
            res = None
            for node in left_nodes:
                res = merge(res, node)
            for node in reversed(right_nodes):
                res = merge(res, node)
            
            return res[2]  # max_subarray
        
        # Initial answer: max subarray sum of entire array
        ans = query(0, n - 1)
        
        # Group indices by value
        from collections import defaultdict
        pos_map = defaultdict(list)
        for i, x in enumerate(nums):
            pos_map[x].append(i)
        
        # For each unique element, remove all its occurrences and compute max subarray sum in segments
        for x, positions in pos_map.items():
            # The segments are defined by consecutive positions of x
            # Start from -1, then each position, then n
            prev = -1
            for pos in positions:
                # Segment from prev+1 to pos-1
                l, r = prev + 1, pos - 1
                if l <= r:
                    seg_max = query(l, r)
                    if seg_max > ans:
                        ans = seg_max
                prev = pos
            # Last segment
            l, r = prev + 1, n - 1
            if l <= r:
                seg_max = query(l, r)
                if seg_max > ans:
                    ans = seg_max
        
        return ans