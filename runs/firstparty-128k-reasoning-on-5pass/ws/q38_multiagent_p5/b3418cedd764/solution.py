import sys

MOD = 998244353

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return
    N, M = data[0], data[1]
    A = [0] + data[2:2 + N]

    if M == 1:
        print(1)
        return

    indeg = [0] * (N + 1)
    for i in range(1, N + 1):
        indeg[A[i]] += 1

    prod = [[1] * (M + 1) for _ in range(N + 1)]
    dirty = [False] * (N + 1)

    q = [i for i in range(1, N + 1) if indeg[i] == 0]
    head = 0
    mod = MOD
    rng = range(1, M + 1)

    while head < len(q):
        u = q[head]
        head += 1
        p = A[u]
        pp = prod[p]

        if not dirty[u]:
            # u has no processed children, so F_u[k] = k.
            if not dirty[p]:
                for k in rng:
                    pp[k] = k
                dirty[p] = True
            else:
                for k in rng:
                    pp[k] = (pp[k] * k) % mod
        else:
            pu = prod[u]
            s = 0
            if not dirty[p]:
                for k in rng:
                    s += pu[k]
                    if s >= mod:
                        s -= mod
                    pp[k] = s
                dirty[p] = True
            else:
                for k in rng:
                    s += pu[k]
                    if s >= mod:
                        s -= mod
                    pp[k] = (pp[k] * s) % mod

        prod[u] = None
        indeg[p] -= 1
        if indeg[p] == 0:
            q.append(p)

    visited = [False] * (N + 1)
    ans = 1

    for i in range(1, N + 1):
        if indeg[i] and not visited[i]:
            v = i
            cycle = []
            while not visited[v]:
                visited[v] = True
                cycle.append(v)
                v = A[v]

            base_node = -1
            for u in cycle:
                if dirty[u]:
                    base_node = u
                    break

            if base_node == -1:
                total = M % mod
            else:
                base = prod[base_node]
                for u in cycle:
                    if u != base_node and dirty[u]:
                        pu = prod[u]
                        for k in rng:
                            base[k] = (base[k] * pu[k]) % mod
                total = sum(base[1:]) % mod

            ans = (ans * total) % mod
            for u in cycle:
                prod[u] = None

    print(ans)

if __name__ == "__main__":
    main()