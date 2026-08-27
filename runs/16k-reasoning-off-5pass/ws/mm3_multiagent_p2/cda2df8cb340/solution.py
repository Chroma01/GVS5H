import sys
from collections import defaultdict

def main():
    input = sys.stdin.readline
    N = int(input())
    A = list(map(int, input().split()))
    sum_A = sum(A)
    # T_0: sum of A_i+A_j over all i<=j
    T0 = (N + 1) * sum_A
    
    # Precompute v2 (number of trailing zeros) for each A_i
    max_val = max(A)
    max_v = 0
    v2_list = []
    for x in A:
        v = (x & -x).bit_length() - 1  # number of trailing zeros
        # alternative: v = (x & -x).bit_length() - 1 works for x>0
        v2_list.append(v)
        if v > max_v:
            max_v = v
    
    # cnt[v] and sumv[v] for each v
    cnt = [0] * (max_v + 2)
    sumv = [0] * (max_v + 2)
    for x, v in zip(A, v2_list):
        cnt[v] += 1
        sumv[v] += x
    
    # suffix sum of sumv: suffix[v] = sum_{k>=v} sumv[k]
    suffix = [0] * (max_v + 3)
    for v in range(max_v, -1, -1):
        suffix[v] = suffix[v+1] + sumv[v]
    
    # Determine t_max: largest t such that 2^t <= 2*max_val
    t_max = 0
    while (1 << (t_max + 1)) <= 2 * max_val:
        t_max += 1
    
    ans = T0
    for t in range(1, t_max + 1):
        M = 1 << t
        # Diagonal part: 2 * sum_{i: 2^{t-1} | A_i} A_i
        # This is 2 * sum of A_i with v2(A_i) >= t-1
        if t - 1 <= max_v:
            diag = 2 * suffix[t-1]
        else:
            diag = 0
        
        # Off-diagonal part: i<j, A_i + A_j ≡ 0 mod M
        # Build dict: residue -> [count, sum]
        res_dict = defaultdict(lambda: [0, 0])
        for x in A:
            r = x % M
            res_dict[r][0] += 1
            res_dict[r][1] += x
        
        off = 0
        # To avoid double counting, process each unordered pair once
        for r, (c, s) in res_dict.items():
            r2 = (M - r) % M
            if r2 not in res_dict:
                continue
            if r < r2:
                c2, s2 = res_dict[r2]
                off += s * c2 + c * s2
            elif r == r2:
                off += (c - 1) * s
            # else: r > r2, skip
        
        T_t = diag + off
        ans -= T_t >> t
    
    print(ans)

if __name__ == "__main__":
    main()