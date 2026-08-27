import sys

MOD = 998244353

def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    N = int(data[idx]); idx += 1
    Q = int(data[idx]); idx += 1
    A = [0] * (N + 1)
    for i in range(2, N + 1):
        A[i] = int(data[idx]) % MOD
        idx += 1

    # modular inverses up to N+1
    inv = [0] * (N + 2)
    inv[1] = 1
    for i in range(2, N + 2):
        inv[i] = MOD - MOD // i * inv[MOD % i] % MOD

    # total number of parent sequences = (N-1)!
    total = 1
    for i in range(2, N):
        total = total * i % MOD

    # For query (u, v), u < v, the probability that edge i (i, P_i) lies on the
    # u-v path (i.e. exactly one of u, v is in subtree of i) is:
    #   2 <= i <= u-1 : 2(i-1) / (i(i+1))
    #   i = u (u>=2)  : (u-1) / u
    #   u < i < v     : 1 / i
    #   i = v         : 1
    #   i > v         : 0
    # Answer = (N-1)! * sum_i A_i * prob_i.
    #
    # Prefix sums:
    #   S1[k] = sum_{i=2}^k A_i * 2(i-1) * inv[i] * inv[i+1]
    #   S2[k] = sum_{i=2}^k A_i * inv[i]
    S1 = [0] * (N + 1)
    S2 = [0] * (N + 1)
    for i in range(2, N + 1):
        c1 = 2 * (i - 1) % MOD * inv[i] % MOD * inv[i + 1] % MOD
        S1[i] = (S1[i - 1] + A[i] * c1) % MOD
        S2[i] = (S2[i - 1] + A[i] * inv[i]) % MOD

    out = []
    for _ in range(Q):
        u = int(data[idx]); idx += 1
        v = int(data[idx]); idx += 1
        if u > v:
            u, v = v, u
        # range [2, u-1] with coefficient 2(i-1)/(i(i+1))
        res = S1[u - 1]
        # i = u (only if u >= 2): coefficient (u-1)/u
        if u >= 2:
            res = (res + A[u] * (u - 1) % MOD * inv[u]) % MOD
        # range [u+1, v-1] with coefficient 1/i
        res = (res + S2[v - 1] - S2[u]) % MOD
        # i = v: coefficient 1
        res = (res + A[v]) % MOD
        res = res * total % MOD
        out.append(str(res))

    sys.stdout.write("\n".join(out) + "\n")

main()