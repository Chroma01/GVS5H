import sys
import threading

def main():
    MOD = 998244353
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    it = iter(input_data)
    N = int(next(it))
    A = [int(next(it)) for _ in range(N-1)]

    # Precompute smallest prime factor up to 1000
    MAX_A = 1000
    spf = list(range(MAX_A + 1))
    for i in range(2, int(MAX_A**0.5) + 1):
        if spf[i] == i:
            for j in range(i*i, MAX_A+1, i):
                if spf[j] == j:
                    spf[j] = i

    primes_used = set()
    exps = {}  # prime -> list of length N-1

    for idx, a in enumerate(A):
        x = a
        while x > 1:
            p = spf[x]
            cnt = 0
            while x % p == 0:
                x //= p
                cnt += 1
            primes_used.add(p)
            if p not in exps:
                exps[p] = [0] * (N-1)
            exps[p][idx] += cnt

    answer = 1
    for p in primes_used:
        e_list = exps[p]
        M = sum(e_list)
        if M == 0:
            continue
        # Precompute powers of p
        p_pow = [1] * (M+1)
        for i in range(1, M+1):
            p_pow[i] = p_pow[i-1] * p % MOD
        # dp0: no zero seen yet, dp1: at least one zero seen
        # Initialize for the first element S_1
        dp0 = [0] * (M+1)
        dp1 = [0] * (M+1)
        # For x=0, we have a zero immediately, so dp1[0] = p^0 = 1
        dp1[0] = 1
        # For x>0, no zero yet, so dp0[x] = p^x
        for x in range(1, M+1):
            dp0[x] = p_pow[x]

        # Process the N-1 transitions
        for e in e_list:
            newdp0 = [0] * (M+1)
            newdp1 = [0] * (M+1)
            if e == 0:
                # Transition is deterministic: y = x
                for y in range(M+1):
                    # From dp0[x] to newdp? at y=x
                    # Since y=x, the flag remains the same
                    if y == 0:
                        newdp1[y] = (newdp1[y] + dp0[y] * p_pow[y]) % MOD
                    else:
                        newdp0[y] = (newdp0[y] + dp0[y] * p_pow[y]) % MOD
                    # From dp1[x] to newdp? at y=x
                    if y == 0:
                        newdp1[y] = (newdp1[y] + dp1[y] * p_pow[y]) % MOD
                    else:
                        newdp1[y] = (newdp1[y] + dp1[y] * p_pow[y]) % MOD
            else:
                for y in range(M+1):
                    s0 = 0
                    s1 = 0
                    x = y - e
                    if x >= 0:
                        s0 = (s0 + dp0[x]) % MOD
                        s1 = (s1 + dp1[x]) % MOD
                    x = y + e
                    if x <= M:
                        s0 = (s0 + dp0[x]) % MOD
                        s1 = (s1 + dp1[x]) % MOD
                    if y == 0:
                        newdp1[y] = (s0 + s1) * p_pow[y] % MOD
                    else:
                        newdp0[y] = s0 * p_pow[y] % MOD
                        newdp1[y] = s1 * p_pow[y] % MOD
            dp0, dp1 = newdp0, newdp1

        G = sum(dp1) % MOD
        answer = answer * G % MOD
    print(answer)

threading.Thread(target=main).start()