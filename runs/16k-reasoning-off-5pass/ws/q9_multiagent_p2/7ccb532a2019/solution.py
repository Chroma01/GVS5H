from collections import Counter

class Solution:
    def makeStringGood(self, s: str) -> int:
        # Count frequency of each character
        freq_map = Counter(s)
        # Get unique frequencies present in the string
        unique_freqs = sorted(list(freq_map.values()))
        
        # Helper function to calculate cost for a target frequency T
        def calculate_cost(target: int) -> int:
            if target == 0:
                # If target is 0, we delete all characters
                return len(s)
            
            surplus = 0
            deficit = 0
            
            for f in unique_freqs:
                if f > target:
                    surplus += (f - target)
                elif f < target:
                    deficit += (target - f)
            
            # Cost is sum of absolute differences minus the amount we can "transfer"
            # Transfer cost is 1 per unit (Change operation)
            # Delete/Insert cost is 2 per unit (1 delete + 1 insert)
            # So we save 1 per unit transferred.
            # Total cost = (surplus + deficit) - min(surplus, deficit)
            return (surplus + deficit) - min(surplus, deficit)
        
        # Consider each unique frequency as a potential target
        min_ops = float('inf')
        for f in unique_freqs:
            cost = calculate_cost(f)
            if cost < min_ops:
                min_ops = cost
        
        # Also consider target frequency 0 (delete everything)
        cost_zero = calculate_cost(0)
        if cost_zero < min_ops:
            min_ops = cost_zero
            
        return min_ops