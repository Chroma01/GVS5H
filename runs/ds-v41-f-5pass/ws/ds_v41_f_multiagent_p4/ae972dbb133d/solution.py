import sys

def main():
    data = sys.stdin.buffer.read().split()
    MOD = 998244353
    pos = 0
    T = int(data[pos]); pos += 1
    out = []
    for _ in range(T):
        H = int(data[pos]); W = int(data[pos + 1]); pos += 2
        rows = data[pos:pos + H]; pos += H
        n = H + W
        parent = list(range(n))
        par = [0] * n          # par[x] = value[x] xor value[parent[x]]
        size = [1] * n
        Gcol = [0] * W         # prefix of c down each column (= G[i][j])
        comp = n
        bad = False
        for i in range(H):
            row = rows[i]
            hprefix = 0        # prefix of c along current row (= Hh[i][j])
            base = W + i       # row variable b_i
            for j, ch in enumerate(row):
                if ch == 65:   # 'A'  -> c = 1
                    hprefix ^= 1
                    Gcol[j] ^= 1
                else:          # 'B'  -> add constraint a_j xor b_i = 1^G^Hh
                    p = 1 ^ Gcol[j] ^ hprefix
                    # find(j)
                    ra = j; pa = 0
                    while parent[ra] != ra:
                        pa ^= par[ra]; ra = parent[ra]
                    if parent[j] != j:
                        cur = j; rem = pa
                        while parent[cur] != cur:
                            nxt = parent[cur]; npar = par[cur]
                            parent[cur] = ra; par[cur] = rem
                            rem ^= npar; cur = nxt
                    # find(base)
                    rb = base; pb = 0
                    while parent[rb] != rb:
                        pb ^= par[rb]; rb = parent[rb]
                    if parent[base] != base:
                        cur = base; rem = pb
                        while parent[cur] != cur:
                            nxt = parent[cur]; npar = par[cur]
                            parent[cur] = rb; par[cur] = rem
                            rem ^= npar; cur = nxt
                    if ra == rb:
                        if (pa ^ pb) != p:
                            bad = True
                    else:
                        S = p ^ pa ^ pb
                        if size[ra] < size[rb]:
                            parent[ra] = rb; par[ra] = S; size[rb] += size[ra]
                        else:
                            parent[rb] = ra; par[rb] = S; size[ra] += size[rb]
                        comp -= 1
            if hprefix:        # row sum of c must be even
                bad = True
        if bad:
            out.append('0')
        else:
            for v in Gcol:     # column sum of c must be even
                if v:
                    bad = True
                    break
            out.append('0' if bad else str(pow(2, comp, MOD)))
    sys.stdout.write('\n'.join(out) + '\n')

main()