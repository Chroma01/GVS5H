import bisect

class Solution:
    def shortestMatchingSubstring(self, s: str, p: str) -> int:
        parts = p.split('*')
        p1, p2, p3 = parts[0], parts[1], parts[2]
        L1, L2, L3 = len(p1), len(p2), len(p3)
        
        def find_all(sub):
            if not sub:
                return []
            res = []
            start = 0
            while True:
                idx = s.find(sub, start)
                if idx == -1:
                    break
                res.append(idx)
                start = idx + 1
            return res

        A = find_all(p1)
        B = find_all(p2)
        C = find_all(p3)
        
        min_len = float('inf')
        found = False
        
        if L2 > 0:
            for j in B:
                if L1 == 0:
                    i = j
                else:
                    idx_i = bisect.bisect_right(A, j - L1) - 1
                    if idx_i < 0:
                        continue
                    i = A[idx_i]
                
                if L3 == 0:
                    k = j + L2
                else:
                    idx_k = bisect.bisect_left(C, j + L2)
                    if idx_k >= len(C):
                        continue
                    k = C[idx_k]
                
                length = k + L3 - i
                if length < min_len:
                    min_len = length
                    found = True
        else:
            if L3 > 0:
                for k in C:
                    if L1 == 0:
                        i = k
                    else:
                        idx_i = bisect.bisect_right(A, k - L1) - 1
                        if idx_i < 0:
                            continue
                        i = A[idx_i]
                    length = k + L3 - i
                    if length < min_len:
                        min_len = length
                        found = True
            else:
                if L1 == 0:
                    min_len = 0
                    found = True
                else:
                    if A:
                        min_len = 0
                        found = True
                    else:
                        return -1
                        
        return min_len if found else -1