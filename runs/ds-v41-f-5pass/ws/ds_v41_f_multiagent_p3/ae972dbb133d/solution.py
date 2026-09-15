import sys
sys.setrecursionlimit(1_000_000)

parent = []
xr = []
sz = []

def find(x):
    if parent[x] == x:
        return x, 0
    p = parent[x]
    r, par = find(p)
    xr[x] ^= par
    parent[x] = r
    return r, xr[x]

def union(a, b, w):
    ra, pa = find(a)
    rb, pb = find(b)
    if ra == rb:
        return 0 if (pa ^ pb) == w else -1
    if sz[ra] < sz[rb]:
        parent[ra] = rb
        xr[ra] = pa ^ pb ^ w
        sz[rb] += sz[ra]
    else:
        parent[rb] = ra
        xr[rb] = pa ^ pb ^ w
        sz[ra] += sz[rb]
    return 1

def solve():
    global parent, xr, sz
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    T = int(next(it))
    MOD = 998244353
    out = []
    for _ in range(T):
        H = int(next(it))
        W = int(next(it))
        N = H + W
        parent = list(range(N))
        xr = [0] * N
        sz = [1] * N
        comp = N
        col_par = [0] * W
        ok = True
        for i in range(H):
            row = next(it)
            if not ok:
                continue
            row_pref = 0
            for j, ch in enumerate(row):
                if ch == 66:  # 'B'
                    w = 1 ^ col_par[j] ^ row_pref
                    res = union(i, H + j, w)
                    if res == -1:
                        ok = False
                        break
                    elif res == 1:
                        comp -= 1
                else:  # 'A'
                    row_pref ^= 1
                    col_par[j] ^= 1
            if ok and row_pref != 0:
                ok = False
        if ok:
            for cp in col_par:
                if cp != 0:
                    ok = False
                    break
        if not ok:
            out.append("0")
        else:
            out.append(str(pow(2, comp, MOD)))
    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()