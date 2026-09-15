import sys
from collections import deque

def solve() -> None:
    data = sys.stdin.read().split()
    if not data:
        return

    n = int(data[0])
    s = data[1]
    t = data[2]

    # Required final letter for each letter appearing in S.
    mp = [-1] * 26
    in_t = [False] * 26
    for ch in t:
        in_t[ord(ch) - 97] = True

    for cs, ct in zip(s, t):
        u = ord(cs) - 97
        v = ord(ct) - 97
        if mp[u] == -1:
            mp[u] = v
        elif mp[u] != v:
            print(-1)
            return

    active = [False] * 26
    for ch in s:
        active[ord(ch) - 97] = True

    # Build the functional graph of unique non-self edges.
    out = [-1] * 26
    indeg = [0] * 26
    edges = 0

    for u in range(26):
        if active[u]:
            v = mp[u]
            if v != u:
                edges += 1
                out[u] = v
                if active[v]:
                    indeg[v] += 1

    indeg0 = indeg[:]

    # Remove all vertices not belonging to a directed cycle.
    q = deque(u for u in range(26) if active[u] and indeg[u] == 0)
    removed = [False] * 26

    while q:
        u = q.popleft()
        removed[u] = True
        v = out[u]
        if v != -1 and active[v]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)

    # Count closed cycles: cycles whose vertices have original indegree exactly 1.
    visited = [False] * 26
    closed_cycles = 0

    for u in range(26):
        if active[u] and not removed[u] and not visited[u]:
            cycle = []
            cur = u

            while cur != -1 and active[cur] and not visited[cur]:
                visited[cur] = True
                cycle.append(cur)
                cur = out[cur]

            if cur != -1 and cur in cycle:
                cycle = cycle[cycle.index(cur):]
                if all(indeg0[v] == 1 for v in cycle):
                    closed_cycles += 1

    # If every letter is occupied and every letter is required as a final letter,
    # the mapping is a permutation. A nontrivial closed cycle then has no buffer.
    if closed_cycles > 0 and all(active) and all(in_t):
        print(-1)
    else:
        print(edges + closed_cycles)

if __name__ == "__main__":
    solve()