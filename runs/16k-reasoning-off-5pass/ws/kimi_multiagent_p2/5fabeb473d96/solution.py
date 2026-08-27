import sys

def main():
    MOD = 998244353
    data = sys.stdin.buffer.read().split()
    idx = 0
    N = int(data[idx]); idx += 1
    Q = int(data[idx]); idx += 1
    # A[1] = 0 dummy; A[2..N] given
    A = [0] * (N + 1)
    for i in range(2, N + 1):
        A[i] = int(data[idx]) % MOD
        idx += 1

    # modular inverses of 1..N
    inv = [0] * (N + 1)
    inv[1] = 1
    for i in range(2, N + 1):
        inv[i] = MOD - (MOD // i) * inv[MOD % i] % MOD

    # (N-1)!
    fact = 1
    for i in range(2, N):
        fact = fact * i % MOD

    # S(t) = sum_{x=2}^{t} A_x * inv(x)  (mod MOD)
    S = [0] * (N + 1)
    for i in range(2, N + 1):
        S[i] = (S[i - 1] + A[i] * inv[i]) % MOD

    out = []
    for _ in range(Q):
        u = int(data[idx]); idx += 1
        v = int(data[idx]); idx += 1
        # ans/(N-1)! = 2(u-1)/u * S(u-1) + A_u*(u-1)/u + (S(v-1) - S(u)) + A_v
        um1 = u - 1
        res = (2 * um1 % MOD) * inv[u] % MOD * S[u - 1] % MOD
        res = (res + A[u] * um1 % MOD * inv[u]) % MOD
        res = (res + S[v - 1] - S[u]) % MOD
        res = (res + A[v]) % MOD
        res = res * fact % MOD
        out.append(str(res))

    sys.stdout.write("\n".join(out) + "\n")

main()