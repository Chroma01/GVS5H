class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        n = len(str1)
        m = len(str2)
        length = n + m - 1
        word = [''] * length
        
        # Step 1: Process 'T' constraints to fill forced characters and check consistency
        forced_char = [''] * length
        conflict = False
        
        for i in range(n):
            if str1[i] == 'T':
                # This 'T' constraint forces word[i...i+m-1] to be str2
                for j in range(m):
                    idx = i + j
                    if idx >= length:
                        break
                    if forced_char[idx] != '':
                        if forced_char[idx] != str2[j]:
                            conflict = True
                            break
                    else:
                        forced_char[idx] = str2[j]
                if conflict:
                    break
        
        if conflict:
            return ""
        
        # Step 2: Precompute 'F' constraints ending at each position
        # f_ending_at[k] contains list of indices i where str1[i] == 'F' and i + m - 1 == k
        f_ending_at = [[] for _ in range(length)]
        for i in range(n):
            if str1[i] == 'F':
                end_idx = i + m - 1
                if end_idx < length:
                    f_ending_at[end_idx].append(i)
        
        # Step 3: Greedily fill the string from left to right
        for k in range(length):
            if forced_char[k] != '':
                word[k] = forced_char[k]
            else:
                # Try characters from 'a' to 'z' to find the lexicographically smallest valid character
                found = False
                for c in range(26):
                    char = chr(ord('a') + c)
                    word[k] = char
                    # Check all 'F' constraints that end exactly at k
                    valid = True
                    for i in f_ending_at[k]:
                        # Check if the substring word[i : k+1] matches str2
                        # Since we fill left-to-right, this substring is fully determined
                        match = True
                        for j in range(m):
                            if word[i + j] != str2[j]:
                                match = False
                                break
                        if match:
                            valid = False
                            break
                    if valid:
                        found = True
                        break
                
                if not found:
                    return ""
        
        return "".join(word)