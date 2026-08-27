class Solution:
    def countComponents(self, nums: List[int], threshold: int) -> int:
        n = len(nums)
        if n == 0:
            return 0
        
        # Union-Find data structure
        parent = list(range(n))
        rank = [0] * n
        num_components = n
        
        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x
        
        def union(x, y):
            nonlocal num_components
            rx, ry = find(x), find(y)
            if rx == ry:
                return
            if rank[rx] < rank[ry]:
                rx, ry = ry, rx
            parent[ry] = rx
            if rank[rx] == rank[ry]:
                rank[rx] += 1
            num_components -= 1
        
        # Map each number to its index
        val_to_idx = {val: i for i, val in enumerate(nums)}
        
        # For each number x in nums, iterate over multiples m = k*x up to threshold
        # If m is also in nums, then lcm(x, m) = m <= threshold, so they are connected.
        # This covers all pairs (a, b) where one divides the other.
        # But what about pairs where neither divides the other?
        # As discussed, if lcm(a, b) = L <= threshold, then both a and b divide L.
        # We can use the sieve-like approach: for each L from 1 to threshold,
        # find all numbers in nums that divide L, and union them.
        
        # Efficient approach:
        # Create a list of indices for each L from 1 to threshold.
        # nodes_at_L[L] will contain indices of numbers in nums that divide L.
        # We can build this by iterating over each x in nums and adding its index to all multiples of x up to threshold.
        
        nodes_at_L = [[] for _ in range(threshold + 1)]
        
        for val, idx in val_to_idx.items():
            if val > threshold:
                continue
            # Add idx to all multiples of val up to threshold
            for m in range(val, threshold + 1, val):
                nodes_at_L[m].append(idx)
        
        # Now, for each L, union all nodes that divide L
        for L in range(1, threshold + 1):
            nodes = nodes_at_L[L]
            if len(nodes) > 1:
                first = nodes[0]
                for i in range(1, len(nodes)):
                    union(first, nodes[i])
        
        return num_components