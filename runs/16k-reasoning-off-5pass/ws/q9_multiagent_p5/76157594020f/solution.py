class Solution:
    def minLength(self, s: str, numOps: int) -> int:
        # Step 1: Compute run lengths
        if not s:
            return 0
        
        runs = []
        current_char = s[0]
        current_length = 1
        
        for i in range(1, len(s)):
            if s[i] == current_char:
                current_length += 1
            else:
                runs.append(current_length)
                current_char = s[i]
                current_length = 1
        runs.append(current_length)
        
        # Step 2: Sort run lengths in descending order
        runs.sort(reverse=True)
        
        # Step 3: Greedily split the largest runs
        for i in range(len(runs)):
            if numOps <= 0:
                break
            
            length = runs[i]
            if length <= 1:
                # Cannot split further, move to next
                continue
            
            # Split length into floor(length/2) and ceil(length/2)
            # The new maximum part is ceil(length/2), calculated as (length + 1) // 2
            new_max = (length + 1) // 2
            
            # Replace the current run with the new maximum part
            runs[i] = new_max
            numOps -= 1
        
        # Step 4: Return the maximum remaining run length
        return max(runs) if runs else 0