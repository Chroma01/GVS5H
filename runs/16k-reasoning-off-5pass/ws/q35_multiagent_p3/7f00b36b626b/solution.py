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
        num_to_idx = {num: i for i, num in enumerate(nums)}
        
        # For each number in nums, iterate through its multiples up to threshold
        # If the multiple is also in nums, union the two indices
        for num in nums:
            # Only need to check multiples if num <= threshold
            # Because if num > threshold, then any multiple will be > threshold
            if num > threshold:
                continue
            # Start from 2*num, step by num
            multiple = 2 * num
            while multiple <= threshold:
                if multiple in num_to_idx:
                    idx1 = num_to_idx[num]
                    idx2 = num_to_idx[multiple]
                    union(idx1, idx2)
                multiple += num
        
        # Count the number of unique roots
        roots = set()
        for i in range(n):
            roots.add(find(i))
        
        return len(roots)