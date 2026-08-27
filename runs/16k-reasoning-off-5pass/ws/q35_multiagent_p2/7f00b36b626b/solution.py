class Solution:
    def countComponents(self, nums: List[int], threshold: int) -> int:
        # Numbers greater than threshold cannot form any edge because lcm(a,b) >= max(a,b)
        # So they are isolated components.
        # We only need to process numbers <= threshold for connectivity.
        
        # Create a set of numbers present in nums that are <= threshold
        present = set()
        for x in nums:
            if x <= threshold:
                present.add(x)
        
        # Count isolated components: numbers > threshold are each their own component
        # Plus, numbers <= threshold that are not connected to anything else will be counted by DSU
        # We'll use DSU for numbers <= threshold.
        
        # Map each number <= threshold to an index 0..k-1 for DSU, or use a dict for DSU parent
        # Since numbers can be up to 10^9, but we only care about those <= threshold (max 2e5),
        # we can use a dictionary for DSU or an array of size threshold+1.
        # Using an array for DSU parent for indices 1..threshold is efficient.
        
        parent = list(range(threshold + 1))
        rank = [0] * (threshold + 1)
        
        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]  # path compression
                x = parent[x]
            return x
        
        def union(x, y):
            rx, ry = find(x), find(y)
            if rx == ry:
                return
            # union by rank
            if rank[rx] < rank[ry]:
                parent[rx] = ry
            elif rank[rx] > rank[ry]:
                parent[ry] = rx
            else:
                parent[ry] = rx
                rank[rx] += 1
        
        # For each number x in present, union with its multiples
        for x in present:
            # Start from 2*x, step by x
            m = 2 * x
            while m <= threshold:
                if m in present:
                    union(x, m)
                m += x
        
        # Count unique components for numbers in present
        # Each number in present will have a root. Count unique roots.
        roots = set()
        for x in present:
            roots.add(find(x))
        
        # The number of connected components from numbers <= threshold is len(roots)
        # Plus, each number > threshold is a separate component
        count_gt_threshold = 0
        for x in nums:
            if x > threshold:
                count_gt_threshold += 1
                
        return len(roots) + count_gt_threshold