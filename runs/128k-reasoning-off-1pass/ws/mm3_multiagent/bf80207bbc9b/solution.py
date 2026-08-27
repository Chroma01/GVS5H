import sys

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    H = int(data[0])
    W = int(data[1])
    rows = data[2:]
    # Ensure we have exactly H rows
    rows = rows[:H]
    
    N = 1 << W
    cnt = [0] * N
    for s in rows:
        val = int(s, 2)
        cnt[val] += 1
    
    # Precompute g[mask] = min(popcount(mask), W - popcount(mask))
    g = [0] * N
    for mask in range(N):
        pc = bin(mask).count('1')
        g[mask] = min(pc, W - pc)
    
    # FWHT for XOR convolution
    # We'll transform both arrays in-place
    f = cnt[:]  # frequency array
    h = g[:]    # weight array
    
    # Perform FWHT on both
    for arr in (f, h):
        step = 1
        while step < N:
            for i in range(0, N, step * 2):
                for j in range(step):
                    u = arr[i + j]
                    v = arr[i + j + step]
                    arr[i + j] = u + v
                    arr[i + j + step] = u - v
            step <<= 1
    
    # Pointwise multiply
    for i in range(N):
        f[i] *= h[i]
    
    # Inverse FWHT
    step = 1
    inv2 = pow(2, -1, 1_000_000_007)  # not needed for integer division, we'll divide by N
    while step < N:
        for i in range(0, N, step * 2):
            for j in range(step):
                u = f[i + j]
                v = f[i + j + step]
                f[i + j] = u + v
                f[i + j + step] = u - v
        step <<= 1
    
    # Divide by N (since XOR convolution's inverse FWHT doesn't include normalization)
    # The result should be integer
    ans = min(f[i] // N for i in range(N))
    print(ans)

if __name__ == "__main__":
    solve()