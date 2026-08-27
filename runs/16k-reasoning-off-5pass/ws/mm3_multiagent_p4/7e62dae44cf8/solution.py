import sys

def solve():
    data = sys.stdin.read().split()
    it = iter(data)
    H = int(next(it))
    W = int(next(it))
    X = int(next(it))
    P = int(next(it)) - 1
    Q = int(next(it)) - 1
    S = [[0]*W for _ in range(H)]
    for i in range(H):
        for j in range(W):
            S[i][j] = int(next(it))
    
    N = H * W
    parent = list(range(N))
    size = [1]*N
    comp_sum = [0]*N
    active = [False]*N
    
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    
    def union(a, b):
        ra = find(a)
        rb = find(b)
        if ra == rb:
            return ra
        if size[ra] < size[rb]:
            ra, rb = rb, ra
        parent[rb] = ra
        size[ra] += size[rb]
        comp_sum[ra] += comp_sum[rb]
        return ra
    
    start_id = P * W + Q
    active[start_id] = True
    comp_sum[start_id] = S[P][Q]
    
    # Build list of all cells with (value, id)
    cells = []
    for i in range(H):
        for j in range(W):
            cells.append((S[i][j], i, j))
    cells.sort()
    
    # Directions
    dirs = [(-1,0),(1,0),(0,-1),(0,1)]
    
    for v, i, j in cells:
        idx = i * W + j
        if not active[idx]:
            active[idx] = True
            comp_sum[idx] = v
        # Check neighbors
        for di, dj in dirs:
            ni, nj = i + di, j + dj
            if 0 <= ni < H and 0 <= nj < W:
                nidx = ni * W + nj
                if active[nidx]:
                    # Check if current cell can be absorbed by neighbor's component
                    # Condition: v < comp_sum[neighbor_root] / X
                    # Equivalent: v * X < comp_sum[neighbor_root]
                    r_nei = find(nidx)
                    if v * X < comp_sum[r_nei]:
                        # Merge current cell into neighbor's component
                        r_cur = find(idx)
                        # Ensure we merge correctly; the neighbor's component must be the one that absorbs
                        # Since v <= comp_sum[r_nei] (processing in ascending order),
                        # the neighbor's component strength is >= v, so it can absorb current cell.
                        new_root = union(r_nei, r_cur)
                        # The new root's comp_sum is already updated inside union
                        # No need to do anything else
                        pass
    
    # Answer: strength of the component containing the start cell
    root = find(start_id)
    print(comp_sum[root])

if __name__ == "__main__":
    solve()