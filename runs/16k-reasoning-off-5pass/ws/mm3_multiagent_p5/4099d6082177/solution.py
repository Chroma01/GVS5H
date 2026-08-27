import sys
from collections import deque

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    K = int(next(it))
    V = N * K
    if V == 1:
        print("Yes")
        return
    adj = [[] for _ in range(V + 1)]
    for _ in range(V - 1):
        u = int(next(it))
        v = int(next(it))
        adj[u].append(v)
        adj[v].append(u)

    if K == 1:
        print("Yes")
        return

    # Early necessary condition: sum max(0, deg(v)-2) == 2N
    deg = [0] * (V + 1)
    for i in range(1, V + 1):
        deg[i] = len(adj[i])
    excess = 0
    for i in range(1, V + 1):
        if deg[i] > 2:
            excess += deg[i] - 2
    if excess != 2 * N:
        print("No")
        return

    # Root the tree at 1 for parent pointers (for DSU optimization)
    parent = [0] * (V + 1)
    visited = [False] * (V + 1)
    q = deque([1])
    visited[1] = True
    parent[1] = -1
    while q:
        u = q.popleft()
        for v in adj[u]:
            if not visited[v]:
                visited[v] = True
                parent[v] = u
                q.append(v)

    # DSU for jumping to next not-removed ancestor (optimization)
    dsu = list(range(V + 1))
    def find(x):
        while dsu[x] != x:
            dsu[x] = dsu[dsu[x]]
            x = dsu[x]
        return x
    def union(x, y):
        x = find(x)
        y = find(y)
        if x != y:
            dsu[x] = y

    removed = [False] * (V + 1)
    cur_deg = deg[:]
    leaves = deque(i for i in range(1, V + 1) if cur_deg[i] == 1)
    paths_removed = 0

    while leaves and paths_removed < N:
        start = leaves.popleft()
        if removed[start] or cur_deg[start] != 1:
            continue

        # Build a path of length K-1 edges (K vertices) starting from this leaf,
        # walking inward along the remaining tree. We must never go back to 'prev'.
        path = [start]
        prev = -1
        cur = start
        success = True
        for _ in range(K - 1):
            # Find the unique neighbor of 'cur' that is not removed and not 'prev'.
            # Because we are walking from a leaf into the tree, 'cur' will have exactly
            # one such neighbor in the remaining tree.
            nxt = -1
            for nb in adj[cur]:
                if not removed[nb] and nb != prev:
                    nxt = nb
                    break
            if nxt == -1:
                success = False
                break
            path.append(nxt)
            prev = cur
            cur = nxt
            # Optional DSU jump: we could also verify the path doesn't collide
            # with already-removed nodes using DSU, but the simple walk above
            # already ensures we only step on unremoved nodes.

        if not success or len(path) != K:
            print("No")
            return

        # Remove the path vertices
        for node in path:
            removed[node] = True
            cur_deg[node] = 0
            # Update DSU: union removed node with its parent to enable fast jumps later
            p = parent[node]
            if p != -1:
                union(node, p)

        # Update degrees of neighbors and collect new leaves
        affected = set()
        for node in path:
            for nb in adj[node]:
                if not removed[nb]:
                    cur_deg[nb] -= 1
                    if cur_deg[nb] == 1:
                        affected.add(nb)

        for nb in affected:
            leaves.append(nb)
        paths_removed += 1

    if paths_removed == N:
        print("Yes")
    else:
        print("No")

if __name__ == "__main__":
    solve()