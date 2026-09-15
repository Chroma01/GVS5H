import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    pos = 0
    n = int(data[pos]); pos += 1
    m = int(data[pos]); pos += 1

    adj = [[] for _ in range(n + 1)]
    for _ in range(m):
        x = int(data[pos]); y = int(data[pos + 1]); z = int(data[pos + 2]); pos += 3
        adj[x].append((y, z))
        if x != y:
            adj[y].append((x, z))

    p = [-1] * (n + 1)          # p[v] = A_v XOR A_root of its component
    compid = [-1] * (n + 1)
    comps = []
    ok = True

    for s in range(1, n + 1):
        if p[s] != -1:
            continue
        ci = len(comps)
        p[s] = 0
        compid[s] = ci
        comp = [s]
        stack = [s]
        while stack:
            u = stack.pop()
            pu = p[u]
            for (v, w) in adj[u]:
                exp = pu ^ w
                pv = p[v]
                if pv == -1:
                    p[v] = exp
                    compid[v] = ci
                    comp.append(v)
                    stack.append(v)
                elif pv != exp:
                    ok = False
        comps.append(comp)

    if not ok:
        sys.stdout.write("-1\n")
        return

    # Choose each component's root value bit-by-bit (bits are independent).
    rootval = [0] * len(comps)
    for k in range(31):          # bit 0..30 (Z <= 1e9 < 2^30)
        bit = 1 << k
        for ci in range(len(comps)):
            comp = comps[ci]
            cnt = 0
            for v in comp:
                if p[v] & bit:
                    cnt += 1
            # root bit 0 -> cnt ones; root bit 1 -> size-cnt ones; pick fewer
            if cnt > len(comp) - cnt:
                rootval[ci] |= bit

    out = []
    for v in range(1, n + 1):
        out.append(p[v] ^ rootval[compid[v]])
    sys.stdout.write(' '.join(map(str, out)))
    sys.stdout.write('\n')

main()