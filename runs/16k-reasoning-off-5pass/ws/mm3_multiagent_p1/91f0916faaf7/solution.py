import sys

MOD = 998244353

def solve():
    input = sys.stdin.readline
    N = int(input().strip())
    A = list(map(int, input().split()))
    
    # Enumerate all primes appearing in A_i
    primes = set()
    for x in A:
        v = 2
        while v * v <= x:
            while x % v == 0:
                primes.add(v)
                x //= v
            v += 1
        if x > 1:
            primes.add(x)
    
    if not primes:
        # All A_i = 1, only sequence is (1,...,1), score=1
        print(1)
        return
    
    answer = 1
    for p in sorted(primes):
        # Extract exponents a_i = v_p(A_i)
        a = []
        for x in A:
            cnt = 0
            while x % p == 0:
                cnt += 1
                x //= p
            a.append(cnt)
        S = sum(a)
        if S == 0:
            continue
        
        # DP for A: walks z_0..z_{N-1} >= 0, weight p^{sum z_i}
        # dpA[x] = weighted sum ending at x
        dpA = [0] * (S + 1)
        for x in range(S + 1):
            dpA[x] = pow(p, x, MOD)
        
        for k in range(1, N):
            ai = a[k-1]
            new_dp = [0] * (S + 1)
            for x in range(S + 1):
                val = 0
                if x - ai >= 0:
                    val += dpA[x - ai]
                if x + ai <= S:
                    val += dpA[x + ai]
                new_dp[x] = val * pow(p, x, MOD) % MOD
            dpA = new_dp
        
        A_sum = sum(dpA) % MOD
        
        # DP for B: walks z_0..z_{N-1} >= 1
        dpB = [0] * (S + 1)
        for x in range(1, S + 1):
            dpB[x] = pow(p, x, MOD)
        
        for k in range(1, N):
            ai = a[k-1]
            new_dp = [0] * (S + 1)
            for x in range(1, S + 1):
                val = 0
                if x - ai >= 1:
                    val += dpB[x - ai]
                if x + ai <= S:
                    val += dpB[x + ai]
                new_dp[x] = val * pow(p, x, MOD) % MOD
            dpB = new_dp
        
        B_sum = sum(dpB[1:]) % MOD
        
        Fp = (A_sum - B_sum) % MOD
        answer = answer * Fp % MOD
    
    print(answer)

solve()