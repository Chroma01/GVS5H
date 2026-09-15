import sys
from collections import deque
from array import array

INF = 10**30
EXACT_LIMIT = 120


def exact_solve(n, adj, s, t):
    """Exact ordered-pair BFS, used only for small graphs."""
    total = n * n
    seen = bytearray(total)
    start = s * n + t
    goal = t * n + s
    q = deque([start])
    seen[start] = 1
    dist = 0

    while q:
        for _ in range(len(q)):
            code = q.popleft()
            if code == goal:
                return dist

            a = code // n
            b = code - a * n

            for na in adj[a]:
                if na == b:
                    continue
                nc = na * n + b
                if not seen[nc]:
                    seen[nc] = 1
                    q.append(nc)

            for nb in adj[b]:
                if nb == a:
                    continue
                nc = a * n + nb
                if not seen[nc]:
                    seen[nc] = 1
                    q.append(nc)

        dist += 1

    return -1


def bfs(src, adj):
    n = len(adj)
    dist = [-1] * n
    parent = [-1] * n
    dist[src] = 0
    q = deque([src])

    while q:
        v = q.popleft()
        nd = dist[v] + 1
        for to in adj[v]:
            if dist[to] == -1:
                dist[to] = nd
                parent[to] = v
                q.append(to)

    return dist, parent


def process_root(n, edges_u, edges_v, root, parent, depth, d_other, current_best):
    """
    Enumerate fundamental cycles of the BFS tree rooted at `root`.

    For a fundamental cycle C, let w be the LCA of the non-tree edge endpoints.
    The minimum depth on C is depth[w].  We need the best distinct pair
    (p, q) on C of depth[p] + d_other[q].  If the minimum d_other vertex is
    not w, it is optimal to take p = w.  Otherwise we need either the second
    minimum d_other on C, or p = a child of w on the cycle and q = w.
    """
    lower_bound = 2 * d_other[root]
    if current_best == lower_bound:
        return current_best

    log = max(1, n.bit_length())

    # up[k][v] = 2^k-th ancestor of v
    up = [array('i', parent)]

    # mn1/mn2 store the best and second best vertex ids by d_other
    # on the path segment of length 2^k starting at v and going upward,
    # excluding the final ancestor.
    mn1_0 = array('i', [-1]) * n
    for v in range(n):
        if parent[v] != -1:
            mn1_0[v] = v

    mn1 = [mn1_0]
    mn2 = [array('i', [-1]) * n]

    d = d_other

    for _ in range(1, log):
        prev_up = up[-1]
        prev_mn1 = mn1[-1]
        prev_mn2 = mn2[-1]

        upk = array('i', [-1]) * n
        m1k = array('i', [-1]) * n
        m2k = array('i', [-1]) * n

        for v in range(n):
            mid = prev_up[v]
            if mid == -1:
                continue

            upk[v] = prev_up[mid]

            r1 = -1
            r2 = -1

            for x in (prev_mn1[v], prev_mn2[v], prev_mn1[mid], prev_mn2[mid]):
                if x == -1 or x == r1 or x == r2:
                    continue
                if r1 == -1 or d[x] < d[r1]:
                    r2 = r1
                    r1 = x
                elif r2 == -1 or d[x] < d[r2]:
                    r2 = x

            m1k[v] = r1
            m2k[v] = r2

        up.append(upk)
        mn1.append(m1k)
        mn2.append(m2k)

    def lca(u, v):
        if depth[u] < depth[v]:
            u, v = v, u

        diff = depth[u] - depth[v]
        bit = 0
        while diff:
            if diff & 1:
                u = up[bit][u]
            diff >>= 1
            bit += 1

        if u == v:
            return u

        for k in range(log - 1, -1, -1):
            uu = up[k][u]
            vv = up[k][v]
            if uu != vv:
                u = uu
                v = vv

        return up[0][u]

    def query_excl(a, b):
        """Top two d_other vertices on path a..b, excluding a. a must be ancestor of b."""
        r1 = -1
        r2 = -1
        diff = depth[b] - depth[a]
        bit = 0

        while diff:
            if diff & 1:
                for x in (mn1[bit][b], mn2[bit][b]):
                    if x == -1 or x == r1 or x == r2:
                        continue
                    if r1 == -1 or d[x] < d[r1]:
                        r2 = r1
                        r1 = x
                    elif r2 == -1 or d[x] < d[r2]:
                        r2 = x

                b = up[bit][b]

            diff >>= 1
            bit += 1

        return r1, r2

    best = current_best

    for u, v in zip(edges_u, edges_v):
        # Tree edges do not create fundamental cycles.
        if parent[u] == v or parent[v] == u:
            continue

        w = lca(u, v)

        t1, t2 = query_excl(w, u)

        # Add the LCA vertex itself.
        x = w
        if x != -1 and x != t1 and x != t2:
            if t1 == -1 or d[x] < d[t1]:
                t2 = t1
                t1 = x
            elif t2 == -1 or d[x] < d[t2]:
                t2 = x

        q1, q2 = query_excl(w, v)
        for x in (q1, q2):
            if x == -1 or x == t1 or x == t2:
                continue
            if t1 == -1 or d[x] < d[t1]:
                t2 = t1
                t1 = x
            elif t2 == -1 or d[x] < d[t2]:
                t2 = x

        if t1 == -1:
            continue

        if t1 != w:
            pair = depth[w] + d[t1]
        else:
            # Minimum d_other is at w.  Either use the second-best d_other,
            # or use a child of w on the cycle as p and w as q.
            pair = depth[w] + 1 + d[w]
            if t2 != -1:
                cand = depth[w] + d[t2]
                if cand < pair:
                    pair = cand

        cycle_len = depth[u] + depth[v] + 1 - 2 * depth[w]
        if cycle_len < 3:
            continue

        cand = cycle_len + 2 * pair
        if cand < best:
            best = cand
            # Only 2D is globally optimal; 2D+1 may still be beaten by 2D.
            if best == lower_bound:
                return best

    return best


def structural_solve(n, adj, eu, ev, s, t):
    dist_s, parent_s = bfs(s, adj)
    dist_t, parent_t = bfs(t, adj)

    D = dist_s[t]
    lower_bound = 2 * D
    ans = INF

    # spare[v] = number of neighbors of v that are not immediate predecessors
    # on any shortest path from S to v nor from T to v.
    spare = [0] * n
    for v in range(n):
        ds = dist_s[v]
        dt = dist_t[v]
        ds_prev = ds - 1
        dt_prev = dt - 1
        cnt = 0
        for u in adj[v]:
            if dist_s[u] != ds_prev and dist_t[u] != dt_prev:
                cnt += 1
        spare[v] = cnt

    for v in range(n):
        ds = dist_s[v]
        dt = dist_t[v]

        # One side neighbor is enough if v is an internal vertex of a shortest
        # S-T path.
        if ds + dt == D and v != s and v != t and spare[v] >= 1:
            cand = lower_bound + 2
            if cand < ans:
                ans = cand

        # Two side neighbors allow a local passing gadget at v, even if v is
        # an endpoint or lies off the shortest path (e.g. a branch/cycle at the
        # end of a tail from S or T).
        if spare[v] >= 2:
            cand = 2 * (ds + dt) + 4
            if cand < ans:
                ans = cand

    del spare

    if ans == lower_bound:
        return ans

    # Cycle passing.  If the graph is a tree, there are no fundamental cycles.
    if len(eu) > n - 1:
        ans = process_root(n, eu, ev, s, parent_s, dist_s, dist_t, ans)
        if ans == lower_bound:
            return ans

        ans = process_root(n, eu, ev, t, parent_t, dist_t, dist_s, ans)

    return -1 if ans >= INF else ans


def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    it = iter(data)
    n = int(next(it))
    m = int(next(it))
    s = int(next(it)) - 1
    t = int(next(it)) - 1

    adj = [[] for _ in range(n)]
    eu = [0] * m
    ev = [0] * m

    for i in range(m):
        u = int(next(it)) - 1
        v = int(next(it)) - 1
        eu[i] = u
        ev[i] = v
        adj[u].append(v)
        adj[v].append(u)

    # For small graphs, use the exact ordered-pair BFS oracle directly.
    if n <= EXACT_LIMIT:
        print(exact_solve(n, adj, s, t))
        return

    print(structural_solve(n, adj, eu, ev, s, t))


if __name__ == "__main__":
    solve()