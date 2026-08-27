import sys

MOD = 998244353

def main():
    import sys
    input_data = sys.stdin.read().split()
    it = iter(input_data)
    N = int(next(it))
    Q = int(next(it))
    A = [0] * (N + 1)  # 1-indexed, A[1] unused
    for i in range(2, N + 1):
        A[i] = int(next(it))
    
    # Precompute factorials
    fact = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = fact[i - 1] * i % MOD
    
    # Precompute modular inverses of 1..N-1
    inv = [0] * (N + 1)
    # inv[1] = 1
    inv[1] = 1
    for i in range(2, N + 1):
        inv[i] = MOD - MOD // i * inv[MOD % i] % MOD
    
    # Prefix sums of B_i = A_i * inv(i-1) for i >= 2
    prefix = [0] * (N + 1)
    for i in range(2, N + 1):
        val = A[i] * inv[i - 1] % MOD
        prefix[i] = (prefix[i - 1] + val) % MOD
    
    fact_n_minus_1 = fact[N - 1]
    
    out_lines = []
    for _ in range(Q):
        u = int(next(it))
        v = int(next(it))
        l = min(u, v)
        r = max(u, v)
        # Sum from l to r of B_i, but B_1 = 0 so prefix[l-1] works correctly
        s = (prefix[r] - prefix[l - 1]) % MOD
        ans = s * fact_n_minus_1 % MOD
        out_lines.append(str(ans))
    
    sys.stdout.write('\n'.join(out_lines))

if __name__ == "__main__":
    main()