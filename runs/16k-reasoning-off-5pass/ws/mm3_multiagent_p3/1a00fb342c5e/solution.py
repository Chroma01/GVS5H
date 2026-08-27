import sys
sys.setrecursionlimit(1 << 25)

def main():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    # Store edges
    edges = []
    for _ in range(M):
        x = int(next(it)) - 1
        y = int(next(it)) - 1
        z = int(next(it))
        edges.append((x, y, z))

    # DSU with parity (xor distance to parent)
    parent = list(range(N))
    rank = [0] * N
    # xor[v] = xor of edge labels from v to its parent
    xor_to_parent = [0] * N

    def find(v):
        if parent[v] != v:
            # path compression with xor accumulation
            orig_parent = parent[v]
            root = find(orig_parent)
            xor_to_parent[v] ^= xor_to_parent[orig_parent]
            parent[v] = root
        return parent[v]

    def union(u, v, w):
        # We want A_u XOR A_v = w
        # Let ru = find(u), rv = find(v)
        # We have: A_u = A_ru XOR xor_to_parent[u]
        #          A_v = A_rv XOR xor_to_parent[v]
        # So condition: (A_ru XOR xu) XOR (A_rv XOR xv) = w
        # => A_ru XOR A_rv = w XOR xu XOR xv
        ru = find(u)
        rv = find(v)
        xu = xor_to_parent[u]
        xv = xor_to_parent[v]
        if ru == rv:
            # Check consistency
            if (xu ^ xv) != w:
                print(-1)
                sys.exit(0)
            return
        # Union by rank
        # We need to set parent[ru] = rv (or vice versa) and adjust xor
        # Let we attach ru under rv, and set xor[ru] such that the equation holds.
        # We need: A_ru XOR xor[ru] = A_rv (so that A_ru = A_rv XOR xor[ru])
        # Actually we set the xor value stored in the child root to represent
        # the xor from the child root to the new parent.
        # We have: A_ru XOR A_rv = w XOR xu XOR xv
        # We want to set parent[ru] = rv, and define xor[ru] = (A_ru XOR A_rv)
        # So xor[ru] = w XOR xu XOR xv
        attach_xor = w ^ xu ^ xv
        if rank[ru] < rank[rv]:
            parent[ru] = rv
            xor_to_parent[ru] = attach_xor
        else:
            # If same rank, we might increase rank; but careful: if we attach rv under ru,
            # we need to compute xor[rv] accordingly.
            # Let's decide: if rank[ru] > rank[rv], attach rv under ru.
            # Compute xor[rv] = A_rv XOR A_ru = attach_xor
            # Because A_ru XOR A_rv = attach_xor => A_rv = A_ru XOR attach_xor
            # So xor[rv] = attach_xor.
            if rank[ru] > rank[rv]:
                parent[rv] = ru
                xor_to_parent[rv] = attach_xor
            else:
                # rank[ru] == rank[rv]
                parent[rv] = ru
                xor_to_parent[rv] = attach_xor
                rank[ru] += 1

    # Process edges to build DSU and detect contradictions
    for (x, y, z) in edges:
        if x == y:
            if z != 0:
                print(-1)
                sys.exit(0)
            # Self-loop with z=0 is redundant, ignore
            continue
        union(x, y, z)

    # After DSU is built, we need to compute the xor distance from each node to its component root.
    # We can do a second pass to find roots and compute dist (xor to root) for all nodes.
    # But we already have xor_to_parent after path compression. However, path compression may not have been called for all nodes.
    # We can call find(v) for all v to ensure they are compressed and we have the correct xor to root.
    # Actually after all unions, we can just call find(v) for each v, and xor_to_parent[v] will be the xor from v to its root.
    # But we also need to map each node to its root and collect dist values per component.
    
    # We'll store an array A initialized to 0.
    A = [0] * N
    
    # Group nodes by root
    # We need to collect dist[v] for each v: dist[v] = xor from v to root = xor_to_parent[v] after find(v)
    # We also need to know which root each node belongs to.
    
    # First, find root for each node and compute dist
    root_of = [0] * N
    dist = [0] * N
    # Also track which roots exist: use dict root -> list of (node, dist)
    comp_nodes = {}
    
    for v in range(N):
        r = find(v)
        root_of[v] = r
        d = xor_to_parent[v]  # After find, this is xor to root
        dist[v] = d
        if r not in comp_nodes:
            comp_nodes[r] = []
        comp_nodes[r].append((v, d))
    
    # For each component, compute minimal sum assignment
    # Two choices: root = 0 or root = F
    # where F = bitwise NOT of bitwise OR of all dists in component
    # We need to consider bits up to some max. Since Z <= 1e9, 30 bits suffice.
    # But dist can be up to that as well. We can set a mask to 2^31 - 1 to keep it within 31 bits.
    # However, the NOT of OR may have bits beyond 30 set, but we can mask to the relevant bits.
    # Actually, the optimal F is the bitwise complement of the OR of all dists, but only up to the highest bit that appears in any dist or Z.
    # Since we are dealing with non-negative integers, we can restrict to bits 0..30 (since 2^30 > 1e9).
    # But to be safe, we can compute F = (~OR) & ((1 << 31) - 1).
    # However, note that if we set root to F, then each node value is dist XOR F.
    # The sum is minimized when F is chosen as described.
    
    # For each component:
    for r, lst in comp_nodes.items():
        # Compute OR of all dists in this component
        or_val = 0
        for v, d in lst:
            or_val |= d
        # Compute F = bitwise NOT of or_val, but we must consider only bits up to some max.
        # Since d <= (1 << 30) - 1 (or maybe higher? Z <= 1e9 < 2^30, but d could be up to ~2^30-1).
        # So we can set F = (~or_val) & ((1 << 31) - 1)
        F = (~or_val) & ((1 << 31) - 1)
        # Compute sums
        S0 = 0
        S1 = 0
        for v, d in lst:
            S0 += d
            S1 += (d ^ F)
        if S0 <= S1:
            # Use root = 0
            for v, d in lst:
                A[v] = d
        else:
            # Use root = F
            for v, d in lst:
                A[v] = d ^ F
    
    # Output
    print(' '.join(map(str, A)))

if __name__ == "__main__":
    main()