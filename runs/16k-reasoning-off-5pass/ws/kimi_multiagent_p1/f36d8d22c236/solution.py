import sys

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    S = data[1]
    T = data[2]

    # Required mapping f[x] = y for each position; conflict => impossible.
    f = {}
    for x, y in zip(S, T):
        prev = f.get(x)
        if prev is None:
            f[x] = y
        elif prev != y:
            print(-1)
            return

    # Functional graph on letters with a real change x -> y (x != y).
    out = {}
    for x, y in f.items():
        if x != y:
            out[x] = y

    # Detect cycles via in-degree elimination (Kahn-style) on <=26 nodes.
    letters = [chr(ord('a') + i) for i in range(26)]
    indeg = {c: 0 for c in letters}
    for x, y in out.items():
        indeg[y] += 1

    stack = [c for c in letters if indeg[c] == 0]
    removed = set()
    while stack:
        u = stack.pop()
        removed.add(u)
        v = out.get(u)
        if v is not None:
            indeg[v] -= 1
            if indeg[v] == 0:
                stack.append(v)

    # Nodes not removed and having an outgoing edge are exactly cycle nodes.
    cycle_nodes = set()
    for c in letters:
        if c not in removed and c in out:
            cycle_nodes.add(c)

    # Count cycles.
    cycles = 0
    seen = set()
    for c in cycle_nodes:
        if c not in seen:
            cycles += 1
            u = c
            while u not in seen:
                seen.add(u)
                u = out[u]

    E = len(out)  # base operations: one per distinct required change

    if cycles > 0:
        # Need a buffer letter: a letter not on any cycle that either
        # (a) does not occur in S at all, or
        # (b) has an outgoing edge (it can be temporarily eliminated from S
        #     by renaming it toward its target, then used as scratch space).
        in_S = set(S)
        buffer_ok = False
        for c in letters:
            if c in cycle_nodes:
                continue
            if c in out or c not in in_S:
                buffer_ok = True
                break
        if not buffer_ok:
            print(-1)
            return

    print(E + cycles)

solve()