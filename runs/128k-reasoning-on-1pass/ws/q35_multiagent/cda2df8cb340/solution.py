import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    N = int(input_data[0])
    A = list(map(int, input_data[1:]))
    
    # Compute S_diag = sum(f(A_i))
    S_diag = 0
    for x in A:
        while x % 2 == 0:
            x //= 2
        S_diag += x
        
    S_all = 0
    # Max possible sum is 2*10^7, so v_2 can be at most 24.
    # We iterate k from 0 to 24.
    for k in range(25):
        mod = 1 << (k + 1)
        target = 1 << k
        
        cnt = {}
        s = {}
        
        for x in A:
            r = x % mod
            cnt[r] = cnt.get(r, 0) + 1
            s[r] = s.get(r, 0) + x
            
        for r in cnt:
            r_prime = (target - r) % mod
            if r_prime in cnt:
                # Sum of (A_i + A_j) for pairs where A_i % mod == r and A_j % mod == r_prime
                term = cnt[r] * s[r_prime] + cnt[r_prime] * s[r]
                S_all += term // (1 << k)
                
    ans = (S_all + S_diag) // 2
    print(ans)

if __name__ == '__main__':
    solve()