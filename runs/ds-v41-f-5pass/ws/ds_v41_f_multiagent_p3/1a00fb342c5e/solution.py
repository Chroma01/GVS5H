import sys
from collections import deque

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    idx = 0
    n = int(data[idx]); idx += 1
    m = int(data[idx]); idx += 1

    adj = [[] for _ in range(n + 1)]
    for _ in range(m):
        x = int(data[idx]); y = int(data[idx + 1]); z = int(data[idx + 2])
        idx += 3
        adj[x].append((y, z))
        if x != y:
            adj[y].append((x, z))

    BITS = 31  # Z <= 1e9 < 2^30, so bits 0..30 are enough

    visited = [False] * (n + 1)
    D = [0] * (n + 1)      # XOR potential relative to component root
    A = [0] * (n + 1)

    for start in range(1, n + 1):
        if visited[start]:
            continue
        visited[start] = True
        D[start] = 0
        comp = [start]
        queue = deque([start])
        ok = True

        while queue:
            u = queue.popleft()
            du = D[u]
            for v, z in adj[u]:
                if not visited[v]:
                    visited[v] = True
                    D[v] = du ^ z
                    comp.append(v)
                    queue.append(v)
                else:
                    if (du ^ D[v]) != z:
                        ok = False

        if not ok:
            sys.stdout.write("-1\n")
            return

        s = len(comp)
        cnt = [0] * BITS
        for v in comp:
            dv = D[v]
            k = 0
            while dv:
                if dv & 1:
                    cnt[k] += 1
                dv >>= 1
                k += 1

        r = 0
        for k in range(BITS):
            if cnt[k] > s - cnt[k]:
                r |= (1 << k)

        for v in comp:
            A[v] = r ^ D[v]

    sys.stdout.write(" ".join(map(str, A[1:])) + "\n")

main()