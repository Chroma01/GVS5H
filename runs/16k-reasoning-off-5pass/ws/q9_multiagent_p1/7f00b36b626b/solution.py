from typing import List

class Solution:
    def countComponents(self, nums: List[int], threshold: int) -> int:
        # DSU implementation
        parent = list(range(threshold + 1))
        rank = [0] * (threshold + 1)
        
        def find(i):
            root = i
            while parent[root] != root:
                root = parent[root]
            # Path compression
            curr = i
            while curr != root:
                nxt = parent[curr]
                parent[curr] = root
                curr = nxt
            return root
        
        def union(i, j):
            root_i = find(i)
            root_j = find(j)
            if root_i != root_j:
                if rank[root_i] < rank[root_j]:
                    parent[root_i] = root_j
                elif rank[root_i] > rank[root_j]:
                    parent[root_j] = root_i
                else:
                    parent[root_j] = root_i
                    rank[root_i] += 1
                return True
            return False

        # Step 1: Separate numbers > threshold (isolated) and <= threshold (connected)
        # Any number x > threshold cannot connect to any y because lcm(x, y) >= x > threshold.
        # Thus, they form isolated components.
        relevant_nums = [x for x in nums if x <= threshold]
        isolated_count = len(nums) - len(relevant_nums)
        
        # Step 2: Build components for numbers <= threshold
        # Strategy: Iterate through every number L from 1 to threshold.
        # For each L, find all divisors d of L such that d is in nums.
        # All such divisors are connected because they share a common multiple L <= threshold.
        # To do this efficiently:
        # 1. Create a list of divisors for each number up to threshold.
        # 2. Populate this list by iterating over each x in relevant_nums and its multiples.
        
        divs = [[] for _ in range(threshold + 1)]
        for x in relevant_nums:
            for m in range(x, threshold + 1, x):
                divs[m].append(x)
        
        # Step 3: Union all divisors found for each common multiple L
        for m in range(1, threshold + 1):
            if len(divs[m]) > 1:
                # Union all elements in divs[m]
                root = divs[m][0]
                for i in range(1, len(divs[m])):
                    union(root, divs[m][i])
        
        # Step 4: Count components
        # Components from isolated numbers (> threshold)
        count = isolated_count
        
        # Components from relevant numbers (<= threshold)
        # Count unique roots among relevant numbers
        roots = set()
        for x in relevant_nums:
            roots.add(find(x))
        count += len(roots)
        
        return count