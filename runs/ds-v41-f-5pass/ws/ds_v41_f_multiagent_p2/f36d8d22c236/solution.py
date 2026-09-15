import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    N = int(data[0])
    S = data[1]
    T = data[2]

    # f[c] = target letter for source letter c
    f = [-1] * 26
    for i in range(N):
        c = S[i] - 97
        t = T[i] - 97
        if f[c] == -1:
            f[c] = t
        elif f[c] != t:
            print(-1)
            return

    D = [c for c in range(26) if f[c] != -1]
    E = sum(1 for c in D if f[c] != c)
    if E == 0:
        print(0)
        return

    image = set(f[c] for c in D)

    # No spare letter AND it is a permutation (non-identity since E>0):
    # an isolated cycle exists but no buffer -> impossible.
    if len(D) == 26 and len(image) == 26:
        print(-1)
        return

    # Build graph of nontrivial edges
    nxt = [-1] * 26
    indeg = [0] * 26
    for c in D:
        if f[c] != c:
            nxt[c] = f[c]
            indeg[f[c]] += 1

    # Count isolated cycles (all nodes on cycle have indegree exactly 1)
    state = [0] * 26  # 0 unvisited, 1 in current path, 2 done
    isolated = 0
    for start in range(26):
        if state[start] != 0:
            continue
        if nxt[start] == -1:
            state[start] = 2
            continue
        path = []
        v = start
        while v != -1 and state[v] == 0:
            state[v] = 1
            path.append(v)
            v = nxt[v]
        if v != -1 and state[v] == 1:
            idx = path.index(v)
            cyc = path[idx:]
            if all(indeg[u] == 1 for u in cyc):
                isolated += 1
        for u in path:
            state[u] = 2

    print(E + isolated)

main()