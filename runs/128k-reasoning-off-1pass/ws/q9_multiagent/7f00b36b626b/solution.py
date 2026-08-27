class Solution:
    def countComponents(self, nums: List[int], threshold: int) -> int:
        # Separate numbers into those > threshold (isolated) and those <= threshold (potential connections)
        large_count = 0
        small_nums = []
        for num in nums:
            if num > threshold:
                large_count += 1
            else:
                small_nums.append(num)
        
        # If no numbers <= threshold, all are isolated
        if not small_nums:
            return large_count
        
        # Initialize DSU for small numbers
        parent = {num: num for num in small_nums}
        
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

        # Array to store the first number found that divides a multiple j
        # Index j corresponds to the multiple value.
        first_occurrence = [-1] * (threshold + 1)
        
        # Iterate through each small number and its multiples
        # Complexity: O(T log T + N) where T is threshold and N is number of small elements
        for x in small_nums:
            # Iterate multiples: x, 2x, 3x, ... <= threshold
            j = x
            while j <= threshold:
                if first_occurrence[j] != -1:
                    # We found another number that divides j, so union them
                    # Both x and first_occurrence[j] divide j, so lcm(x, first_occurrence[j]) divides j <= threshold
                    union(x, first_occurrence[j])
                else:
                    first_occurrence[j] = x
                j += x
        
        # Count disjoint sets in small_nums
        components_small = 0
        for num in small_nums:
            if parent[num] == num:
                components_small += 1
                
        return large_count + components_small