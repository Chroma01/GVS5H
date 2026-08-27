import sys

def main():
    MOD = 998244353
    data = sys.stdin.buffer.read().split()
    pos = 0
    N = int(data[pos]); pos += 1
    Q = int(data[pos]); pos += 1
    A = [0] * (N + 1)  # 1-indexed; A[i] for i in 2..N
    for i in range(2, N + 1):
        A[i] = int(data[pos]) % MOD
        pos += 1

    # Modular inverses of 1..N+1
    inv = [0] * (N + 2)
    inv[1] = 1
    for i in range(2, N + 2):
        inv[i] = MOD - (MOD // i) * inv[MOD % i] % MOD

    # P1[t] = sum_{i=2}^{t} A_i * inv(i+1)
    # P2[t] = sum_{i=2}^{t} A_i * inv(i+1)^2
    P1 = [0] * (N + 1)
    P2 = [0] * (N + 1)
    for i in range(2, N + 1):
        w = A[i] * inv[i + 1] % MOD
        P1[i] = (P1[i - 1] + w) % MOD
        P2[i] = (P2[i - 1] + w * inv[i + 1]) % MOD

    # (N-1)!
    fact = 1
    for i in range(2, N):
        fact = fact * i % MOD

    out = []
    for _ in range(Q):
        u = int(data[pos]); pos += 1
        v = int(data[pos]); pos += 1
        # inner = sum over edges i of A_i * Pr[edge i on u-v path]
        # Case split on i relative to u < v:
        #   i = v:            f(i,v)=1, u not in subtree -> contribution A_v
        #   u < i < v:        only v can be in subtree(i) -> A_i * v/((i+1)(v-1))
        #   i = u (u >= 2):   f(u,u)=1, f(u,v)=v/((u+1)(v-1))
        #                     -> A_u * (1 - f(u,v))
        #   2 <= i < u:       A_i * (f(i,u) + f(i,v) - 2 f(i,u) f(i,v))
        #                     with f(i,x) = x/((i+1)(x-1))
        inner = A[v]
        if v - 1 >= u + 1:
            inner = (inner + v % MOD * inv[v - 1] % MOD *
                     ((P1[v - 1] - P1[u]) % MOD)) % MOD
        if u >= 2:
            fuv = v % MOD * inv[u + 1] % MOD * inv[v - 1] % MOD
            inner = (inner + A[u] * (1 - fuv)) % MOD
            cu = u % MOD * inv[u - 1] % MOD
            cv = v % MOD * inv[v - 1] % MOD
            inner = (inner + (cu + cv) % MOD * P1[u - 1]) % MOD
            inner = (inner - 2 * cu % MOD * cv % MOD * P2[u - 1]) % MOD
        out.append(str(fact * (inner % MOD) % MOD))
    sys.stdout.write("\n".join(out) + "\n")

main()