class Solution:
    def maximumWeight(self, intervals: List[List[int]]) -> List[int]:
        n = len(intervals)
        # Sort intervals by right endpoint, keeping original indices
        # Each element: (l, r, weight, original_index)
        sorted_intervals = sorted([(l, r, w, i) for i, (l, r, w) in enumerate(intervals)], key=lambda x: x[1])
        
        # Extract sorted arrays for easier access
        L = [x[0] for x in sorted_intervals]
        R = [x[1] for x in sorted_intervals]
        W = [x[2] for x in sorted_intervals]
        OrigIdx = [x[3] for x in sorted_intervals]
        
        # dp[k][i] = (max_weight, list_of_original_indices)
        # k ranges from 0 to 4, i ranges from 0 to n-1
        # We'll use a list of lists for dp
        # dp[k][i] stores the best result using at most k intervals from first i+1 intervals (sorted)
        
        # Initialize dp table
        # dp[k][i] = (weight, indices_list)
        dp = [[(0, []) for _ in range(n)] for _ in range(5)]
        
        # For k=0, all are (0, [])
        
        # Precompute prev index for each interval using binary search
        # For interval i, find the largest j such that R[j] < L[i]
        # Since R is sorted (because we sorted by R), we can use bisect
        import bisect
        
        prev = [-1] * n
        for i in range(n):
            # Find rightmost interval j with R[j] < L[i]
            # bisect_left returns the first index where R[j] >= L[i]
            # so the index before that is the last one with R[j] < L[i]
            idx = bisect.bisect_left(R, L[i])
            if idx > 0:
                prev[i] = idx - 1
            else:
                prev[i] = -1
        
        # Fill DP table
        for k in range(1, 5):
            for i in range(n):
                # Option 1: exclude interval i
                if i > 0:
                    excl_weight, excl_indices = dp[k][i-1]
                else:
                    excl_weight, excl_indices = 0, []
                
                # Option 2: include interval i
                p = prev[i]
                if p != -1:
                    incl_weight, incl_indices = dp[k-1][p]
                else:
                    incl_weight, incl_indices = 0, []
                incl_weight += W[i]
                incl_indices = incl_indices + [OrigIdx[i]]
                
                # Compare: first by weight (higher is better), then by indices list (lexicographically smaller is better)
                if incl_weight > excl_weight:
                    dp[k][i] = (incl_weight, incl_indices)
                elif incl_weight == excl_weight:
                    # Choose lexicographically smaller list of indices
                    if incl_indices < excl_indices:
                        dp[k][i] = (incl_weight, incl_indices)
                    else:
                        dp[k][i] = (excl_weight, excl_indices)
                else:
                    dp[k][i] = (excl_weight, excl_indices)
        
        # The answer is the indices list from dp[4][n-1]
        _, result_indices = dp[4][n-1]
        return result_indices