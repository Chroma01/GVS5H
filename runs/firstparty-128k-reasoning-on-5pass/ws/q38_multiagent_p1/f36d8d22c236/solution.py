import sys

def main():
    data = sys.stdin.read().split()
    if not data:
        return

    n = int(data[0])
    s = data[1]
    t = data[2]

    req = [-1] * 26
    present = [False] * 26

    for cs, ct in zip(s, t):
        a = ord(cs) - 97
        b = ord(ct) - 97
        present[a] = True
        if req[a] == -1:
            req[a] = b
        elif req[a] != b:
            print(-1)
            return

    m = 0
    img = set()
    nxt = [-1] * 26

    for a in range(26):
        if present[a]:
            b = req[a]
            img.add(b)
            if b != a:
                m += 1
                nxt[a] = b

    if len(img) == 26 and m > 0:
        print(-1)
        return

    indeg = [0] * 26
    for a in range(26):
        b = nxt[a]
        if b != -1:
            indeg[b] += 1

    state = [0] * 26
    extra = 0

    for i in range(26):
        if nxt[i] == -1 or state[i] != 0:
            continue

        path = []
        cur = i
        while nxt[cur] != -1 and state[cur] == 0:
            state[cur] = 1
            path.append(cur)
            cur = nxt[cur]

        if nxt[cur] != -1 and state[cur] == 1:
            idx = path.index(cur)
            cycle = path[idx:]
            if all(indeg[v] == 1 for v in cycle):
                extra += 1

        for v in path:
            state[v] = 2

    print(m + extra)

if __name__ == "__main__":
    main()