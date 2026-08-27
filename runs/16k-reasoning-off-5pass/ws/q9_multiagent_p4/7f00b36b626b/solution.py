class Solution:
    def countComponents(self, nums: List[int], threshold: int) -> int:
        # Step 1: Identify numbers greater than threshold.
        # These numbers cannot form any edges because lcm(a, b) >= max(a, b).
        # Each such number is its own connected component.
        greater_count = 0
        for x in nums:
            if x > threshold:
                greater_count += 1
        
        # Step 2: Filter numbers <= threshold and store their indices for DSU.
        small_nums = [x for x in nums if x <= threshold]
        val_to_idx = {val: i for i, val in enumerate(small_nums)}
        n_small = len(small_nums)
        
        # Step 3: Initialize DSU for the small numbers.
        parent = list(range(n_small))
        def find(i):
            if parent[i] != i:
                parent[i] = find(parent[i])
            return parent[i]
        
        def union(i, j):
            root_i = find(i)
            root_j = find(j)
            if root_i != root_j:
                parent[root_i] = root_j
                return True
            return False
        
        # Step 4: Precompute divisors for all numbers from 1 to threshold using a sieve-like method.
        # We create a list where divisors[j] contains all divisors of j.
        divisors = [[] for _ in range(threshold + 1)]
        for i in range(1, threshold + 1):
            for j in range(i, threshold + 1, i):
                divisors[j].append(i)
        
        # Step 5: Iterate through each number L from 1 to threshold.
        # If L exists in nums, retrieve its precomputed divisors.
        # For each divisor d of L, if d also exists in nums, union the sets containing L and d.
        # This connects L with all its divisors present in the array.
        # Since lcm(d, L) = L (because d divides L) and L <= threshold, the edge condition is satisfied.
        for L in range(1, threshold + 1):
            if L in val_to_idx:
                for d in divisors[L]:
                    if d in val_to_idx:
                        union(val_to_idx[d], val_to_idx[L])
        
        # Step 6: Count connected components among small numbers.
        roots = set()
        for i in range(n_small):
            roots.add(find(i))
        small_components = len(roots)
        
        # Total components = components from small numbers + isolated large numbers
        return small_components + greater_count