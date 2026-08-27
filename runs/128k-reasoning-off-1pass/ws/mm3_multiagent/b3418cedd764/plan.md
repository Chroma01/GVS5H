We need to count assignments `x_i ∈ [1, M]` such that `x_i ≤ x_{A_i}` for all `i`.  
The condition `x_i ≤ x_{A_i}` forms a directed graph where each node points to its parent `A_i`. Each connected component is a functional graph (each node has outdegree 1), so its structure is a collection of rooted trees (reverse edges) attached to cycles.  
For a tree rooted at `r`, the condition enforces a non-decreasing constraint from root to leaves: if a node is a child of `p`, then `x_child ≤ x_parent`. This forces the values along any root-to-leaf path to be non-increasing, so the maximal value must be at the root, and the root can be any of the M values.  
We can DP on each tree: treat the value of the root as the maximum, and count assignments for each possible root value `v ∈ [1, M]`. For a node, its contribution given its parent's value is the number of ways to assign it a value `≤` parent's value. This becomes a tree DP that, for a given node, produces a polynomial in the parent's value (in terms of `v = x_parent`). The final count for the component is the sum over `v` of (ways from root with value `v`).

To handle this efficiently for `N, M ≤ 2025`, we do DP on each tree, computing for each node a polynomial `f_node(k) = number of ways to assign the subtree of `node` given that the value of `node` is exactly k`. We can store `f_node` as an array of length M. Merging children uses prefix sums. For a leaf, `f_leaf(k) = 1` for all `k`. For an internal node with children, `f_node(k) = (Π_{child} ( Σ_{j=1..k} f_child(j) ))`. Since `M` is up to 2025, naive O(N·M·degree) per node is acceptable: total O(N·M). After DP on trees, we attach them to the cycles.

For a cycle, each node is a root of its own tree (the trees hanging off the cycle). We have a cycle of length `L`. For each node `i` on the cycle, we have a function `g_i(k) = number of assignments of its attached tree when the cycle node's value is exactly k`. We need to count assignments `(y_1,...,y_L)` of the cycle nodes' values such that `y_i ≤ y_{next(i)}` (i.e., non-decreasing along the cycle) and total ways = Π_i g_i(y_i). This is a DP on the cycle: we can break the cycle at some edge, DP from the first node to the last, where the state is the chosen value for the previous node, and we sum over valid next values. Complexity O(L·M²) which is too slow if L is large. However, constraints are up to 2025, so O(N·M²) in worst case is ~4 million, which is fine. Actually M is up to 2025, so M² is ~4e6, times N up to 2025 could be ~8e9, which is too slow. But we can optimize: the DP on a cycle is like a convolution. Alternatively, we can treat the whole structure as a set of constraints. Another approach: topological order? Not possible because of cycles.

Alternative: Use inclusion–exclusion or generating functions? The condition `x_i ≤ x_{A_i}` is equivalent to: for each edge `i → A_i`, `x_i ≤ x_{A_i}`. This is a partial order constraint if the graph were a DAG. With cycles, we need all `x_i` on a cycle to be equal? Not necessarily: the cycle can have different values as long as they are non-decreasing around the cycle, which forces all values on the cycle to be equal. Indeed, if `y_1 ≤ y_2 ≤ ... ≤ y_L ≤ y_1` (since it's a cycle), then all inequalities must be equalities, so all `y_i` must be the same. Therefore, on any cycle, all values must be equal. Great! So for a cycle of length L, the cycle nodes must all have the same value `v`. For each cycle node, we multiply the number of ways to assign its attached tree given its value is `v`. But we must also satisfy the edge from the last node to the first: since values are equal, that condition is automatically satisfied. So the number of assignments for a cycle component is: sum over `v=1..M` of ( Π_{i in cycle} g_i(v) ). This is O(M·L) per cycle. We can compute it by precomputing for each `v` the product of `g_i(v)` over cycle nodes, and sum. But we can also compute the product for all `v` in O(M·L) by iterating nodes and maintaining a running product array.

Thus the overall algorithm:
1. Build the graph. For each node, find its cycle. Use standard algorithm: find nodes in cycles via indegree reduction (Kahn's algorithm) or DFS.
2. The graph consists of several components, each with exactly one directed cycle. Each non-cycle node is a tree rooted at a cycle node.
3. For each component, process the trees attached to cycle nodes. For each node not in a cycle, compute its DP array `f_node[1..M]` as described: `f_node[v] = Π_{child c} ( Σ_{j=1..v} f_c[j] )`. Process nodes in reverse topological order from leaves upward.
4. For each cycle node `r`, we already computed `f_r` (if it has children) which is the number of ways to assign its attached tree given that the cycle node itself has value `v`. So the number of ways for the whole component is `sum_{v=1..M} ( Π_{r in cycle} f_r[v] )`. We can compute this by initializing an array `prod[v] = 1` for `v=1..M`, then for each cycle node `r`, multiply `prod[v] *= f_r[v]` for all `v`, then sum `prod[v]` and add to answer.
5. Answer is sum of these sums over all components, modulo 998244353.

Time complexity: For each node, we compute its DP. The DP for a node with `d` children involves for each child computing a prefix sum array (which we can precompute for each child to avoid repeated work), then multiplying. But if we just do the naive product, for a node we do: for each value `v`, multiply over children the prefix sum of child's f up to v. We can precompute prefix sums of each child's f, say `pc_c[v] = Σ_{j=1..v} f_c[j]`. Then for the node, `f_node[v] = Π_{c} pc_c[v]`. We can compute this for all `v` by iterating `v` from 1 to M, maintaining a running product: start with `1`, for each child `c`, multiply by `pc_c[v]`. That's O(degree * M) per node. Summing over all nodes, each edge is considered once (from parent to child), so total O(N*M). Good.

We need to be careful with the order: we must compute children's f before parent's f. This is a reverse topological order. Since we removed cycle nodes, the remaining graph is a DAG (a forest of trees). We can process nodes in reverse topological order (e.g., using the order from Kahn's algorithm). We can store an order of nodes not in cycles: start from leaves, go up. We can do a BFS from leaves: since we already have indegrees (considering only edges within the tree part), we can push leaves (nodes with no children in the tree? Wait, edges are from child to parent? Let's define the graph: we have directed edge i → A_i. For tree nodes, they are not in a cycle, so following edges eventually leads to a cycle. So if we consider the reverse edges (i.e., from A_i to i), the tree structure is a rooted tree where root is a cycle node. We can build the reverse adjacency list: for each node, list of children (nodes that point to it). Then for tree nodes, we process from leaves (nodes with no children) up to the cycle node. The cycle nodes are not processed in this step; they will be handled when combining the cycle.

Actually, we need f values for all nodes, including cycle nodes, but for cycle nodes, the DP also includes their children. So we can compute f for all nodes in the trees, and for cycle nodes we will combine the children's f to get f_cycle_node. So we can treat cycle nodes as roots of their trees. We can compute f for all nodes using a DFS or iterative post-order on the tree. Since the tree size is N minus number of cycle nodes, and M is up to 2025, we can do recursion if depth is not too big, but N can be 2025, recursion depth might be okay in Python with increased recursion limit, but we can also do iterative.

Plan for DP computation:
- After finding the set of cycle nodes (using indegree elimination), we have the remaining nodes. For each non-cycle node, its parent is A_i. We can process nodes in reverse topological order: start from nodes that have no children in the reverse graph (i.e., nodes with outdegree 0 in the original graph? Actually, original graph: each node has exactly one outgoing edge. In the reverse graph, a node can have many outgoing edges (to its children). Leaves in the tree are nodes that have no children, i.e., no node points to them except possibly their parent? Wait, in the reverse graph, edges are from parent to child. So a leaf in the tree is a node that has no children, meaning no other node has A_i = this node. So we can find leaves by counting in-degree in the reverse graph. Alternatively, we can simply do a DFS from cycle nodes, computing f recursively.

We can do recursive DFS with memoization. For each node, compute f_node(v) for v=1..M.
- If node is a leaf (no children), f_node(v) = 1.
- Else, recursively compute f_child for all children. Then precompute prefix sums for each child: pc_child[v] = (pc_child[v-1] + f_child[v]) % MOD.
- Then for v in 1..M: f_node[v] = product over children of pc_child[v] % MOD.
- Return f_node.

We need to be careful about recursion depth: N ≤ 2025, so it's fine. We'll set recursionlimit.

Now, for the cycle combination: For each component, we have a cycle. We can find the cycle by starting from any node in the component and following A_i until we revisit a node. Since the graph is functional, each component has exactly one cycle. We can do a DFS to find the cycle: maintain visited states (0=unvisited, 1=visiting, 2=visited). When we find a back edge to a node in state 1, we have found a cycle. We can collect the cycle nodes.

Alternatively, we already know the cycle nodes from the indegree elimination: the nodes that were not removed are exactly the nodes in cycles. But we also need to group them into cycles (each component's cycle). We can pick an unvisited cycle node, follow A_i until we return to it, collecting nodes. This works because each component has exactly one cycle, and all cycle nodes are in the same cycle. So we can group them.

Steps in detail:
1. Read N, M, A (1-indexed).
2. Build array A. For each i, parent = A[i].
3. Find cycle nodes:
   - Compute indegree for each node (considering edges i -> A[i]).
   - Initialize a queue with nodes having indegree 0.
   - While queue not empty: pop u, mark as not in cycle, let p = A[u], decrement indegree of p, if indegree of p becomes 0, push p.
   - After this, nodes with indegree > 0 are in cycles.
4. For each node not in a cycle, we will compute f. For cycle nodes, we also compute f (but their f will be used in cycle combination).
5. Build reverse adjacency list: for each i, add i to children[A[i]]. But only for non-cycle nodes? Actually, we need children for all nodes to compute f, because a cycle node can have tree children. So we include all nodes: for i from 1 to N, if A[i] != i? But we can just add i to children[A[i]] for all i. However, cycle nodes are part of a cycle, so they also have children (the trees attached to them). So we include all.
6. Compute f for all nodes via DFS from cycle nodes? Actually, we can compute f for all nodes in the trees, but we need f for cycle nodes as well. Since cycle nodes may have children, we can compute their f similarly. But careful: a cycle node's f depends on its children, but not on its cycle neighbors. So we can compute f for all nodes by doing a DFS that stops at cycle nodes? Actually, cycle nodes are not roots of trees; they are part of a cycle. But we can still compute their f by considering only their children (which are not in cycles). So we can define a function compute_f(u) that computes f for node u assuming u is not part of a cycle, or if it is, we still compute f based on its children (which are not in cycles). But we must ensure we don't follow cycle edges. So in the DFS, when we are at a node u, we only recursively call for children that are not in cycles? Actually, children of a cycle node are never in cycles (by definition, because cycles are only the cycle nodes). So it's safe: for any node, its children (nodes v such that A[v] = u) are either in a cycle or not. If v is in a cycle, then u is also in a cycle (since the edge is part of a cycle). So for a cycle node, its children are never in cycles. For a non-cycle node, its children are also not in cycles. So we can simply compute f for all nodes by DFS, but we must avoid infinite recursion: if we call compute_f on a cycle node, it will compute f for its children, but not follow its parent (which is also a cycle node). We need to ensure that we don't recursively call compute_f on a cycle node from another cycle node. So we can do: for each node that is not in a cycle, we can compute f in a bottom-up order. Alternatively, we can do a DFS from cycle nodes that only goes into non-cycle nodes. That is, we can start a DFS from each cycle node, but only traverse edges in the reverse direction (i.e., to children), and only go to non-cycle nodes. That will cover all non-cycle nodes exactly once, because each non-cycle node belongs to exactly one such tree (attached to a cycle node). So we can do:
   - For each cycle node c, run a DFS (or iterative) that computes f for all nodes in its tree, including c. In the DFS, we only go to children that are not cycle nodes. So we can define a recursive function that takes u, and if u is a leaf (no children), f[u] = [1]*M. Else, for each child v (where v is in children[u] and not in cycle), recursively compute f[v], then compute f[u].
   - But careful: we need f for the cycle node c as well, so we must compute it after computing f for all its descendants. So we can do a post-order traversal.

We can do it iteratively: for each component, we have a set of tree nodes. We can process them in reverse topological order: start from leaves (nodes with no children that are non-cycle). We can find leaves by looking at children count among non-cycle nodes. Alternatively, we can just do a recursive DFS with memoization; since the tree depth is at most N, recursion is fine. We'll need to pass the cycle node set to avoid going into cycles.

So algorithm for computing f:
- is_cycle = array of bool.
- children = list of lists for reverse adjacency (1-indexed).
- For each node, we will store an array f of length M (0-indexed for v=0..M-1, but we use 1-indexed for clarity). We can use 0-indexed internally: f[v-1] corresponds to value v.
- Define a function get_f(u): if f[u] is already computed, return it. Otherwise:
   - If u is a leaf in the tree (i.e., no children that are not in cycles), then f[u] = [1] * M.
   - Else, for each child v in children[u]:
        if not is_cycle[v]: (actually, we can just call get_f(v) because if v is in cycle, we shouldn't be calling from u if u is not in cycle? But wait, if u is not in cycle, it can have a child that is in a cycle? No, because if v is in cycle, then A[v] = u, but then u is in the cycle as well (since cycle is strongly connected). Actually, it's possible that a cycle node points to a non-cycle node? No, by definition, if v is in a cycle, following A from v eventually returns to v, so all nodes in that path are in the cycle. So if A[v] = u and v is in cycle, then u is in the cycle. So a non-cycle node cannot have a child that is in a cycle. So for any node, its children (nodes that point to it) are either all in cycles or all not? Actually, a node can have children that are in cycles only if the node itself is in a cycle. Because if a child v is in a cycle, then A[v] = u, so u is in the cycle. So only cycle nodes can have children that are in cycles. But wait, a cycle node can have children that are in cycles? That would mean two cycles connected, but the graph is functional, so each node has exactly one outgoing edge, so cycles are disjoint. So a cycle node cannot have a child that is in a different cycle. And it cannot have a child that is in the same cycle because that would mean the cycle is not a simple cycle? Actually, in a functional graph, a cycle is a set of nodes where each node points to the next, and no other edges go into the cycle from outside? Actually, nodes outside the cycle can point into the cycle, but nodes in the cycle only point to other nodes in the cycle. So a cycle node's children (nodes that point to it) can be either in the cycle (only its predecessor in the cycle) or not in the cycle (trees attached). So when we compute f for a cycle node, we must consider only its children that are not in the cycle, because the child that is in the cycle is part of the cycle and will be handled in the cycle combination. So we need to exclude cycle nodes from the tree children. So in get_f(u), we should only consider children v such that v is not in cycle. Because if v is in cycle, then the edge v -> u is part of the cycle, and we don't want to include it in the tree DP. So we filter out cycle children.

Thus, for any node u, when computing f[u], we only consider children v where not is_cycle[v]. This works for both cycle and non-cycle nodes. For a non-cycle node, all its children are non-cycle (as argued). For a cycle node, we exclude the one child that is in the cycle (its predecessor in the cycle). So we can compute f for all nodes using the same recursive function, provided we only recurse on non-cycle children. But we must avoid infinite recursion: if we call get_f on a cycle node, it will compute f for its non-cycle children, and then combine. It will not call get_f on cycle nodes because we filter them out. So it's safe.

But we need to be careful: when we call get_f on a cycle node, we might have already computed f for that node? We can compute f for all nodes exactly once. Since the graph of non-cycle nodes is a forest, we can compute f for all nodes by a DFS from cycle nodes. So we can do:
   For each node u in 1..N:
       if not computed_f[u]:
           compute_f(u)
But we must ensure that when we call compute_f(u), we don't call it on a cycle node from a non-cycle node. Actually, compute_f(u) will only call compute_f on its non-cycle children. So if we start from a cycle node, it will compute f for that cycle node and all nodes in its tree. But what about a non-cycle node that is not reachable from any cycle node? That can't happen because every non-cycle node eventually leads to a cycle. So we can just iterate over all nodes and call compute_f if not computed. But we need to avoid stack overflow on deep trees. With N=2025, it's fine.

We'll implement compute_f(u) as:
   if computed[u]: return
   Let child_list = [v for v in children[u] if not is_cycle[v]]
   If child_list is empty: f[u] = [1] * M
   Else:
       for v in child_list: compute_f(v)
       Precompute prefix sums for each child: for each v, prefix_v = [0]*M, for i in range(M): prefix_v[i] = (prefix_v[i-1] + f[v][i]) % MOD
       Then f[u][i] = product over v in child_list of prefix_v[i] % MOD
   computed[u] = True

We need to store f as a list of length M for each node. Since N and M are up to 2025, storing N*M integers is about 4 million, which is okay in memory (about 32 MB if using Python integers? Actually Python integers are objects, so memory could be high. But 2025*2025 = 4,100,625, each integer in Python is 28 bytes, so about 115 MB, might be borderline. We need to be memory efficient. We can use array of ints or use numpy? But we are in Python, we can use list of lists. But 4 million Python integers is about 4e6 * 28 = 112 MB, plus overhead for lists, might be too much. However, we can optimize: we don't need to store f for all nodes simultaneously. We can compute f for each tree and combine into the cycle, then discard the f arrays for that tree? But we need f for each node to compute its parent's f. So we need to keep f for all nodes until the parent's f is computed. In a tree, we can compute f from leaves up, and after computing f for a node, we don't need its children's f anymore. But since we compute recursively, we could compute f for a node and then let the children's f be garbage collected. But in Python, they might be kept if we store them in a list. We can avoid storing f for all nodes by doing a post-order traversal that returns the f array. But then we need to store f for each node until the parent is processed. In a tree, the parent is processed after children, so we can return the f array from the child to the parent, and then the child doesn't need to keep it. So we can write a function that returns the f array, and the parent will use it to compute its own f. But then we need to store the returned f arrays in the parent during computation. We can do that by having the children return their f arrays, and the parent computes its own f and returns it, and the children's f arrays can be freed after the parent uses them. However, in Python, if we do recursion, the local variables go out of scope. So we can implement it as:

def dfs(u):
    child_fs = []
    for v in children[u]:
        if not is_cycle[v]:
            child_fs.append(dfs(v))
    if not child_fs:
        return [1] * M
    else:
        # compute prefix sums for each child
        prefixes = []
        for cf in child_fs:
            pref = [0] * M
            s = 0
            for i in range(M):
                s = (s + cf[i]) % MOD
                pref[i] = s
            prefixes.append(pref)
        f_u = [1] * M
        for i in range(M):
            prod = 1
            for pref in prefixes:
                prod = prod * pref[i] % MOD
            f_u[i] = prod
        return f_u

This way, we don't store f globally; we only keep f for the current path. But we also need f for cycle nodes to combine in the cycle. So we need to keep f for cycle nodes. So we can do: for each cycle node c, call dfs(c) and store the returned f array in a dictionary or list for cycle nodes. That will compute f for the entire tree attached to c, and we only need to keep f for c. So we don't need to store f for all nodes. This is memory efficient.

But we also need to handle multiple cycle nodes in the same component. So we can do:
   For each component, find the cycle. Let cycle_nodes be the list of nodes in the cycle.
   For each node c in cycle_nodes, call dfs(c) to get f_c (an array of length M). This dfs will only traverse non-cycle nodes, so it won't go into other cycle nodes. But careful: if a non-cycle node has a child that is a cycle node, that cycle node is excluded because we filter is_cycle[v]. So that's fine.
   Then we need to combine these f_c over the cycle. As argued, all cycle nodes must have the same value v. So the number of ways for the component is sum_{v=1..M} ( Π_{c in cycle_nodes} f_c[v] ). We can compute this by initializing an array prod = [1] * M, then for each c in cycle_nodes, multiply prod[v] by f_c[v] for all v, then sum prod[v].

So overall algorithm:
- Find cycle nodes (is_cycle).
- Build children adjacency list.
- Find components: we can find connected components in the underlying undirected graph? But it's easier: since we have is_cycle, we can find cycles by picking an unvisited cycle node, then following A until we loop. We'll also need to traverse the trees to compute f for cycle nodes. But we can just iterate over all cycle nodes and if not visited in the cycle traversal, we extract the cycle.

Steps:
1. Read input.
2. Compute is_cycle using indegree elimination.
3. Build children: for i in 1..N: children[A[i]].append(i)
4. Find cycles: We can do a visited array for nodes. For each node i from 1 to N:
       if is_cycle[i] and not visited_cycle_node[i]:
           # extract cycle starting at i
           cycle = []
           cur = i
           while not visited_cycle_node[cur]:
               visited_cycle_node[cur] = True
               cycle.append(cur)
               cur = A[cur]
           # Now we have the cycle. But careful: this might not be a simple cycle if we start at a node that is part of a cycle but we might go around multiple times? Actually, since we mark visited as we go, we stop when we hit a visited node. So the cycle we collect is the nodes from the first unvisited to the last before revisiting. This gives the correct cycle.
5. For each cycle, we have a list of cycle nodes. For each c in cycle, compute f_c via dfs(c). Note: dfs(c) will only go to non-cycle children. It will not visit other cycle nodes because they are filtered. So it's safe.
6. Then combine: prod = [1] * M; for c in cycle: for v in 0..M-1: prod[v] = prod[v] * f_c[v] % MOD; component_ways = sum(prod) % MOD; add to answer.
7. Print answer mod 998244353.

We need to be careful: What about nodes that are not in any cycle? That can't happen because the graph is functional and every node eventually reaches a cycle. So all nodes are in some component.

Now, complexity: For each non-cycle node, we visit it exactly once (in the dfs from its cycle root). The dfs does O(M * degree) work. Total over all nodes: O(N*M + total_edges_in_reverse * M). But each edge is considered once when computing the parent's f. So total O(N*M). Actually, for each node, we compute prefix sums for each child. The prefix sum for a child of length M takes O(M) per child. So total over all nodes: sum over nodes of (number of non-cycle children * M). Each non-cycle child is counted once (at its parent). So total O(N*M). And the product for each node is also O(degree * M). So overall O(N*M). For N=M=2025, that's about 4 million operations, which is fast.

But wait, in the dfs, for a node with d children, we compute prefix arrays for each child, then for each i in 0..M-1, we multiply d numbers. That's O(d*M). So total is sum d_i * M = M * (sum d_i) = M * (N - number_of_cycle_nodes) because each non-cycle node has exactly one parent (but we are counting children, so sum of children over all nodes equals number of edges, which is N). Actually, each node except the roots of the trees (which are cycle nodes) has exactly one parent. But in the reverse graph, each node can have many children. The sum of children over all nodes is N (since each node appears as a child exactly once, except cycle nodes? Wait, each node i has parent A[i], so i is a child of A[i]. So each node is a child of exactly one node. So total number of children across all nodes is N. So sum of d_i = N. But in our dfs, we only count non-cycle children. So sum of d_i over all nodes (including cycle nodes) is N, but for cycle nodes, we exclude the cycle child. So the sum of d_i we actually use is N - number_of_cycle_nodes (since each cycle node has one cycle child that we exclude, and that cycle child is also a cycle node). Actually, careful: In the reverse graph, each node has a set of children. For a cycle node, one of its children is its predecessor in the cycle, which is also a cycle node. We exclude that. So the number of non-cycle children summed over all nodes is N - (number of cycle nodes) because each cycle node loses one child (the cycle predecessor). But each node that is a cycle node is also a child of some node (its predecessor), so that edge is excluded. So total non-cycle children = N - C, where C is number of cycle nodes. So total work is O(M * (N - C)) for prefix sums, plus O(M * (N - C)) for products. So it's fine.

Now, we need to implement the dfs carefully to avoid recursion depth issues? N=2025, recursion depth might be up to 2025, which is safe if we set recursionlimit to, say, 10000. So we can use recursion.

We also need to be careful with modulo operations.

Let's test with the sample.

Sample 1:
N=3, M=3, A=[2,1,1]
Edges: 1->2, 2->1, 3->1.
Cycle nodes: 1 and 2 (since 3 leads to 1). is_cycle: [False, True, True] (1-indexed: index 1: True? Let's compute: indegree: 1 has indegree from 2 and 3 -> 2, 2 has indegree from 1 -> 1, 3 has indegree 0. Start with node 3: indegree 0, pop, mark not cycle, decrement indegree of A[3]=1 -> indegree of 1 becomes 1. Now queue empty. So cycle nodes: 1 and 2 (indegree >0). Correct.
Children: 
1: from 2 and 3 -> [2,3] but 2 is cycle, so non-cycle children: [3]
2: from 1 -> [1] but 1 is cycle, so non-cycle children: []
3: from? A[3]=1, so 1 has child 3, already.
Now cycle: start at 1: visited? no, mark 1, cycle=[1], cur=A[1]=2, not visited, mark 2, cycle=[1,2], cur=A[2]=1, visited, stop. So cycle=[1,2].
Now dfs:
dfs(1): non-cycle children: [3] (since 2 is cycle). dfs(3): no non-cycle children, return [1,1,1]. Then for node 1, prefix for child 3: prefix_3 = [1,2,3] (since 1+1=2, 2+1=3). Then f_1[v] = prefix_3[v] = [1,2,3].
dfs(2): no non-cycle children, return [1,1,1].
Now combine: prod = [1,1,1]; for c=1: prod = [1,2,3]; for c=2: prod = [1*1, 2*1, 3*1] = [1,2,3]. Sum = 1+2+3=6. Correct.

Sample 2:
N=4, M=9, A=[1,1,1,1]
All nodes point to 1. So cycle: only node 1? Actually, follow: 1->1, 2->1, 3->1, 4->1. So indegree: 1 has 4, others 0. So nodes 2,3,4 are popped. Node 1 remains. So is_cycle: only node 1. Children of 1: 2,3,4. Non-cycle children: [2,3,4]. dfs(2): leaf, return [1]*9. Similarly 3,4. For node 1: prefixes: for each child, prefix is [1,2,3,...,9]. So f_1[v] = (v)^3? Actually product of three prefixes each equal to v, so v^3. So f_1 = [1^3, 2^3, ..., 9^3]. Cycle combination: only node 1, so prod = f_1. Sum_{v=1..9} v^3 = (9*10/2)^2 = 45^2 = 2025. Correct.

Sample 3: We'll test later.

One more thing: What if a node has no non-cycle children? Then f[u] = [1]*M. That means no constraints from below, so any value is allowed.

Now, we need to ensure that the dfs is efficient. We'll write it as a nested function to capture MOD, M, children, is_cycle.

We also need to handle the case where M=0? But M>=1.

Now, let's think about potential pitfalls:
- The cycle might be of length 1: a self-loop. In that case, the cycle node has itself as a child in the cycle, but we exclude it. So dfs(cycle_node) will only consider non-cycle children. That's correct.
- The cycle might be of length >1.
- The graph might have multiple components. We need to sum over all components.

We should also consider that some nodes might not be reachable from any cycle node if there is a bug? But by construction, every node is either in a cycle or leads to a cycle, so it will be visited.

Now, we need to implement the dfs carefully to avoid recomputation. Since we call dfs for each cycle node separately, and the trees are disjoint, there is no overlap. So we can just call dfs for each cycle node in each cycle.

Now, we need to find the cycles. We can do a simple loop: for i in 1..N, if is_cycle[i] and not visited_cycle[i], then extract the cycle. But we need to make sure we traverse the cycle correctly. Since is_cycle nodes are exactly the cycle nodes, we can do:
   cur = i
   while not visited_cycle[cur]:
       visited_cycle[cur] = True
       cycle.append(cur)
       cur = A[cur]
   # But this will mark all cycle nodes in this component as visited. However, it might also mark nodes that are not in the cycle? Actually, if we start at a cycle node and follow A, we will stay within the cycle because A of a cycle node is another cycle node. So it's fine.

But wait: what if there is a cycle that is not reachable from i? Actually, all cycle nodes are in some cycle. So we will cover all.

Now, we need to store the f arrays for cycle nodes temporarily. We can compute f for each cycle node and then immediately combine and add to answer, and then discard the f array. That saves memory.

So the algorithm in code:

def solve():
    import sys
    sys.setrecursionlimit(10000)
    MOD = 998244353
    input = sys.stdin.readline
    N, M = map(int, input().split())
    A = [0] + list(map(int, input().split()))  # 1-indexed
    # Step 1: find cycle nodes
    indeg = [0]*(N+1)
    for i in range(1, N+1):
        indeg[A[i]] += 1
    from collections import deque
    q = deque()
    for i in range(1, N+1):
        if indeg[i] == 0:
            q.append(i)
    is_cycle = [False]*(N+1)
    while q:
        u = q.popleft()
        is_cycle[u] = False  # actually, we can set a separate array, but we want True for cycle nodes. Initially is_cycle[i] = True for all? Let's do: is_cycle = [True]*(N+1) for i=1..N, and set to False when popped.
    # Better: initialize is_cycle = [False]*(N+1); for i in 1..N: is_cycle[i] = True (all are cycle nodes initially). Then when we pop, set is_cycle[u] = False.
    # Let's do that.
    is_cycle = [True]*(N+1)
    for i in range(1, N+1):
        if indeg[i] == 0:
            q.append(i)
    while q:
        u = q.popleft()
        is_cycle[u] = False
        v = A[u]
        indeg[v] -= 1
        if indeg[v] == 0:
            q.append(v)
    # Now is_cycle[i] is True iff i is in a cycle.
    # Step 2: build reverse adjacency
    children = [[] for _ in range(N+1)]
    for i in range(1, N+1):
        children[A[i]].append(i)
    # Step 3: find cycles and compute answer
    visited_cycle = [False]*(N+1)
    ans = 0
    # Define dfs function
    def dfs(u):
        # returns f array for node u (considering only non-cycle children)
        child_fs = []
        for v in children[u]:
            if not is_cycle[v]:
                child_fs.append(dfs(v))
        if not child_fs:
            return [1]*M
        # compute prefix sums for each child
        prefixes = []
        for cf in child_fs:
            pref = [0]*M
            s = 0
            for i in range(M):
                s = (s + cf[i]) % MOD
                pref[i] = s
            prefixes.append(pref)
        f_u = [1]*M
        for i in range(M):
            prod = 1
            for pref in prefixes:
                prod = prod * pref[i] % MOD
            f_u[i] = prod
        return f_u
    # Iterate over all nodes to find cycles
    for i in range(1, N+1):
        if is_cycle[i] and not visited_cycle[i]:
            # extract cycle
            cycle = []
            cur = i
            while not visited_cycle[cur]:
                visited_cycle[cur] = True
                cycle.append(cur)
                cur = A[cur]
            # Now we have a cycle. For each node in cycle, compute f
            # But we need to compute f for each cycle node. However, we must be careful: when we compute dfs for a cycle node, it will only go to non-cycle children. So it's fine.
            # Compute f for each cycle node
            f_cycle = []
            for c in cycle:
                f_cycle.append(dfs(c))
            # Combine: all cycle nodes must have same value v
            prod = [1]*M
            for f_c in f_cycle:
                for v in range(M):
                    prod[v] = prod[v] * f_c[v] % MOD
            comp_ways = sum(prod) % MOD
            ans = (ans + comp_ways) % MOD
    print(ans)

We need to test with sample 1,2,3.

But wait: In the cycle extraction, we might not visit all cycle nodes if we start at a node that is not the first? Actually, if we have a cycle, and we start at any node in the cycle, we will traverse the entire cycle and mark all. So it's fine.

However, there is a subtle bug: In the cycle extraction, we use `while not visited_cycle[cur]`. But what if the cycle has nodes that are already visited from a previous cycle? That can't happen because cycles are disjoint. So it's safe.

Now, let's test with sample 1 mentally: it works.

Sample 2: works.

Sample 3: We'll write a quick test in mind? Maybe not.

But we should consider a case where a cycle node has a child that is also a cycle node? That would mean the cycle is not simple? Actually, in a functional graph, a cycle is a set of nodes where each node points to the next, and there are no other edges among them. So a cycle node's only cycle child is its predecessor in the cycle. So it's fine.

Now, what about the memory for f_cycle? We store f for each cycle node temporarily. The number of cycle nodes in a component is at most N, and M is at most 2025, so storing f for all cycle nodes in the worst case (if the whole graph is one big cycle) would be N*M, which is about 4 million, again memory concern. But in that case, the cycle is the whole graph, and we compute f for each cycle node. But if the graph is a single cycle, then each cycle node has no non-cycle children, so dfs(c) returns [1]*M. So f_cycle is a list of N lists of length M. That's N*M integers. For N=2025, M=2025, that's 4 million integers, which is about 4e6 * 28 = 112 MB, plus overhead for lists. That might be too much. But we can optimize: we don't need to store all f_cycle at once. We can compute the product on the fly. Since we need to compute for each v, the product of f_c[v] over all cycle nodes c. We can do:

prod = [1]*M
for c in cycle:
    f_c = dfs(c)
    for v in range(M):
        prod[v] = prod[v] * f_c[v] % MOD
comp_ways = sum(prod) % MOD

This way, we only store one f_c at a time. So we should do that.

So modify the loop:
for c in cycle:
    f_c = dfs(c)
    for v in range(M):
        prod[v] = prod[v] * f_c[v] % MOD

That is more memory efficient.

Now, we need to ensure that dfs is efficient. The recursion depth might be up to N. We'll set recursionlimit.

Now, let's consider the time complexity of dfs: For a node with many children, we compute prefix sums for each child. That is O(degree * M). For a node with no children, O(M). So total O(N*M). For N=M=2025, it's about 4 million operations, which is fast in Python if optimized. However, the inner loop of multiplying prefixes for each i is O(degree * M). We can optimize by precomputing the product incrementally? For each i, we multiply all prefixes. That's fine.

We can also optimize the prefix computation by using a running sum.

Now, we need to be careful with modulo: we do modulo after each addition and multiplication.

Now, let's test with a small case: N=1, M=5, A=[1]. Then is_cycle: indegree of 1 is 1, no nodes with indegree 0, so is_cycle[1]=True. Cycle: start at 1, visited? no, mark 1, cycle=[1], cur=A[1]=1, visited, stop. dfs(1): children: [1] but is_cycle[1] is True, so no non-cycle children, return [1]*5. prod = [1]*5. For c=1: f_c = [1,1,1,1,1], prod becomes [1,1,1,1,1]. sum = 5. That makes sense: x1 can be any of 1..5, and condition x1 <= x1 is always true. So answer 5. Correct.

What if N=2, M=2, A=[1,1]. Then cycle: node 1 is cycle, node 2 is not. Children of 1: [2] (non-cycle). dfs(2): leaf, [1,1]. dfs(1): child 2, prefix_2 = [1,2], f_1 = [1,2]. prod = [1,2]. sum = 3. Let's enumerate: x1 and x2 in {1,2}, condition: x2 <= x1. So possibilities: (1,1), (2,1), (2,2). So 3. Correct.

Now, what about a cycle of length 2: N=2, M=3, A=[2,1]. Both are cycle nodes. children: 1: from 2, 2: from 1. But both children are cycle, so dfs for each returns [1,1,1]. prod = [1,1,1]. sum = 3. Enumerate: x1, x2 in {1,2,3}, condition: x1 <= x2 and x2 <= x1, so x1=x2. So 3 possibilities. Correct.

Now, what about a cycle with trees: N=3, M=2, A=[2,3,1]. So 1->2, 2->3, 3->1. Cycle: all three. Children: 1: from 3, 2: from 1, 3: from 2. But all children are cycle, so dfs returns [1,1] for each. prod = [1,1]. sum=2. Enumerate: x1,x2,x3 in {1,2}, conditions: x1<=x2, x2<=x3, x3<=x1 => all equal. So 2. Correct.

Now, a cycle with one tree: N=4, M=3, A=[2,3,1,1]. Nodes: 1,2,3 in cycle? Check: 1->2, 2->3, 3->1, so cycle. 4->1, so 4 is tree. Children: 1: from 3 and 4. For dfs(1): non-cycle children: [4]. dfs(4): leaf, [1,1,1]. prefix_4 = [1,2,3]. f_1 = [1,2,3]. dfs(2): non-cycle children: none (child 1 is cycle), so [1,1,1]. dfs(3): non-cycle children: none (child 2 is cycle), so [1,1,1]. Then prod = [1,2,3] * [1,1,1] * [1,1,1] = [1,2,3]. sum=6. Let's enumerate: x1,x2,x3,x4 in {1,2,3}. Conditions: x1<=x2, x2<=x3, x3<=x1 => x1=x2=x3. And x4<=x1. So if x1=v, then x4 can be 1..v. So for v=1: 1 way; v=2: 2 ways; v=3: 3 ways. Total 1+2+3=6. Correct.

So the algorithm seems correct.

Now, we need to implement it efficiently in Python. We'll use list comprehensions and avoid unnecessary overhead.

One potential issue: recursion depth. For a chain of length 2025, recursion depth is 2025, which is fine if we set recursionlimit to, say, 10000. But we can also implement dfs iteratively to be safe. However, recursive is simpler.

We'll also need to handle the case where M=0? But M>=1.

Now, let's write the code.

We'll also test with sample 3 by running mentally? Maybe not necessary.

We should also consider that the input might have large N and M, so we need to ensure that the code is efficient enough. The main loop is O(N*M) which is about 4 million, and the inner operations are simple arithmetic. In Python, 4 million operations might be a bit slow if not optimized, but it should be under 1 second. However, we have the prefix sum computation and product computation per node, so total operations might be around 10 million, still okay.

We can optimize by using local variables and avoiding attribute lookups.

Now, let's code.

We'll structure the code as described.

One more thing: In the dfs, we compute prefix sums for each child. We can do that in a separate function or inline. Inline is fine.

We'll also use `range(M)` for the loops.

Now, let's write the final code.</mm:think>### PLAN
We model the constraints as a functional graph. Each connected component has exactly one directed cycle; other nodes form rooted trees attached to cycle nodes. The condition `x_i ≤ x_{A_i}` forces values along any root-to-leaf path to be non-increasing, and on a cycle all values must be equal. For a tree node `u`, we compute `f_u(v)` = number of ways to assign its subtree when `u` has value `v`. This is done via bottom-up DP: `f_u(v) = ∏_{child c} (∑_{j=1}^v f_c(j))`. For a cycle of length `L`, all cycle nodes must share the same value `v`, so the component count is `∑_{v=1}^M ∏_{c in cycle} f_c(v)`. We find cycle nodes using indegree elimination, extract cycles, compute tree DPs recursively, and combine.