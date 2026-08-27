class Solution:
    def shortestMatchingSubstring(self, s: str, p: str) -> int:
        # Split pattern on the two '*' characters
        parts = p.split('*')
        # p contains exactly two '*', so parts has length 3
        left, middle, right = parts[0], parts[1], parts[2]
        n = len(s)
        
        # Special case: pattern is "**" -> empty substring matches
        if not left and not middle and not right:
            return 0
        
        # Helper to collect all start indices where pattern part occurs in s
        def get_occurrences(pattern):
            if not pattern:
                return []  # empty pattern has no explicit occurrences
            occs = []
            start = 0
            plen = len(pattern)
            while True:
                idx = s.find(pattern, start)
                if idx == -1:
                    break
                occs.append(idx)
                start = idx + 1
            return occs
        
        L = get_occurrences(left)   # start indices of left
        M = get_occurrences(middle) # start indices of middle
        R = get_occurrences(right)  # start indices of right
        
        # If any non-empty part has no occurrences, no match possible
        if left and not L:
            return -1
        if middle and not M:
            return -1
        if right and not R:
            return -1
        
        # Two-pointer sweep over middle occurrences
        # We need: left ends before middle starts, right starts after middle ends
        # For empty parts, the constraint is relaxed accordingly.
        
        ans = float('inf')
        
        # If middle is empty, we need left followed by right (right after left)
        if not middle:
            # left occurrence must end before right starts
            for l in L:
                # find smallest right >= l + len(left)
                # binary search in R
                import bisect
                pos = bisect.bisect_left(R, l + len(left))
                if pos < len(R):
                    r = R[pos]
                    length = r + len(right) - l
                    if length < ans:
                        ans = length
            return ans if ans != float('inf') else -1
        
        # Middle is non-empty (we already returned -1 if no occurrences)
        iL = 0  # pointer into L: largest left that ends before m
        iR = 0  # pointer into R: smallest right that starts after m_end
        
        lenL = len(left)
        lenM = len(middle)
        lenR = len(right)
        
        # Convert L and R to lists of (start, end) for easier handling
        # end is inclusive index
        # For left, end = l + lenL - 1
        # For right, start = r, end = r + lenR - 1
        
        for m in M:
            m_end = m + lenM - 1
            
            # Advance iL to the largest left that ends before m
            # left end = L[iL] + lenL - 1; we need < m (or <= m if left empty)
            # If left is empty, any position works, but we can set l = m
            if not left:
                l_start = m
                l_end = m - 1  # empty
            else:
                # Find largest l such that l + lenL - 1 < m
                # iL should point to the first l that satisfies, then take previous
                # We can advance iL while next left also ends before m
                while iL < len(L) and L[iL] + lenL - 1 < m:
                    iL += 1
                # Now iL is the first index that doesn't satisfy, or len(L)
                # The largest satisfying is iL - 1
                if iL == 0:
                    # No left ends before m
                    continue
                l_start = L[iL - 1]
                l_end = l_start + lenL - 1
            
            # Advance iR to the smallest right that starts after m_end
            # We need r > m_end (strictly after, since middle occupies m..m_end)
            # If right is empty, we can take r_start = m_end + 1
            if not right:
                r_start = m_end + 1
                r_end = m_end  # empty
            else:
                # iR is pointer; we need R[iR] > m_end
                # Advance iR while current right starts <= m_end
                while iR < len(R) and R[iR] <= m_end:
                    iR += 1
                if iR == len(R):
                    # No right starts after m_end
                    # Note: we shouldn't reset iR because m is increasing
                    # but we might need to continue for later m? Actually if iR is at end, no more right can work
                    # but we continue to next m; iR stays at len(R) which is fine
                    continue
                r_start = R[iR]
                r_end = r_start + lenR - 1
            
            # Compute length of window [l_start, r_end]
            length = r_end - l_start + 1
            if length < ans:
                ans = length
        
        return ans if ans != float('inf') else -1