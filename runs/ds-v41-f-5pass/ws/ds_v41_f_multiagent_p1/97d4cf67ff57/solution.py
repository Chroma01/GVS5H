import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])
    idx = 1
    adj = [[] for _ in range(n)]
    for _ in range(n - 1):
        a = int(data[idx]) - 1
        b = int(data[idx + 1]) - 1
        idx += 2
        adj[a].append(b)
        adj[b].append(a)

    # Root the tree at 0, get a parent-before-child order iteratively.
    parent = [-1] * n
    order = []
    visited = bytearray(n)
    stack = [0]
    visited[0] = 1
    while stack:
        v = stack.pop()
        order.append(v)
        for w in adj[v]:
            if not visited[w]:
                visited[w] = 1
                parent[w] = v
                stack.append(w)

    # down[v] = B(parent(v), v): best branch on v's side using edge (parent,v), rooted at v.
    # B(u,v) = 1 (leaf) or 1 + top-3 of B(v,w) over w != u, if at least 3 such neighbors.
    down = [1] * n
    for v in reversed(order):
        if v == 0:
            continue
        m1 = m2 = m3 = 0
        cnt = 0
        for w in adj[v]:
            if parent[w] == v:
                val = down[w]
                cnt += 1
                if val > m1:
                    m3 = m2
                    m2 = m1
                    m1 = val
                elif val > m2:
                    m3 = m2
                    m2 = val
                elif val > m3:
                    m3 = val
        if cnt >= 3:
            down[v] = 1 + m1 + m2 + m3

    # up[v] = B(v, parent(v)): rerooting pass, parent-before-child order.
    up = [0] * n
    ans = -1
    for v in order:
        entries = []
        if v != 0:
            entries.append((up[v], -1))  # branch through parent edge
        for w in adj[v]:
            if parent[w] == v:
                entries.append((down[w], w))  # branch through child edge
        entries.sort(reverse=True)

        # Candidate: v is the degree-4 root of the alkane -> pick 4 best branches.
        if len(entries) >= 4:
            cand = 1 + entries[0][0] + entries[1][0] + entries[2][0] + entries[3][0]
            if cand > ans:
                ans = cand

        # Compute up[c] for each child: top-3 branch values of v excluding c.
        for c in adj[v]:
            if parent[c] == v:
                s = 0
                cnt = 0
                for val, tag in entries:
                    if tag == c:
                        continue
                    s += val
                    cnt += 1
                    if cnt == 3:
                        break
                up[c] = 1 + s if cnt == 3 else 1

    sys.stdout.write(str(ans) + "\n")

main()