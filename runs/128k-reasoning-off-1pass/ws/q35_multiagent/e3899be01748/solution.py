class Solution:
    def countSubstrings(self, s: str) -> int:
        n = len(s)
        ans = 0
        
        # d = 1, 2, 5: All substrings ending in d are divisible by d
        for d in [1, 2, 5]:
            for j in range(n):
                if int(s[j]) == d:
                    ans += j + 1
                    
        # d = 4: Divisible by 4 iff last two digits form a number divisible by 4
        for j in range(n):
            if int(s[j]) == 4:
                if j == 0:
                    ans += 1
                else:
                    val = int(s[j-1:j+1])
                    if val % 4 == 0:
                        ans += j + 1
                    else:
                        ans += 1
                        
        # d = 8: Divisible by 8 iff last three digits form a number divisible by 8
        for j in range(n):
            if int(s[j]) == 8:
                if j == 0:
                    ans += 1
                elif j == 1:
                    val = int(s[0:2])
                    if val % 8 == 0:
                        ans += 2
                    else:
                        ans += 1
                else:
                    val = int(s[j-2:j+1])
                    if val % 8 == 0:
                        ans += j + 1
                    else:
                        ans += 1
                        
        # d = 3, 6, 9: Divisible by d iff sum of digits is divisible by d
        # For d=6, since it ends in 6, it's always even, so just check sum % 3 == 0
        for d in [3, 6, 9]:
            freq = [0] * d
            # prefix_sum[0] = 0
            freq[0] = 1
            current_sum = 0
            for j in range(n):
                current_sum += int(s[j])
                rem = current_sum % d
                if int(s[j]) == d:
                    # We need prefix_sum[i] % d == current_sum % d for i from 0 to j
                    ans += freq[rem]
                # Update freq for next iteration
                freq[rem] += 1
                
        # d = 7: Use frequency array with modular inverse
        # Precompute modular inverse of 10^k mod 7 for k=0..5
        # 10^0=1, 10^1=3, 10^2=2, 10^3=6, 10^4=4, 10^5=5
        # Inverses: inv(1)=1, inv(3)=5, inv(2)=4, inv(6)=6, inv(4)=2, inv(5)=3
        inv_pow = [1, 5, 4, 6, 2, 3]
        
        freq7 = [[0]*6 for _ in range(7)] # freq7[rem][index%6]
        # Initialize with prefix_sum[0] = 0 at index 0
        freq7[0][0] = 1
        
        current_rem = 0
        for j in range(n):
            digit = int(s[j])
            current_rem = (current_rem * 10 + digit) % 7
            idx = j + 1 # This is the index in the prefix array for the current position
            idx_mod = idx % 6
            
            if digit == 7:
                # We need to count i (0 <= i <= j) such that
                # P[i] * 10^(j-i+1) == P[j+1] (mod 7)
                # P[i] == P[j+1] * inv(10^(j-i+1)) (mod 7)
                # Let L = j-i+1. Then i = j+1-L.
                # i % 6 = (j+1-L) % 6 = (idx - L) % 6.
                # For a bucket `b = i % 6`, we have L % 6 = (idx - b) % 6.
                # Required P[i] = current_rem * inv_pow[(idx - b) % 6] % 7.
                
                for b in range(6):
                    req_rem = (current_rem * inv_pow[(idx - b) % 6]) % 7
                    ans += freq7[req_rem][b]
            
            # Update frequency array
            freq7[current_rem][idx_mod] += 1
            
        return ans