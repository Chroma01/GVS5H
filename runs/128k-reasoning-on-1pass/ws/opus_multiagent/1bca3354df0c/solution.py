import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0]); ne = int(data[1])
    deg = [0]*(n+2)
    U = [0]*ne; V = [0]*ne
    ptr = 2
    for i in range(ne):
        u = int(data[ptr]); v = int(data[ptr+1]); ptr += 2
        U[i] = u; V[i] = v
        deg[u] += 1; deg[v] += 1
    head = [0]*(n+2)
    s = 0
    for v in range(1, n+1):
        head[v] = s
        s += deg[v]
    head[n+1] = s
    pos = head[:]
    adj = [0]*(2*ne)
    for i in range(ne):
        u = U[i]; v = V[i]
        adj[pos[u]] = v; pos[u] += 1
        adj[pos[v]] = u; pos[v] += 1

    color = [-1]*(n+1)
    sumxy = 0
    K = 0   # number of odd-size components
    I = 0   # number of isolated vertices
    for s0 in range(1, n+1):
        if color[s0] != -1:
            continue
        color[s0] = 0
        c0 = 1; c1 = 0
        stack = [s0]
        while stack:
            u = stack.pop()
            cu = color[u]
            nc = cu ^ 1
            for k in range(head[u], head[u]+deg[u]):
                w = adj[k]
                if color[w] == -1:
                    color[w] = nc
                    if nc == 0:
                        c0 += 1
                    else:
                        c1 += 1
                    stack.append(w)
        x = c0; y = c1
        sumxy += x*y
        if (x + y) & 1:
            K += 1
        if x + y == 1:
            I += 1

    if n & 1:
        # a*b is always even  =>  total moves == ne (mod 2)
        print("Aoki" if (ne & 1) else "Takahashi")
        return

    phi = sumxy - ne          # currently addable internal edges
    m = K // 2
    if I == 2*m:
        win = ((phi + m) & 1) == 1
    elif I >= 2*m - 2:
        win = True
    else:
        win = (ne & 1) == 1
    print("Aoki" if win else "Takahashi")


# ------------------------------------------------------------------
# development helper: python prog.py --selftest [Nmax]
# brute-force minimax over abstract states, compared with the formula
# ------------------------------------------------------------------
def _formula(state):
    N = sum(x+y for x, y, e in state)
    M = sum(e for x, y, e in state)
    if N & 1:
        return (M & 1) == 1
    sumxy = sum(x*y for x, y, e in state)
    K = sum(1 for x, y, e in state if (x+y) & 1)
    I = sum(1 for x, y, e in state if x+y == 1)
    phi = sumxy - M
    m = K // 2
    if I == 2*m:
        return ((phi + m) & 1) == 1
    if I >= 2*m - 2:
        return True
    return (M & 1) == 1


def _selftest(argv):
    sys.setrecursionlimit(100000)
    memo = {}

    def moves(state):
        res = set()
        L = list(state)
        k = len(L)
        for i in range(k):
            x, y, e = L[i]
            if e < x*y:
                nl = L[:i] + [(x, y, e+1)] + L[i+1:]
                res.add(tuple(sorted(nl)))
        for i in range(k):
            for j in range(i+1, k):
                x1, y1, e1 = L[i]
                x2, y2, e2 = L[j]
                rest = [L[t] for t in range(k) if t != i and t != j]
                cands = []
                if (x1 >= 1 and y2 >= 1) or (y1 >= 1 and x2 >= 1):
                    cands.append((x1+x2, y1+y2))
                if (x1 >= 1 and x2 >= 1) or (y1 >= 1 and y2 >= 1):
                    cands.append((x1+y2, y1+x2))
                for (a, b) in cands:
                    if a < b:
                        a, b = b, a
                    res.add(tuple(sorted(rest + [(a, b, e1+e2+1)])))
        return res

    def win(state):
        r = memo.get(state)
        if r is not None:
            return r
        r = False
        for ns in moves(state):
            if not win(ns):
                r = True
                break
        memo[state] = r
        return r

    def gen(N):
        comps = []
        for size in range(1, N+1):
            for y in range(0, size//2 + 1):
                x = size - y
                if y == 0:
                    if size == 1:
                        comps.append((1, 0, 0))
                else:
                    for e in range(x+y-1, x*y+1):
                        comps.append((x, y, e))
        comps.sort()
        out = []

        def rec(idx, remaining, cur):
            if remaining == 0:
                out.append(tuple(sorted(cur)))
                return
            for t in range(idx, len(comps)):
                c = comps[t]
                if c[0] + c[1] <= remaining:
                    rec(t, remaining - (c[0]+c[1]), cur + [c])
        rec(0, N, [])
        return out

    nmax = int(argv[2]) if len(argv) > 2 else 8
    bad = 0
    for N in range(1, nmax+1):
        for st in gen(N):
            if win(st) != _formula(st):
                bad += 1
                print("MISMATCH", st, "brute:", win(st), "formula:", _formula(st))
                if bad > 20:
                    return
        print("N =", N, "ok")
    print("all ok" if bad == 0 else "mismatches: %d" % bad)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--selftest":
        _selftest(sys.argv)
    else:
        main()