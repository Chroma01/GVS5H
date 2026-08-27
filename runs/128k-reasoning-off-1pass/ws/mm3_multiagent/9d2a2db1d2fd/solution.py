import sys
sys.setrecursionlimit(1 << 25)
input = sys.stdin.readline

def main():
    H, W = map(int, input().split())
    F = [list(map(int, input().split())) for _ in range(H)]
    
    # Build merge tree using union-find
    # Sort cells by height descending
    cells = []
    for i in range(H):
        for j in range(W):
            cells.append((F[i][j], i, j))
    cells.sort(reverse=True)
    
    # Union-Find structure
    parent_uf = [[(i, j) for j in range(W)] for i in range(H)]
    
    def find(x):
        i, j = x
        if parent_uf[i][j] != (i, j):
            parent_uf[i][j] = find(parent_uf[i][j])
        return parent_uf[i][j]
    
    # Tree storage
    max_nodes = H * W * 3 + 10
    weight = [0] * max_nodes
    children = [[] for _ in range(max_nodes)]
    leaf_id = [[-1] * W for _ in range(H)]
    
    # Assign leaf IDs
    node_counter = 0
    for i in range(H):
        for j in range(W):
            leaf_id[i][j] = node_counter
            weight[node_counter] = F[i][j]
            node_counter += 1
    
    # Active cells
    active = [[False] * W for _ in range(H)]
    # set_node maps a set root (i,j) to the current tree node ID
    set_node = [[0] * W for _ in range(H)]
    for i in range(H):
        for j in range(W):
            set_node[i][j] = leaf_id[i][j]
    
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    # Process cells in descending height order
    for h, i, j in cells:
        active[i][j] = True
        for di, dj in dirs:
            ni, nj = i + di, j + dj
            if 0 <= ni < H and 0 <= nj < W and active[ni][nj]:
                ri = find((i, j))
                rj = find((ni, nj))
                if ri != rj:
                    # Get tree node IDs of the two components
                    n1 = set_node[ri[0]][ri[1]]
                    n2 = set_node[rj[0]][rj[1]]
                    # Create new internal node with weight h
                    weight[node_counter] = h
                    children[node_counter] = [n1, n2]
                    # Union the sets
                    parent_uf[ri[0]][ri[1]] = rj
                    # Update set_node for the merged component
                    set_node[rj[0]][rj[1]] = node_counter
                    node_counter += 1
    
    # Find root of the tree
    final_root = find((0, 0))
    tree_root = set_node[final_root[0]][final_root[1]]
    N = node_counter
    
    # Preprocess LCA with binary lifting
    LOG = 20
    depth = [0] * N
    par = [[-1] * N for _ in range(LOG)]
    
    # Iterative DFS from tree root
    stack = [(tree_root, 0, -1)]
    visited = [False] * N
    while stack:
        v, d, p = stack.pop()
        if visited[v]:
            continue
        visited[v] = True
        depth[v] = d
        par[0][v] = p
        for c in children[v]:
            stack.append((c, d + 1, v))
    
    for k in range(1, LOG):
        for v in range(N):
            if par[k-1][v] != -1:
                par[k][v] = par[k-1][par[k-1][v]]
    
    def lca(u, v):
        if depth[u] < depth[v]:
            u, v = v, u
        diff = depth[u] - depth[v]
        bit = 0
        while diff:
            if diff & 1:
                u = par[bit][u]
            diff >>= 1
            bit += 1
        if u == v:
            return u
        for k in range(LOG - 1, -1, -1):
            if par[k][u] != par[k][v]:
                u = par[k][u]
                v = par[k][v]
        return par[0][u]
    
    # Process queries
    Q = int(input())
    out = []
    for _ in range(Q):
        A, B, Y, C, D, Z = map(int, input().split())
        A -= 1
        B -= 1
        C -= 1
        D -= 1
        u = leaf_id[A][B]
        v = leaf_id[C][D]
        ancestor = lca(u, v)
        h = weight[ancestor]
        ans = max(abs(Y - Z), max(0, Y - h) + max(0, Z - h))
        out.append(str(ans))
    
    print('\n'.join(out))

if __name__ == "__main__":
    main()