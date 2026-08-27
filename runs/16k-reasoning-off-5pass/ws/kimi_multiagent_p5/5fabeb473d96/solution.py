import sys

MOD = 998244353

def solve():
    data = sys.stdin.buffer.read().split()
    pos = 0
    N = int(data[pos]); pos += 1
    Q = int(data[pos]); pos += 1
    A = [0] * (N + 1)
    for i in range(2, N + 1):
        A[i] = int(data[pos]) % MOD; pos += 1

    # modular inverses up to N+1, O(N) linear recurrence
    inv = [0] * (N + 2)
    inv[1] = 1
    for i in range(2, N + 2):
        inv[i] = MOD - (MOD // i) * inv[MOD % i] % MOD

    # S1[i] = sum_{k=2..i} A_k * 2(k-1)/(k(k+1))
    # S2[i] = sum_{k=2..i} A_k / k
    S1 = [0] * (N + 1)
    S2 = [0] * (N + 1)
    for k in range(2, N + 1):
        c1 = 2 * (k - 1) % MOD * inv[k] % MOD * inv[k + 1] % MOD
        S1[k] = (S1[k - 1] + A[k] * c1) % MOD
        S2[k] = (S2[k - 1] + A[k] * inv[k]) % MOD

    fact = 1
    for i in range(2, N):
        fact = fact * i % MOD  # (N-1)!

    out = []
    for _ in range(Q):
        u = int(data[pos]); pos += 1
        v = int(data[pos + 1]); pos += 2
        if u > v:
            u, v = v, u
        s = S1[u - 1] if u >= 2 else 0
        if u >= 2:
            s = (s + A[u] * (u - 1) % MOD * inv[u]) % MOD
        lo = u + 1 if u >= 2 else 2
        if v - 1 >= lo:
            s = (s + S2[v - 1] - S2[lo - 1]) % MOD
        s = (s + A[v]) % MOD
        out.append(str(s * fact % MOD))
    sys.stdout.write("\n".join(out) + "\n")

solve()