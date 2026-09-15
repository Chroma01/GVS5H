import sys

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    N = int(data[0])
    P = int(data[1])
    half = N // 2
    Kmax = N * (N - 1) // 2

    # factorials up to N
    fact = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = fact[i-1] * i % P
    invfact = [1] * (N + 1)
    invfact[N] = pow(fact[N], P - 2, P)
    for i in range(N, 0, -1):
        invfact[i-1] = invfact[i] * i % P

    # binomial coefficients up to N
    C = [[0] * (N + 1) for _ in range(N + 1)]
    for i in range(N + 1):
        C[i][0] = C[i][i] = 1
        for j in range(1, i):
            C[i][j] = (C[i-1][j-1] + C[i-1][j]) % P

    # transition list for (previous layer size a, new layer size b)
    # factor: (z^a - 1)^b * z^{C(b,2)} * (1/b!)  where z = 1+x
    trans = [[None] * (half + 1) for _ in range(half + 1)]
    for a in range(1, half + 1):
        for b in range(1, half + 1):
            lst = []
            invfb = invfact[b]
            cb2 = b * (b - 1) // 2
            for j in range(b + 1):
                delta = a * j + cb2
                coef = C[b][j] * invfb % P
                if (b - j) & 1:
                    coef = (-coef) % P
                if coef:
                    lst.append((delta, coef))
            trans[a][b] = lst

    # max polynomial length for a given number of used vertices
    lims = [0] * (N + 1)
    for used in range(N + 1):
        lims[used] = used * (used - 1) // 2 + 1

    # DP over layers
    # state: (even_used, odd_used, last_layer_size) -> polynomial in z
    cur = {(1, 0, 1): [1]}
    parity = 0  # 0 even, 1 odd
    final = [0] * (Kmax + 1)

    while cur:
        nxt = {}
        next_parity = 1 - parity
        for (e, o, last), src in cur.items():
            nz = [(k, v) for k, v in enumerate(src) if v]
            if not nz:
                continue
            if parity == 0:
                maxb = half - o
                if maxb <= 0:
                    continue
                for b in range(1, maxb + 1):
                    new_e = e
                    new_o = o + b
                    used_new = new_e + new_o
                    lst = trans[last][b]
                    if new_e == half and new_o == half:
                        dest = final
                    else:
                        key = (new_e, new_o, b)
                        dest = nxt.get(key)
                        if dest is None:
                            dest = [0] * lims[used_new]
                            nxt[key] = dest
                    for k, v in nz:
                        for delta, coef in lst:
                            dest[k + delta] += v * coef
            else:
                maxb = half - e
                if maxb <= 0:
                    continue
                for b in range(1, maxb + 1):
                    new_e = e + b
                    new_o = o
                    used_new = new_e + new_o
                    lst = trans[last][b]
                    if new_e == half and new_o == half:
                        dest = final
                    else:
                        key = (new_e, new_o, b)
                        dest = nxt.get(key)
                        if dest is None:
                            dest = [0] * lims[used_new]
                            nxt[key] = dest
                    for k, v in nz:
                        for delta, coef in lst:
                            dest[k + delta] += v * coef
        for key, arr in nxt.items():
            nxt[key] = [x % P for x in arr]
        cur = nxt
        parity = next_parity

    final = [x % P for x in final]
    mul = fact[N-1]
    for i in range(Kmax + 1):
        final[i] = final[i] * mul % P

    # binomial coefficients up to Kmax
    factK = [1] * (Kmax + 1)
    for i in range(1, Kmax + 1):
        factK[i] = factK[i-1] * i % P
    invfactK = [1] * (Kmax + 1)
    invfactK[Kmax] = pow(factK[Kmax], P - 2, P)
    for i in range(Kmax, 0, -1):
        invfactK[i-1] = invfactK[i] * i % P

    ans = []
    for M in range(N - 1, Kmax + 1):
        s = 0
        for K in range(M, Kmax + 1):
            fk = final[K]
            if fk:
                comb = factK[K] * invfactK[M] % P * invfactK[K - M] % P
                s += fk * comb
        ans.append(str(s % P))
    print(' '.join(ans))

if __name__ == "__main__":
    main()