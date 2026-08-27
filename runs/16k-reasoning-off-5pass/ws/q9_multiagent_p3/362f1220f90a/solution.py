class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        n = len(str1)
        m = len(str2)
        length = n + m - 1
        
        # Initialize result array with None
        res = [None] * length
        # Track which positions are fixed by 'T' constraints
        is_fixed = [False] * length
        
        # Step 1: Process all 'T' constraints
        for i in range(n):
            if str1[i] == 'T':
                for k in range(m):
                    idx = i + k
                    if res[idx] is not None:
                        if res[idx] != str2[k]:
                            return ""
                    else:
                        res[idx] = str2[k]
                    is_fixed[idx] = True
        
        # Step 2: Fill remaining positions with 'a'
        for i in range(length):
            if res[i] is None:
                res[i] = 'a'
        
        # Step 3: Process all 'F' constraints
        for i in range(n):
            if str1[i] == 'F':
                # Check if the current window matches str2
                match = True
                for k in range(m):
                    if res[i + k] != str2[k]:
                        match = False
                        break
                
                if match:
                    # We need to change one character in this window to break the match
                    # To minimize lexicographically, change the rightmost character that is NOT fixed by 'T'
                    changed = False
                    for k in range(m - 1, -1, -1):
                        idx = i + k
                        if not is_fixed[idx]:
                            res[idx] = 'b'
                            changed = True
                            break
                    
                    if not changed:
                        # All characters in this window are fixed by 'T' and match str2
                        return ""
        
        return "".join(res)