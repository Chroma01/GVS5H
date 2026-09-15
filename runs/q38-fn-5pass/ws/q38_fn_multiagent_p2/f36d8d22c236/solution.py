import sys

def solve():
    data = sys.stdin.read().split()
    if not data:
        return

    n = int(data[0])
    s = data[1]
    t = data[2]

    to = [-1] * 26
    active = [False] * 26

    for cs, ct in zip(s, t):
        a = ord(cs) - 97
        b = ord(ct) - 97
        active[a] = True

        if to[a] == -1:
            to[a] = b
        elif to[a] != b:
            print(-1)
            return

    base = 0
    indeg = [0] * 26
    seen_target = [False] * 26
    injective = True

    for i in range(26):
        if not active[i]:
            continue

        j = to[i]

        if j != i:
            base += 1
            indeg[j] += 1

        if seen_target[j]:
            injective = False
        else:
            seen_target[j] = True

    state = [0] * 26
    closed_cycles = 0

    for i in range(26):
        if not active[i] or state[i] != 0:
            continue

        path = []
        cur = i

        while cur != -1 and active[cur] and state[cur] == 0:
            state[cur] = 1
            path.append(cur)
            cur = to[cur]

        if cur != -1 and active[cur] and state[cur] == 1:
            start = path.index(cur)
            cycle = path[start:]

            if len(cycle) >= 2:
                closed = True
                for v in cycle:
                    if indeg[v] != 1:
                        closed = False
                        break

                if closed:
                    closed_cycles += 1

        for v in path:
            state[v] = 2

    if closed_cycles > 0 and all(active) and injective:
        print(-1)
    else:
        print(base + closed_cycles)

if __name__ == "__main__":
    solve()