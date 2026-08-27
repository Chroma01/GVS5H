import bisect

class Solution:
    def shortestMatchingSubstring(self, s: str, p: str) -> int:
        # Quick case: pattern is exactly "**"
        if p == "**":
            return 0
        
        # Split pattern into three parts
        parts = p.split('*')
        # Since p contains exactly two '*', we get exactly 3 parts
        p1, p2, p3 = parts[0], parts[1], parts[2]
        n = len(s)
        
        # Helper: compute prefix function for KMP
        def compute_lps(pattern):
            lps = [0] * len(pattern)
            length = 0  # length of previous longest prefix suffix
            i = 1
            while i < len(pattern):
                if pattern[i] == pattern[length]:
                    length += 1
                    lps[i] = length
                    i += 1
                else:
                    if length != 0:
                        length = lps[length - 1]
                    else:
                        lps[i] = 0
                        i += 1
            return lps
        
        # Helper: find all start indices where pattern occurs in s
        def kmp_search(text, pattern):
            if not pattern:
                return []  # empty pattern, no occurrences (handled separately)
            lps = compute_lps(pattern)
            occurrences = []
            i = 0  # index for text
            j = 0  # index for pattern
            while i < len(text):
                if pattern[j] == text[i]:
                    i += 1
                    j += 1
                if j == len(pattern):
                    occurrences.append(i - j)  # start index
                    j = lps[j - 1]
                elif i < len(text) and pattern[j] != text[i]:
                    if j != 0:
                        j = lps[j - 1]
                    else:
                        i += 1
            return occurrences
        
        # For each part, get start indices of occurrences
        # For empty parts, we treat specially later
        occ1 = kmp_search(s, p1) if p1 else []
        occ2 = kmp_search(s, p2) if p2 else []
        occ3 = kmp_search(s, p3) if p3 else []
        
        # If any non-empty part has no occurrences, impossible
        if (p1 and not occ1) or (p2 and not occ2) or (p3 and not occ3):
            return -1
        
        # Convert start indices to end indices (exclusive) for easier comparison.
        ends1 = [start + len(p1) for start in occ1] if p1 else []
        ends2 = [start + len(p2) for start in occ2] if p2 else []
        ends3 = [start + len(p3) for start in occ3] if p3 else []
        
        INF = float('inf')
        ans = INF
        
        # We need to find the minimum total length where:
        # start1 + len(p1) <= start2  (if p1 non-empty; if p1 empty, start1 <= start2)
        # start2 + len(p2) <= start3  (if p2 non-empty; if p2 empty, start2 <= start3)
        # Total length = start3 + len(p3) - start1
        # We want to minimize this.
        
        # Case handling based on which parts are non-empty:
        # We'll iterate over the rightmost non-empty part to anchor the end.
        
        if p3:
            # p3 is non-empty, so it anchors the end of the substring.
            # For each occurrence of p3:
            for start3 in occ3:
                end3 = start3 + len(p3)
                
                if p2:
                    # p2 is non-empty: need to find p2 occurrence that ends <= end3
                    # Use binary search to find the latest p2 end <= end3
                    idx2 = bisect.bisect_right(ends2, end3) - 1
                    if idx2 < 0:
                        continue
                    start2 = occ2[idx2]
                    end2 = ends2[idx2]
                    
                    if p1:
                        # p1 non-empty: need p1 end <= end2
                        idx1 = bisect.bisect_right(ends1, end2) - 1
                        if idx1 < 0:
                            continue
                        start1 = occ1[idx1]
                    else:
                        # p1 empty: start1 can be any position <= start2
                        # To minimize total length, set start1 = start2
                        start1 = start2
                else:
                    # p2 empty: we can set start2 = start3 (since start2 <= start3 is required)
                    start2 = start3
                    
                    if p1:
                        # p1 non-empty: need end1 <= start2 = start3
                        idx1 = bisect.bisect_right(ends1, start3) - 1
                        if idx1 < 0:
                            continue
                        start1 = occ1[idx1]
                    else:
                        # Both p1 and p2 empty
                        start1 = start3
                
                total_len = end3 - start1
                if total_len < ans:
                    ans = total_len
        
        else:
            # p3 is empty
            # The substring ends after p2 (or at the same position if p2 is empty)
            if p2:
                # p2 non-empty: iterate over all p2 occurrences
                for start2 in occ2:
                    end2 = start2 + len(p2)
                    # Substring ends at end2
                    
                    if p1:
                        # p1 non-empty: need end1 <= start2 (p1 must finish before p2 starts)
                        idx1 = bisect.bisect_right(ends1, start2) - 1
                        if idx1 < 0:
                            continue
                        start1 = occ1[idx1]
                    else:
                        # p1 empty: start1 can be any position <= start2
                        # To minimize, set start1 = start2
                        start1 = start2
                    
                    total_len = end2 - start1
                    if total_len < ans:
                        ans = total_len
            else:
                # p2 empty and p3 empty
                if p1:
                    # p1 non-empty: the shortest substring is just p1 itself
                    # We already verified p1 occurs in s
                    ans = len(p1)
                else:
                    # Both empty, already handled
                    ans = 0
        
        if ans == INF:
            return -1
        return ans