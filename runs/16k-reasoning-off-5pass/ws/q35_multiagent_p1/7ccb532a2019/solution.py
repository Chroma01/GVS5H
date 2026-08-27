class Solution:
    def makeStringGood(self, s: str) -> int:
        n = len(s)
        # Count frequencies of each character
        freq = [0] * 26
        for c in s:
            freq[ord(c) - ord('a')] += 1
        
        # Sort frequencies in descending order
        freq.sort(reverse=True)
        
        min_ops = n  # worst case: delete all and insert nothing (or other extreme)
        
        # Iterate over all possible target frequencies k
        # k can be from 1 to n
        for k in range(1, n + 1):
            # For each k, iterate over the number of characters m to keep (from 1 to 26)
            # But m*k should be considered; however, we can always insert, so m can be up to 26
            # But if m*k > n + (some bound), it might be expensive. Actually, we just compute cost.
            # We only need to consider m such that there are at least m characters with non-zero frequency? 
            # Actually, we can keep any m characters from the 26, but if a character has 0 frequency, 
            # then keeping it means we must insert k copies, which costs k. 
            # So we should consider m from 1 to 26, but note that if we keep a character with 0 frequency, 
            # the deficit is k and surplus is 0.
            
            # To optimize, we can break early if m exceeds the number of characters that have non-zero freq? 
            # Not necessary since 26 is small.
            
            for m in range(1, 27):
                # Calculate surplus and deficit for the top m characters
                surplus = 0
                deficit = 0
                for i in range(m):
                    if freq[i] > k:
                        surplus += freq[i] - k
                    elif freq[i] < k:
                        deficit += k - freq[i]
                
                # Cost for excluded characters: delete all their occurrences
                excluded_cost = sum(freq[m:])
                
                # Total cost = max(surplus, deficit) + excluded_cost
                # Explanation: 
                #   - Each change operation can reduce one surplus and one deficit.
                #   - So min(surplus, deficit) changes are used.
                #   - Remaining surplus: surplus - min(surplus, deficit) = max(0, surplus - deficit) -> must be deleted
                #   - Remaining deficit: deficit - min(surplus, deficit) = max(0, deficit - surplus) -> must be inserted
                #   - Total cost = (surplus - min(S,D)) + (deficit - min(S,D)) + min(S,D) + excluded_cost
                #                = max(surplus, deficit) + excluded_cost
                cost = max(surplus, deficit) + excluded_cost
                
                if cost < min_ops:
                    min_ops = cost
        
        return min_ops