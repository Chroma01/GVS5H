class Solution:
    def minCostGoodCaption(self, caption: str) -> str:
        n = len(caption)
        if n < 3:
            return ""
        
        min_ops = float('inf')
        best_char = None
        
        # Iterate through all possible target characters from 'a' to 'z'
        # We iterate in ascending order to ensure that if costs are equal,
        # the lexicographically smallest character is chosen.
        for target_code in range(ord('a'), ord('z') + 1):
            target_char = chr(target_code)
            current_ops = 0
            
            # Calculate cost to convert entire string to target_char
            for char in caption:
                current_ops += abs(ord(char) - ord(target_char))
            
            # Update if we found a strictly smaller cost
            if current_ops < min_ops:
                min_ops = current_ops
                best_char = target_char
        
        # If best_char is still None, it means no valid character was found
        # (This case is theoretically impossible given the constraints and logic above)
        if best_char is None:
            return ""
            
        return best_char * n