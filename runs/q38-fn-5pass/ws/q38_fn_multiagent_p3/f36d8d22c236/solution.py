import sys

def solve():
    data = sys.stdin.read().split()
    if not data:
        return

    N = int(data[0])
    S = data[1]
    T = data[2]

    # forced[c] = final letter forced for original letter c, or -1 if unused.
    forced = [-1] * 26

    for s, t in zip(S, T):
        u = ord(s) - 97
        v = ord(t) - 97
        if forced[u] == -1:
            forced[u] = v
        elif forced[u] != v:
            print(-1)
            return

    used = [f != -1 for f in forced]
    used_count = sum(used)

    # indeg counts all incoming edges from used source letters, including self-loops.
    indeg = [0] * 26
    edges = 0

    for u in range(26):
        if used[u]:
            v = forced[u]
            indeg[v] += 1
            if v != u:
                edges += 1

    # A buffer is an initially empty letter, or a letter that can be emptied
    # by merging two classes with the same final target.
    buffer = (used_count < 26) or (max(indeg) >= 2)

    # Count nontrivial cycles where every node has indegree exactly 1.
    # Such cycles have no incoming tree and need one extra operation.
    state = [0] * 26  # 0: unvisited, 1: visiting, 2: done
    pure_cycles = 0

    for i in range(26):
        if used[i] and state[i] == 0:
            path = []
            pos = {}
            cur = i

            while cur != -1 and used[cur] and state[cur] == 0:
                state[cur] = 1
                pos[cur] = len(path)
                path.append(cur)
                cur = forced[cur]

            if cur != -1 and used[cur] and state[cur] == 1:
                cycle = path[pos[cur]:]
                if len(cycle) > 1 and all(indeg[x] == 1 for x in cycle):
                    pure_cycles += 1

            for node in path:
                state[node] = 2

    if pure_cycles > 0 and not buffer:
        print(-1)
    else:
        print(edges + pure_cycles)

if __name__ == "__main__":
    solve()