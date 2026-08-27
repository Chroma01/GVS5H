import sys

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    H = int(data[0])
    W = int(data[1])
    rows = data[2:2+H]
    n = 1 << W
    f = [0] * n
    for r in rows:
        mask = 0
        for j, ch in enumerate(r):
            if ch == '1':
                mask |= 1 << j
        f[mask] += 1
    
    # Compute g(x) = min(popcount(x), W - popcount(x))
    g = [0] * n
    for x in range(n):
        pc = bin(x).count('1')
        g[x] = min(pc, W - pc)
    
    # FWHT using floats (safe for W <= 18)
    f_float = [float(x) for x in f]
    g_float = [float(x) for x in g]
    
    def fwht_float(a, invert):
        n = len(a)
        h = 1
        while h < n:
            for i in range(0, n, h * 2):
                for j in range(h):
                    u = a[i + j]
                    v = a[i + j + h]
                    a[i + j] = u + v
                    a[i + j + h] = u - v
            h <<= 1
        if invert:
            inv_n = 1.0 / n
            for i in range(n):
                a[i] *= inv_n
    
    fwht_float(f_float, False)
    fwht_float(g_float, False)
    
    for i in range(n):
        f_float[i] *= g_float[i]
    
    fwht_float(f_float, True)
    
    ans = min(int(round(x)) for x in f_float)
    print(ans)

solve()