class Solution:
    def makeStringGood(self, s: str) -> int:
        from collections import Counter
        
        freq = Counter(s)
        freqs = list(freq.values())
        n = len(s)
        
        # Option 1: Delete all characters (target frequency 0)
        ans = n
        
        # Option 2: Target frequency k > 0
        # We iterate through all possible target frequencies k from 1 to max_freq.
        # The optimal k is guaranteed to be within this range because if k > max_freq,
        # we would just be inserting characters to reach k for all present characters,
        # which is generally more expensive than reducing to max_freq or lower.
        # Specifically, if we choose k > max_freq, cost = sum(k - f) for all f.
        # This is linear in k, so the minimum for k > max_freq would be at k = max_freq + 1?
        # Actually, if we keep all characters, cost = sum(|f - k|). This is convex.
        # The minimum of sum(|f - k|) occurs at the median of freqs.
        # However, we also have the option to remove characters.
        # Checking k from 1 to max_freq covers all "reduce to existing level" strategies.
        # Is it possible optimal k is not in freqs?
        # Consider freqs = [2, 5]. Median is 2. k=2 cost = 0 + 3 = 3.
        # k=3 cost = 1 + 2 = 3. k=4 cost = 2 + 1 = 3.
        # k=5 cost = 3 + 0 = 3.
        # It seems checking existing frequencies is sufficient, but checking all up to max_freq is safe.
        # Given N <= 20000, O(N * 26) is perfectly fine.
        
        max_freq = max(freqs) if freqs else 0
        
        for k in range(1, max_freq + 1):
            surplus = 0
            deficit = 0
            removed_cost = 0
            
            for f in freqs:
                if f > k:
                    # Must delete excess
                    surplus += (f - k)
                elif f < k:
                    # Decide whether to keep or remove this character
                    # Cost to keep (fill deficit) = k - f
                    # Cost to remove (delete all) = f
                    # Keep if (k - f) <= f  => k <= 2f => 2f >= k
                    if 2 * f >= k:
                        deficit += (k - f)
                    else:
                        removed_cost += f
            
            # Cost is sum of deletions for removed chars + balancing cost for kept chars
            # Balancing cost is max(surplus, deficit) because min(surplus, deficit) can be fixed by changes
            current_ops = removed_cost + max(surplus, deficit)
            if current_ops < ans:
                ans = current_ops
                
        return ans