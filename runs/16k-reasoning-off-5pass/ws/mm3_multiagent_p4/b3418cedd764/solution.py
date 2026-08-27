import sys
sys.setrecursionlimit(10000)
MOD = 998244353

def main():
    import sys
    sys.setrecursionlimit(10000)
    data = sys.stdin.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    A = [0] * (N + 1)
    for i in range(1, N + 1):
        A[i] = int(next(it))
    
    # Find cycles using state: 0=unvisited, 1=visiting (in current stack), 2=processed
    state = [0] * (N + 1)
    # To record nodes that are part of cycles: cycle_id[i] = id of cycle, or -1
    cycle_id = [-1] * (N + 1)
    cycles = []  # list of lists of nodes forming cycles
    
    # We'll also build children list only for non-cycle edges
    children = [[] for _ in range(N + 1)]
    # But we only add edges from a node to its parent if the edge is not part of a cycle
    # We'll need to know which edges are cycle edges. We'll store cycle_set of pairs.
    
    # First, find all cycles via DFS stack
    sys.setrecursionlimit(10000)
    def dfs(u, stack):
        state[u] = 1
        stack.append(u)
        v = A[u]
        if state[v] == 0:
            dfs(v, stack)
        elif state[v] == 1:
            # found a cycle: nodes from v to end of stack
            idx = stack.index(v)  # O(L) but sum of L^2 over all cycles could be large; we can avoid by using a dict
            # Better: maintain position dict
            pass
        # Actually, we need to avoid O(L) per cycle. Use a map node->index in stack.
        # Let's redesign: store position in current path.
        pos_in_stack = {}
        def dfs2(u):
            state[u] = 1
            pos_in_stack[u] = len(stack)
            stack.append(u)
            v = A[u]
            if state[v] == 0:
                dfs2(v)
            elif state[v] == 1:
                # cycle from v to u
                start = pos_in_stack[v]
                cycle = stack[start:]
                cid = len(cycles)
                cycles.append(cycle)
                for node in cycle:
                    cycle_id[node] = cid
            stack.pop()
            del pos_in_stack[u]
            state[u] = 2
        for i in range(1, N + 1):
            if state[i] == 0:
                dfs2(i)
    
    # The above code is messy. Let's write a clean iterative version using recursion but with a global path map.
    state = [0] * (N + 1)
    cycle_id = [-1] * (N + 1)
    cycles = []
    path_pos = {}
    path = []
    
    sys.setrecursionlimit(10000)
    def dfs(u):
        state[u] = 1
        path_pos[u] = len(path)
        path.append(u)
        v = A[u]
        if state[v] == 0:
            dfs(v)
        elif state[v] == 1:
            start = path_pos[v]
            cycle = path[start:]
            cid = len(cycles)
            cycles.append(cycle)
            for node in cycle:
                cycle_id[node] = cid
        path.pop()
        del path_pos[u]
        state[u] = 2
    
    for i in range(1, N + 1):
        if state[i] == 0:
            dfs(i)
    
    # Build children only for non-cycle edges
    # We need to add edge u -> v (meaning u is child of v) if A[u] = v and edge is not a cycle edge.
    # Determine cycle edge membership: an edge (u, A[u]) is a cycle edge iff u is in a cycle and A[u] is the next in the cycle.
    # For each cycle, we can mark the edge from each node to its successor in the cycle.
    cycle_edge = [False] * (N + 1)  # cycle_edge[u] = True if edge u->A[u] is a cycle edge
    for cycle in cycles:
        L = len(cycle)
        for idx, u in enumerate(cycle):
            nxt = cycle[(idx + 1) % L]
            if A[u] == nxt:
                cycle_edge[u] = True
            else:
                # This shouldn't happen because in a functional graph, if u is in a cycle, A[u] is the next in the cycle.
                # But just in case, treat as cycle edge anyway.
                cycle_edge[u] = True
    
    # Build children adjacency: for each node u, if not cycle edge, add u as child of A[u]
    for u in range(1, N + 1):
        if not cycle_edge[u]:
            children[A[u]].append(u)
    
    # Now we have a forest of trees rooted at cycle nodes (or isolated cycle nodes).
    # We need to compute f[u][k] for each node u in the trees (including cycle nodes? Actually, we will compute g for cycle nodes separately).
    # For tree nodes, we compute f[u][k] = number of assignments in subtree of u (excluding parent) where x_u = k.
    # For leaves: f[u][k] = 1 for all k (since only one node, any value is allowed; but wait, there is no constraint from children).
    # Actually, leaf has no children, so f[u][k] = 1 (empty product). So base is 1.
    
    # We'll compute f for all tree nodes (including those that are cycle nodes? For cycle nodes, we will later combine. But it's okay to compute f for cycle nodes as if they were tree roots; their children are the trees attached. So we can compute f for all nodes in the graph (including cycle nodes) and then treat the cycle combination separately.)
    # Actually, for cycle nodes, we don't have an edge to their successor in the cycle (since that's a cycle edge, excluded). So the children list for a cycle node is exactly the trees attached. So f[cycle_node][k] correctly counts assignments of the attached tree given x_cycle_node = k.
    
    # So we compute f for all nodes. Since the graph is a functional graph with cycles removed, it's a DAG (forest) with edges from child to parent. We can process in reverse topological order. Since it's a tree, we can do a simple DFS from each node (or from cycle nodes) and compute bottom-up.
    
    # We'll compute f[u] as a list of length M+1 (1-indexed). We'll store as Python list of ints.
    f = [None] * (N + 1)
    
    # Process nodes in reverse order of a topological sort of the forest.
    # Since the graph is a forest of trees rooted at cycle nodes, we can just do a post-order DFS from each cycle node.
    # But there may be nodes not in cycles? Actually every node is either in a cycle or leads to a cycle. So all nodes are in trees rooted at cycle nodes. So we can just do a post-order DFS from each cycle node, covering all nodes exactly once.
    
    # We'll use a stack to do iterative post-order: push (node, state=0), when state=0, push children then mark state=1. But simpler: use recursion (with increased limit) since N<=2025.
    sys.setrecursionlimit(10000)
    def compute(u):
        # compute f[u][1..M]
        # base: list of 1's
        if not children[u]:
            f[u] = [1] * (M + 1)
            return
        # For each child, we need prefix sums of f[child]
        # We'll compute for each k, the product of prefix sums over children.
        # Approach: initialize f[u][k] = 1 for all k, then for each child c, update f[u][k] = f[u][k] * (sum_{t=1}^k f[c][t]) mod MOD.
        # Since M is small, we can do O(degree * M).
        # We'll first compute f for all children recursively.
        for c in children[u]:
            compute(c)
        # Now compute f[u]
        fu = [1] * (M + 1)
        # We can compute prefix product? Not directly because product of prefix sums. But we can iterate children and update.
        for c in children[u]:
            fc = f[c]
            # compute prefix sums of fc
            # We'll accumulate product
            # For each k from 1 to M:
            #   fu[k] = fu[k] * (sum_{t=1}^k fc[t]) % MOD
            # We can precompute prefix sums of fc to avoid O(M^2).
            prefix = [0] * (M + 1)
            s = 0
            for k in range(1, M + 1):
                s = (s + fc[k]) % MOD
                prefix[k] = s
            # Now update fu
            for k in range(1, M + 1):
                fu[k] = fu[k] * prefix[k] % MOD
        f[u] = fu
    
    # Compute f for all nodes
    for i in range(1, N + 1):
        if f[i] is None:
            compute(i)
    
    # Now combine for each cycle.
    ans = 1
    for cycle in cycles:
        # For each v from 1 to M, compute product over cycle nodes of f[node][v]
        total = 0
        # We can compute for each v the product, then sum.
        # To be efficient, we can iterate v from 1 to M and compute product.
        # But M=2025, L up to N, so O(L * M) is fine.
        for v in range(1, M + 1):
            prod = 1
            for u in cycle:
                prod = prod * f[u][v] % MOD
            total = (total + prod) % MOD
        ans = ans * total % MOD
    
    print(ans)

if __name__ == "__main__":
    main()