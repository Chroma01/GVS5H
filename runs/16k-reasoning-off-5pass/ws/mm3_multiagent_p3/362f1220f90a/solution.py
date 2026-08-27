class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        n = len(str1)
        m = len(str2)
        L = n + m - 1
        
        # word[j] will hold the character assigned, or None if unassigned
        word = [None] * L
        
        # For each window starting at i (0 <= i < n), we track:
        # assigned[i]: how many positions in word[i..i+m-1] are assigned
        # matches[i]: how many of those assigned positions equal str2[k-i]
        assigned = [0] * n
        matches = [0] * n
        
        def get_covering_windows(j):
            # Windows that cover position j: i in [max(0, j-m+1), min(n-1, j)]
            start = max(0, j - m + 1)
            end = min(n - 1, j)
            return range(start, end + 1)
        
        for j in range(L):
            # Step 1: Determine if any 'T' constraint forces a character at position j
            forced = None
            conflict = False
            for i in get_covering_windows(j):
                if str1[i] == 'T':
                    c = str2[j - i]
                    if forced is None:
                        forced = c
                    elif forced != c:
                        conflict = True
                        break
            if conflict:
                return ""
            
            # Step 2: Determine candidate characters to try
            if forced is not None:
                candidates = [forced]
            else:
                candidates = [chr(ord('a') + k) for k in range(26)]
            
            # Step 3: Try each candidate
            found = False
            for c in candidates:
                # Tentatively assign c to position j and check windows covering j
                temp_changes = []
                valid = True
                
                for i in get_covering_windows(j):
                    old_assigned = assigned[i]
                    old_matches = matches[i]
                    new_assigned = old_assigned + 1
                    new_matches = old_matches
                    if c == str2[j - i]:
                        new_matches += 1
                    
                    # Check constraints for this window after this assignment
                    if str1[i] == 'T':
                        if new_assigned == m and new_matches < m:
                            valid = False
                            break
                    else:  # 'F'
                        if new_assigned == m and new_matches == m:
                            valid = False
                            break
                    
                    temp_changes.append((i, old_assigned, old_matches))
                
                if valid:
                    # Commit the changes
                    word[j] = c
                    for i, old_a, old_m in temp_changes:
                        assigned[i] = old_a + 1
                        if c == str2[j - i]:
                            matches[i] = old_m + 1
                        else:
                            matches[i] = old_m
                    found = True
                    break
                # else: try next candidate (no need to rollback since we didn't commit)
            
            if not found:
                return ""
        
        # Final verification (optional, but safe)
        # Check all T windows are satisfied
        for i in range(n):
            if str1[i] == 'T':
                window = word[i:i+m]
                if any(ch is None for ch in window):
                    return ""
                if "".join(window) != str2:
                    return ""
            else:  # 'F'
                window = word[i:i+m]
                if all(ch is not None for ch in window):
                    if "".join(window) == str2:
                        return ""
        
        return "".join(word)