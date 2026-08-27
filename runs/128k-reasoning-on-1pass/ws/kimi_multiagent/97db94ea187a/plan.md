```python
import sys
from array import array

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    N = int(data[0]); P = int(data[1])
    half = N // 2
    Mmax = N * (N - 1) // 2
    L = Mmax + 1

    # factorials / inverse factorials mod P (P > 435)
    fact = [1] * (Mmax + 1)
    for i in range(1, Mmax + 1):
        fact[i] = fact[i - 1] * i % P
    invfact = [1] * (Mmax + 1)
    invfact[Mmax] = pow(fact[Mmax], P - 2, P)
    for i in range(Mmax, 0, -1):
        invfact[i - 1] = invfact[i] * i % P

    # Binomial rows for final basis change (1+x)^E -> x^m
    C = [[0] * (E + 1) for E in range(L)]
    for E in range(L):
        row = C[E]
        row[0] = row[E] = 1
        if E > 1:
            prev = C[E - 1]
            for m in range(1, E):
                v = prev[m - 1] + prev[m]
                if v >= P:
                    v -= P
                row[m] = v

    sz = half + 1
    # FE[e][o][a]: last layer has even index; FO similarly for odd index.
    # Polynomials are stored in the basis {(1+x)^E}; multiplication becomes shifts in E.
    FE = [[[None] * sz for _ in range(sz)] for _ in range(sz)]
    FO = [[[None] * sz for _ in range(sz)] for _ in range(sz)]
    bFE = [[] for _ in range(N + 1)]
    bFO = [[] for _ in range(N + 1)]

    FE[1][0][1] = array('i', [0]) * L
    FE[1][0][1][0] = 1
    bFE[1].append((1, 0, 1))

    c2 = [i * (i - 1) // 2 for i in range(sz)]

    # trans[a][b] = list of (shift, signed_coeff/b!) for
    # (1+x)^(C(b,2)) * ((1+x)^a - 1)^b / b!
    trans = [[None] * sz for _ in range(sz)]
    for a in range(1, sz):
        for b in range(1, sz):
            lst = []
            base = c2[b]
            for j in range(b + 1):
                w = invfact[j] * invfact[b - j] % P
                if (b - j) & 1:
                    w = P - w
                lst.append((base + a * j, w))
            trans[a][b] = lst

    for used in range(1, N):
        # last layer even -> add odd layer
        for e, o, a in bFE[used]:
            src = FE[e][o][a]
            if src is None:
                continue
            lim = half - o
            if lim <= 0:
                continue
            maxE = used * (used - 1) // 2
            for b in range(1, lim + 1):
                ne, no = e, o + b
                tgt = FO[ne][no][b]
                if tgt is None:
                    tgt = array('i', [0]) * L
                    FO[ne][no][b] = tgt
                    bFO[used + b].append((ne, no, b))
                tr = trans[a][b]
                for E in range(maxE + 1):
                    val = src[E]
                    if not val:
                        continue
                    for sh, w in tr:
                        nE = E + sh
                        if nE > Mmax:
                            break
                        s = tgt[nE] + (val * w) % P
                        if s >= P:
                            s -= P
                        tgt[nE] = s

        # last layer odd -> add even layer
        for e, o, a in bFO[used]:
            src = FO[e][o][a]
            if src is None:
                continue
            lim = half - e
            if lim <= 0:
                continue
            maxE = used * (used - 1) // 2
            for b in range(1, lim + 1):
                ne, no = e + b, o
                tgt = FE[ne][no][b]
                if tgt is None:
                    tgt = array('i', [0]) * L
                    FE[ne][no][b] = tgt
                    bFE[used + b].append((ne, no, b))
                tr = trans[a][b]
                for E in range(maxE + 1):
                    val = src[E]
                    if not val:
                        continue
                    for sh, w in tr:
                        nE = E + sh
                        if nE > Mmax:
                            break
                        s = tgt[nE] + (val * w) % P
                        if s >= P:
                            s -= P
                        tgt[nE] = s

    # Sum all balanced terminal states in the (1+x)^E basis.
    fb = [0] * L
    for a in range(1, sz):
        p = FE[half][half][a]
        if p is not None:
            for E in range(L):
                v = fb[E] + p[E]
                if v >= P:
                    v -= P
                fb[E] = v
        p = FO[half][half][a]
        if p is not None:
            for E in range(L):
                v = fb[E] + p[E]
                if v >= P:
                    v -= P
                fb[E] = v

    # Change basis: coefficient of x^m gets sum_E fb[E] * C(E, m).
    ans = [0] * L
    for E in range(L):
        val = fb[E]
        if not val:
            continue
        row = C[E]
        for m in range(E + 1):
            ans[m] = (ans[m] + val * row[m]) % P

    mult = fact[N - 1]
    out = [str(ans[m] * mult % P) for m in range(N - 1, Mmax + 1)]
    sys.stdout.write(' '.join(out))

if __name__ == '__main__':
    solve()
```