import sys
from collections import deque

def solve():
    data = sys.stdin.read().split()
    if not data:
        return

    n = int(data[0])
    s = data[1]
    t = data[2]

    to = [-1] * 26
    mask_s = 0
    mask_t = 0

    for cs, ct in zip(s, t):
        u = ord(cs) - 97
        v = ord(ct) - 97
        mask_s |= 1 << u
        mask_t |= 1 << v

        if to[u] == -1:
            to[u] = v
        elif to[u] != v:
            print(-1)
            return

    has_edge = [False] * 26
    indeg = [0] * 26
    edges = 0

    for u in range(26):
        if to[u] != -1 and to[u] != u:
            has_edge[u] = True
            edges += 1
            indeg[to[u]] += 1

    indeg_orig = indeg[:]
    work = indeg[:]

    q = deque()
    for u in range(26):
        if has_edge[u] and work[u] == 0:
            q.append(u)

    removed = [False] * 26
    while q:
        u = q.popleft()
        removed[u] = True
        v = to[u]
        if has_edge[v]:
            work[v] -= 1
            if work[v] == 0:
                q.append(v)

    visited = [False] * 26
    bad_cycles = 0

    for u in range(26):
        if has_edge[u] and not removed[u] and not visited[u]:
            cur = u
            cycle = []
            while cur != -1 and not visited[cur]:
                visited[cur] = True
                cycle.append(cur)
                cur = to[cur]

            if all(indeg_orig[x] == 1 for x in cycle):
                bad_cycles += 1

    full = (1 << 26) - 1
    if bad_cycles > 0 and mask_s == full and mask_t == full:
        print(-1)
    else:
        print(edges + bad_cycles)

if __name__ == "__main__":
    solve()