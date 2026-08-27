import sys

def solve():
    data = sys.stdin.read().split()
    if not data:
        return

    S = data[1]
    T = data[2]

    forced = [-1] * 26
    present = [False] * 26

    for cs, ct in zip(S, T):
        a = ord(cs) - ord('a')
        b = ord(ct) - ord('a')
        present[a] = True
        if forced[a] == -1:
            forced[a] = b
        elif forced[a] != b:
            print(-1)
            return

    P = [i for i in range(26) if present[i]]

    changed = 0
    image = set()
    for a in P:
        b = forced[a]
        image.add(b)
        if a != b:
            changed += 1

    if len(P) == 26 and len(image) == 26 and changed > 0:
        print(-1)
        return

    indeg = [0] * 26
    for a in P:
        b = forced[a]
        if present[b]:
            indeg[b] += 1

    state = [0] * 26  # 0: unvisited, 1: visiting, 2: done
    pure_cycles = 0

    for start in P:
        if state[start] != 0:
            continue

        cur = start
        path = []
        pos = {}

        while present[cur] and state[cur] == 0:
            state[cur] = 1
            pos[cur] = len(path)
            path.append(cur)
            cur = forced[cur]

        if present[cur] and state[cur] == 1:
            cycle = path[pos[cur]:]
            if len(cycle) >= 2:
                pure = True
                for v in cycle:
                    if indeg[v] != 1:
                        pure = False
                        break
                if pure:
                    pure_cycles += 1

        for v in path:
            state[v] = 2

    print(changed + pure_cycles)

if __name__ == "__main__":
    solve()