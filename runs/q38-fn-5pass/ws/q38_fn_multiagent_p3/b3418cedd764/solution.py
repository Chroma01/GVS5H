import sys

MOD = 998244353


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N, M = data[0], data[1]
    A = [x - 1 for x in data[2:2 + N]]

    # indeg[u] = number of children of u in the reversed forest
    indeg = [0] * N
    for a in A:
        indeg[a] += 1

    # acc[u] stores the partial product of prefix-sum arrays of processed children.
    # For a non-cycle node, when all children are processed, acc[u] is f_u.
    # For a cycle node, acc[u] remains f_u for the attached non-cycle tree.
    acc = [None] * N

    stack = [i for i in range(N) if indeg[i] == 0]

    mod = MOD
    m = M
    rng = range(1, m + 1)
    base = list(range(m + 1))  # prefix array of a leaf: [0, 1, 2, ..., M]

    # Kahn pruning: process non-cycle nodes bottom-up.
    while stack:
        u = stack.pop()
        p = A[u]
        arr = acc[u]

        if arr is None:
            # u is a leaf: its prefix array is v.
            pacc = acc[p]
            if pacc is None:
                acc[p] = base.copy()
            else:
                for v in rng:
                    pacc[v] = (pacc[v] * v) % mod
        else:
            # acc[u] is f_u. Convert it to prefix sums S_u, then merge into parent.
            acc[u] = None
            pacc = acc[p]

            if pacc is None:
                s = 0
                for v in rng:
                    s += arr[v]
                    if s >= mod:
                        s -= mod
                    arr[v] = s
                acc[p] = arr
            else:
                s = 0
                for v in rng:
                    s += arr[v]
                    if s >= mod:
                        s -= mod
                    pacc[v] = (pacc[v] * s) % mod

        indeg[p] -= 1
        if indeg[p] == 0:
            stack.append(p)

    ans = 1
    visited = [False] * N

    # Remaining nodes with indeg > 0 are exactly cycle nodes.
    for i in range(N):
        if indeg[i] > 0 and not visited[i]:
            nodes = []
            cur = i
            while not visited[cur]:
                visited[cur] = True
                nodes.append(cur)
                cur = A[cur]

            prod = None
            for u in nodes:
                f = acc[u]
                if f is not None:
                    if prod is None:
                        prod = f
                    else:
                        for v in rng:
                            prod[v] = (prod[v] * f[v]) % mod

            if prod is None:
                contrib = m % mod
            else:
                contrib = sum(prod[1:]) % mod

            ans = (ans * contrib) % mod

            # Free arrays no longer needed.
            for u in nodes:
                acc[u] = None

    print(ans)


if __name__ == "__main__":
    solve()