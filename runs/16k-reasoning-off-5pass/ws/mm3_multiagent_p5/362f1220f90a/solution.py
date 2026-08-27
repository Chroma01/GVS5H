class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        n, m = len(str1), len(str2)
        N = n + m - 1
        res = [''] * N
        fixed = [False] * N
        
        # Place T's
        for i in range(n):
            if str1[i] == 'T':
                for k in range(m):
                    p = i + k
                    if fixed[p]:
                        if res[p] != str2[k]:
                            return ""
                    else:
                        res[p] = str2[k]
                        fixed[p] = True
        
        # Compute match_count for F intervals
        match_count = [0] * n
        for p in range(N):
            if fixed[p]:
                i_start = max(0, p - m + 1)
                i_end = min(p, n - 1)
                for i in range(i_start, i_end + 1):
                    if str1[i] == 'F':
                        k = p - i
                        if res[p] == str2[k]:
                            match_count[i] += 1
        
        # Check for fully matched F intervals (violation)
        for i in range(n):
            if str1[i] == 'F' and match_count[i] == m:
                return ""
        
        # Greedy fill remaining positions
        for p in range(N):
            if fixed[p]:
                continue
            i_start = max(0, p - m + 1)
            i_end = min(p, n - 1)
            found = False
            for ch in 'abcdefghijklmnopqrstuvwxyz':
                valid = True
                for i in range(i_start, i_end + 1):
                    if str1[i] == 'F':
                        k = p - i
                        if ch == str2[k] and match_count[i] == m - 1:
                            valid = False
                            break
                if valid:
                    res[p] = ch
                    fixed[p] = True
                    # Update match_count for F intervals covering p
                    for i in range(i_start, i_end + 1):
                        if str1[i] == 'F':
                            k = p - i
                            if ch == str2[k]:
                                match_count[i] += 1
                    found = True
                    break
            if not found:
                return ""
        
        return "".join(res)