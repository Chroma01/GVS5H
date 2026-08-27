class Solution:
    def maxSubarraySum(self, nums: List[int]) -> int:
        n = len(nums)
        if n == 0:
            return 0
        
        # Precompute end_max and start_index
        # end_max[i] = max subarray sum ending at i
        # start_index[i] = start index of that subarray
        end_max = [0] * n
        start_index = [0] * n
        
        end_max[0] = nums[0]
        start_index[0] = 0
        
        for i in range(1, n):
            if end_max[i-1] > 0:
                end_max[i] = end_max[i-1] + nums[i]
                start_index[i] = start_index[i-1]
            else:
                end_max[i] = nums[i]
                start_index[i] = i
        
        # Global max subarray sum (case of no removal)
        global_max = max(end_max)
        
        # Collect all segments for each unique element
        # For each unique x, we get a list of segments [l, r]
        # We will process these segments offline.
        
        # Map from value to list of indices
        from collections import defaultdict
        indices_map = defaultdict(list)
        for i, x in enumerate(nums):
            indices_map[x].append(i)
        
        # List of queries: (l, r, query_index)
        # We'll store the result for each query in a list
        queries = []
        query_results = []
        
        for x, indices in indices_map.items():
            # Add boundary indices for easier segment extraction
            # segments: [0, indices[0]-1], [indices[0]+1, indices[1]-1], ..., [indices[-1]+1, n-1]
            prev = -1
            for idx in indices:
                l = prev + 1
                r = idx - 1
                if l <= r:
                    queries.append((l, r))
                prev = idx
            # Last segment
            l = prev + 1
            r = n - 1
            if l <= r:
                queries.append((l, r))
        
        num_queries = len(queries)
        if num_queries == 0:
            return global_max
            
        # We will process queries offline.
        # Sort queries by l descending.
        # Also, we want to add indices j to a segment tree when start_index[j] >= l.
        # Instead, we iterate l from n-1 down to 0.
        # For each l, we add all j such that start_index[j] == l into a segment tree at position j.
        # Then for all queries with left boundary l, we query the segment tree for max in [l, r].
        
        # Group queries by l
        queries_by_l = defaultdict(list)
        for idx, (l, r) in enumerate(queries):
            queries_by_l[l].append((l, r, idx))
            
        # Group indices j by start_index[j]
        indices_by_start = defaultdict(list)
        for j in range(n):
            indices_by_start[start_index[j]].append(j)
            
        # Segment tree for range maximum query
        # Size: n
        # We'll use an array based segment tree.
        size = 1
        while size < n:
            size *= 2
        tree = [-float('inf')] * (2 * size)
        
        def update(pos, value):
            # Update position pos with value
            idx = pos + size
            tree[idx] = value
            idx //= 2
            while idx > 0:
                tree[idx] = max(tree[2*idx], tree[2*idx+1])
                idx //= 2
                
        def query(l, r):
            # Query max in [l, r]
            l += size
            r += size
            res = -float('inf')
            while l <= r:
                if l % 2 == 1:
                    res = max(res, tree[l])
                    l += 1
                if r % 2 == 0:
                    res = max(res, tree[r])
                    r -= 1
                l //= 2
                r //= 2
            return res
        
        # Process from l = n-1 down to 0
        # Initialize query_results array
        query_results = [-float('inf')] * num_queries
        
        # We need to map query index to result
        # Instead, we can store results in a list and then assign
        # But we have queries_by_l, so we can process in order.
        
        # Let's create an array for results indexed by query index
        res_arr = [-float('inf')] * num_queries
        
        # Iterate l from n-1 down to 0
        for l in range(n-1, -1, -1):
            # Add all j with start_index[j] == l
            for j in indices_by_start[l]:
                update(j, end_max[j])
                
            # Process all queries starting at l
            if l in queries_by_l:
                for (ql, qr, qidx) in queries_by_l[l]:
                    # Query max in [ql, qr]
                    val = query(ql, qr)
                    res_arr[qidx] = val
                    
        # The answer is the maximum of:
        # 1. Global max subarray sum (no removal)
        # 2. Max over all query results (removal of some x)
        ans = global_max
        for val in res_arr:
            if val > ans:
                ans = val
                
        return ans