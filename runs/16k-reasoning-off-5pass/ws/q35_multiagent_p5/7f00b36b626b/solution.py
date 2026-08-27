class Solution:
    def countComponents(self, nums: List[int], threshold: int) -> int:
        # Filter out numbers greater than threshold since they can't form any edges
        # because lcm(a, b) >= max(a, b)
        valid_nums = [x for x in nums if x <= threshold]
        
        # If no valid numbers, each number in original nums is its own component
        if not valid_nums:
            return len(nums)
        
        # Create a set for O(1) lookup
        num_set = set(valid_nums)
        
        # Map each valid number to an index for DSU
        # We'll use a dictionary for DSU parent pointers
        parent = {}
        rank = {}
        
        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]
        
        def union(x, y):
            rx, ry = find(x), find(y)
            if rx == ry:
                return
            if rank[rx] < rank[ry]:
                parent[rx] = ry
            elif rank[rx] > rank[ry]:
                parent[ry] = rx
            else:
                parent[ry] = rx
                rank[rx] += 1
        
        # Initialize DSU for each valid number
        for x in valid_nums:
            parent[x] = x
            rank[x] = 0
        
        # For each divisor d from 1 to threshold, union all multiples of d present in num_set
        # This is efficient because the total number of iterations is O(threshold * log(threshold))
        for d in range(1, threshold + 1):
            # Find all multiples of d that are in num_set
            # Start from d, then 2*d, 3*d, ... up to threshold
            first = None
            multiple = d
            while multiple <= threshold:
                if multiple in num_set:
                    if first is None:
                        first = multiple
                    else:
                        union(first, multiple)
                multiple += d
        
        # Count the number of unique roots for valid numbers
        roots = set()
        for x in valid_nums:
            roots.add(find(x))
        
        # The number of connected components among valid numbers is len(roots)
        # Each invalid number ( > threshold) is its own component
        invalid_count = len(nums) - len(valid_nums)
        
        return len(roots) + invalid_count