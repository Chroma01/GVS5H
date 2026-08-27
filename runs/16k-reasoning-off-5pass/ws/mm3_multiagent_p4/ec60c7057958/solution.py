from typing import List

class Solution:
    def permute(self, n: int, k: int) -> List[int]:
        if n <= 0:
            return []
        
        # Cap to avoid huge numbers; k <= 1e15
        INF = 10**16
        
        # Precompute DP: dp[o][e][0] = ways with o odds, e evens, next need even
        #                dp[o][e][1] = ways with o odds, e evens, next need odd
        dp = [[[0]*2 for _ in range(n+1)] for _ in range(n+1)]
        for o in range(n+1):
            for e in range(n+1):
                # Base case: no numbers left
                if o == 0 and e == 0:
                    dp[o][e][0] = 1
                    dp[o][e][1] = 1
                else:
                    # need even (needOdd=False -> index 0)
                    if e == 0:
                        dp[o][e][0] = 0
                    else:
                        val = e * dp[o][e-1][1]
                        dp[o][e][0] = min(val, INF)
                    
                    # need odd (needOdd=True -> index 1)
                    if o == 0:
                        dp[o][e][1] = 0
                    else:
                        val = o * dp[o-1][e][0]
                        dp[o][e][1] = min(val, INF)
        
        # Remaining numbers
        odds = [i for i in range(1, n+1) if i % 2 == 1]
        evens = [i for i in range(1, n+1) if i % 2 == 0]
        
        result = []
        rem_o = len(odds)
        rem_e = len(evens)
        
        for pos in range(n):
            # Determine candidates in lexicographic order
            if pos == 0:
                # First position: try all remaining numbers in sorted order
                candidates = []
                i, j = 0, 0
                while i < rem_o and j < rem_e:
                    if odds[i] < evens[j]:
                        candidates.append(odds[i]); i += 1
                    else:
                        candidates.append(evens[j]); j += 1
                while i < rem_o:
                    candidates.append(odds[i]); i += 1
                while j < rem_e:
                    candidates.append(evens[j]); j += 1
            else:
                # Subsequent positions: must match required parity
                if len(result) > 0:
                    last = result[-1]
                    if last % 2 == 1:  # last was odd, need even
                        candidates = evens[:rem_e]
                    else:  # last was even, need odd
                        candidates = odds[:rem_o]
                else:
                    candidates = []
            
            if not candidates:
                return []
            
            found = False
            for x in candidates:
                if x % 2 == 1:  # odd
                    new_o = rem_o - 1
                    new_e = rem_e
                    next_need_odd = False  # next must be even
                    count = dp[new_o][new_e][0]  # need even
                else:  # even
                    new_o = rem_o
                    new_e = rem_e - 1
                    next_need_odd = True  # next must be odd
                    count = dp[new_o][new_e][1]  # need odd
                
                if k > count:
                    k -= count
                else:
                    # Choose x
                    result.append(x)
                    if x % 2 == 1:
                        # Remove from odds
                        odds = [y for y in odds if y != x]
                        rem_o -= 1
                    else:
                        evens = [y for y in evens if y != x]
                        rem_e -= 1
                    found = True
                    break
            
            if not found:
                return []
        
        return result