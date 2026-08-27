class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        n = len(str1)
        m = len(str2)
        length = n + m - 1
        res = [''] * length
        
        # Phase 1: Apply all 'T' constraints
        # We fill the result array based on 'T' constraints.
        # If a position is already filled with a conflicting character, return "".
        for i, char in enumerate(str1):
            if char == 'T':
                for j in range(m):
                    idx = i + j
                    if res[idx] != '':
                        if res[idx] != str2[j]:
                            return ""
                    else:
                        res[idx] = str2[j]
        
        # Phase 2: Check if any 'F' constraint is already violated by 'T' constraints
        # If an 'F' window is fully filled and equals str2, no solution exists.
        for i, char in enumerate(str1):
            if char == 'F':
                # Check if the window [i, i+m-1] is fully filled and equals str2
                # Since m is small (<= 500), slicing and comparing is efficient enough here.
                # We check if the slice exists (indices are valid) and matches str2.
                if i + m <= length:
                    window = "".join(res[i:i+m])
                    if window == str2:
                        return ""
        
        # Phase 3: Greedy fill remaining positions
        # Iterate through the result array from left to right.
        # For any empty position, try characters 'a' through 'z' greedily.
        # Optimization: We only need to check the 'F' constraint that *ends* exactly at the current position i.
        # An 'F' constraint at index k ends at k + m - 1. So if we are filling index i, we check if k = i - m + 1 is an 'F'.
        # Any 'F' constraint ending before i was already validated when its last character was filled.
        # Any 'F' constraint ending after i is not yet fully filled (contains empty slots), so it cannot equal str2 yet.
        for i in range(length):
            if res[i] == '':
                # Try characters 'a' to 'z'
                for c in "abcdefghijklmnopqrstuvwxyz":
                    res[i] = c
                    valid = True
                    
                    # Check the 'F' constraint that ends exactly at i
                    k = i - m + 1
                    if 0 <= k < n and str1[k] == 'F':
                        # Check if window [k, k+m-1] matches str2
                        # We construct the window string and compare
                        # Since we just filled res[i], the window is now fully filled.
                        window = "".join(res[k:k+m])
                        if window == str2:
                            valid = False
                    
                    if valid:
                        break
                
                # If no character works for this position, return ""
                if res[i] == '':
                    return ""
        
        return "".join(res)