import sys

MOD = 998244353

def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    N = int(data[idx]); idx += 1
    Q = int(data[idx]); idx += 1
    A = [0] * (N + 1)  # 1-indexed; A[1] unused
    for i in range(2, N + 1):
        A[i] = int(data[idx]); idx += 1
    
    # Compute modular inverse of k for k=1..N
    inv = [0] * (N + 1)
    inv[1] = 1
    for k in range(2, N + 1):
        inv[k] = MOD - MOD // k * inv[MOD % k] % MOD
    
    # Prefix sum S[t] = sum_{k=2}^{t} A_k * inv[k]
    S = [0] * (N + 1)
    for t in range(2, N + 1):
        S[t] = (S[t-1] + A[t] * inv[t]) % MOD
    
    # (N-1)! mod MOD
    fact = 1
    for i in range(2, N):
        fact = fact * i % MOD
    
    out = []
    for _ in range(Q):
        u = int(data[idx]); idx += 1
        v = int(data[idx]); idx += 1
        if u > v:
            u, v = v, u
        
        # Sum of A_k/k for k in (u, v)
        inner = (S[v-1] - S[u]) % MOD
        
        # Add A_v
        inner = (inner + A[v]) % MOD
        
        # Add A_u * (u-1)/u if u >= 2
        if u >= 2:
            inner = (inner + A[u] * (u - 1) % MOD * inv[u]) % MOD
        
        ans = fact * inner % MOD
        out.append(str(ans))
    
    sys.stdout.write('\n'.join(out))

if __name__ == "__main__":
    main()