import sys

def solve():
    data = sys.stdin.read().split()
    if not data:
        return

    n = int(data[0])
    s = data[1]
    t = data[2]

    target = [-1] * 26

    for cs, ct in zip(s, t):
        c = ord(cs) - 97
        d = ord(ct) - 97
        if target[c] == -1:
            target[c] = d
        elif target[c] != d:
            print(-1)
            return

    present = [False] * 26
    appearing = []
    for c in range(26):
        if target[c] != -1:
            present[c] = True
            appearing.append(c)

    mandatory = 0
    for c in appearing:
        if target[c] != c:
            mandatory += 1

    indeg = [0] * 26
    for c in appearing:
        d = target[c]
        if present[d]:
            indeg[d] += 1

    state = [0] * 26
    pure_cycles = 0

    for c in appearing:
        if state[c] != 0:
            continue

        path = []
        pos = {}
        u = c

        while u is not None and state[u] == 0:
            state[u] = 1
            pos[u] = len(path)
            path.append(u)
            d = target[u]
            u = d if present[d] else None

        if u is not None and state[u] == 1 and u in pos:
            cycle = path[pos[u]:]
            if len(cycle) >= 2 and all(indeg[v] == 1 for v in cycle):
                pure_cycles += 1

        for v in path:
            state[v] = 2

    if pure_cycles > 0 and len(appearing) == 26 and all(indeg[c] == 1 for c in appearing):
        print(-1)
    else:
        print(mandatory + pure_cycles)

if __name__ == "__main__":
    solve()