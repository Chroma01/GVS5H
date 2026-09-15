import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    m = n - 1
    A = list(map(int, data[1:1 + m]))
    MOD = 998244353

    # Factor each A_i and group exponents by prime.
    # pe[p][idx] = v_p(A_idx)
    pe = {}
    for idx in range(m):
        y = A[idx]
        d = 2
        while d * d <= y:
            if y % d == 0:
                c = 0
                while y % d == 0:
                    y //= d
                    c += 1
                if d in pe:
                    pe[d][idx] = c
                else:
                    lst = [0] * m
                    lst[idx] = c
                    pe[d] = lst
            d += 1
        if y > 1:
            if y in pe:
                pe[y][idx] += 1
            else:
                lst = [0] * m
                lst[idx] = 1
                pe[y] = lst

    ans = 1
    for p, a in pe.items():
        W = 0
        for x in a:
            W += x
        if W == 0:
            continue

        pp = [1] * (W + 1)
        for h in range(1, W + 1):
            pp[h] = pp[h - 1] * p % MOD

        # ---- Left DP ----
        # cur[h] = sum over sign choices of edges 1..i-1 with all d_1..d_{i-1} >= 1,
        #          d_i = h, weight p^{d_1+...+d_{i-1}}   (position i weight excluded)
        cur = [0] * (W + 1)
        for h in range(1, W + 1):
            cur[h] = 1
        Ld = {1: 1}
        for i in range(m):
            v = a[i]
            if v == 0:
                cur = [x * y % MOD for x, y in zip(cur, pp)]
            else:
                Ld[i + 2] = pp[v] * cur[v] % MOD
                c = [x * y % MOD for x, y in zip(cur, pp)]
                term1 = [0] * v + c[1:W - v + 1]
                term2 = c[1 + v:W + 1] + [0] * v
                newcur = [(x + y) % MOD for x, y in zip(term1, term2)]
                cur = [0] + newcur

        # ---- Right DP ----
        # V[h] = sum over sign choices of edges i..N-1 with d_i = h, all later >= 0,
        #        weight p^{d_{i+1}+...+d_N}
        V = [1] * (W + 1)
        Rd = {}
        for i in range(m - 1, -1, -1):
            v = a[i]
            if v == 0:
                V = [x * y % MOD for x, y in zip(V, pp)]
            else:
                Rd[i + 2] = V[0]
                c2 = [x * y % MOD for x, y in zip(V, pp)]
                term1 = c2[v:W + 1] + [0] * v
                term2 = [0] * v + c2[0:W + 1 - v]
                V = [(x + y) % MOD for x, y in zip(term1, term2)]
        Rd[1] = V[0]

        Fp = 0
        for j, lv in Ld.items():
            Fp += lv * Rd[j]
        ans = ans * (Fp % MOD) % MOD

    print(ans % MOD)

main()