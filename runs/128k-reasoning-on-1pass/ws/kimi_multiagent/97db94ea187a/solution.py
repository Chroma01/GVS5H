import sys


def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    N = int(data[0]); P = int(data[1])
    half = N // 2
    Mmax = N * (N - 1) // 2
    L = Mmax + 1
    L16 = L * 16          # 16 bytes = 128 bits per packed coefficient
    sz = half + 1

    try:
        import numpy as np
        HAVE_NP = True
    except Exception:
        HAVE_NP = False

    fact = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = fact[i - 1] * i % P
    invfact = [1] * sz
    invfact[half] = pow(fact[half], P - 2, P)
    for i in range(half, 0, -1):
        invfact[i - 1] = invfact[i] * i % P

    c2 = [i * (i - 1) // 2 for i in range(sz)]

    # trans[a][b]: factor (1+x)^C(b,2) * ((1+x)^a - 1)^b / b!
    # In the {(1+x)^E} basis this is a sum of shifts:
    #   sum_j (-1)^(b-j) / (j! (b-j)!)  *  (1+x)^(C(b,2) + a*j)
    # stored as (shift_in_bits, weight).
    trans = [[None] * sz for _ in range(sz)]
    for a in range(1, sz):
        for b in range(1, sz):
            lst = []
            base = c2[b]
            for j in range(b + 1):
                w = invfact[j] * invfact[b - j] % P
                if (b - j) & 1:
                    w = P - w
                lst.append(((base + a * j) << 7, w))
            trans[a][b] = lst

    # Polynomials are stored as packed big integers: coefficient of (1+x)^E
    # lives in bits [128E, 128E+128).  Coefficients are reduced mod P only
    # when a state is used as a source; between reductions a coefficient
    # accumulates <= 15 contributions each < P^2 < 2^60, so every
    # coefficient stays < 2^64 < 2^128 and no limb ever carries.
    FE = [[[0] * sz for _ in range(sz)] for _ in range(sz)]
    FO = [[[0] * sz for _ in range(sz)] for _ in range(sz)]
    bFE = [[] for _ in range(N + 1)]
    bFO = [[] for _ in range(N + 1)]
    FE[1][0][1] = 1
    bFE[1].append((1, 0, 1))

    if HAVE_NP:
        P64 = np.uint64(P)
        R64 = np.uint64((1 << 64) % P)

        def unpack(x):
            a = np.frombuffer(x.to_bytes(L16, 'little'), dtype=np.uint64)
            return (a[0::2] % P64 + (a[1::2] % P64) * R64) % P64

        def repack(r):
            out = np.zeros(2 * L, dtype=np.uint64)
            out[0::2] = r
            return int.from_bytes(out.tobytes(), 'little')
    else:
        def unpack(x):
            b = x.to_bytes(L16, 'little')
            return [int.from_bytes(b[k * 16:(k + 1) * 16], 'little') % P
                    for k in range(L)]

        def repack(r):
            return int.from_bytes(
                b''.join(v.to_bytes(16, 'little') for v in r), 'little')

    for used in range(1, N):
        # last layer has even distance -> append an odd layer
        for e, o, a in bFE[used]:
            if o >= half:
                continue
            packed = FE[e][o][a]
            if not packed:
                continue
            src = repack(unpack(packed))
            tra = trans[a]
            for b in range(1, half - o + 1):
                no = o + b
                tgt = FO[e][no][b]
                if tgt == 0:
                    bFO[used + b].append((e, no, b))
                for shb, w in tra[b]:
                    tgt += (src * w) << shb
                FO[e][no][b] = tgt
        # last layer has odd distance -> append an even layer
        for e, o, a in bFO[used]:
            if e >= half:
                continue
            packed = FO[e][o][a]
            if not packed:
                continue
            src = repack(unpack(packed))
            tra = trans[a]
            for b in range(1, half - e + 1):
                ne = e + b
                tgt = FE[ne][o][b]
                if tgt == 0:
                    bFE[used + b].append((ne, o, b))
                for shb, w in tra[b]:
                    tgt += (src * w) << shb
                FE[ne][o][b] = tgt

    mult = fact[N - 1]
    if HAVE_NP:
        fb = np.zeros(L, dtype=np.uint64)
        for a in range(1, sz):
            x = FE[half][half][a]
            if x:
                fb = (fb + unpack(x)) % P64
            x = FO[half][half][a]
            if x:
                fb = (fb + unpack(x)) % P64
        # binomial matrix C[E][m] for the basis change (1+x)^E -> x^m
        C = np.zeros((L, L), dtype=np.int64)
        C[:, 0] = 1
        for E in range(1, L):
            C[E, 1:E] = (C[E - 1, :E - 1] + C[E - 1, 1:E]) % P
            C[E, E] = 1
        ans = ((fb.astype(np.int64)[:, None] * C) % P).sum(axis=0) % P
        out = [str(int(ans[m]) * mult % P) for m in range(N - 1, Mmax + 1)]
    else:
        fb = [0] * L
        for a in range(1, sz):
            x = FE[half][half][a]
            if x:
                r = unpack(x)
                fb = [(u + v) % P for u, v in zip(fb, r)]
            x = FO[half][half][a]
            if x:
                r = unpack(x)
                fb = [(u + v) % P for u, v in zip(fb, r)]
        Crows = [[1]]
        for E in range(1, L):
            prev = Crows[-1]
            row = [1] * (E + 1)
            for m in range(1, E):
                v = prev[m - 1] + prev[m]
                if v >= P:
                    v -= P
                row[m] = v
            Crows.append(row)
        ans = [0] * L
        for E in range(L):
            v = fb[E]
            if not v:
                continue
            row = Crows[E]
            for m in range(E + 1):
                ans[m] = (ans[m] + v * row[m]) % P
        out = [str(ans[m] * mult % P) for m in range(N - 1, Mmax + 1)]

    sys.stdout.write(' '.join(out))


if __name__ == '__main__':
    solve()