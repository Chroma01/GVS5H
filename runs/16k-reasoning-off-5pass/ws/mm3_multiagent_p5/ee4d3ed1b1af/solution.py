class Solution:
    def shortestMatchingSubstring(self, s: str, p: str) -> int:
        # Split pattern p into three parts based on two '*'
        star1 = p.index('*')
        star2 = p.index('*', star1 + 1)
        P1 = p[:star1]
        P2 = p[star1 + 1:star2]
        P3 = p[star2 + 1:]
        
        n = len(s)
        
        # KMP search: returns list of start indices of pattern in text
        def kmp_occurrences(text, pattern):
            if not pattern:
                return []
            m = len(pattern)
            # Compute LPS array
            lps = [0] * m
            for i in range(1, m):
                j = lps[i - 1]
                while j > 0 and pattern[i] != pattern[j]:
                    j = lps[j - 1]
                if pattern[i] == pattern[j]:
                    j += 1
                lps[i] = j
            # Find occurrences
            occ = []
            j = 0
            for i in range(len(text)):
                while j > 0 and text[i] != pattern[j]:
                    j = lps[j - 1]
                if text[i] == pattern[j]:
                    j += 1
                if j == m:
                    occ.append(i - m + 1)
                    j = lps[j - 1]
            return occ
        
        # Precompute occurrence lists
        L1 = kmp_occurrences(s, P1) if P1 else None  # start indices of P1
        M2 = kmp_occurrences(s, P2) if P2 else None  # start indices of P2
        Q3 = kmp_occurrences(s, P3) if P3 else None  # start indices of P3
        R3 = [x + len(P3) - 1 for x in Q3] if P3 else None  # end indices of P3
        
        ans = float('inf')
        
        # Helper for binary search
        import bisect
        
        # Case A: all non-empty
        if P1 and P2 and P3:
            for m in M2:
                # Find largest l in L1 with l + |P1| <= m
                target_l = m - len(P1)
                idx_l = bisect.bisect_right(L1, target_l) - 1
                if idx_l < 0:
                    continue
                l = L1[idx_l]
                # Find smallest r in R3 with r >= m + |P2| + |P3| - 1
                target_r = m + len(P2) + len(P3) - 1
                idx_r = bisect.bisect_left(R3, target_r)
                if idx_r >= len(R3):
                    continue
                r = R3[idx_r]
                ans = min(ans, r - l + 1)
        
        # Case B: P1 empty, P2 non-empty, P3 non-empty
        elif not P1 and P2 and P3:
            for m in M2:
                l = m
                target_r = m + len(P2) + len(P3) - 1
                idx_r = bisect.bisect_left(R3, target_r)
                if idx_r >= len(R3):
                    continue
                r = R3[idx_r]
                ans = min(ans, r - l + 1)
        
        # Case C: P1 non-empty, P2 empty, P3 non-empty
        elif P1 and not P2 and P3:
            for l in L1:
                # Find smallest q (start of P3) >= l + |P1|
                target_q = l + len(P1)
                idx_q = bisect.bisect_left(Q3, target_q)
                if idx_q >= len(Q3):
                    continue
                q = Q3[idx_q]
                r = q + len(P3) - 1
                ans = min(ans, r - l + 1)
        
        # Case D: P1 non-empty, P2 non-empty, P3 empty
        elif P1 and P2 and not P3:
            for m in M2:
                target_l = m - len(P1)
                idx_l = bisect.bisect_right(L1, target_l) - 1
                if idx_l < 0:
                    continue
                l = L1[idx_l]
                r = m + len(P2) - 1
                ans = min(ans, r - l + 1)
        
        # Case E: P1 empty, P2 empty, P3 non-empty
        elif not P1 and not P2 and P3:
            if Q3:
                ans = min(ans, len(P3))
        
        # Case F: P1 non-empty, P2 empty, P3 empty
        elif P1 and not P2 and not P3:
            if L1:
                ans = min(ans, len(P1))
        
        # Case G: P1 empty, P2 non-empty, P3 empty
        elif not P1 and P2 and not P3:
            if M2:
                ans = min(ans, len(P2))
        
        # Case H: all empty (**)
        else:
            ans = 0
        
        return ans if ans != float('inf') else -1