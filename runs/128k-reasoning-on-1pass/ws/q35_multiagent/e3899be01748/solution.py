class Solution:
    def countSubstrings(self, s: str) -> int:
        n = len(s)
        # Precompute solutions[d][exp][target] -> list of r such that (r * 10^exp) % d == target
        # We use period 6 for all d <= 9 as 10^k mod d is periodic with period <= 6
        solutions = [[[[] for _ in range(9)] for _ in range(6)] for _ in range(10)]
        
        for d in range(1, 10):
            for exp in range(6):
                mul = pow(10, exp, d)
                for target in range(d):
                    for r in range(d):
                        if (r * mul) % d == target:
                            solutions[d][exp][target].append(r)
                            
        # cnt[d][rem][offset] stores count of indices i such that P[i] % d == rem and i % 6 == offset
        cnt = [[[0]*6 for _ in range(9)] for _ in range(10)]
        # Initialize with P[0] = 0 at index 0
        for d in range(1, 10):
            cnt[d][0][0] = 1
            
        prefix_rem = [0]*10
        ans = 0
        
        for j in range(n):
            digit = int(s[j])
            # Update prefix remainders for all d
            for d in range(1, 10):
                prefix_rem[d] = (prefix_rem[d] * 10 + digit) % d
                
            # If the last digit is non-zero, check divisibility
            if digit != 0:
                d = digit
                k = (j + 1) % 6
                for offset in range(6):
                    exp = (k - offset) % 6
                    target = prefix_rem[d]
                    # Add counts of valid starting positions
                    for r in solutions[d][exp][target]:
                        ans += cnt[d][r][offset]
                        
            # Update counts for the current position j+1
            for d in range(1, 10):
                cnt[d][prefix_rem[d]][(j + 1) % 6] += 1
                
        return ans