import sys
from collections import deque
from itertools import accumulate

def main():
    data = sys.stdin.buffer.read().split()
    N = int(data[0]); M = int(data[1])
    A = [int(data[2 + i]) - 1 for i in range(N)]
    MOD = 998244353

    # --- Peel non-cycle nodes (edges: i -> A[i]) ---
    indeg = [0] * N
    for i in range(N):
        indeg[A[i]] += 1
    q = deque(i for i in range(N) if indeg[i] == 0)
    order = []
    removed = [False] * N
    while q:
        u = q.popleft()
        order.append(u)
        removed[u] = True
        v = A[u]
        indeg[v] -= 1
        if indeg[v] == 0:
            q.append(v)
    is_cycle = [not removed[i] for i in range(N)]

    try:
        import numpy as np
    except ImportError:
        np = None

    if np is not None:
        leaf_P = np.arange(1, M + 1, dtype=np.int64)  # prefix of all-ones = [1..M]
        F = {}   # non-cycle node -> accumulator (product of children prefixes)
        H = {}   # cycle node     -> product of non-cycle children prefixes

        for u in order:
            acc = F.pop(u, None)
            if acc is None:
                P = leaf_P
                is_leaf = True
            else:
                P = np.cumsum(acc)
                P %= MOD
                is_leaf = False
            p = A[u]
            target = H if is_cycle[p] else F
            ex = target.get(p)
            if ex is None:
                target[p] = leaf_P.copy() if is_leaf else P
            else:
                ex *= P
                ex %= MOD

        visited = [False] * N
        ans = 1
        for i in range(N):
            if is_cycle[i] and not visited[i]:
                total = None
                j = i
                while not visited[j]:
                    visited[j] = True
                    Hj = H.get(j)
                    if total is None:
                        total = Hj.copy() if Hj is not None else np.ones(M, dtype=np.int64)
                    elif Hj is not None:
                        total *= Hj
                        total %= MOD
                    j = A[j]
                c = int(total.sum() % MOD)
                ans = ans * c % MOD
        sys.stdout.write(str(ans) + "\n")
    else:
        leaf_P = list(range(1, M + 1))
        F = {}
        H = {}
        for u in order:
            acc = F.pop(u, None)
            if acc is None:
                P = leaf_P
                is_leaf = True
            else:
                P = [x % MOD for x in accumulate(acc)]
                is_leaf = False
            p = A[u]
            target = H if is_cycle[p] else F
            ex = target.get(p)
            if ex is None:
                target[p] = leaf_P[:] if is_leaf else P
            else:
                if is_leaf:
                    target[p] = [a * (k + 1) % MOD for k, a in enumerate(ex)]
                else:
                    target[p] = [a * b % MOD for a, b in zip(ex, P)]

        visited = [False] * N
        ans = 1
        for i in range(N):
            if is_cycle[i] and not visited[i]:
                total = None
                j = i
                while not visited[j]:
                    visited[j] = True
                    Hj = H.get(j)
                    if total is None:
                        total = Hj[:] if Hj is not None else [1] * M
                    elif Hj is not None:
                        total = [a * b % MOD for a, b in zip(total, Hj)]
                    j = A[j]
                ans = ans * (sum(total) % MOD) % MOD
        sys.stdout.write(str(ans) + "\n")

main()