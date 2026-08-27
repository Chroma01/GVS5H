class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        n = len(str1)
        m = len(str2)
        total_len = n + m - 1
        
        # Initialize word array with None
        word = [None] * total_len
        # Track which positions are forced by T constraints
        forced = [False] * total_len
        
        # Process T constraints
        for i in range(n):
            if str1[i] == 'T':
                for j in range(m):
                    pos = i + j
                    if word[pos] is not None:
                        if word[pos] != str2[j]:
                            return ""
                    else:
                        word[pos] = str2[j]
                        forced[pos] = True
        
        # Fill non-forced positions with 'a'
        for i in range(total_len):
            if word[i] is None:
                word[i] = 'a'
        
        # Process F constraints
        # We iterate from left to right. For each F constraint that is violated,
        # we fix it by changing the rightmost non-forced character in its window.
        for i in range(n):
            if str1[i] == 'F':
                # Check if word[i:i+m] == str2
                # To avoid creating a new string slice every time (which is O(m)),
                # we can compare character by character.
                match = True
                for j in range(m):
                    if word[i + j] != str2[j]:
                        match = False
                        break
                if match:
                    # Violation found, need to fix
                    # Find the rightmost non-forced index j in [0, m-1]
                    fix_j = -1
                    for j in range(m - 1, -1, -1):
                        if not forced[i + j]:
                            fix_j = j
                            break
                    
                    if fix_j == -1:
                        # No non-forced character to change, cannot fix
                        return ""
                    
                    # Change word[i+fix_j] to break the match
                    # Set to 'a' if it's not equal to str2[fix_j], else 'b'
                    pos = i + fix_j
                    if word[pos] != str2[fix_j]:
                        # It's already not equal, but we are in a match situation,
                        # so this shouldn't happen. Actually, if it's not forced,
                        # it was set to 'a'. So if str2[fix_j] is not 'a', then
                        # word[pos] ('a') != str2[fix_j], so the substring wouldn't match.
                        # Therefore, if we are here, word[pos] must equal str2[fix_j].
                        # So we must change it to something else.
                        # The smallest character different from str2[fix_j] is:
                        # 'a' if str2[fix_j] != 'a', else 'b'
                        word[pos] = 'a' if str2[fix_j] != 'a' else 'b'
                    else:
                        # word[pos] == str2[fix_j], so we need to change it.
                        word[pos] = 'a' if str2[fix_j] != 'a' else 'b'
        
        # Final verification of all F constraints
        for i in range(n):
            if str1[i] == 'F':
                match = True
                for j in range(m):
                    if word[i + j] != str2[j]:
                        match = False
                        break
                if match:
                    return ""
        
        return "".join(word)