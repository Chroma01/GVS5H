import sys

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    s, t = data[1], data[2]

    target = [-1] * 26
    present = [False] * 26

    for a, b in zip(s, t):
        i = ord(a) - 97
        j = ord(b) - 97
        present[i] = True
        if target[i] == -1:
            target[i] = j
        elif target[i] != j:
            print(-1)
            return

    m = 0
    for i in range(26):
        if present[i] and target[i] != i:
            m += 1

    if m == 0:
        print(0)
        return

    indeg = [0] * 26
    for i in range(26):
        if present[i]:
            indeg[target[i]] += 1

    if all(present) and all(indeg[i] == 1 for i in range(26)):
        print(-1)
        return

    out = [-1] * 26
    for i in range(26):
        if present[i] and target[i] != i and present[target[i]]:
            out[i] = target[i]

    state = [0] * 26
    extra = 0

    for i in range(26):
        if state[i] == 0 and out[i] != -1:
            path = []
            pos = [-1] * 26
            v = i
            while v != -1 and state[v] == 0:
                state[v] = 1
                pos[v] = len(path)
                path.append(v)
                v = out[v]

            if v != -1 and state[v] == 1:
                if all(indeg[x] == 1 for x in path[pos[v]:]):
                    extra += 1

            for u in path:
                state[u] = 2

    print(m + extra)

if __name__ == "__main__":
    main()