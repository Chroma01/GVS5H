class Solution:
    def makeStringGood(self, s: str) -> int:
        from collections import Counter
        
        freq = Counter(s)
        if not freq:
            return 0
        
        max_freq = max(freq.values())
        total_len = len(s)
        min_ops = total_len  # Case where we delete all characters (k=0)
        
        # Iterate over all possible target frequencies k from 1 to max_freq
        for k in range(1, max_freq + 1):
            # Calculate X: sum of excesses for characters with freq >= k
            # These characters are always kept because dropping them costs f_c,
            # while keeping them contributes (f_c - k) to X.
            # Since f_c - k < f_c, keeping is always better for these.
            X = 0
            for f in freq.values():
                if f >= k:
                    X += (f - k)
            
            # Identify characters with freq < k
            # For these, we have a choice: keep or drop.
            Y_all = 0
            keep_candidates = []
            
            for f in freq.values():
                if f < k:
                    Y_all += (k - f)
                    keep_candidates.append(f)
            
            if Y_all <= X:
                # Keep all characters with f < k
                # Cost is determined by X (since max(X, Y_all) = X)
                # Dropped sum is 0
                current_ops = X
            else:
                # Y_all > X, we need to select a subset to minimize cost
                # We keep a character with freq f (where f < k) if 2*f > k.
                # If 2*f <= k, dropping it (cost f) is cheaper or equal to keeping it (cost k-f).
                
                Y_subset = 0
                sum_kept_f = 0
                for f in keep_candidates:
                    if 2 * f > k:
                        Y_subset += (k - f)
                        sum_kept_f += f
                
                # Sum of frequencies for dropped small characters
                sum_small_f = sum(keep_candidates)
                sum_dropped_f = sum_small_f - sum_kept_f
                
                # Total cost = (cost of dropped chars) + max(X, Y_subset)
                current_ops = sum_dropped_f + max(X, Y_subset)
            
            if current_ops < min_ops:
                min_ops = current_ops
        
        return min_ops