import sys
import math
from collections import defaultdict

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    it = iter(input_data)
    N = int(next(it))
    A = [int(next(it)) for _ in range(N)]
    
    if N == 0:
        print(0)
        return
    
    total_sum = sum(A)
    S0 = (N + 1) * total_sum
    answer = S0
    
    max_val = max(A)
    # We need k such that 2^k <= 2*max_val, since max sum is 2*max_val.
    # Actually S_k becomes 0 when 2^k > 2*max_val.
    if max_val > 0:
        max_k = int(math.log2(2 * max_val)) + 1
    else:
        max_k = 0
    
    for k in range(1, max_k + 1):
        M = 1 << k
        groups = {}
        for a in A:
            r = a % M
            q = a // M
            if r in groups:
                groups[r][0] += 1
                groups[r][1] += q
            else:
                groups[r] = [1, q]
        
        Sk = 0
        half_M = M // 2
        
        # Self-pairs for r=0 and r=M/2 (where 2r ≡ 0 mod M)
        for r_special in [0, half_M]:
            if r_special in groups:
                cnt, sumq = groups[r_special]
                # Sum of (q_i + q_j + 1) over i<=j in this group:
                # = (cnt+1)*sumq + cnt*(cnt+1)/2
                # Multiplied by M
                Sk += M * ((cnt + 1) * sumq + cnt * (cnt + 1) // 2)
        
        # Cross-pairs: r + s = M, r < s, r not 0 or M/2
        for r in groups:
            if r == 0 or r == half_M:
                continue
            s = (M - r) % M
            if r < s and s in groups:
                cnt_r, sumq_r = groups[r]
                cnt_s, sumq_s = groups[s]
                Sk += M * (cnt_s * sumq_r + cnt_r * sumq_s + cnt_r * cnt_s)
        
        # Sk is divisible by M = 2^k
        answer -= Sk // M
    
    print(answer)

if __name__ == "__main__":
    solve()