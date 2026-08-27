import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        print("Yes")
        return
    n = int(data[0]); k = int(data[1])
    m = n * k
    if k == 1 or m <= 1:
        print("Yes")
        return

    E = m - 1
    # parse edges
    vals = list(map(int, data[2:2 + 2 * E]))

    deg = [0] * (m + 2)
    for x in vals:
        deg[x] += 1

    start = [0] * (m + 2)
    acc = 0
    for v in range(1, m + 1):
        start[v] = acc
        acc += deg[v]
    start[m + 1] = acc

    pos = start[:]
    adj = [0] * (2 * E)
    for i in range(E):
        a = vals[2 * i]
        b = vals[2 * i + 1]
        adj[pos[a]] = b
        pos[a] += 1
        adj[pos[b]] = a
        pos[b] += 1

    # BFS from vertex 1
    par = [0] * (m + 1)
    order = [0] * m
    visited = bytearray(m + 1)
    order[0] = 1
    visited[1] = 1
    cnt = 1
    head = 0
    while head < cnt:
        v = order[head]
        head += 1
        for i in range(start[v], start[v + 1]):
            w = adj[i]
            if not visited[w]:
                visited[w] = 1
                par[w] = v
                order[cnt] = w
                cnt += 1

    ssum = [0] * (m + 1)
    ccnt = [0] * (m + 1)

    ok = True
    for idx in range(m - 1, -1, -1):
        v = order[idx]
        c = ccnt[v]
        s = 1 + ssum[v]
        if c > 2 or s > k:
            ok = False
            break
        if s == k:
            # path closed within subtree, nothing propagates
            continue
        # s < k : must extend upward
        if c == 2:
            ok = False
            break
        p = par[v]
        if p == 0:
            # v is root, cannot extend further
            ok = False
            break
        ssum[p] += s
        ccnt[p] += 1

    sys.stdout.write("Yes\n" if ok else "No\n")


main()