class Solution:
    def countComponents(self, nums: List[int], threshold: int) -> int:
        n = len(nums)
        parent = list(range(n))
        
        def find(i):
            while parent[i] != i:
                parent[i] = parent[parent[i]]
                i = parent[i]
            return i
            
        def union(i, j):
            root_i, root_j = find(i), find(j)
            if root_i != root_j:
                parent[root_i] = root_j
                return True
            return False
            
        # Map each number <= threshold to its index in nums
        val_to_idx = {v: i for i, v in enumerate(nums) if v <= threshold}
        
        # first_divisor[m] stores the index of the first number in nums that divides m
        first_divisor = [-1] * (threshold + 1)
        
        # Sieve-like approach: for each number, union it with other numbers that share a common multiple <= threshold
        for v in val_to_idx:
            idx = val_to_idx[v]
            # Iterate through all multiples of v up to threshold
            for m in range(v, threshold + 1, v):
                if first_divisor[m] == -1:
                    first_divisor[m] = idx
                else:
                    union(first_divisor[m], idx)
                    
        # Count unique connected components
        roots = set()
        for i in range(n):
            roots.add(find(i))
            
        return len(roots)