import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    N = int(data[0])
    S = data[1].decode()
    T = data[2].decode()

    f = [-1] * 26
    for i in range(N):
        a = ord(S[i]) - 97
        b = ord(T[i]) - 97
        if f[a] == -1:
            f[a] = b
        elif f[a] != b:
            print(-1)
            return

    present = set(ord(c) - 97 for c in S)
    base = 0
    for c in present:
        if f[c] != c:
            base += 1

    # Find cycles in the functional graph restricted to present letters.
    visited = [False] * 26
    cycles = []
    for start in present:
        if visited[start]:
            continue
        path = []
        idx = {}
        cur = start
        while cur in present and not visited[cur] and cur not in idx:
            idx[cur] = len(path)
            path.append(cur)
            cur = f[cur]
        if cur in idx:
            cycle_nodes = path[idx[cur]:]
            if len(cycle_nodes) > 1:
                cycles.append(cycle_nodes)
        for node in path:
            visited[node] = True

    # Count isolated cycles (cycles with no tree attached).
    iso = 0
    for cycle_nodes in cycles:
        cycle_set = set(cycle_nodes)
        isolated = True
        for c in present:
            if c not in cycle_set and f[c] in cycle_set:
                isolated = False
                break
        if isolated:
            iso += 1

    if iso == 0:
        print(base)
    else:
        # A spare letter is available if some letter never appears in S,
        # or if all 26 appear but the mapping is not injective.
        if len(present) < 26:
            print(base + iso)
        else:
            U = set(f[c] for c in present)
            if len(U) < 26:
                print(base + iso)
            else:
                print(-1)

if __name__ == "__main__":
    main()