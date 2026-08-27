import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    adj = [[] for _ in range(N + 1)]
    edges = []
    for _ in range(M):
        x = int(next(it)); y = int(next(it)); z = int(next(it))
        adj[x].append((y, z))
        adj[y].append((x, z))
        edges.append((x, y, z))

    d = [0] * (N + 1)       # XOR distance from component root
    comp = [-1] * (N + 1)   # component id
    comp_sizes = []
    comp_bits = []          # per-component bit counts
    comp_members = []       # store members to avoid second pass
    ncomp = 0

    for s in range(1, N + 1):
        if comp[s] != -1:
            continue
        cid = ncomp
        ncomp += 1
        stack = [s]
        comp[s] = cid
        d[s] = 0
        members = [s]
        while stack:
            u = stack.pop()
            for v, z in adj[u]:
                if comp[v] == -1:
                    comp[v] = cid
                    d[v] = d[u] ^ z
                    stack.append(v)
                    members.append(v)
        comp_sizes.append(len(members))
        comp_members.append(members)
        # count bits (31 bits covers Z <= 1e9 < 2^30)
        bits = [0] * 31
        for v in members:
            dv = d[v]
            b = 0
            while dv:
                if dv & 1:
                    bits[b] += 1
                dv >>= 1
                b += 1
        comp_bits.append(bits)

    # consistency check
    for x, y, z in edges:
        if (d[x] ^ d[y]) != z:
            sys.stdout.write("-1\n")
            return

    # choose root value per component minimizing sum
    ans = [0] * (N + 1)
    for cid in range(ncomp):
        size = comp_sizes[cid]
        bits = comp_bits[cid]
        r = 0
        for b in range(31):
            c = bits[b]
            # root bit = 0 -> c vertices have bit set
            # root bit = 1 -> size - c vertices have bit set
            if size - c < c:
                r |= (1 << b)
        for v in comp_members[cid]:
            ans[v] = r ^ d[v]

    out = ' '.join(str(ans[i]) for i in range(1, N + 1))
    sys.stdout.write(out + "\n")

main()