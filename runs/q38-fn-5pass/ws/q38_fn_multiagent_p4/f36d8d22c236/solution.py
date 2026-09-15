import sys

def solve():
    data = sys.stdin.read().split()
    if not data:
        return

    n = int(data[0])
    s = data[1]
    t = data[2]

    target = [-1] * 26
    present_s = [False] * 26
    present_t = [False] * 26

    for cs, ct in zip(s, t):
        a = ord(cs) - 97
        b = ord(ct) - 97
        present_s[a] = True
        present_t[b] = True

        if target[a] == -1:
            target[a] = b
        elif target[a] != b:
            print(-1)
            return

    edge = [-1] * 26
    indeg = [0] * 26
    edges = 0

    for i in range(26):
        if present_s[i]:
            ti = target[i]
            indeg[ti] += 1
            if ti != i:
                edge[i] = ti
                edges += 1

    state = [0] * 26
    closed_cycles = 0

    for i in range(26):
        if edge[i] != -1 and state[i] == 0:
            path = []
            pos = {}
            u = i

            while u != -1 and state[u] == 0:
                state[u] = 1
                pos[u] = len(path)
                path.append(u)
                u = edge[u]

            if u != -1 and state[u] == 1:
                cycle = path[pos[u]:]
                # A cycle needs one extra operation only if no outside
                # present letter maps into it. Then every cycle vertex has
                # indegree exactly 1 (only its predecessor inside the cycle).
                if all(indeg[v] == 1 for v in cycle):
                    closed_cycles += 1

            for v in path:
                state[v] = 2

    # If all 26 letters are present in both strings, no temporary letter can
    # ever be created. Any nontrivial cycle is then impossible.
    if closed_cycles > 0 and all(present_s) and all(present_t):
        print(-1)
    else:
        print(edges + closed_cycles)

if __name__ == "__main__":
    solve()