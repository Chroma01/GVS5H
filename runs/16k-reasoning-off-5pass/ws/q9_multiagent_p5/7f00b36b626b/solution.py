class Solution:
    def countComponents(self, nums: List[int], threshold: int) -> int:
        # Numbers greater than threshold cannot form any edges because lcm(u, v) >= max(u, v) > threshold.
        # They are isolated components.
        invalid_count = sum(1 for x in nums if x > threshold)
        
        # Filter numbers <= threshold. These are the only ones that can be connected.
        valid_nums = [x for x in nums if x <= threshold]
        
        if not valid_nums:
            return invalid_count
        
        # DSU Initialization
        # Since all valid numbers are <= threshold, we can use a list of size threshold + 1.
        # parent[i] represents the parent of the node with value i.
        limit = threshold
        parent = list(range(limit + 1))
        
        def find(x: int) -> int:
            # Path compression
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]
        
        def union(x: int, y: int) -> bool:
            rootX = find(x)
            rootY = find(y)
            if rootX != rootY:
                parent[rootX] = rootY
                return True
            return False
        
        # Create a boolean array `exists` to mark presence of valid numbers up to `threshold`
        # This allows O(1) checking if a number is in the input array.
        exists = [False] * (limit + 1)
        for x in valid_nums:
            exists[x] = True
        
        # Iterate through each potential common multiple M from 1 to threshold.
        # If two numbers u and v are multiples of M, then lcm(u, v) divides M.
        # Since M <= threshold, lcm(u, v) <= threshold, so u and v are connected.
        # We group all multiples of M present in the array into the same component.
        for m in range(1, limit + 1):
            # Collect all multiples of m present in valid_nums
            multiples = []
            k = 1
            while True:
                val = k * m
                if val > limit:
                    break
                if exists[val]:
                    multiples.append(val)
                k += 1
            
            # If there are 2 or more multiples, union them all together
            if len(multiples) > 1:
                root = multiples[0]
                for i in range(1, len(multiples)):
                    union(root, multiples[i])
        
        # Count the number of disjoint sets among valid numbers
        components = 0
        for x in valid_nums:
            if parent[x] == x:
                components += 1
        
        return components + invalid_count