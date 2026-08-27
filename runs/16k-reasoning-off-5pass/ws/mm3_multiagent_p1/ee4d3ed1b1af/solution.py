class Solution:
    def shortestMatchingSubstring(self, s: str, p: str) -> int:
        n = len(s)
        # Split pattern p into A, B, C at the two '*'
        star1 = p.find('*')
        star2 = p.find('*', star1 + 1)
        A = p[:star1]
        B = p[star1+1:star2]
        C = p[star2+1:]
        lenA, lenB, lenC = len(A), len(B), len(C)
        
        # If pattern is "**", empty substring matches, length 0
        if lenA == 0 and lenB == 0 and lenC == 0:
            return 0
        
        # Z-algorithm
        def z_algorithm(s):
            n = len(s)
            z = [0] * n
            z[0] = n
            l = r = 0
            for i in range(1, n):
                if i < r:
                    z[i] = min(r - i, z[i - l])
                while i + z[i] < n and s[z[i]] == s[i + z[i]]:
                    z[i] += 1
                if i + z[i] > r:
                    l, r = i, i + z[i]
            return z
        
        # Compute prefA[i]: longest prefix of A matching s starting at i
        if lenA > 0:
            concat = A + '$' + s
            z = z_algorithm(concat)
            prefA = [0] * n
            offset = lenA + 1
            for i in range(n):
                prefA[i] = min(z[offset + i], lenA)
        else:
            prefA = [0] * n  # empty prefix always matches (length 0)
        
        # Compute prefB[i]: longest prefix of B matching s starting at i
        if lenB > 0:
            concat = B + '$' + s
            z = z_algorithm(concat)
            prefB = [0] * n
            offset = lenB + 1
            for i in range(n):
                prefB[i] = min(z[offset + i], lenB)
        else:
            prefB = [0] * n
        
        # Compute sufC[i]: longest suffix of C matching s ending at i
        if lenC > 0:
            rev_s = s[::-1]
            rev_c = C[::-1]
            concat = rev_c + '$' + rev_s
            z = z_algorithm(concat)
            sufC = [0] * n
            offset = lenC + 1
            for i in range(n):
                rev_pos = n - 1 - i
                if offset + rev_pos < len(concat):
                    sufC[i] = min(z[offset + rev_pos], lenC)
                else:
                    sufC[i] = 0
        else:
            sufC = [0] * n
        
        # validB[i] = True if prefB[i] >= lenB (i.e., B fully matches starting at i)
        if lenB > 0:
            validB = [prefB[i] >= lenB for i in range(n)]
        else:
            validB = [True] * n  # empty B matches anywhere
        
        # earliestB[i] = smallest index k <= i such that validB[k] is True, or n if none
        earliestB = [n] * n
        min_so_far = n
        for i in range(n):
            if validB[i]:
                min_so_far = min(min_so_far, i)
            earliestB[i] = min_so_far
        
        # Find shortest matching substring
        ans = float('inf')
        j = 0  # end pointer
        
        for i in range(n):
            # Check if A matches starting at i
            if prefA[i] < lenA:
                continue
            
            # Minimum end index needed:
            # substring s[i..j] must contain A, B, C
            # i + lenA - 1 is end of A
            # then B (lenB) and C (lenC)
            if lenB > 0:
                min_j = i + lenA - 1 + lenB + lenC
            else:
                min_j = i + lenA - 1 + lenC
            
            if min_j >= n:
                # As i increases, min_j increases, so no later i can work either
                break
            
            if j < min_j:
                j = min_j
            
            # Find smallest j >= min_j such that sufC[j] == lenC and
            # there exists valid B in [i+lenA, j-lenC]
            while j < n:
                if sufC[j] < lenC:
                    j += 1
                    continue
                
                left = i + lenA
                right = j - lenC
                
                if lenB == 0:
                    # B is empty, just need C at end and A at start
                    if right >= left - 1:  # j-lenC >= i+lenA-1, i.e., A and C can meet/overlap? No, they can't overlap if B is empty but both can be empty.
                        # Actually if B is empty, we just need A then C, they can be adjacent or overlap if one is empty
                        # left is start of B (i+lenA), right is end of B (j-lenC)
                        # If B is empty, we need left > right (i.e., the "gap" is empty)
                        # left = i + lenA, right = j - lenC
                        # We need i+lenA <= j-lenC+1, i.e., j >= i+lenA+lenC-1
                        # Which is exactly min_j. So we just need j >= min_j and C matches.
                        if j >= min_j:
                            break
                        else:
                            j += 1
                    else:
                        j += 1
                else:
                    if right < left:
                        j += 1
                        continue
                    # Check if earliestB[right] is in [left, right]
                    if earliestB[right] <= right and earliestB[right] >= left:
                        break
                    j += 1
            
            if j < n and sufC[j] >= lenC:
                # Final validation
                if lenB == 0:
                    if j >= i + lenA + lenC - 1:
                        ans = min(ans, j - i + 1)
                else:
                    if j - lenC >= i + lenA:
                        k = earliestB[j - lenC]
                        if k >= i + lenA and k <= j - lenC:
                            ans = min(ans, j - i + 1)
        
        return ans if ans != float('inf') else -1