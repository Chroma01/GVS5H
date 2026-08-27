class Solution:
    def countComponents(self, nums: List[int], threshold: int) -> int:
        # Filter numbers that are greater than threshold
        # Since lcm(a, b) >= max(a, b), any number > threshold cannot be part of any edge
        filtered_nums = [x for x in nums if x <= threshold]
        
        if not filtered_nums:
            return 0
            
        # Create a set for O(1) lookup and a boolean array for presence
        present_set = set(filtered_nums)
        present = [False] * (threshold + 1)
        for x in filtered_nums:
            present[x] = True
            
        # Initialize Union-Find
        parent = {x: x for x in filtered_nums}
        rank = {x: 0 for x in filtered_nums}
        
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
                
        # For each number L in the filtered list, find all its divisors d
        # If d is also in the set, then lcm(d, L) = L <= threshold, so they are connected.
        # This ensures that if two numbers a and b have lcm(a,b) = L <= threshold,
        # and L is in the set, then a and b are connected via L.
        # But what if L is NOT in the set? 
        # Actually, if lcm(a,b) = L <= threshold, then a and b are divisors of L.
        # We need to connect a and b. The above method only connects divisors to L if L is present.
        # If L is not present, we miss the connection.
        
        # Correction: The standard efficient approach for small threshold is:
        # Iterate over each possible GCD g from 1 to threshold.
        # For each g, collect all multiples of g that are present in the set.
        # All such multiples are connected to each other? No, only if their LCM <= threshold.
        # But note: if we have multiples a = i*g and b = j*g, then lcm(a,b) = g * lcm(i,j).
        # This is <= threshold only if g * lcm(i,j) <= threshold.
        
        # Actually, a simpler and correct approach given the constraints:
        # Since threshold is small (2e5), we can iterate over each number x in filtered_nums.
        # For each x, iterate over all multiples m = 2*x, 3*x, ... up to threshold.
        # If m is in the set, union x and m.
        # This catches all cases where one number divides the other.
        # Does it catch cases where neither divides the other but lcm(a,b) <= threshold?
        # Example: a=6, b=10, threshold=30. lcm(6,10)=30.
        # 6's multiples: 12, 18, 24, 30. If 30 is in set, 6-30.
        # 10's multiples: 20, 30. If 30 is in set, 10-30.
        # So 6 and 10 are connected via 30.
        # But what if 30 is NOT in the set? Then 6 and 10 are not connected by this method.
        # However, the problem states: "Two nodes i and j are connected if lcm(nums[i], nums[j]) <= threshold".
        # So 6 and 10 SHOULD be connected directly.
        
        # The multiple-only strategy is insufficient when the LCM itself is not in the array.
        
        # Correct approach: 
        # For each number x in filtered_nums, iterate over all divisors d of x.
        # If d is in the set and d != x, union x and d.
        # This works because if lcm(a,b) = L <= threshold, then a and b are divisors of L.
        # If L is in the set, then a and b are both connected to L.
        # If L is NOT in the set, then we need another way.
        # But note: if lcm(a,b) = L <= threshold, then a and b are divisors of L.
        # We can iterate over all L from 1 to threshold. For each L, if L is in the set,
        # then all divisors of L that are in the set are connected to L.
        # This ensures that if a and b are divisors of L (and L is in the set), they are connected.
        # What if L is not in the set? Then a and b are not connected via L.
        # But they should be connected directly because lcm(a,b)=L<=threshold.
        
        # To handle the case where L is not in the set, we can do:
        # For each L from 1 to threshold:
        #   Find all divisors of L that are in the set.
        #   If there are multiple such divisors, union them all together.
        # This is efficient because the sum of the number of divisors for all L up to T is O(T log T).
        
        # Let's implement this:
        # 1. Mark presence of each number in a boolean array.
        # 2. For each L from 1 to threshold:
        #      If L is not in the set, skip? No, we still need to find divisors that are in the set.
        #      Actually, we only care about L that are in the set? No.
        #      Consider a=6, b=10, threshold=30. L=30. If 30 is not in the set, we still need to connect 6 and 10.
        #      So we iterate L from 1 to threshold regardless of whether L is in the set.
        #      For each L, find all divisors d of L such that d is in the set.
        #      If there are at least two such divisors, union them.
        
        # This is correct and efficient.
        
        # Re-initialize parent and rank for clarity
        parent = {x: x for x in filtered_nums}
        rank = {x: 0 for x in filtered_nums}
        
        # For each L from 1 to threshold, find all divisors that are in the set
        for L in range(1, threshold + 1):
            # Find all divisors of L
            # Instead of finding all divisors, we can iterate multiples of potential divisors?
            # Better: iterate d from 1 to sqrt(L) to find divisors.
            divisors = []
            d = 1
            while d * d <= L:
                if L % d == 0:
                    if present[d]:
                        divisors.append(d)
                    if d != L // d:
                        other = L // d
                        if present[other]:
                            divisors.append(other)
                d += 1
            
            # Union all divisors found for this L
            if len(divisors) > 1:
                first = divisors[0]
                for i in range(1, len(divisors)):
                    union(first, divisors[i])
                    
        # Count number of connected components
        roots = set()
        for x in filtered_nums:
            roots.add(find(x))
            
        return len(roots)