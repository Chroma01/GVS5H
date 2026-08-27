from typing import List

class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        # Precompute positions of each number (1-indexed)
        # pos[x] stores the 0-based index of number x in the array nums = [1, 2, ..., n]
        pos = [0] * (n + 1)
        for i in range(n):
            pos[i + 1] = i
        
        # Build adjacency list for conflicts
        # adj[x] will contain a list of numbers that conflict with x
        adj = [[] for _ in range(n + 1)]
        for a, b in conflictingPairs:
            adj[a].append(b)
            adj[b].append(a)
        
        max_valid = 0
        
        # Iterate over each pair to remove
        for i in range(len(conflictingPairs)):
            a, b = conflictingPairs[i]
            
            left = 0
            current_valid = 0
            
            # Sliding window over the array nums (which is effectively 1, 2, ..., n)
            # right is the 0-based index of the end of the window
            for right in range(n):
                num = right + 1
                
                # Check for conflicts involving 'num' with elements currently in the window
                # We need to shrink the window from the left until no conflict exists
                while True:
                    found_conflict = False
                    for neighbor in adj[num]:
                        # Skip the removed pair
                        if (num == a and neighbor == b) or (num == b and neighbor == a):
                            continue
                        
                        # Check if 'neighbor' is currently in the window [left, right]
                        # 'neighbor' is in the window if its position is between left and right (inclusive)
                        if left <= pos[neighbor] <= right:
                            found_conflict = True
                            break
                    
                    if not found_conflict:
                        break
                    
                    # Conflict found, increment left to shrink the window
                    left += 1
                
                # Add the number of valid subarrays ending at 'right'
                # These are subarrays starting from index 'left' to 'right'
                current_valid += (right - left + 1)
            
            if current_valid > max_valid:
                max_valid = current_valid
                
        return max_valid