class Solution:
    def maxScore(self, points: List[int], m: int) -> int:
        n = len(points)
        
        # Helper function to check if a minimum score x is achievable
        def can_achieve(x: int) -> bool:
            if x == 0:
                return True
            
            # Calculate minimum visits required for each index
            # v[i] = ceil(x / points[i])
            # To avoid floating point, use (x + points[i] - 1) // points[i]
            v = [(x + p - 1) // p for p in points]
            
            total_visits = sum(v)
            
            # If total visits alone exceed m, it's impossible
            # Note: The actual moves might be more than total_visits due to backtracking
            # But if total_visits > m, definitely impossible.
            if total_visits > m:
                return False
            
            # Calculate the minimal moves required to achieve these visit counts.
            # The path starts at -1, moves to 0 (1 move), then performs a contiguous walk.
            # The minimal number of moves to achieve visit counts v is:
            # moves = total_visits + 2 * max(0, max_imbalance)
            # where max_imbalance = max_{i} (prefix_sum_v[i] - suffix_sum_v[i+1])
            # This can be rewritten as: max_{i} (2 * prefix_sum_v[i] - total_visits)
            
            # Compute prefix sums and find max imbalance
            prefix_sum = 0
            max_imbalance = 0
            
            for i in range(n):
                prefix_sum += v[i]
                # Imbalance at split after index i:
                # Left part: v[0]...v[i], sum = prefix_sum
                # Right part: v[i+1]...v[n-1], sum = total_visits - prefix_sum
                # Imbalance = Left - Right = 2 * prefix_sum - total_visits
                imbalance = 2 * prefix_sum - total_visits
                if imbalance > max_imbalance:
                    max_imbalance = imbalance
            
            min_moves = total_visits + 2 * max(0, max_imbalance)
            
            return min_moves <= m

        # Binary search on the answer
        # Lower bound: 0
        # Upper bound: max(points) * m is a safe upper bound, but we can tighten it.
        # The maximum possible score for any index is points[i] * m.
        # So the max possible minimum is max(points) * m.
        low = 0
        high = max(points) * m
        ans = 0
        
        while low <= high:
            mid = (low + high) // 2
            if can_achieve(mid):
                ans = mid
                low = mid + 1
            else:
                high = mid - 1
                
        return ans