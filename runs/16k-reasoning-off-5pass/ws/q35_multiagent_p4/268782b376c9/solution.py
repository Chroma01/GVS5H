class Solution:
    def maxScore(self, points: List[int], m: int) -> int:
        n = len(points)
        
        # Helper function to check if a minimum score 'x' is achievable
        def check(x):
            # Calculate required visits for each index
            req = [(x + p - 1) // p for p in points]
            
            total_req = sum(req)
            if total_req > m:
                return False
            
            # Precompute prefix sums of req
            prefix = [0] * (n + 1)
            for i in range(n):
                prefix[i + 1] = prefix[i] + req[i]
            
            # The minimum moves to satisfy req is:
            # sum(req) + min_{0 <= k <= n} ( max(0, k - prefix[k]) + max(0, (n - k) - (total_req - prefix[k])) )
            # Explanation:
            # We split the array at index k (0 to n).
            # Left part: indices 0 to k-1. We need to cover k indices.
            #   If sum(req[0..k-1]) < k, we need extra moves to "fill" the left part.
            #   The deficit is k - prefix[k].
            # Right part: indices k to n-1. We need to cover n-k indices.
            #   If sum(req[k..n-1]) < n-k, we need extra moves to "fill" the right part.
            #   The deficit is (n-k) - (total_req - prefix[k]).
            # The extra moves are the sum of these deficits (clamped at 0).
            # We minimize this extra cost over all possible split points k.
            
            min_extra = float('inf')
            for k in range(n + 1):
                left_deficit = max(0, k - prefix[k])
                right_deficit = max(0, (n - k) - (total_req - prefix[k]))
                extra = left_deficit + right_deficit
                if extra < min_extra:
                    min_extra = extra
            
            return (total_req + min_extra) <= m

        # Binary search for the maximum minimum score
        low = 0
        high = 10**18  # Sufficiently large upper bound
        ans = 0
        
        while low <= high:
            mid = (low + high) // 2
            if check(mid):
                ans = mid
                low = mid + 1
            else:
                high = mid - 1
                
        return ans