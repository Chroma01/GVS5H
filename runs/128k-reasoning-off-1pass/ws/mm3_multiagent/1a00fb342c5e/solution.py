import sys

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    
    parent = list(range(N + 1))
    xor_to_parent = [0] * (N + 1)
    
    def find(x):
        if parent[x] != x:
            orig_parent = parent[x]
            root, xor_up = find(orig_parent)
            parent[x] = root
            xor_to_parent[x] ^= xor_up
        return parent[x], xor_to_parent[x]
    
    inconsistent = False
    for _ in range(M):
        x = int(next(it))
        y = int(next(it))
        z = int(next(it))
        if inconsistent:
            continue
        if x == y:
            if z != 0:
                inconsistent = True
            continue
        rx, vx = find(x)
        ry, vy = find(y)
        if rx == ry:
            if (vx ^ vy) != z:
                inconsistent = True
        else:
            # attach rx under ry
            parent[rx] = ry
            xor_to_parent[rx] = vx ^ vy ^ z
    
    if inconsistent:
        print(-1)
        return
    
    # Group nodes by component root
    comps = {}
    for i in range(1, N + 1):
        r, v = find(i)
        if r not in comps:
            comps[r] = []
        comps[r].append((i, v))
    
    A = [0] * (N + 1)
    BITS = 31  # enough for 0..2^30
    
    for root, nodes in comps.items():
        size = len(nodes)
        cnt1 = [0] * BITS
        for _, v in nodes:
            for b in range(BITS):
                cnt1[b] += (v >> b) & 1
        c = 0
        for b in range(BITS):
            if cnt1[b] * 2 > size:  # more ones than zeros -> set this bit to 1
                c |= (1 << b)
        for idx, v in nodes:
            A[idx] = v ^ c
    
    # Output
    out = ' '.join(str(A[i]) for i in range(1, N + 1))
    sys.stdout.write(out)

if __name__ == "__main__":
    solve()