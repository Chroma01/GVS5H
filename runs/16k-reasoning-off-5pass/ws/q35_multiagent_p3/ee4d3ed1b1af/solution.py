import bisect

class Solution:
    def shortestMatchingSubstring(self, s: str, p: str) -> int:
        # Split pattern into A, B, C
        first_star = p.find('*')
        second_star = p.find('*', first_star + 1)
        
        A = p[:first_star]
        B = p[first_star+1:second_star]
        C = p[second_star+1:]
        
        lenA, lenB, lenC = len(A), len(B), len(C)
        
        # Helper to find all start indices of a pattern in s
        def find_all_starts(pattern, text):
            if not pattern:
                return []
            starts = []
            start = 0
            while True:
                idx = text.find(pattern, start)
                if idx == -1:
                    break
                starts.append(idx)
                start = idx + 1
            return starts
        
        starts_A = find_all_starts(A, s)
        starts_B = find_all_starts(B, s)
        starts_C = find_all_starts(C, s)
        
        min_len = float('inf')
        
        if lenB > 0:
            # Precompute ends_A for binary search
            ends_A = [start + lenA for start in starts_A]
            
            for start_B in starts_B:
                # Find best A: largest end_A <= start_B
                if lenA > 0:
                    # bisect_right returns insertion point after all elements <= start_B
                    idx = bisect.bisect_right(ends_A, start_B)
                    if idx == 0:
                        continue  # no valid A
                    end_A_exclusive = ends_A[idx - 1]
                    start_A = end_A_exclusive - lenA
                else:
                    # A is empty, so effective start_A is start_B
                    start_A = start_B
                
                # Find best C: smallest start_C >= start_B + lenB
                if lenC > 0:
                    idx = bisect.bisect_left(starts_C, start_B + lenB)
                    if idx == len(starts_C):
                        continue  # no valid C
                    start_C = starts_C[idx]
                else:
                    # C is empty, so effective start_C is start_B + lenB
                    start_C = start_B + lenB
                
                current_len = start_C + lenC - start_A
                if current_len < min_len:
                    min_len = current_len
        else:
            # B is empty
            if lenA == 0 and lenC == 0:
                return 0
            elif lenA == 0:
                # Pattern is * C
                for start_C in starts_C:
                    current_len = start_C + lenC
                    if current_len < min_len:
                        min_len = current_len
            elif lenC == 0:
                # Pattern is A *
                if starts_A:
                    min_len = lenA  # shortest is A itself
            else:
                # Pattern is A * C, both non-empty
                ends_A = [start + lenA for start in starts_A]
                for start_C in starts_C:
                    # Find largest end_A <= start_C
                    idx = bisect.bisect_right(ends_A, start_C)
                    if idx == 0:
                        continue
                    end_A_exclusive = ends_A[idx - 1]
                    start_A = end_A_exclusive - lenA
                    current_len = start_C + lenC - start_A
                    if current_len < min_len:
                        min_len = current_len
        
        return min_len if min_len != float('inf') else -1