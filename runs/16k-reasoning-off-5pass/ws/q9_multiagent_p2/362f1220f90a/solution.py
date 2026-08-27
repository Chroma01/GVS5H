class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        n = len(str1)
        m = len(str2)
        length = n + m - 1
        
        # Initialize word with placeholders
        word = [''] * length
        forced = [None] * length
        
        # Step 1: Apply 'T' constraints
        for i, char in enumerate(str1):
            if char == 'T':
                for j in range(m):
                    idx = i + j
                    if forced[idx] is not None and forced[idx] != str2[j]:
                        return ""
                    forced[idx] = str2[j]
        
        # Step 2: Identify critical 'F' windows
        # A window is critical if str1[i] == 'F' and the forced characters 
        # do not already make the substring different from str2.
        critical_windows = []
        
        for i in range(n):
            if str1[i] == 'F':
                # Check if the window is already satisfied by forced characters
                satisfied = False
                for j in range(m):
                    idx = i + j
                    if forced[idx] is not None and forced[idx] != str2[j]:
                        satisfied = True
                        break
                
                if not satisfied:
                    # This window is critical. It matches str2 on all forced positions.
                    # We need to find free positions in [i, i+m-1].
                    free_positions = []
                    for j in range(m):
                        idx = i + j
                        if forced[idx] is None:
                            free_positions.append(idx)
                    
                    if not free_positions:
                        # No free positions to break the equality -> Impossible
                        return ""
                    
                    critical_windows.append({
                        'start': i,
                        'last_free': free_positions[-1]
                    })
        
        # Step 3: Precompute 'must_break_at' for each index k.
        # must_break_at[k] contains characters that CANNOT be placed at k
        # because if we place them, we fail to break a critical window where k is the last free position.
        must_break_at = [set() for _ in range(length)]
        
        for cw in critical_windows:
            last_free = cw['last_free']
            start = cw['start']
            # At index last_free, we MUST pick a char != str2[last_free - start]
            forbidden_char = str2[last_free - start]
            must_break_at[last_free].add(forbidden_char)
            
        # Step 4: Greedy construction
        for k in range(length):
            if forced[k] is not None:
                word[k] = forced[k]
            else:
                forbidden = must_break_at[k]
                c = 'a'
                while c in forbidden:
                    c = chr(ord(c) + 1)
                word[k] = c
                
        return "".join(word)