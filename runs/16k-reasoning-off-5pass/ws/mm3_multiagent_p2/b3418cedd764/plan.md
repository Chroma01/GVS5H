We need to count assignments x_i ∈ [1,M] such that x_i ≤ x_{A_i} for all i. This is equivalent to counting functions from the functional graph defined by A to [1,M] that are non-decreasing along edges. Since each node must be ≤ its parent, the value at a node is bounded above by the value at its parent. The constraint graph is a directed forest (each node points to A_i, possibly itself). For each weakly connected component, we can treat it as a rooted tree where roots are nodes with A_i = i (self-loops) or nodes that are part of cycles. Actually A defines a functional graph; each component has exactly one cycle. For nodes on the cycle, they must all have equal values because each must be ≤ the next and the next ≤ the next, forming a cycle of inequalities, forcing equality. For each tree hanging off a cycle node, the values must be ≤ the value at the attachment point, and within the tree they must be non-decreasing toward the root (the cycle node). So we can process each component by fixing the value v at the cycle (1..M), then for each tree attached, count assignments where each node's value is in [1, v] and non-decreasing toward the root. This is a classic DP on trees: for each node, dp[node][k] = number of ways to assign values to the subtree rooted at node such that node's value = k (1 ≤ k ≤ v). Since v ≤ M ≤ 2025, we can afford O(N * M) per component if we sum over v. But we need to sum over v from 1 to M, which would be O(N * M^2) too large. Instead, we can compute for each tree a polynomial (or prefix sums) representing the number of assignments as a function of the maximum allowed value v. Specifically, for a tree rooted at a cycle node, define f(v) = number of assignments to the tree where all values ≤ v and non-decreasing toward root. Then the total answer is sum over v=1..M of (product over trees in the component of f_i(v)) * (number of ways to assign the cycle values, which is 1 if we fix v for all cycle nodes). Since all cycle nodes must have the same value v, the contribution for a component is sum_{v=1}^M ∏_{trees} f_i(v). We can precompute f_i(v) for all v efficiently using DP with prefix sums.

For a tree rooted at r (the attachment point on the cycle), we need to compute for each node u, an array g_u where g_u[k] = number of ways to assign values to the subtree of u such that u's value = k (1 ≤ k ≤ M). Then f(v) = sum_{k=1}^v g_r[k] (since root's value can be any k ≤ v). Actually the root's value is exactly the cycle node's value v, so we need g_r[v] (the number of ways where root's value = v). Wait: the root of the tree is the cycle node itself. The cycle node's value is fixed to v. For the tree attached to it, the root of the tree is that cycle node, but its value is already fixed to v. So we need the number of ways to assign values to the rest of the tree (excluding the cycle node) such that each node's value ≤ its parent and ≤ v. This is exactly the DP where we treat the cycle node as root with fixed value v. So we need to compute for each node u (including the cycle node as root) the number of ways to assign its subtree given that its value is exactly some k. For the cycle node, we need the number of ways for its attached trees given its value = k. That is the product over children of the sum over child value ≤ k of (ways for child's subtree). So we can compute bottom-up: for each node u, define dp_u[k] = number of ways to assign the subtree rooted at u (including u) such that u's value = k. Then dp_u[k] = ∏_{c child of u} (∑_{t=1}^k dp_c[t]). This is because each child c must have a value t ≤ k, and the subtrees are independent. So we can compute dp_u for all k from 1 to M in O(M) per node if we precompute prefix sums of dp_c. Since N, M ≤ 2025, total O(N * M) is feasible (about 4 million). Then for each cycle node r, the contribution for a fixed v is dp_r[v] (the number of ways to assign the entire component, including the cycle node's value = v). Since all cycle nodes in the same component must have the same value, we need to multiply dp for each cycle node? Wait: the cycle consists of several nodes. They are all roots of trees. The component has a cycle of length L. For each node on the cycle, it has a value v (same for all). The trees attached to each cycle node are independent given the cycle node's value. So the total number of assignments for the component with cycle value v is ∏_{r in cycle} dp_r[v], where dp_r[v] is computed as above (including the cycle node itself as root of its attached tree). But note: dp_r[v] includes the assignment of the cycle node's value? Actually dp_r[v] is defined as the number of ways to assign the subtree rooted at r (including r) such that r's value = v. Since r is on the cycle, its value is fixed to v, and the subtree includes the attached trees (excluding other cycle nodes). So yes, dp_r[v] counts the ways for the trees attached to r. Since the cycle nodes are independent given the common value v, the total ways for the component is ∏_{r in cycle} dp_r[v]. However, we must ensure that the cycle nodes themselves satisfy the inequalities among themselves. Since they form a cycle, each must be ≤ the next, and with equality forced, they all have the same value v. So the assignment of the cycle nodes is just choosing v, and then each cycle node's attached trees are assigned independently. So the total for the component is sum_{v=1}^M ∏_{r in cycle} dp_r[v].

But wait: dp_r[v] includes the value of r itself? Actually dp_r[v] is defined as the number of ways to assign the subtree rooted at r (including r) such that r's value = v. Since r is a cycle node, its value is fixed to v, and the subtree consists of the trees attached to r (excluding other cycle nodes). So dp_r[v] counts the number of ways to assign those attached trees. So the product over cycle nodes gives the total number of ways for the entire component given v. So the answer is sum over v of that product.

Now we need to compute dp for all nodes. The graph is a functional graph: each node has out-degree 1 (to A_i). We can reverse edges to get a forest of trees rooted at cycle nodes. We can find cycles using standard algorithm (e.g., DFS or topological removal). Then for each node not in any cycle, it belongs to a tree rooted at some cycle node. We can compute dp for all nodes in post-order (from leaves up). Since the graph is a forest of trees directed toward the root (cycle node), we can process nodes in reverse topological order: start from nodes with no children (in the reversed graph) and go up.

We need to compute dp_u[k] for k=1..M. The recurrence: dp_u[k] = ∏_{c ∈ children(u)} (∑_{t=1}^k dp_c[t]). Let prefix_c[k] = ∑_{t=1}^k dp_c[t]. Then dp_u[k] = ∏_{c} prefix_c[k]. We can compute prefix_c array for each child. Since M ≤ 2025, we can store arrays of size M+1 for each node? That would be O(N*M) memory, which is about 4 million integers, feasible (4e6 * 4 bytes = 16 MB). Actually N=2025, M=2025, N*M ≈ 4 million, which is fine. But we need to be careful with memory in Python: 4 million integers might be heavy (each int is 28 bytes in Python), so we need to use lists of lists or maybe use array module or numpy? But we can optimize: we only need dp for nodes that are not cycle nodes? Actually we need dp for all nodes to compute up to the cycle nodes. But we can compute dp on the fly and discard after use? However, we need dp for children to compute parent. Since we process from leaves up, we can compute dp for a node after we have computed dp for all its children. Then we can keep dp for the node until its parent is processed. Since the tree depth can be up to N, we might need to keep dp for all nodes until the root is processed. But we can process in a bottom-up order: we can compute a topological order of the reversed graph (i.e., order such that children come before parents). Then we can compute dp for each node in that order, and we can discard dp for a node after its parent has been processed? But we need dp for children when computing parent. If we process in order where children come before parents, we can compute dp for a node and keep it until its parent is processed. Since each node has exactly one parent (in the original graph), we can keep dp for all nodes until the end. But memory might be high. However, we can store dp as a list of length M+1 for each node. With N=2025, M=2025, that's about 4 million integers. In Python, each integer is about 28 bytes, so 112 MB, which might be borderline but possibly okay if we use small integers? But we are modulo 998244353, so we can use Python's int, but we can also use array('I') or list of ints? Actually Python ints are objects, so memory is large. We need to optimize.

Alternative: we can compute dp using prefix sums and only keep the current dp array for each node when processing its parent. Since each node is used only once as a child of its parent, we can free the child's dp after the parent is computed. But we need to compute prefix sums for each child. We can compute prefix sums on the fly when computing the parent. Specifically, for a node u, we need for each child c, the prefix sum array prefix_c[k] = sum_{t=1}^k dp_c[t]. We can compute this from dp_c. If we have dp_c as a list, we can compute prefix_c in O(M) time. Then we multiply across children. So we need dp_c for each child at the time we compute u. After computing u, we can discard dp_c. So we can process nodes in a post-order traversal: for each tree rooted at a cycle node, we do a DFS post-order, compute dp for leaves first, then for internal nodes. We can keep dp for the current node in a local variable, and after returning to parent, we can pass it up. Actually we can compute dp for each node and return it to the parent. In a recursive DFS, we can compute dp for a node by recursively computing dp for children, then combining. This way we don't need to store dp for all nodes simultaneously; we only need to keep dp for the current recursion stack. However, the recursion depth could be up to N=2025, which is fine. But we need to compute dp for all nodes in all trees. We can do a DFS from each cycle node, compute dp for the tree, and then for the cycle node we get dp_cycle[v] (the number of ways for the attached trees). Then we can sum over v.

But careful: the cycle node itself is part of the cycle. Its dp should include the ways for its attached trees, but not include other cycle nodes. So we can treat each cycle node as the root of a tree (its attached subtree). We can compute dp for that tree using DFS, where the root is the cycle node. However, the cycle node's value is fixed to v, so we need dp_root[v] where dp_root is computed as per recurrence. So we can compute dp for the tree rooted at the cycle node, with the cycle node as the root. That dp will be an array of length M+1 (index from 1 to M). Then the contribution for that cycle node is dp_root[v]. Then the product over cycle nodes in the component is ∏ dp_root_i[v].

So algorithm:
1. Build graph: for each i, A_i is the parent. Build reverse adjacency list: children[i] = list of nodes j such that A_j = i.
2. Find all cycles in the functional graph. We can do this by:
   - Compute indegree for each node.
   - Use queue to remove nodes with indegree 0 iteratively (topological removal). The remaining nodes are exactly the nodes in cycles.
   - For each remaining node, if not visited, traverse the cycle by following A_i until we return to start, marking all nodes in that cycle.
3. For each cycle node, we will compute dp for its attached tree (excluding other cycle nodes). The attached tree consists of all nodes that are not in any cycle and whose path to the cycle leads to this cycle node. We can do a DFS from each cycle node, but we must avoid going into other cycle nodes. So we can treat the cycle nodes as roots, and do DFS on the reversed graph, but only visiting nodes that are not in any cycle. Since the reversed graph from a cycle node will only lead to nodes that eventually reach that cycle node (because the original graph is functional, each node has exactly one outgoing edge, so the reversed graph is a forest where each tree is rooted at a cycle node). So we can simply do a DFS from each cycle node on the reversed graph, but we need to ensure we don't visit other cycle nodes. Since we only start DFS from cycle nodes and only follow edges to non-cycle nodes, and from non-cycle nodes we only follow edges to their parent (which is either a cycle node or another non-cycle node). But in the reversed graph, from a non-cycle node, its children are nodes that point to it. So if we start from a cycle node and do DFS on reversed graph, we will visit all nodes in its tree. However, we must be careful: if we start from a cycle node, we might also visit other cycle nodes if there is an edge from a non-cycle node to a cycle node? Actually in the reversed graph, edges go from parent to child. So from a cycle node, its children are nodes that have A_i = that cycle node. Those children are non-cycle nodes (since if a child were a cycle node, then that child would have A_i = cycle node, but cycle nodes have A_i pointing to another cycle node, so they cannot have a parent that is a cycle node unless the cycle has length 1? Wait: consider a cycle of length >1: each node in the cycle has A_i pointing to the next node in the cycle. So a cycle node does not have any incoming edge from another cycle node? Actually it does: each cycle node has exactly one incoming edge from the previous node in the cycle. So in the reversed graph, each cycle node has exactly one child that is a cycle node (the previous node in the cycle). So if we start DFS from a cycle node and follow reversed edges, we might go to that previous cycle node. But we want to avoid that. So we need to treat the cycle nodes specially: we should not traverse edges that lead to other cycle nodes. So we can mark all cycle nodes, and during DFS from a cycle node, we only visit nodes that are not cycle nodes. That is safe because from a non-cycle node, its parent is either a cycle node or a non-cycle node. But if we start from a cycle node and go to its children (non-cycle nodes), then from those non-cycle nodes, their children are also non-cycle nodes (since if a non-cycle node had a child that is a cycle node, that would mean the cycle node points to the non-cycle node, but cycle nodes only point to other cycle nodes). So actually, from a cycle node, all nodes reachable via reversed edges without passing through another cycle node are exactly the tree attached to that cycle node. So we can do DFS from each cycle node, but we should not follow edges to other cycle nodes. So we can simply do: for each cycle node, run a DFS that visits only non-cycle nodes. That will cover all non-cycle nodes exactly once because each non-cycle node has a unique path to a cycle node.

So we can compute dp for each tree rooted at a cycle node using a post-order traversal. We can do a recursive DFS that returns the dp array for the subtree rooted at that node. For a leaf (non-cycle node with no children), dp[k] = 1 for all k (since the node itself can be any value k, and there are no further constraints). Actually careful: for a leaf node u (non-cycle), its value can be any k from 1 to M, and there are no children, so dp_u[k] = 1. But wait: the recurrence is dp_u[k] = ∏_{c} (∑_{t=1}^k dp_c[t]). If no children, then product over empty set is 1. So dp_u[k] = 1 for all k. That makes sense: a leaf can take any value independently.

For an internal node u (non-cycle), we compute dp_u[k] = ∏_{c} prefix_c[k], where prefix_c[k] = sum_{t=1}^k dp_c[t]. We can compute prefix_c from dp_c. Since we have dp_c from recursive call, we can compute prefix_c on the fly.

We need to do this for all nodes in all trees. Since N and M are up to 2025, recursion depth up to 2025 is fine. But we need to be careful about recursion limit in Python (default 1000). We can either increase recursion limit or use iterative post-order. We'll increase recursion limit.

After we compute dp for the tree rooted at a cycle node r, we get an array dp_r[1..M]. Then for the component containing that cycle, we need to multiply dp_r[v] for all cycle nodes in that component, and sum over v. But note: each cycle node's dp_r[v] counts the ways for the trees attached to that cycle node. However, the cycle nodes themselves are connected in a cycle. Their values must be equal. So for a given v, the total ways for the component is ∏_{r in cycle} dp_r[v]. So we need to compute for each component, an array comp[v] = ∏_{r in cycle} dp_r[v]. Then the answer is sum_{v=1}^M comp[v] modulo 998244353.

But we have multiple components. The total answer is the product over components of (sum_{v=1}^M comp_c[v])? Wait: components are independent because there are no constraints between them. So the total number of assignments is the product over components of the number of assignments for that component. For each component, the number of assignments is sum_{v=1}^M ∏_{r in cycle} dp_r[v]. So we can compute for each component its total count, then multiply all component counts modulo 998244353.

Alternatively, we can compute the overall answer by summing over v? But components are independent, so we can compute per component and multiply.

So steps:
- Read N, M, A.
- Build children list: children[i] = [j for j in range(N) if A[j] == i] (using 0-indexed).
- Find cycle nodes:
   - indegree = [0]*N.
   - For i in range(N): indegree[A[i]-1] += 1.
   - queue = deque([i for i in range(N) if indegree[i]==0]).
   - While queue: pop i, let p = A[i]-1; indegree[p]--; if indegree[p]==0: push p.
   - After this, nodes with indegree > 0 are in cycles.
   - Mark cycle nodes: is_cycle = [False]*N; for i in range(N): if indegree[i]>0: is_cycle[i]=True.
- Find cycles: for each i where is_cycle[i] and not visited, traverse cycle: start = i; while not visited[current]: mark visited; current = A[current]-1. Collect cycle nodes in order.
- For each cycle node, we will compute dp for its attached tree. We can do a DFS from the cycle node, but we need to avoid visiting other cycle nodes. So we can define a function dfs(u) that computes dp for the subtree rooted at u, assuming u is not a cycle node? Actually we want to compute dp for the tree rooted at the cycle node. But the cycle node itself is a cycle node, so we need to compute dp for the cycle node as well. We can treat the cycle node as the root of its attached tree, but we need to compute dp for it using the same recurrence, where its children are the non-cycle nodes that point to it. So we can write a function that computes dp for any node u, but if u is a cycle node, we should not include other cycle nodes as children. However, in the children list, a cycle node may have a child that is another cycle node (the previous node in the cycle). So we need to filter children: when computing dp for a cycle node, we only consider children that are not cycle nodes. For non-cycle nodes, all children are non-cycle nodes (since if a non-cycle node had a cycle node as child, that would mean the cycle node points to the non-cycle node, but cycle nodes only point to cycle nodes). So we can do: in the DFS, when computing dp for a node u, we iterate over its children, but skip any child that is a cycle node. That way, for a cycle node, we only process its non-cycle children. For non-cycle nodes, we process all children (which are non-cycle). So we can write a recursive function that takes node u and returns dp array for the subtree rooted at u (including u). The function will:
   - For each child v in children[u]:
        if is_cycle[v]: skip (do not include in product).
        else: recursively get dp_v.
   - Then compute dp_u[k] = product over included children of (prefix_v[k]).
   - If no included children, dp_u[k] = 1 for all k.
   - Return dp_u.

But careful: for a cycle node, we want dp_u to represent the number of ways for the attached trees given that u's value is k. That is exactly what the above computes: dp_u[k] = ∏_{c (non-cycle)} (∑_{t=1}^k dp_c[t]). So that works.

Now, we need to compute dp for each cycle node. We can call dfs(cycle_node) for each cycle node. But note: if we call dfs on a cycle node, it will recursively compute dp for its non-cycle descendants. Since each non-cycle node is in exactly one tree, we will compute dp for each non-cycle node exactly once. So we can do that.

However, we need to be careful about recursion depth: the tree depth could be up to N. We'll set recursionlimit.

Now, after we have dp for each cycle node, we need to group cycle nodes into components. We already identified cycles. For each cycle, we have a list of cycle nodes. For each cycle node, we have computed dp_cycle_node (an array of length M+1). Then for that component, we compute comp_dp[v] = product over cycle nodes in the cycle of dp_cycle_node[v]. Then the component's total is sum_{v=1}^M comp_dp[v] mod MOD. Then we multiply all component totals to get the answer.

But wait: what about cycles of length 1? That is, a node with A_i = i. That node is a cycle node. Its attached trees are computed as above. So it's fine.

Now, we need to compute dp arrays efficiently. Since M ≤ 2025, we can store arrays as lists of length M+1 (index 0 unused). For each node, we compute dp_u[k] for k=1..M. The recurrence involves product of prefix sums. We can compute prefix sums for each child. Since we have dp_c from recursion, we can compute prefix_c[k] = (prefix_c[k-1] + dp_c[k]) % MOD. Then dp_u[k] = product over children of prefix_c[k] mod MOD. We can compute this in O(M * degree) per node. Since total sum of degrees over all nodes is N (each node has exactly one parent, so total edges = N). But in the reversed graph, each node can have multiple children. The total number of child-parent relationships is N. So total work over all nodes is O(N * M) if we process each node once. Actually for each node, we do O(M * number_of_children) operations. Sum over nodes of (M * number_of_children) = M * (total number of children) = M * N. So total O(N*M) = about 4 million, which is fine.

But we need to be careful with the product: we need to multiply prefix_c[k] for each child. We can do that in a loop over k from 1 to M, and for each k, multiply over children. That is O(M * degree). Alternatively, we can compute for each child its prefix array, then for each k, multiply them. That's the same.

We can optimize by precomputing prefix arrays for children and then multiplying. But since M is small, it's fine.

Now, we need to implement the DFS. We'll write a recursive function:

def dfs(u):
    # returns dp array for subtree rooted at u (including u)
    # u is assumed to be not a cycle node? Actually we call it for cycle nodes too, but we skip cycle children.
    dp = [0] * (M+1)
    # For each child v in children[u]:
    #   if is_cycle[v]: continue
    #   else: dp_v = dfs(v)
    # Then compute dp[k] = product over children of (sum_{t=1}^k dp_v[t])
    # If no children: dp[k] = 1 for all k.
    # We'll compute prefix sums for each child.
    child_prefixes = []  # list of prefix arrays
    for v in children[u]:
        if is_cycle[v]:
            continue
        dp_v = dfs(v)
        # compute prefix sum
        prefix = [0] * (M+1)
        s = 0
        for k in range(1, M+1):
            s = (s + dp_v[k]) % MOD
            prefix[k] = s
        child_prefixes.append(prefix)
    if not child_prefixes:
        for k in range(1, M+1):
            dp[k] = 1
    else:
        for k in range(1, M+1):
            prod = 1
            for pref in child_prefixes:
                prod = prod * pref[k] % MOD
            dp[k] = prod
    return dp

But this creates a new prefix array for each child, which uses memory. However, we only need the prefix array temporarily for the parent computation. We can compute it on the fly inside the k loop? That would be O(M * degree) but without storing prefix arrays. We can do:

for v in children[u]:
    if is_cycle[v]: continue
    dp_v = dfs(v)
    # we have dp_v, we need to use it to compute prefix sums for each k.
    # We can compute prefix sums incrementally as we iterate k.
    # But we need to multiply across children. So we can do:
    # For each k, we need sum_{t=1}^k dp_v[t]. We can precompute an array prefix_v.
    # Since we have dp_v, we can compute prefix_v in O(M) time and store it.
    # That's fine.

But we can also avoid storing prefix_v by noting that we can compute the product incrementally if we process children one by one and update a running product array. For example, we can start with an array prod[k] = 1 for all k. Then for each child v, we compute prefix_v[k] = sum_{t=1}^k dp_v[t], and then update prod[k] = prod[k] * prefix_v[k] % MOD. This way we only keep one prod array and one prefix_v array at a time. That is more memory efficient. So we can do:

def dfs(u):
    prod = [1] * (M+1)  # initialize to 1 for all k
    for v in children[u]:
        if is_cycle[v]:
            continue
        dp_v = dfs(v)
        # compute prefix_v
        prefix = [0] * (M+1)
        s = 0
        for k in range(1, M+1):
            s = (s + dp_v[k]) % MOD
            prefix[k] = s
        # update prod
        for k in range(1, M+1):
            prod[k] = prod[k] * prefix[k] % MOD
    # Now prod[k] is the product over children of prefix_v[k]
    # But if there are no children, prod[k] remains 1, which is correct.
    # However, we need to return dp_u[k] = prod[k]? Wait: dp_u[k] = product over children of (sum_{t=1}^k dp_c[t]). That is exactly prod[k]. So we can return prod.
    # But careful: if there are no children, prod[k] = 1, which is correct.
    # So we can return prod directly.
    return prod

But wait: is that correct? For a leaf node with no children, prod[k] = 1, so dp_u[k] = 1. That matches. So we can return prod as the dp array.

But we need to ensure that we don't modify prod in place for the parent? Actually we return prod, and the parent will use it as dp_v. So it's fine.

However, we need to be careful: the prod array is shared? No, we create a new list prod for each call. So it's fine.

This approach uses O(M) memory per recursion call, and recursion depth up to N, so total memory O(N*M) in the worst case if we keep all dp arrays on the stack? Actually in recursion, we keep the local variables for each call. Since each call returns a list of length M+1, and we keep it until the parent finishes processing, the total memory on the stack is O(depth * M). Depth can be up to N, so O(N*M) again. But we can optimize by using iterative post-order traversal to avoid deep recursion and large stack memory. However, with N=2025 and M=2025, depth 2025, each list of 2026 integers (Python ints) is about 2026*28 ≈ 56KB, times 2025 is about 113MB, which might be too much. But we can use arrays of type 'int' from the array module to reduce memory? Or we can use numpy? But we want pure Python.

We can try to reduce memory by using smaller data types? But we need modulo 998244353, which fits in 32-bit. We can use Python's built-in int but they are objects. Alternatively, we can use list of ints but maybe it's okay? 113MB might be borderline but could pass if memory limit is high. But typical memory limit might be 256MB, so it might be okay. However, we can do better by using iterative post-order and freeing memory as we go.

We can compute dp for all nodes in a bottom-up order without recursion. We can perform a topological sort on the reversed graph? Actually the reversed graph is a forest where each node has a unique parent (the original A_i). So we can process nodes in order of decreasing depth from the cycle nodes. We can do a BFS from cycle nodes to assign depths, then process nodes in reverse order of depth (from leaves to roots). But we need to know the children for each node. We can compute a list of nodes in post-order by doing a DFS iteratively. We can use a stack to simulate recursion.

Let's design an iterative post-order traversal:
- For each cycle node, we want to traverse its tree (non-cycle nodes) in post-order.
- We can do a stack-based DFS: push (node, state) where state=0 means first visit, state=1 means processing children.
- Start with cycle nodes: for each cycle node, push (cycle_node, 0). But we need to avoid going to other cycle nodes. So when we explore children, we only push non-cycle children.
- While stack: pop (u, state). If state=0: push (u, 1) and then push all non-cycle children with state=0.
- If state=1: compute dp_u using dp of children (which are already computed because they were pushed before and processed). We need to store dp for each node until its parent is processed. So we need an array dp[node] that holds the dp list for that node. We can store it in a list of lists. But we can also compute and store in a dictionary or list of size N, each being a list of length M+1. That would be O(N*M) memory anyway. But we can free the dp of a node after its parent is processed? In the iterative approach, we process nodes in post-order, so when we process a node, its children have already been processed. After we compute dp for the node, we can keep it until its parent is processed. But if we process nodes in post-order, we process a node only after all its descendants. So when we process a node, its children are already processed, but we still need their dp to compute the node's dp. After we compute the node's dp, we can discard the children's dp if we no longer need them. But the children's dp might be needed by other parents? No, each non-cycle node has exactly one parent (the node it points to in original graph). So once we have processed a node, its dp is only needed for its parent. So after we process the parent, we can discard the child's dp. So we can free memory as we go. In the iterative post-order, we process nodes in order such that when we process a node, we have already processed all its children. After we compute dp for the node, we can keep it until its parent is processed. But if we process nodes in a global post-order (like a list of nodes in post-order), then when we process a node, its children have been processed earlier, but we still have their dp stored. We can free the dp of a child after we have processed its parent. So we can do: after computing dp for node u, we add u to a list. Then when we process the parent of u, we use dp[u]. After the parent is processed, we can delete dp[u] to free memory. But we need to know when to delete. We can do a second pass? Alternatively, we can process nodes in a specific order: we can compute a post-order list for each tree, and then process that list, and after processing a node, we can delete its dp if it is not needed anymore. But we need to ensure that we don't delete a node's dp before its parent uses it. So we can process the post-order list in reverse? Actually in post-order, children come before parents. So if we process the list in order, when we process a node, its children have already been processed, but their dp is still stored. After we process the node, we can delete the dp of its children? But the children might have other parents? No, each node has only one parent. So after we process a node, its children's dp is no longer needed because the only parent that needed them is this node. So we can delete the children's dp after processing the node. However, if we process the list sequentially, we might delete a child's dp before another node that also needs it? But each child has only one parent, so once we process the parent, the child is done. So we can delete the child's dp immediately after the parent is processed. But we need to know which children to delete. We can keep track of the parent of each node. So after processing node u, we can look at its children and delete their dp arrays. But we need to have stored the children list. We can do that.

Alternatively, we can use recursion with increased recursion limit and hope memory is okay. Given constraints, maybe recursion is simpler and memory might be acceptable. Let's estimate: N=2025, M=2025. In the worst case, the tree is a chain of length 2025. In recursion, we go down the chain, each call creates a prod list of length M+1. At the deepest point, we have 2025 prod lists on the stack, each of size 2026. That's about 2025*2026*28 bytes ≈ 114 MB. Plus overhead for lists and other variables, maybe 150 MB. That might be too much for Python. So we should avoid deep recursion with large lists.

We can use an iterative approach to reduce memory. Let's design an iterative post-order traversal that computes dp for each node and stores it in a list, but we can free memory as we go.

We can do the following:
- First, find all cycle nodes and mark them.
- Build children list.
- For each cycle node, we will compute dp for its tree. We can do a DFS from the cycle node, but we need to compute dp for all nodes in the tree. We can use a stack to get a post-order list.
- We can do: for each cycle node, run a DFS that collects nodes in post-order (excluding other cycle nodes). We can use a stack: push (cycle_node, False). While stack: pop (u, visited). If not visited: push (u, True) and push all non-cycle children with (child, False). If visited: add u to post_order list.
- After we have post_order list for a tree, we process it in order (which is post-order, so children before parents). For each node u in post_order list, we compute dp_u using dp of its children (which are already computed because they appear earlier in the list). We need to store dp for each node until its parent is processed. But we can store dp in a list indexed by node number. However, we can free dp of a node after its parent is processed. Since we process the list in order, when we process a node, its children have been processed, but their dp is still stored. After we process the node, we can delete the dp of its children. But we need to know which children to delete. We can keep a list of children for each node. So after computing dp_u, we can iterate over its children (non-cycle) and delete their dp arrays (set to None). But careful: a child might be shared? No, each node has exactly one parent, so no sharing. So we can delete.

But we need to be careful: when we delete a child's dp, we must ensure that no other node needs it. Since the child has only one parent, and we are processing the parent now, it's safe.

So we can do:
- Initialize dp = [None] * N.
- For each cycle node, do iterative DFS to get post_order list.
- Then for u in post_order:
    - Compute dp_u using dp of children (which are not None).
    - Store dp[u] = dp_u.
    - After storing, for each child v in children[u] (non-cycle), we can set dp[v] = None to free memory.
- After processing all nodes in the tree, we have dp for the cycle node stored in dp[cycle_node]. We can then use that for the component.

But note: the cycle node itself is not in the post_order list because we started from it and we only push non-cycle children. So we need to compute dp for the cycle node separately. We can compute dp for the cycle node using the same method: treat it as a node with children (non-cycle). We can compute dp_cycle_node by iterating over its non-cycle children, using their dp (which are already computed and stored). So after processing the post_order list for the tree, we can compute dp for the cycle node as:
    prod = [1]*(M+1)
    for v in children[cycle_node]:
        if is_cycle[v]: continue
        # dp[v] is already computed
        prefix = compute prefix from dp[v]
        for k in 1..M: prod[k] = prod[k] * prefix[k] % MOD
    dp[cycle_node] = prod

Then we can free dp of its children.

So overall, we can process each component (cycle) independently.

Now, we need to group cycle nodes into components. We already have cycles. For each cycle, we have a list of cycle nodes. We will compute dp for each cycle node in that cycle. Then for the cycle, we compute comp_dp[v] = product over cycle nodes of dp_cycle_node[v]. Then component_total = sum_{v=1}^M comp_dp[v] % MOD. Then multiply all component_totals.

But careful: what if there are multiple cycles? They are independent, so we multiply.

Now, we need to implement the iterative DFS to get post-order for each tree. We can do it per cycle node. But note: a cycle node might have multiple trees? Actually each cycle node is the root of one tree (the set of nodes that eventually reach that cycle node). So we can process each cycle node separately. However, if we process each cycle node separately, we might visit the same non-cycle node multiple times? No, because each non-cycle node belongs to exactly one tree (the cycle node it reaches). So we can process each cycle node independently. But we need to ensure we don't process the same non-cycle node twice. So we can mark visited non-cycle nodes. Alternatively, we can process all cycle nodes in one go by doing a DFS from all cycle nodes simultaneously, but we need to avoid crossing between trees. Since trees are disjoint, we can just process each cycle node separately, but we need to avoid revisiting nodes. We can keep a global visited array for non-cycle nodes. When we do DFS from a cycle node, we only visit non-cycle nodes that are not visited. But we need to compute dp for all nodes. Actually, we can compute dp for all nodes in a single bottom-up pass without explicitly separating by cycle. We can do a topological order of the entire graph (excluding cycle nodes). Since the graph is a forest of trees rooted at cycle nodes, we can compute a post-order for all non-cycle nodes together. We can do a DFS from all cycle nodes, but we need to avoid going from one tree to another. Since trees are disjoint, we can start DFS from each cycle node and mark visited. That will cover all non-cycle nodes exactly once. So we can do:

visited = [False]*N
post_order = []
for each cycle node r:
    stack = [(r, False)]  # but we don't want to include r in post_order? Actually we want to compute dp for r later.
    while stack:
        u, processed = stack.pop()
        if processed:
            if u != r:  # we don't want to add cycle nodes to post_order? Actually we want to compute dp for cycle nodes separately, but we can include them if we handle correctly.
                post_order.append(u)
            continue
        if visited[u]: continue
        visited[u] = True
        stack.append((u, True))
        for v in children[u]:
            if is_cycle[v]: continue  # don't go to other cycle nodes
            if not visited[v]:
                stack.append((v, False))

But this will include cycle nodes in the traversal? We start from cycle nodes, but we don't want to process them as part of post_order because we will compute dp for them separately. However, we can include them in post_order and compute dp for them as well, but then we need to be careful: when computing dp for a cycle node, we should not include other cycle nodes as children. But in the DFS, we skip children that are cycle nodes. So if we include cycle nodes in post_order, we would compute dp for them using only non-cycle children. That is exactly what we want. So we can actually include cycle nodes in the post_order traversal. Then we can compute dp for all nodes (including cycle nodes) in one pass. But then we need to ensure that when we compute dp for a cycle node, we don't use dp of other cycle nodes. Since we skip cycle children, it's fine. So we can do a single DFS from all cycle nodes, collecting all nodes (cycle and non-cycle) in post-order. Then we process the post_order list: for each node u in post_order, compute dp_u using dp of its non-cycle children (which are already computed because they appear earlier in post-order). Then we store dp[u]. After processing all nodes, we have dp for all nodes, including cycle nodes. Then for each cycle, we compute comp_dp[v] = product over cycle nodes of dp[cycle_node][v]. Then component_total = sum_{v=1}^M comp_dp[v]. Then multiply.

This is simpler: we don't need to separate per cycle. We just do one DFS from all cycle nodes to get a global post-order of all nodes that are either cycle or non-cycle. But careful: the DFS from cycle nodes will only visit nodes that are reachable from cycle nodes via reversed edges without passing through another cycle node. That covers all nodes because every node eventually reaches a cycle node. So it covers all N nodes. So we can do:

- Find cycle nodes.
- Initialize visited = [False]*N.
- post_order = []
- For each cycle node r:
    if not visited[r]:
        stack = [(r, False)]
        while stack:
            u, processed = stack.pop()
            if processed:
                post_order.append(u)
                continue
            if visited[u]:
                continue
            visited[u] = True
            stack.append((u, True))
            for v in children[u]:
                if is_cycle[v]:
                    continue
                if not visited[v]:
                    stack.append((v, False))

This will visit all nodes. Note: we skip children that are cycle nodes. So from a cycle node, we only go to non-cycle children. From a non-cycle node, we go to its children (which are non-cycle). So we cover all non-cycle nodes. And we include cycle nodes in post_order. So post_order will contain all nodes, with cycle nodes appearing after their non-cycle descendants? Actually in post-order, children come before parents. Since we skip cycle children, a cycle node will have no cycle children, so its non-cycle children will be processed before it. So cycle nodes will appear after their non-cycle descendants. That's fine.

Now, we process post_order in order. For each node u in post_order:
    - Compute dp_u as described: product over non-cycle children of prefix sums.
    - We need to have dp for children already computed. Since children are non-cycle and appear earlier in post_order, they are computed.
    - Store dp[u] in an array dp_arrays[u] (list of length M+1).

After processing all nodes, we have dp for all nodes.

Then for each cycle (component), we have a list of cycle nodes. For each cycle node, we have dp[cycle_node]. We compute comp_dp[v] = product over cycle nodes in that cycle of dp[cycle_node][v] mod MOD. Then component_total = sum_{v=1}^M comp_dp[v] mod MOD. Then multiply all component_totals.

But wait: what about cycles of length 1? That's fine.

Now, we need to compute dp_u efficiently. We can do:

def compute_dp(u):
    prod = [1] * (M+1)
    for v in children[u]:
        if is_cycle[v]:
            continue
        # dp[v] is already computed
        dp_v = dp_arrays[v]
        # compute prefix sums
        prefix = [0] * (M+1)
        s = 0
        for k in range(1, M+1):
            s = (s + dp_v[k]) % MOD
            prefix[k] = s
        # update prod
        for k in range(1, M+1):
            prod[k] = prod[k] * prefix[k] % MOD
    return prod

But we can avoid creating a separate prefix array by updating prod incrementally using dp_v directly. We can do:

for v in children[u]:
    if is_cycle[v]: continue
    dp_v = dp_arrays[v]
    # we need to multiply prod[k] by sum_{t=1}^k dp_v[t]
    # We can compute the prefix sum on the fly as we iterate k.
    s = 0
    for k in range(1, M+1):
        s = (s + dp_v[k]) % MOD
        prod[k] = prod[k] * s % MOD

This way we don't need to store prefix array. So:

for v in children[u]:
    if is_cycle[v]: continue
    dp_v = dp_arrays[v]
    s = 0
    for k in range(1, M+1):
        s = (s + dp_v[k]) % MOD
        prod[k] = prod[k] * s % MOD

This is O(M) per child. Total O(M * degree). Good.

Now, we need to store dp_arrays for all nodes. That's O(N*M) memory. But we can free memory after use? In this approach, we need dp for all nodes when computing their parents. But we process post_order in order, so when we compute dp for a node, we need dp of its children. After we compute dp for the node, we can free the dp of its children if we no longer need them. But in the global post_order, a node's children are processed before it, but they might be needed by other parents? No, each node has exactly one parent. So after we process a node, its children's dp is no longer needed. So we can free them. However, in the loop over post_order, we process nodes sequentially. When we process node u, we need dp of its children. Those children have been processed earlier, and their dp is still stored. After we compute dp_u, we can delete the dp of its children. But we need to know which children to delete. We can iterate over children[u] (non-cycle) and set dp_arrays[child] = None. But careful: a child might be a cycle node? We skip cycle children, so children are non-cycle. And non-cycle nodes have exactly one parent, so once we process the parent, the child is done. So we can delete.

But we also need dp for cycle nodes later for component computation. So we should not delete dp of cycle nodes. But cycle nodes are not children of any node? Actually cycle nodes are roots, they have no parent in the reversed graph? They have parents in the original graph, but in the reversed graph, they have incoming edges from non-cycle nodes and from other cycle nodes. But we skip cycle children, so cycle nodes are not children of any node in our traversal. So they are only roots. So we will not delete dp of cycle nodes because they are not children of any node (except possibly other cycle nodes, but we skip). So we can safely delete dp of non-cycle nodes after their parent is processed.

So we can modify the loop: after computing dp_u, for each child v in children[u] (non-cycle), set dp_arrays[v] = None. But we need to ensure that we don't delete a child that is needed by another node? Since each non-cycle node has exactly one parent, and we are processing the parent now, it's safe.

But what about a non-cycle node that is a child of multiple parents? Impossible because each node has exactly one outgoing edge, so in the reversed graph, each node can have multiple incoming edges (multiple children), but each node has exactly one parent (the node it points to). So a non-cycle node is a child of exactly one node (its parent). So yes.

So we can do:

dp_arrays = [None] * N
for u in post_order:
    prod = [1] * (M+1)
    for v in children[u]:
        if is_cycle[v]:
            continue
        dp_v = dp_arrays[v]
        if dp_v is None:
            # should not happen
            continue
        s = 0
        for k in range(1, M+1):
            s = (s + dp_v[k]) % MOD
            prod[k] = prod[k] * s % MOD
    dp_arrays[u] = prod
    # free children
    for v in children[u]:
        if is_cycle[v]:
            continue
        dp_arrays[v] = None

But careful: when we free children, we might free a child that is also a child of another node? No, as argued. But we need to ensure that we don't free a child before its parent is processed. Since we process in post-order, children are processed before parents. So when we process u, its children have already been processed. After we process u, we free them. That's fine.

However, we must be careful: in the loop, we are iterating over children[u] to compute prod, and then again to free. We can combine.

Now, after processing all nodes, we have dp_arrays for cycle nodes. Then we compute components.

We need to find cycles. We already have is_cycle array. We also need to group cycle nodes into cycles. We can do:

cycles = []
visited_cycle = [False]*N
for i in range(N):
    if is_cycle[i] and not visited_cycle[i]:
        # traverse cycle
        cycle = []
        cur = i
        while not visited_cycle[cur]:
            visited_cycle[cur] = True
            cycle.append(cur)
            cur = A[cur] - 1
        cycles.append(cycle)

Now, for each cycle, we compute comp_dp[v] = product over node in cycle of dp_arrays[node][v]. Then component_total = sum(comp_dp) % MOD. Then answer = product of component_totals % MOD.

But wait: what if there are no cycles? That can't happen because every functional graph has at least one cycle. But if N=1 and A_1=1, then cycle of length 1.

Now, we need to consider the case where there are multiple cycles. They are independent, so we multiply.

Now, let's test with sample inputs.

Sample 1:
N=3, M=3, A=[2,1,1] (1-indexed: A1=2, A2=1, A3=1)
Graph: 1->2, 2->1, 3->1. So cycle: 1<->2. Node 3 points to 1.
Cycle nodes: 1,2. Node 3 is non-cycle.
Children:
1: children of 1 are nodes that point to 1: A2=1, A3=1 -> children: [2,3]
2: children: A1=2 -> children: [1]
3: children: none.
is_cycle: 1 and 2 are cycle.
Now, post-order traversal from cycle nodes:
Start from 1: stack [(1,False)]
Process 1: push (1,True), push children: 2 (cycle, skip), 3 (non-cycle, push (3,False))
Stack: (1,True), (3,False)
Pop (3,False): push (3,True), no children.
Stack: (1,True), (3,True)
Pop (3,True): post_order.append(3)
Pop (1,True): post_order.append(1)
Now start from 2: but visited[2]? We haven't visited 2 yet. So push (2,False). Process 2: push (2,True), children: 1 (cycle, skip). So stack: (2,True). Pop (2,True): post_order.append(2).
So post_order = [3,1,2]
Now process:
u=3: children: none. prod = [1,1,1,1] (M=3, indices 1..3). dp[3] = [1,1,1,1]. Free children: none.
u=1: children: 2 (cycle, skip), 3 (non-cycle). dp_v = dp[3] = [1,1,1,1]. Compute s: for k=1: s=1, prod[1]=1*1=1; k=2: s=2, prod[2]=1*2=2; k=3: s=3, prod[3]=1*3=3. So dp[1] = [1,2,3]. Free child 3: dp[3]=None.
u=2: children: 1 (cycle, skip). So no non-cycle children. prod = [1,1,1,1]. dp[2] = [1,1,1,1]. Free children: none.
Now cycles: cycle1: [1,2] (since from 1 we go to 2, from 2 go to 1). Actually we need to traverse cycle: start at 1: visited? We need to collect cycle nodes. We'll do: for i=1: is_cycle, not visited_cycle. cur=1: cycle=[1], cur=A[1]-1=2-1=1? Wait A1=2, so A[1]-1=1? Actually careful: A is 1-indexed. We stored A as 0-indexed? Let's define: read A as list of ints, subtract 1 to make 0-indexed. So A[0]=1 (since A1=2 -> 1), A[1]=0, A[2]=0. So cycle: 0 and 1. So cycle nodes: 0 and 1.
Now comp_dp[v] = dp[0][v] * dp[1][v] mod MOD.
dp[0] = [1,2,3] (for v=1,2,3)
dp[1] = [1,1,1]
So comp_dp[1]=1*1=1, comp_dp[2]=2*1=2, comp_dp[3]=3*1=3.
Sum = 1+2+3=6. That's the answer. Correct.

Sample 2:
N=4, M=9, A=[1,1,1,1] (all point to 1). So cycle: node 1 (index 0) is a cycle node (since A1=1). Nodes 2,3,4 point to 1. So cycle nodes: [0]. Non-cycle: 1,2,3.
Children:
0: children: 1,2,3 (since A2=1, A3=1, A4=1)
1: children: none
2: children: none
3: children: none
is_cycle: only 0.
Post-order: start from 0: stack [(0,False)]. Process 0: push (0,True), push children 1,2,3 (non-cycle). Stack: (0,True), (1,False), (2,False), (3,False). Pop (3,False): push (3,True), no children. Pop (3,True): post_order.append(3). Pop (2,False): push (2,True), no children. Pop (2,True): post_order.append(2). Pop (1,False): push (1,True), no children. Pop (1,True): post_order.append(1). Pop (0,True): post_order.append(0).
So post_order = [3,2,1,0]
Process:
u=3: no children, dp[3]=[1]*10 (M=9, indices 1..9)
u=2: no children, dp[2]=[1]*10
u=1: no children, dp[1]=[1]*10
u=0: children: 1,2,3. For each child, compute s and update prod.
For child 1: dp_v=[1]*10, s: for k=1: s=1, prod[1]=1; k=2: s=2, prod[2]=2; ... k=9: s=9, prod[9]=9.
For child 2: similarly, prod[k] = prod[k] * (k) because s=k. So prod[k] = k * k = k^2.
For child 3: prod[k] = k^2 * k = k^3.
So dp[0][k] = k^3.
Now cycle: [0]. comp_dp[v] = dp[0][v] = v^3.
Sum_{v=1}^{9} v^3 = (9*10/2)^2 = (45)^2 = 2025. Correct.

Sample 3: We'll trust.

So algorithm seems correct.

Now, we need to implement efficiently.

We need to be careful with indices: use 0-indexed.

Steps:
1. Read N, M.
2. Read A list of N integers, subtract 1 to make 0-indexed.
3. Build children: list of lists, size N. For i in range(N): children[A[i]].append(i).
4. Find cycle nodes:
   - indegree = [0]*N.
   - For i in range(N): indegree[A[i]] += 1.
   - queue = deque([i for i in range(N) if indegree[i]==0]).
   - While queue: i = queue.popleft(); p = A[i]; indegree[p] -= 1; if indegree[p]==0: queue.append(p).
   - is_cycle = [False]*N; for i in range(N): if indegree[i]>0: is_cycle[i]=True.
5. Build post_order:
   - visited = [False]*N
   - post_order = []
   - For each i in range(N): if is_cycle[i] and not visited[i]:
        stack = [(i, False)]
        while stack:
            u, processed = stack.pop()
            if processed:
                post_order.append(u)
                continue
            if visited[u]:
                continue
            visited[u] = True
            stack.append((u, True))
            for v in children[u]:
                if is_cycle[v]:
                    continue
                if not visited[v]:
                    stack.append((v, False))
   - This will visit all nodes. Note: we start from cycle nodes, but we might also start from non-cycle nodes? No, we only start from cycle nodes. But what if there are cycle nodes that are not visited because they are not reachable from any cycle node? Actually all cycle nodes are roots, so they are visited when we start from them. But we need to ensure we start from all cycle nodes. We iterate over all i, and if is_cycle[i] and not visited[i], we start DFS. That covers all cycle nodes.
6. Initialize dp_arrays = [None]*N.
7. Process post_order:
   For u in post_order:
        prod = [1] * (M+1)  # index 0 unused
        for v in children[u]:
            if is_cycle[v]:
                continue
            dp_v = dp_arrays[v]
            # dp_v should not be None
            s = 0
            for k in range(1, M+1):
                s = (s + dp_v[k]) % MOD
                prod[k] = prod[k] * s % MOD
        dp_arrays[u] = prod
        # free children
        for v in children[u]:
            if is_cycle[v]:
                continue
            dp_arrays[v] = None
8. Find cycles:
   visited_cycle = [False]*N
   cycles = []
   for i in range(N):
        if is_cycle[i] and not visited_cycle[i]:
            cycle = []
            cur = i
            while not visited_cycle[cur]:
                visited_cycle[cur] = True
                cycle.append(cur)
                cur = A[cur]
            cycles.append(cycle)
9. Compute answer:
   ans = 1
   for cycle in cycles:
        comp_dp = [1] * (M+1)
        for node in cycle:
            dp_node = dp_arrays[node]
            for k in range(1, M+1):
                comp_dp[k] = comp_dp[k] * dp_node[k] % MOD
        total = sum(comp_dp[1:]) % MOD
        ans = ans * total % MOD
   print(ans)

But wait: in step 7, we free children after processing u. However, we need to ensure that when we process u, the children's dp are still available. Since we process in post_order, children are processed before u, so their dp is stored. After we process u, we free them. That's fine.

But we must be careful: in the loop for u, we iterate over children[u] to compute prod, and then again to free. We can combine into one loop:

for v in children[u]:
    if is_cycle[v]:
        continue
    dp_v = dp_arrays[v]
    s = 0
    for k in range(1, M+1):
        s = (s + dp_v[k]) % MOD
        prod[k] = prod[k] * s % MOD
    dp_arrays[v] = None

That frees immediately after using. That's even better.

Now, we need to consider memory: dp_arrays is a list of N lists. Each list is of length M+1. That's N*(M+1) integers. With N=2025, M=2025, that's about 4 million integers. In Python, each integer is about 28 bytes, so about 112 MB. Plus overhead for lists, maybe more. This might be too much. We need to reduce memory.

We can try to use array('I') or maybe use a single 2D list? But still each integer is a Python object. We can use the built-in 'int' but they are objects. Alternatively, we can use numpy, but that's not allowed in standard Python.

We can try to reduce memory by using smaller data types? But we need modulo 998244353, which fits in 32-bit unsigned. We can use Python's 'int' but we can also use the 'int' from the 'ctypes' module? Not easy.

We can try to compute dp on the fly without storing all dp arrays. Since we process in post_order, we only need dp for the current node and its children. But we need dp for children when computing parent. So we need to keep dp for children until parent is processed. In the post_order, when we process a node, its children have been processed and their dp is stored. After we process the node, we can free the children's dp. So the maximum number of dp arrays stored at any time is the maximum number of nodes that are ancestors of the current node in the post-order? Actually, in post-order, we process nodes in a sequence. When we are at node u, we have processed all nodes in its subtree. So we have dp for all nodes in the subtree of u. But we only need dp for the children of u to compute u. After we compute u, we can free the children. So the number of dp arrays stored at any time is at most the size of the subtree of the current node. In the worst case, if the tree is a chain, when we are at the root, we have processed all nodes, so we have dp for all nodes. That's O(N) dp arrays. So memory is O(N*M) anyway.

But we can optimize by not storing dp for all nodes simultaneously. We can store dp in a list, but we can free as we go. In the chain case, when we process the leaf, we store dp for leaf. Then we process its parent: we need dp for leaf, so we keep it. After computing parent, we free leaf. So at any time, we only have dp for the current node and its ancestors? Actually, in a chain, when we process the leaf, we have dp for leaf. Then we process its parent: we need dp for leaf, so we keep leaf. After computing parent, we free leaf. So we have dp for parent. Then we process grandparent: we need dp for parent, so we keep parent. After computing grandparent, we free parent. So we only have one dp array at a time (the current node's dp) plus maybe the dp of its children? But children are freed immediately after use. So in the chain, we only need to store dp for the current node and its children? But children are freed after use. So we only need to store dp for the current node and its children that are not yet processed? Actually, when processing a node, we need dp for its children. Those children have been processed and their dp is stored. After we use them, we free them. So we only need to store dp for the current node and its children that are not yet freed. But since we free immediately after use, we only need to store dp for the current node and its children that are still needed? Actually, when processing node u, we need dp for all its children. Those children are stored. After we compute u, we free all children. So we only need to store dp for u and its children. But u's children are multiple. So we need to store dp for u and all its children. In the worst case, a node can have many children. But the total number of dp arrays stored at any time is at most the size of the subtree of the current node? Actually, when we are at node u, we have processed all nodes in its subtree. So we have dp for all nodes in the subtree. But we only need dp for the children of u. The other nodes in the subtree (descendants of children) have been processed and their dp freed? Wait, in our algorithm, we free a child's dp after processing its parent. So when we process u, we have processed all nodes in the subtree of u. For each child v of u, we have processed v and all its descendants. But after processing v, we freed v's children. So at the time we process u, we have dp for v (the child) stored, but not for v's children. So we have dp for u's children only. So the number of dp arrays stored is 1 (for u) + number of children of u. In the worst case, if u has many children, that could be large. But the sum over all nodes of (1 + number of children) is O(N). So total memory over time is O(N) dp arrays? Actually, we store dp for each node until its parent is processed. So the maximum number of dp arrays stored at any time is the maximum number of nodes that are waiting for their parent to be processed. In a tree, that is the maximum number of leaves? Actually, consider a node with many children. When we process the children, we store their dp. Then we process the parent, we need all children's dp, so we keep them. After processing parent, we free all children. So at the moment of processing parent, we have dp for parent and all its children. So the number is 1 + degree(parent). In the worst case, if a node has degree N-1, then we store N dp arrays. So memory could be O(N) dp arrays, each of size M. So O(N*M) memory in the worst case. But if we free children immediately after using them in the parent's computation, we still need to keep them until the parent is computed. So we cannot free them earlier. So we need to store dp for all children of the current node. So memory is O(N*M) in the worst case.

But maybe we can reduce memory by using a different approach: we can compute dp for each tree separately, and for each tree, we only need to keep dp for the nodes in that tree. But still, for a tree with many nodes, we need to store dp for all nodes until the root is computed. So memory is O(size of tree * M). Since total size is N, total memory is O(N*M). So we cannot avoid O(N*M) memory if we store dp for all nodes. However, we can try to use a more memory-efficient data structure. For example, we can use a list of arrays('I') which store integers as C unsigned int, which is 4 bytes each. That would reduce memory to about 16 MB. We can use the 'array' module. But we need to do modulo operations, which might be slower. Alternatively, we can use a list of lists but with small integers? Not possible.

We can try to use a 2D list where each row is a list of ints, but we can also use a single list of length N*(M+1) and index by node* (M+1) + k. That might be more memory efficient because we avoid the overhead of list objects. But still, each integer is a Python object. So we need to use something like 'array' or 'numpy'.

Given the constraints, maybe we can use the 'array' module with type 'I' (unsigned int) or 'L' (unsigned long). But we need to perform modulo operations, which might require converting to int. However, we can store numbers modulo 998244353, which fits in 32 bits. We can use array('I') and then convert to int when needed? But we need to do multiplication and addition, which might be slow if we convert to int each time. Alternatively, we can use a list of lists but with the knowledge that memory might be okay. Let's estimate: N=2025, M=2025, so N*(M+1) = 2025*2026 = about 4.1 million. Each Python int is about 28 bytes (on 64-bit), so about 115 MB. Plus overhead for the list of lists: each list has overhead, so maybe 150 MB. That might be too much for some judges with memory limit 256 MB, but could be okay if the limit is higher. However, to be safe, we should try to reduce memory.

We can try to use a different approach: we can compute dp for each tree using recursion and return the dp array to the parent, and then discard the child's dp after the parent is computed. In