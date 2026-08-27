import sys
from itertools import product

MOD = 998244353

# Allowed states as (n, e, s, w) tuples
A_STATES = [(1,1,0,0),(0,1,1,0),(0,0,1,1),(1,0,0,1)]  # NE, ES, SW, WN
B_STATES = [(1,0,1,0),(0,1,0,1)]                        # NS, EW

def brute(H, W, grid):
    states = []
    for i in range(H):
        for j in range(W):
            states.append(A_STATES if grid[i][j] == 'A' else B_STATES)
    count = 0
    for choice in product(*[range(len(s)) for s in states]):
        # assign ports
        n = [[0]*W for _ in range(H)]
        e = [[0]*W for _ in range(H)]
        s = [[0]*W for _ in range(H)]
        w = [[0]*W for _ in range(H)]
        idx = 0
        for i in range(H):
            for j in range(W):
                st = states[idx][choice[idx]]
                n[i][j], e[i][j], s[i][j], w[i][j] = st
                idx += 1
        ok = True
        for i in range(H):
            if not ok: break
            for j in range(W):
                if e[i][j] != w[i][(j+1) % W]:
                    ok = False; break
                if s[i][j] != n[(i+1) % H][j]:
                    ok = False; break
        if ok:
            count += 1
    return count % MOD

class WDSU:
    """Weighted union-find tracking xor to parent."""
    def __init__(self, n):
        self.par = list(range(n))
        self.w = [0]*n   # xor from node to parent
        self.comps = n
    def find(self, x):
        if self.par[x] != x:
            r, wx = self.find(self.par[x])
            self.w[x] ^= wx
            self.par[x] = r
        return self.par[x], self.w[x]
    def union(self, a, b, c):
        # require value(a) xor value(b) = c
        ra, wa = self.find(a)
        rb, wb = self.find(b)
        if ra == rb:
            return (wa ^ wb) == c
        self.par[ra] = rb
        self.w[ra] = wa ^ wb ^ c
        self.comps -= 1
        return True

def fast(H, W, grid):
    A = [[1 if grid[i][j] == 'A' else 0 for j in range(W)] for i in range(H)]
    # parity checks
    for i in range(H):
        if sum(A[i]) & 1:
            return 0
    for j in range(W):
        if sum(A[i][j] for i in range(H)) & 1:
            return 0
    # V[i][j] = xor of A[k][j] for k=1..i ; Hh[i][j] = xor of A[i][l] for l=1..j
    V = [[0]*W for _ in range(H)]
    for j in range(W):
        acc = 0
        for i in range(1, H):
            acc ^= A[i][j]
            V[i][j] = acc
    Hh = [[0]*W for _ in range(H)]
    for i in range(H):
        acc = 0
        for j in range(1, W):
            acc ^= A[i][j]
            Hh[i][j] = acc
    dsu = WDSU(H + W)
    for i in range(H):
        for j in range(W):
            if A[i][j] == 0:  # B cell
                c = 1 ^ V[i][j] ^ Hh[i][j]
                if not dsu.union(i, H + j, c):
                    return 0
    return pow(2, dsu.comps, MOD)

def run_tests():
    # Sample tests
    samples = [
        (3, 3, ["AAB","AAB","BBB"], 2),
        (3, 3, ["BBA","ABA","AAB"], 0),
        (3, 4, ["BAAB","BABA","BBAA"], 2),
    ]
    for H, W, g, exp in samples:
        f = fast(H, W, g)
        b = brute(H, W, g)
        print(f"sample grid={g} fast={f} brute={b} expected={exp}")
        assert f == exp and b == exp, "SAMPLE MISMATCH"

    # Random small grids: compare fast vs brute
    import random
    random.seed(12345)
    for trial in range(300):
        H = random.randint(2, 3)
        W = random.randint(2, 3)
        g = ["".join(random.choice("AB") for _ in range(W)) for _ in range(H)]
        f = fast(H, W, g)
        b = brute(H, W, g)
        if f != b:
            print(f"MISMATCH grid={g} fast={f} brute={b}")
            sys.exit(1)
    print("All random tests passed.")

    # A few 2x4 / 4x2 spot checks
    for trial in range(60):
        H, W = random.choice([(2,4),(4,2)])
        g = ["".join(random.choice("AB") for _ in range(W)) for _ in range(H)]
        f = fast(H, W, g)
        b = brute(H, W, g)
        if f != b:
            print(f"MISMATCH grid={g} fast={f} brute={b}")
            sys.exit(1)
    print("All 2x4/4x2 tests passed.")

def solve():
    data = sys.stdin.buffer.read().split()
    pos = 0
    T = int(data[pos]); pos += 1
    out = []
    for _ in range(T):
        H = int(data[pos]); W = int(data[pos+1]); pos += 2
        grid = [data[pos+i].decode() for i in range(H)]
        pos += H
        out.append(str(fast(H, W, grid)))
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        run_tests()
    else:
        solve()