import sys
from collections import deque

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return
    N, M = data[0], data[1]
    A = [x - 1 for x in data[2:2 + N]]
    MOD = 998244353
    M1 = M + 1
    rng = range(1, M1)

    indeg = [0] * N
    for a in A:
        indeg[a] += 1

    q = deque([i for i in range(N) if indeg[i] == 0])
    is_cycle = [True] * N
    while q:
        v = q.popleft()
        is_cycle[v] = False
        u = A[v]
        indeg[u] -= 1
        if indeg[u] == 0:
            q.append(u)

    comp_id = [-1] * N
    comp_count = 0
    for i in range(N):
        if is_cycle[i] and comp_id[i] == -1:
            cur = i
            while comp_id[cur] == -1:
                comp_id[cur] = comp_count
                cur = A[cur]
            comp_count += 1

    child_count = [0] * N
    for i in range(N):
        if not is_cycle[i]:
            child_count[A[i]] += 1

    acc = [None] * N
    H = [None] * comp_count
    base = list(range(M1))

    def mul(a, b, rng=rng, mod=MOD):
        for i in rng:
            a[i] = (a[i] * b[i]) % mod

    def prefix(a, rng=rng, mod=MOD):
        s = 0
        for i in rng:
            s += a[i]
            if s >= mod:
                s -= mod
            a[i] = s
        a[0] = 0

    q = deque([i for i in range(N) if not is_cycle[i] and child_count[i] == 0])

    while q:
        v = q.popleft()
        if acc[v] is None:
            f = base.copy()
        else:
            f = acc[v]
            acc[v] = None
            prefix(f)

        p = A[v]
        if is_cycle[p]:
            cid = comp_id[p]
            if H[cid] is None:
                H[cid] = f
            else:
                mul(H[cid], f)
        else:
            if acc[p] is None:
                acc[p] = f
            else:
                mul(acc[p], f)
            child_count[p] -= 1
            if child_count[p] == 0:
                q.append(p)

    ans = 1
    for cid in range(comp_count):
        h = H[cid]
        if h is None:
            factor = M % MOD
        else:
            s = 0
            for i in rng:
                s += h[i]
                if s >= MOD:
                    s -= MOD
            factor = s
        ans = (ans * factor) % MOD

    print(ans)

if __name__ == "__main__":
    main()