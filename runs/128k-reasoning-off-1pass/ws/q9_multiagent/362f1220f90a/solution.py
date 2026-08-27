class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        n = len(str1)
        m = len(str2)
        length = n + m - 1
        word = [''] * length
        
        # Step 1: Apply all 'T' constraints
        for i in range(n):
            if str1[i] == 'T':
                # Check for conflicts before assigning
                for j in range(m):
                    if word[i + j] != '' and word[i + j] != str2[j]:
                        return ""
                # Assign the substring
                for j in range(m):
                    word[i + j] = str2[j]
        
        # Step 2: Fill unset positions greedily
        for i in range(length):
            if word[i] == '':
                # Try characters from 'a' to 'z'
                for c in "abcdefghijklmnopqrstuvwxyz":
                    word[i] = c
                    # Check if this choice violates any 'F' constraint
                    # We only need to check 'F' constraints where the window [j, j+m-1] is fully determined.
                    # A window starting at j is fully determined by index i if j + m - 1 <= i.
                    # This implies j <= i - m + 1.
                    # Also, j must be a valid index in str1 (0 <= j < n).
                    
                    valid = True
                    # Calculate the range of j to check
                    # Upper bound for j is i - m + 1. In Python range, the stop value is exclusive, so i - m + 2.
                    # Lower bound is 0.
                    start_j = 0
                    end_j = min(n, i - m + 2)
                    
                    for j in range(start_j, end_j):
                        if str1[j] == 'F':
                            # Check if word[j:j+m] equals str2
                            window_str = "".join(word[j:j+m])
                            if window_str == str2:
                                valid = False
                                break
                    if valid:
                        break
                
                # If no character works, return empty string
                if word[i] == '':
                    return ""
        
        return "".join(word)