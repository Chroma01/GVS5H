import sys

def main():
    data = sys.stdin.buffer.read().split()
    MOD = 998244353
    pos = 0
    N = int(data[pos]); pos += 1
    Q = int(data[pos]); pos += 1

    A = [0] * (N + 2)
    for i in range(2, N + 1):
        A[i] = int(data[pos]) % MOD
        pos += 1

    # modular inverses for 1..N+1
    LIM = N + 1
    inv = [0] * (LIM + 1)
    inv[1] = 1
    for i in range(2, LIM + 1):
        inv[i] = (MOD - (MOD // i) * inv[MOD % i] % MOD) % MOD

    # pref1[i] = sum_{j=2..i} A_j / j
    # pref2[i] = sum_{j=2..i} A_j * 2(j-1)/(j(j+1))
    pref1 = [0] * (N + 2)
    pref2 = [0] * (N + 2)
    for i in range(2, N + 1):
        pref1[i] = (pref1[i - 1] + A[i] * inv[i]) % MOD
        pref2[i] = (pref2[i - 1]
                    + A[i] * (2 * (i - 1) % MOD) % MOD * inv[i] % MOD * inv[i + 1]) % MOD

    # number of parent sequences = (N-1)!
    F = 1
    for i in range(2, N):
        F = F * i % MOD

    out = []
    for _ in range(Q):
        u = int(data[pos]); pos += 1
        v = int(data[pos]); pos += 1
        if u == 1:
            # sum_{i=2..v-1} A_i/i + A_v
            E = (pref1[v - 1] + A[v]) % MOD
        else:
            # i<u: 2(i-1)/(i(i+1)) ; i=u: (u-1)/u ; u<i<v: 1/i ; i=v: 1
            E = (pref2[u - 1]
                 + A[u] * ((u - 1) % MOD) % MOD * inv[u]
                 + pref1[v - 1] - pref1[u]
                 + A[v]) % MOD
        out.append(str(E * F % MOD))

    sys.stdout.write("\n".join(out) + "\n")

main()