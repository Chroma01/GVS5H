import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    S = data[1].strip()
    T = data[2].strip()

    # Build required mapping f[c] = target of letter c
    f = [-1] * 26
    present = [False] * 26
    for sc, tc in zip(S, T):
        a = ord(sc) - 97
        b = ord(tc) - 97
        present[a] = True
        if f[a] == -1:
            f[a] = b
        elif f[a] != b:
            print(-1)
            return

    # Non-self edges
    edge = [False] * 26          # edge[c]: c maps to a different letter
    indeg = [0] * 26             # in-degree counting only non-self edges
    edges = 0
    for c in range(26):
        if f[c] != -1 and f[c] != c:
            edge[c] = True
            edges += 1
            indeg[f[c]] += 1

    if edges == 0:
        print(0)
        return

    # Impossible case: no usable buffer letter exists.
    # A buffer is a letter with 0 occurrences at some point:
    #  - a letter not appearing in S, or
    #  - a letter that appears but can be permanently zeroed (in-degree 0,
    #    counting self-loops as occupying in-degree too).
    # If all 26 letters appear in S and every letter has in-degree >= 1
    # (self-loop counts), then the mapping on present letters is all cycles
    # and no buffer can ever be created -> impossible (since edges > 0).
    if all(present):
        ok_buffer = False
        for c in range(26):
            # in-degree including self-loop
            d = indeg[c] + (1 if (f[c] == c) else 0)
            if d == 0:
                ok_buffer = True
                break
        if not ok_buffer:
            print(-1)
            return

    # Count cycles in the non-self functional graph where every node has
    # in-degree exactly 1 (no external incoming edge). Each such pure cycle
    # costs one extra operation (temporary rename).
    state = [0] * 26  # 0 = unvisited, 1 = in stack, 2 = done
    extra = 0
    for start in range(26):
        if not edge[start] or state[start] != 0:
            continue
        # walk from start
        path = []
        cur = start
        while cur != -1 and edge[cur] and state[cur] == 0:
            state[cur] = 1
            path.append(cur)
            cur = f[cur]
        if cur != -1 and edge[cur] and state[cur] == 1:
            # found a cycle: nodes from first occurrence of cur in path
            idx = path.index(cur)
            cyc = path[idx:]
            if all(indeg[node] == 1 for node in cyc):
                extra += 1
        for node in path:
            state[node] = 2

    print(edges + extra)

main()