import sys
import random
from itertools import permutations


def solve(n, edges, A, B):
    """DSU-sweep minimum bottleneck matching. edges: list of (w,u,v)."""
    cnt = [0] * (n + 1)
    for a in A:
        cnt[a] += 1
    for b in B:
        cnt[b] -= 1

    es = sorted(edges, key=lambda e: e[0])
    parent = list(range(n + 1))
    rank_ = [0] * (n + 1)
    surplus = cnt[:]  # surplus[root] = #A - #B in component

    ans = 0
    for w, u, v in es:
        ru = u
        while parent[ru] != ru:
            parent[ru] = parent[parent[ru]]
            ru = parent[ru]
        rv = v
        while parent[rv] != rv:
            parent[rv] = parent[parent[rv]]
            rv = parent[rv]
        if ru == rv:
            continue
        s1 = surplus[ru]
        s2 = surplus[rv]
        if s1 > 0 and s2 < 0:
            m = s1 if s1 < -s2 else -s2
            ans += m * w
        elif s1 < 0 and s2 > 0:
            m = -s1 if -s1 < s2 else s2
            ans += m * w
        if rank_[ru] < rank_[rv]:
            ru, rv = rv, ru
        parent[rv] = ru
        if rank_[ru] == rank_[rv]:
            rank_[ru] += 1
        surplus[ru] = s1 + s2
    return ans


# ---------------- brute force validation ----------------

def brute(n, edges, A, B):
    INF = float('inf')
    g = [[INF] * (n + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        g[i][i] = 0
    for w, u, v in edges:
        if w < g[u][v]:
            g[u][v] = w
            g[v][u] = w
    for kk in range(1, n + 1):
        gk = g[kk]
        for i in range(1, n + 1):
            gi = g[i]
            aik = gi[kk]
            for j in range(1, n + 1):
                cand = aik if aik > gk[j] else gk[j]
                if cand < gi[j]:
                    gi[j] = cand
    best = INF
    L = len(B)
    for perm in permutations(range(L)):
        tot = 0
        for i in range(L):
            tot += g[A[i]][B[perm[i]]]
            if tot >= best:
                break
        if tot < best:
            best = tot
    return best


def gen_graph(n, rng):
    perm = list(range(1, n + 1))
    rng.shuffle(perm)
    eset = set()
    for i in range(1, n):
        u = perm[i]
        v = perm[rng.randrange(i)]
        if u > v:
            u, v = v, u
        eset.add((u, v))
    possible = [(i, j) for i in range(1, n + 1) for j in range(i + 1, n + 1)
                if (i, j) not in eset]
    rng.shuffle(possible)
    extra = rng.randint(0, len(possible))
    for e in possible[:extra]:
        eset.add(e)
    maxw = rng.choice([1, 2, 3, 5, 10 ** 9])
    return [(rng.randint(1, maxw), u, v) for (u, v) in eset]


def gen_AB(n, rng):
    verts = list(range(1, n + 1))
    rng.shuffle(verts)
    cut = rng.randint(1, n - 1)
    SA = verts[:cut]
    SB = verts[cut:]
    k = rng.randint(1, n)
    A = [rng.choice(SA) for _ in range(k)]
    B = [rng.choice(SB) for _ in range(k)]
    return A, B


def selftest():
    rng = random.Random(12345)
    T = 5000
    for t in range(T):
        n = rng.randint(2, 7)
        edges = gen_graph(n, rng)
        A, B = gen_AB(n, rng)
        fast = solve(n, edges, A, B)
        slow = brute(n, edges, A, B)
        if fast != slow:
            print("FAIL")
            print("n =", n)
            print("edges =", edges)
            print("A =", A)
            print("B =", B)
            print("fast =", fast, "brute =", slow)
            return
    print("PASS", T, "random tests")


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    idx = 0
    n = int(data[idx]); idx += 1
    m = int(data[idx]); idx += 1
    k = int(data[idx]); idx += 1
    edges = []
    for _ in range(m):
        u = int(data[idx]); v = int(data[idx + 1]); w = int(data[idx + 2])
        idx += 3
        edges.append((w, u, v))
    A = [0] * k
    B = [0] * k
    for i in range(k):
        A[i] = int(data[idx]); idx += 1
    for i in range(k):
        B[i] = int(data[idx]); idx += 1
    print(solve(n, edges, A, B))


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--selftest":
        selftest()
    else:
        main()