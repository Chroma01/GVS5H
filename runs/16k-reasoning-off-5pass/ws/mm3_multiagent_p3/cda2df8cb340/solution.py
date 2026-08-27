import sys

def solve():
    import sys
    input = sys.stdin.readline
    N = int(input())
    A = list(map(int, input().split()))
    
    if N == 0:
        print(0)
        return
    
    max_val = max(A)
    max_sum = 2 * max_val
    K_max = max_sum.bit_length()
    
    pow2 = [1 << i for i in range(K_max + 2)]
    
    ans = 0
    
    for k in range(K_max + 1):
        mod = pow2[k + 1]
        mask = mod - 1
        
        cnt = {}
        sm = {}
        for a in A:
            r = a & mask
            cnt[r] = cnt.get(r, 0) + 1
            sm[r] = sm.get(r, 0) + a
        
        target = pow2[k]
        T_k = 0
        for r in cnt:
            r2 = (target - r) & mask
            if r2 in cnt:
                T_k += 2 * sm[r] * cnt[r2]
        
        if k == 0:
            D_k = 2 * sum(a for a in A if a & 1)
        else:
            cond = pow2[k - 1]
            modk = pow2[k]
            D_k = 2 * sum(a for a in A if a % modk == cond)
        
        ans += (T_k + D_k) // pow2[k + 1]
    
    print(ans)

if __name__ == "__main__":
    solve()