class Solution:
    def countComponents(self, nums: List[int], threshold: int) -> int:
        # Initialize Union-Find (DSU) structures
        # Using a dictionary for parent pointers to handle sparse data efficiently
        parent = {}
        
        # Iterative find with path compression to avoid recursion depth issues
        def find(x):
            path = []
            while parent[x] != x:
                path.append(x)
                x = parent[x]
            for node in path:
                parent[node] = x
            return x
        
        def union(x, y):
            rootX = find(x)
            rootY = find(y)
            if rootX != rootY:
                parent[rootX] = rootY
                return True
            return False

        # Helper to get root and initialize if needed
        def get_root(x):
            if x not in parent:
                parent[x] = x
            return find(x)

        # Count components
        # 1. Numbers > threshold are isolated components
        # 2. Numbers <= threshold need to be checked for connections
        
        # We will use a set for O(1) lookup of numbers present in nums
        num_set = set(nums)
        
        # Initialize DSU for all numbers <= threshold
        # Also count numbers > threshold as they are isolated
        large_count = 0
        
        # First pass: count numbers > threshold and initialize DSU for numbers <= threshold
        for x in nums:
            if x > threshold:
                large_count += 1
            else:
                get_root(x)
        
        # Total components starts with large_count + count of numbers <= threshold
        # But we will decrement when we merge components
        total_nodes_le_threshold = sum(1 for x in nums if x <= threshold)
        total_components = large_count + total_nodes_le_threshold
        
        # Iterate through numbers <= threshold to find edges
        # For each x, check multiples k*x <= threshold
        # If k*x exists in nums, then lcm(x, k*x) = k*x <= threshold, so they are connected
        for x in nums:
            if x > threshold:
                continue
            
            # Check multiples
            # We only need to check multiples up to threshold
            # Optimization: if x > threshold, loop won't run, but we already filtered
            # Also, if x > threshold, we skip. Here x <= threshold.
            # We iterate k starting from 2 (since k=1 is x itself)
            # The multiple is m = k * x. We need m <= threshold.
            # So k goes from 2 up to threshold // x
            
            limit = threshold // x
            for k in range(2, limit + 1):
                m = k * x
                if m in num_set:
                    # Check if they are already connected
                    rootX = find(x)
                    rootM = find(m)
                    if rootX != rootM:
                        union(x, m)
                        total_components -= 1
        
        return total_components