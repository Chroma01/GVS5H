import sys
from collections import deque

def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    N = int(data[idx]); idx += 1
    M = int(data[idx]); idx += 1

    adj = [[] for _ in range(N + 1)]
    for _ in range(M):
        x = int(data[idx]); y = int(data[idx + 1]); z = int(data[idx + 2])
        idx += 3
        adj[x].append((y, z))
        adj[y].append((x, z))

    p = [0] * (N + 1)          # xor-potential relative to component root
    comp = [-1] * (N + 1)      # component id
    comp_vertices = []         # list of vertex lists per component
    ok = True

    for start in range(1, N + 1):
        if comp[start] != -1:
            continue
        cid = len(comp_vertices)
        comp[start] = cid
        p[start] = 0
        dq = deque([start])
        verts = [start]
        while dq and ok:
            u = dq.popleft()
            pu = p[u]
            for v, z in adj[u]:
                need = pu ^ z
                if comp[v] == -1:
                    comp[v] = cid
                    p[v] = need
                    verts.append(v)
                    dq.append(v)
                else:
                    if p[v] != need:
                        ok = False
                        break
        if not ok:
            break
        comp_vertices.append(verts)

    if not ok:
        sys.stdout.write("-1\n")
        return

    ans = [0] * (N + 1)
    for verts in comp_vertices:
        s = len(verts)
        # count ones per bit
        cnt = [0] * 30
        for v in verts:
            x = p[v]
            b = 0
            while x:
                if x & 1:
                    cnt[b] += 1
                x >>= 1
                b += 1
        # choose flip constant t: bit set iff flipping reduces ones
        t = 0
        for b in range(30):
            if cnt[b] > s - cnt[b]:
                t |= (1 << b)
        for v in verts:
            ans[v] = p[v] ^ t

    sys.stdout.write(" ".join(str(ans[i]) for i in range(1, N + 1)) + "\n")

main()