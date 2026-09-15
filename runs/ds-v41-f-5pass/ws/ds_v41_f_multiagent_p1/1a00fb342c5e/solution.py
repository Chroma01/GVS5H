import sys
from collections import deque


def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    m = int(data[idx]); idx += 1

    adj = [[] for _ in range(n + 1)]
    for _ in range(m):
        x = int(data[idx]); idx += 1
        y = int(data[idx]); idx += 1
        z = int(data[idx]); idx += 1
        if x == y:
            # A_x XOR A_x == 0, so nonzero self-loop is impossible
            if z != 0:
                sys.stdout.write("-1\n")
                return
            continue
        adj[x].append((y, z))
        adj[y].append((x, z))

    D = [-1] * (n + 1)   # D[v] = XOR of edge labels on path from component root to v
    comps = []
    for s in range(1, n + 1):
        if D[s] != -1:
            continue
        D[s] = 0
        comp = [s]
        q = deque([s])
        while q:
            u = q.popleft()
            du = D[u]
            for v, z in adj[u]:
                expected = du ^ z
                if D[v] == -1:
                    D[v] = expected
                    comp.append(v)
                    q.append(v)
                elif D[v] != expected:
                    sys.stdout.write("-1\n")
                    return
        comps.append(comp)

    A = [0] * (n + 1)
    for comp in comps:
        size = len(comp)
        R = 0
        # choose each bit of the root value independently
        for b in range(31):
            mask = 1 << b
            c = 0
            for v in comp:
                if D[v] & mask:
                    c += 1
            if size - c < c:   # setting this bit to 1 yields fewer ones
                R |= mask
        for v in comp:
            A[v] = R ^ D[v]

    sys.stdout.write(' '.join(str(A[i]) for i in range(1, n + 1)) + '\n')


main()