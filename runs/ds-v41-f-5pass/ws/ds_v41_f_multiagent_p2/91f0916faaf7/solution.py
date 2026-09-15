import sys

def main():
    data = sys.stdin.buffer.read().split()
    N = int(data[0])
    A = list(map(int, data[1:1 + N - 1]))
    M = 998244353

    # factor each A_i
    factors = []
    for x in A:
        f = {}
        y = x
        d = 2
        while d * d <= y:
            if y % d == 0:
                c = 0
                while y % d == 0:
                    y //= d
                    c += 1
                f[d] = c
            d += 1
        if y > 1:
            f[y] = f.get(y, 0) + 1
        factors.append(f)

    allp = set()
    for f in factors:
        allp.update(f)

    n = N - 1
    ans = 1

    for p in allp:
        a_list = [f.get(p, 0) for f in factors]
        S = sum(a_list)
        if S == 0:
            continue
        B = S + 1
        # powers p^h
        pw = [1] * B
        for h in range(1, B):
            pw[h] = pw[h - 1] * p % M

        # D[h]     = dp0[h] : not yet visited height 0
        # D[B+h]   = dp1[h] : height 0 already visited
        D = [0] * (2 * B)
        for h in range(1, B):
            D[h] = pw[h]
        D[B] = 1
        PW = pw + pw

        i = 0
        while i < n:
            a = a_list[i]
            if a == 0:
                # batch a run of consecutive zero steps: factor p^(h*L)
                j = i
                while j < n and a_list[j] == 0:
                    j += 1
                L = j - i
                q = pow(p, L, M)
                f = [1] * B
                for h in range(1, B):
                    f[h] = f[h - 1] * q % M
                F = f + f
                D = [x * y % M for x, y in zip(D, F)]
                i = j
            else:
                # shift right by a (within each block)
                su = [0] * a + D[:B - a] + [0] * a + D[B:2 * B - a]
                # shift left by a (within each block)
                sd = D[a:B] + [0] * a + D[B + a:2 * B] + [0] * a
                newD = [(x + y) * w % M for x, y, w in zip(su, sd, PW)]
                newD[0] = 0                              # landing at 0 sets flag
                newD[B] = (newD[B] + D[a]) % M           # dp0[a] -> dp1[0]
                D = newD
                i += 1

        contrib = sum(D[B:2 * B]) % M
        ans = ans * contrib % M

    print(ans % M)

main()