import sys


def main():
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    S = data[1]
    T = data[2]

    # Build required mapping f: letter in S -> letter in T
    f = {}
    for c, d in zip(S, T):
        if c in f:
            if f[c] != d:
                print(-1)
                return
        else:
            f[c] = d

    if S == T:
        print(0)
        return

    present = set(S)
    distinctT = set(T)

    # Saturated alphabet in both, but S != T: f is a non-identity permutation,
    # no empty label and no merge -> cannot break any cycle.
    if len(present) == 26 and len(distinctT) == 26:
        print(-1)
        return

    # Base cost: every letter that must change needs one operation.
    E = 0
    for c in present:
        if f[c] != c:
            E += 1

    # in-degree of each letter among letters present in S
    indeg = {}
    for c in present:
        d = f[c]
        indeg[d] = indeg.get(d, 0) + 1

    # Find cycles (length >= 2).  A cycle needs one extra operation iff
    # every node on it has in-degree exactly 1 (no incoming edge from outside).
    state = {c: 0 for c in present}  # 0 unvisited, 1 on stack, 2 done
    extra = 0
    for start in present:
        if state[start] != 0:
            continue
        path = []
        pos = {}
        u = start
        while True:
            if u not in state:          # reached a letter not in S (sink)
                for v in path:
                    state[v] = 2
                break
            if state[u] == 2:           # reached already-finished node
                for v in path:
                    state[v] = 2
                break
            if state[u] == 1:           # found a cycle
                idx = pos[u]
                cyc = path[idx:]
                if len(cyc) >= 2 and all(indeg.get(v, 0) == 1 for v in cyc):
                    extra += 1
                for v in path:
                    state[v] = 2
                break
            state[u] = 1
            pos[u] = len(path)
            path.append(u)
            u = f[u]

    print(E + extra)


if __name__ == "__main__":
    main()