class Solution:
    def countComponents(self, nums: List[int], threshold: int) -> int:
        n = len(nums)
        if n == 0:
            return 0
        
        # Union-Find data structure
        parent = list(range(n))
        rank = [0] * n
        
        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]  # Path compression
                x = parent[x]
            return x
        
        def union(x, y):
            rx, ry = find(x), find(y)
            if rx == ry:
                return
            # Union by rank
            if rank[rx] < rank[ry]:
                parent[rx] = ry
            elif rank[rx] > rank[ry]:
                parent[ry] = rx
            else:
                parent[ry] = rx
                rank[rx] += 1
        
        # Create a set for O(1) lookup and a mapping from value to index
        num_set = set(nums)
        val_to_idx = {val: i for i, val in enumerate(nums)}
        
        # For each number in nums, iterate over its multiples up to threshold
        # If a multiple exists in nums, union the two indices
        for a in nums:
            # If a > threshold, it can't form any edge because lcm(a, b) >= a > threshold
            if a > threshold:
                continue
            # Iterate over multiples: a*2, a*3, ... up to threshold
            # Start from k=2 because k=1 is the same element
            k = 2
            while k * a <= threshold:
                m = k * a
                if m in num_set:
                    # Union the indices of a and m
                    idx_a = val_to_idx[a]
                    idx_m = val_to_idx[m]
                    union(idx_a, idx_m)
                k += 1
        
        # Count the number of unique roots
        roots = set()
        for i in range(n):
            roots.add(find(i))
        
        return len(roots)