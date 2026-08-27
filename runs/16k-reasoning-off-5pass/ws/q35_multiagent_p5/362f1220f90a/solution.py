class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        n = len(str1)
        m = len(str2)
        total_len = n + m - 1
        
        # Step 1: Process 'T' constraints to determine forced characters
        forced = [None] * total_len
        for i in range(n):
            if str1[i] == 'T':
                for k in range(m):
                    idx = i + k
                    c = str2[k]
                    if forced[idx] is None:
                        forced[idx] = c
                    elif forced[idx] != c:
                        return ""  # Contradiction in 'T' constraints
        
        # Step 2: Initialize result array with forced characters
        res = [None] * total_len
        for i in range(total_len):
            if forced[i] is not None:
                res[i] = forced[i]
        
        # Step 3: Precompute 'F' constraints ending at each index
        f_constraints_ending_at = [[] for _ in range(total_len)]
        for i in range(n):
            if str1[i] == 'F':
                end_index = i + m - 1
                if end_index < total_len:
                    f_constraints_ending_at[end_index].append(i)
        
        # Step 4: Fill in the remaining positions
        for i in range(total_len):
            if res[i] is None:
                assigned = False
                for c in "abcdefghijklmnopqrstuvwxyz":
                    res[i] = c
                    valid = True
                    for j in f_constraints_ending_at[i]:
                        # Check if the substring res[j:j+m] equals str2
                        # Since m is small, we can do a direct comparison
                        if res[j:j+m] == str2:
                            valid = False
                            break
                    if valid:
                        assigned = True
                        break
                    else:
                        res[i] = None  # backtrack
                if not assigned:
                    return ""
            else:
                # Check if forced character causes any 'F' constraint to be violated
                for j in f_constraints_ending_at[i]:
                    if res[j:j+m] == str2:
                        return ""
        
        return "".join(res)