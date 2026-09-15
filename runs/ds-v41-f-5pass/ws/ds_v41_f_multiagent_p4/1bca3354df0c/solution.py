import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    pos = 0
    n = int(data[pos]); pos += 1
    m = int(data[pos]); pos += 1

    adj = [[] for _ in range(n + 1)]
    eu = [0] * m
    ev = [0] * m
    for i in range(m):
        u = int(data[pos]); pos += 1
        v = int(data[pos]); pos += 1
        eu[i] = u
        ev[i] = v
        adj[u].append(v)
        adj[v].append(u)

    comp = [-1] * (n + 1)
    color = [0] * (n + 1)
    comp_x = []   # size of larger colour class in component
    comp_y = []   # size of smaller colour class
    comp_sz = []  # total vertices in component

    cid = 0
    for s in range(1, n + 1):
        if comp[s] != -1:
            continue
        comp[s] = cid
        color[s] = 0
        stack = [s]
        cnt0 = 0
        cnt1 = 0
        size = 0
        while stack:
            u = stack.pop()
            size += 1
            if color[u] == 0:
                cnt0 += 1
            else:
                cnt1 += 1
            for w in adj[u]:
                if comp[w] == -1:
                    comp[w] = cid
                    color[w] = color[u] ^ 1
                    stack.append(w)
        a, b = cnt0, cnt1
        if a < b:
            a, b = b, a
        comp_x.append(a)
        comp_y.append(b)
        comp_sz.append(size)
        cid += 1

    # edge count per component
    ecount = [0] * cid
    for i in range(m):
        ecount[comp[eu[i]]] += 1

    o = 0      # number of odd-sized components
    iso = 0    # number of isolated vertices (size-1 components, all odd)
    S = 0      # sum of C(x,2)+C(y,2) over components (same-colour pairs)
    for c in range(cid):
        sz = comp_sz[c]
        if sz & 1:
            o += 1
            if sz == 1:
                iso += 1
        x = comp_x[c]
        y = comp_y[c]
        S += x * (x - 1) // 2 + y * (y - 1) // 2

    b = o - iso                      # odd non-isolated components
    base = n * (n - 1) // 2 - m - S

    if n & 1:
        aoki = (m & 1) == 1
    else:
        if b == 0:
            aoki = (base & 1) == 1
        else:
            aoki = (o % 4 == 2) or (b <= 2)

    sys.stdout.write("Aoki\n" if aoki else "Takahashi\n")

main()