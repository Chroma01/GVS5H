import sys

def main():
    data = sys.stdin.buffer.read().split()
    # data[0] = N, data[1] = S, data[2] = T
    S = data[1].decode()
    T = data[2].decode()

    # Required mapping: every occurrence of letter a must become letter b.
    f = {}
    for a, b in zip(S, T):
        if a in f:
            if f[a] != b:
                # same source letter forced to two different targets
                print(-1)
                return
        else:
            f[a] = b

    if S == T:
        print(0)
        return

    dS = len(set(S))
    dT = len(set(T))

    # If S already uses all 26 letters and T uses all 26 letters but S != T,
    # f is a non-identity permutation. Every operation merges (target always
    # present) -> distinct-letter count drops and can never return to 26. -1.
    if dS == 26 and dT == 26:
        print(-1)
        return

    # Count required move-edges a -> f(a), a != f(a), and in-degrees.
    E = 0
    indeg = {}
    for a, b in f.items():
        if a != b:
            E += 1
            indeg[b] = indeg.get(b, 0) + 1

    # Find "pure" cycles: real cycles whose every node has in-degree exactly 1
    # (no tree feeds into the cycle). Each such cycle costs one extra operation.
    visited = set()
    pure = 0
    for start in f:
        if start in visited:
            continue
        path = []
        pos = {}
        cur = start
        while cur not in visited and cur not in pos and f.get(cur, cur) != cur:
            pos[cur] = len(path)
            path.append(cur)
            cur = f[cur]
        if cur in pos:
            cycle = path[pos[cur]:]
            if all(indeg.get(x, 0) == 1 for x in cycle):
                pure += 1
        for node in path:
            visited.add(node)

    print(E + pure)

main()