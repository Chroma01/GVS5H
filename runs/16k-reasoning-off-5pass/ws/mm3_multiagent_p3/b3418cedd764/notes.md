
## ideation
The condition is `x_i <= x_{A_i}` for all i. The directed graph defined by edges i -> A_i may contain cycles. On any cycle, transitivity of <= forces all involved vertices to have the same value. So we must contract each strongly connected component (SCC) of the functional graph to a single node. After contraction, we obtain a DAG. On the DAG, the condition `value(v) <= value(u)` for each edge v -> u is equivalent to: if v has outgoing neighbors c1..ck, then `value(v) <= min(value(c1),...,value(ck))`.

We can process the DAG in reverse topological order. For each node v, let `f_v[t]` = number of ways to assign values to the subtree rooted at v (i.e., v and all its descendants) such that `value(v) = t`. Then:

`f_v[t] = prod_{child c of v} ( sum_{s=t..M} f_c[s] )`  (since child must be >= t).

We need `sum_{t=1..M} f_v[t]` for the root(s) of the DAG. The graph is a functional graph, so the contracted DAG has exactly one source (the SCC containing the "sink" of the original graph, or more generally a unique minimal element? Actually after contracting, there is exactly one node with out-degree 0, call it root). The answer is `sum_{t} f_root[t]`.

We can compute `f_v[t]` using prefix sums. Let `g_c[t] = sum_{s=t..M} f_c[s]` (suffix sums). Then `f_v[t] = prod_c g_c[t]`. We can compute suffix sums for each child, then take product over children for each t in O(M * deg(v)). Total O(N * M) since sum of degrees is O(N). N, M <= 2025, so N*M ~ 4e6 which is fast.

Steps:
1. Read N, M, array A (1-indexed).
2. Build adjacency list of the functional graph: edge i -> A[i].
3. Find SCCs using Kosaraju or Tarjan. N is small, we can use Kosaraju.
4. Contract: each SCC gets a new id. Build DAG edges between component ids (avoid self-loops).
5. Topological sort of DAG (Kahn's algorithm). Since it's a functional graph, the DAG is actually a tree-like structure (each node has out-degree at most something? Actually after contracting, each node's out-degree could be up to N, but total edges <= N).
6. Process nodes in reverse topological order. For each node v, compute its f_v array:
   - For each child c, compute suffix sums g_c[t] = sum_{s=t..M} f_c[s] mod P.
   - For t=1..M: f_v[t] = product over children of g_c[t] mod P. If v has no children (leaf in DAG, i.e., out-degree 0 after contraction), then f_v[t] = 1 for all t (since no constraints on v from children; wait, actually if v is a leaf in the DAG, it has no outgoing edges in the DAG, but it could have self-loops in the original graph? No, self-loops are within the same SCC, already contracted. So leaf means no outgoing edges in DAG, so no constraints. But we still need to count all possible values for v. For each t, there is exactly 1 way to assign v=t and the rest (no children) is empty product = 1. So f_v[t] = 1. Then answer is sum f_root[t] = M. That makes sense: if there's a single SCC with no outgoing edges (a cycle with no external edges), all its nodes must be equal, and that value can be anything from 1..M, so M ways. That matches: for a simple cycle of length k, answer is M.
7. Sum f_root[t] over t=1..M to get answer.

Let's verify with sample 1: N=3, A=[2,1,1]. Edges: 1->2, 2->1, 3->1. SCCs: {1,2} (cycle), {3}. Edges: {1,2} -> {3}? Wait: edge 1->2 is inside SCC. Edge 2->1 inside. Edge 3->1: from node 3 to SCC {1,2}. So DAG: component C={1,2} has outgoing edge to component D={3}? Actually 3->1, so node 3 points to C. So edges: D -> C. C has no outgoing edges (since its only outgoing edges were to itself and maybe others? 1->2, 2->1 are internal. So C is a sink). So DAG: D -> C. Topological order: D, C. Process C first (leaf). f_C[t] = 1 for all t. Then f_D[t] = sum_{s=t..M} f_C[s] = M - t + 1. Answer = sum_{t=1..M} f_D[t] = sum_{t=1}^M (M - t + 1) = M(M+1)/2. For M=3: 3*4/2 = 6. Matches sample.

Sample 2: N=4, A=[1,1,1,1]. SCCs: each node alone? Edge 1->1, so {1} is a self-loop, forms its own SCC. 2->1, 3->1, 4->1. So SCCs: {1}, {2}, {3}, {4}. Edges: 2->{1}, 3->{1}, 4->{1}. {1} has no outgoing. DAG: 2->1, 3->1, 4->1. Process 1: f_1[t] = 1. Process 2: f_2[t] = sum_{s=t..M} f_1[s] = M-t+1. Similarly for 3,4. Then we need to sum over roots? But there are multiple sources: 2,3,4 are sources. Wait, the condition must hold for all i. The constraint is x_i <= x_{A_i}. So we have a system of inequalities. It's not necessarily that there is a single root. The DAG is a set of nodes with edges. The condition is that for each edge u->v, x_u <= x_v. The number of valid assignments is the number of functions f: nodes -> [1,M] such that f(u) <= f(v) for all edges. This is a classic counting on a poset (the DAG). The total number is the product over antichains? Actually we can compute by processing in topological order. For each node v, its value must be >= the values of its predecessors. Wait, my earlier formulation had v <= children. That is the same as v's predecessors <= v. Let's be careful.

The condition is: for every i, x_i <= x_{A_i}. So edge i -> A_i: x_i <= x_{A_i}. So if we have edge u -> v, then x_u <= x_v. That means the value increases along the direction of edges. So in the DAG, we need x_u <= x_v for each edge u->v. That is equivalent to: for each node v, x_v >= max_{predecessors u of v} x_u. So the value is bounded below by the maximum of its predecessors. This is different from what I wrote earlier. I wrote v <= min(children). That is equivalent because if v has outgoing edges to children, then x_v <= x_{child} for each child, so x_v <= min_{child} x_child. So both are correct, but the DP direction changes. If we process in reverse topological order (starting from sinks), then for a node v, its children are the nodes it points to. The constraint is x_v <= min_{child} x_child. So if we know the distributions of children, we can compute distribution of v. That's what I had. But then the answer is the sum over the root? The root in that case is the source of the DAG (nodes with no incoming edges). Because if we process from sinks backwards, the sources are the last to be processed, and they have no constraints from predecessors? Wait, if we process from sinks (reverse topological), then for a node v, its children are the nodes that v points to. Those children are "later" in the topological order (i.e., closer to sinks). So if we go in reverse topological order (from sinks to sources), we are processing children before parents. For a source node (no incoming edges), it has no predecessors, so it only has the constraint from its children? But wait, a source node has outgoing edges (unless it's the only node). The constraint is x_source <= x_child. So it is bounded above by its children. So it is not unconstrained; it must be <= the minimum of its children. So in the reverse DP, we start from sinks (which have no outgoing edges, so no constraints from children, so x_sink can be anything: f_sink[t] = 1). Then for a node v, given its children's f_c, we compute f_v[t] = number of ways where v=t and all children are >= t. That is correct. Then the answer is the sum of f_source[t] over all source nodes? But the sources are multiple. The condition must hold for all nodes. The DP for each source node computes the number of assignments to the entire subgraph reachable from that source? Actually, if there are multiple sources, the graph is not connected in the DAG. But the condition is global: every edge must satisfy x_u <= x_v. The variables are all nodes. The DP as described processes each component separately. If we process a node v, we compute f_v[t] assuming that the entire subgraph of descendants (in the DAG) is assigned consistently with v=t. But what about interactions between different branches? In a DAG, a node can have multiple outgoing edges to different children, but those children's subgraphs are disjoint except for sharing v. The DP accounts for that: f_v[t] = product over children of (ways for child to be >= t). This is correct because the subgraphs of different children are independent given the constraint on the connecting edge. However, if there are multiple sources, they are not connected to each other, so the total number of assignments is the product of the number of assignments for each source's component? But the components are disjoint in the DAG? Actually, the original graph is a functional graph, so each node has out-degree 1. After contracting SCCs, the resulting graph is also a functional graph? Let's check: each node in the contracted graph corresponds to an SCC. For each SCC, pick a representative node i in it. Its edge goes to A[i]. The target A[i] is in some SCC. So the contracted graph has an edge from the SCC of i to the SCC of A[i]. So the contracted graph is also a functional graph (each node has out-degree exactly 1). A functional graph has exactly one cycle per connected component? Actually, a functional graph is a set of components each containing exactly one cycle. After contracting SCCs (which are exactly the cycles, because in a functional graph SCCs are the cycles plus trees attached? Wait, in a functional graph, each component has exactly one cycle. The SCCs are the nodes on the cycle, and each node not on the cycle is its own SCC (since no cycles). So after contracting, the cycles become single nodes. The resulting graph is a set of trees feeding into cycle nodes. The cycle nodes now have out-degree 1 (to each other? Actually, after contraction, the cycle becomes a single node? No, if we contract each SCC, the cycle of SCCs collapses to a single SCC if it's a cycle of length >1? Wait, in the original functional graph, the SCCs are the cycles. If the cycle has length k>1, then all k nodes are in the same SCC. So the SCC is the entire cycle. So the contracted graph has a single node representing the whole cycle. That node has no outgoing edges to other nodes (since all its edges are internal). So it's a sink. The trees attached to the cycle point to the cycle node. So the contracted graph is a forest of trees directed towards roots (the cycle nodes), and each root has no outgoing edges. There can be multiple roots (one per cycle). These roots are the sinks in the DAG (out-degree 0). The sources (in-degree 0) are the leaves of the trees.

Now, the condition x_i <= x_{A_i} means: for each node, its value is <= the value of the node it points to. In the contracted graph, this means: for each edge u->v, x_u <= x_v. Since the graph is a forest of trees pointing to roots (the cycles), the roots have no outgoing edges, so they have no upper bound from successors. But they have lower bounds from their predecessors (the trees). The leaves have no incoming edges, so they have no lower bound, but they have upper bounds from their successors.

If we process in reverse topological order (from roots to leaves), then for a root (sink in DAG, out-degree 0), there are no children, so f_root[t] = 1. Then for a node v, f_v[t] = product_{child c} (sum_{s=t..M} f_c[s]). At the end, the leaves (sources in DAG) are processed. For each leaf, we get f_leaf[t]. But the leaves are independent? Actually, the whole graph is a single DAG. The number of valid assignments is the sum over t of f_root[t]? No, the root is a sink (out-degree 0). The leaves are the sources. The DP I described computes for each node v, the number of ways to assign the subgraph consisting of v and all its descendants (i.e., all nodes reachable from v) such that x_v = t. If we start from the sinks (which have no descendants), f_sink[t] = 1. Then for a node v, we compute f_v[t] based on its children. This gives the number of assignments for the entire subgraph rooted at v. But the whole graph is not necessarily a single tree; it's a set of trees feeding into roots. The roots are the sinks. The leaves are the sources. If we process from roots to leaves, we are going backwards along edges. Actually, if the edge is u->v, then u is a predecessor of v. If we process in reverse topological order, we are processing v before u. That is correct because v is a child of u. So the children are processed first. For a root (sink), it has no children, so f_root[t] = 1. For a node u that points to v, we compute f_u[t] using f_v. This gives the number of assignments for the subtree rooted at u. If the graph is a forest where each tree has a root (sink), then each tree is independent. The total number of assignments is the product over all trees of the number of assignments for that tree. But the number of assignments for a tree with root r is sum_{t} f_r[t]? Wait, f_r[t] is the number of assignments for the tree rooted at r given that x_r = t. If we want the total number of assignments for the tree, we sum over t: sum_t f_r[t]. But in our reverse DP, we start at the leaves? Let's clarify.

Suppose we have a tree: leaf L -> A -> B, where B is the root (sink). Edges: L->A, A->B. Constraints: x_L <= x_A <= x_B.
We want to count assignments.
If we process in reverse topological order (B, then A, then L):
- B is sink: f_B[t] = 1 (no constraints on B from below; B can be anything, and there is exactly 1 way to assign the rest of the tree (nothing) given B=t).
- A points to B: f_A[t] = sum_{s=t..M} f_B[s] = M-t+1. This is the number of ways to assign A=t and the subtree below A (which is just B) such that B >= t.
- L points to A: f_L[t] = sum_{s=t..M} f_A[s] = sum_{s=t..M} (M-s+1) = ... This is the number of ways to assign L=t and the rest (A and B) consistent.
Now, the total number of assignments for the whole tree: we need to assign all three nodes. The DP f_L[t] counts assignments where L=t and the rest are consistent. So the total is sum_t f_L[t]. That is, we sum at the source (leaf) because the leaf is the "top" of the tree in the direction of edges. Alternatively, we can compute the total directly: the number of assignments is the number of tuples (x_L, x_A, x_B) with 1 <= x_L <= x_A <= x_B <= M. That is C(M+3-1, 3) = C(M+2, 3) = (M+2)(M+1)M/6. Let's check DP: f_L[t] = sum_{s=t..M} f_A[s]. f_A[t] = M-t+1. f_L[t] = sum_{s=t..M} (M-s+1) = sum_{u=1..M-t+1} u = (M-t+1)(M-t+2)/2. Sum_t f_L[t] = sum_{k=1..M} k(k+1)/2 = ... which should equal C(M+2,3). For M=3: C(5,3)=10. f_L[1] = 3*4/2=6, f_L[2]=2*3/2=3, f_L[3]=1*2/2=1, sum=10. Correct.
So the answer is sum_{t} f_source[t] where source is a node with in-degree 0 (a leaf in the tree). But wait, in a forest, there are multiple leaves. However, the DP as described computes f for every node. The total number of assignments is the product over all connected components of the sum over t of f_component_root[t]? No, the components are trees. The trees are independent because there are no edges between them. So the total assignments is the product over trees of (number of assignments for that tree). For a tree, the number of assignments is the sum over t of f_leaf[t] for any leaf? Actually, the number of assignments for the tree is the sum over t of f_root[t]? Let's think: In a tree with root R (sink), the constraints are x_v <= x_parent(v) for all v. The total number of assignments is the number of functions from nodes to [1,M] such that for each edge, child <= parent. This is equivalent to: assign values to nodes such that along any path from leaf to root, the values are non-decreasing. We can compute this by DP: for each node v, let g_v[t] be the number of ways to assign the subtree rooted at v (v and all its descendants) such that x_v = t. Then g_v[t] = product_{child c of v} (sum_{s=t..M} g_c[s]). The root R has no children? Wait, in the tree, the root R is the sink (out-degree 0). It has no children. So g_R[t] = 1. The total number of assignments for the tree is sum_t g_R[t]? No, g_R[t] is the number of ways to assign the whole tree given that the root is t. But the root has no parent, so it is free? Actually, the root has no upper bound, so it can be any value, and there is exactly 1 way to assign the rest given the root's value. So the number of assignments given root=t is 1. Thus total assignments = sum_t 1 = M. That's wrong because we have constraints on other nodes. The mistake is that the "subtree rooted at v" in the direction of edges: if v is a root (sink), its subtree is just itself. The rest of the tree is not in its subtree; it's in the subtrees of its predecessors. So the DP must be done from leaves to root or from root to leaves? Let's define direction carefully.

Original constraint: x_i <= x_{A_i}. Edge i -> A_i.
This means the value increases as we follow edges. So if we think of the graph as a set of trees pointing towards a cycle (or a sink in the contracted graph), the leaves are the sources, the roots are the sinks (cycles). The constraint is: child <= parent. So the value is non-decreasing from leaves to roots.
We can compute the number of assignments by processing from leaves to roots: for a leaf, it has no children, so it can be any value? Wait, a leaf has out-degree 0? No, in a functional graph, every node has out-degree 1. So a "leaf" in the tree sense (a node whose in-degree is 0) has out-degree 1, pointing to its parent. It has no children. The constraint is x_leaf <= x_parent. So the leaf is the minimum on its path. It has no lower bound, but it has an upper bound from its parent. So if we process from leaves to roots, we are going against the edge direction. That might be easier: for each node v, let h_v[t] be the number of ways to assign the "upward" subtree (v and all its ancestors? Actually, the tree is directed towards the root. If we process from leaves to root, we can compute for each node the number of ways to assign the subtree consisting of v and all its descendants? But v's descendants are the nodes that point to v. That is, the subtree rooted at v in the reverse graph. Let's define the reverse graph: edge A_i -> i. In the reverse graph, the edges go from parent to child. The constraint is x_child <= x_parent. So in the reverse graph, we have a forest of trees directed from root (the cycle node) to leaves (the sources). The constraint is: for each edge parent -> child, x_child <= x_parent. This is the same as: each child must be <= its parent. This is a classic problem: count assignments to a tree where each child is <= its parent. The number of assignments is the product over nodes of something? Actually, if we process in topological order of the reverse graph (from root to leaves), we can compute the number of ways to assign each node given its parent. But the root (the cycle node) has no parent, so it can be any value. The number of ways to assign the whole tree is: for the root, choose any value t in [1,M]. For each child, its value must be <= parent's value. So if we process root first, we can compute for each node the number of ways to assign its subtree given its own value. This is exactly the same as before but with the direction reversed.

Let's formalize: Let G be the contracted graph. It is a DAG. For each edge u->v, we have x_u <= x_v.
We want to count the number of functions f: V -> [1,M] such that f(u) <= f(v) for all edges.
This is the number of order-preserving maps from the poset defined by the DAG to the chain [1,M].
This is a known problem: the number of order-preserving maps from a poset P to a chain of size M is equal to the number of antichains? Not exactly. There is a formula using linear extensions, but that's #P-hard. However, for a DAG that is a forest of trees (or more generally, any DAG), we can compute it by DP if the DAG has a certain structure. But here the DAG is actually a forest of trees (since it's a functional graph contracted by SCCs). The contracted graph of a functional graph is a set of trees whose roots are the cycle nodes (which become single nodes with self-loops? Wait, after contracting, the cycles become single nodes. But those nodes have a self-loop in the original graph? Actually, if the cycle has length >1, the SCC is the whole cycle. In the contracted graph, we don't add self-loops. So the cycle node has no outgoing edges. If the cycle has length 1 (a self-loop), then the SCC is a single node. In the contracted graph, we also don't add a self-loop? Usually when contracting SCCs, we don't add self-loops. So the cycle nodes are sinks (out-degree 0). The trees point to these sinks. So the contracted graph is a forest of trees directed towards the roots (sinks). There are no edges between trees. So the problem decomposes into independent trees. For each tree, we need to count assignments such that for each edge u->v (u is child, v is parent), x_u <= x_v.

Now, for a single tree, we can root it at the sink (the root of the tree). The sink has no parent. For any other node, it has exactly one parent (the node it points to). The constraint is: for each node except the root, its value <= its parent's value. The root has no parent, so it can be any value in [1,M]. We can compute the number of valid assignments for a tree by DP. Let the root be r. For each node v, let subtree(v) be the set of descendants of v in the tree (including v). We want to count assignments to all nodes in the tree. We can compute for each node v and each value t, the number of ways to assign subtree(v) such that x_v = t. This is g_v[t] = product_{child c of v} (sum_{s=1..t} g_c[s]). Because each child c must have x_c <= x_v = t. So given x_v = t, the children can be any value in [1..t] independently. The number of ways for child c to have value s is g_c[s]. So the number of ways for child c to be <= t is sum_{s=1..t} g_c[s]. Then g_v[t] is the product of these over all children. For a leaf (no children), g_leaf[t] = 1 for all t. For the root, the total number of assignments for the tree is sum_{t=1..M} g_root[t].

Wait, is that correct? Let's test with the simple tree: leaf L -> A -> B (B is root, sink). Edges: L->A, A->B. In this tree, B is root. Children: A is child of B, L is child of A.
DP:
- L: leaf, g_L[t] = 1 for all t.
- A: child is L. g_A[t] = sum_{s=1..t} g_L[s] = t.
- B: child is A. g_B[t] = sum_{s=1..t} g_A[s] = sum_{s=1..t} s = t(t+1)/2.
Total assignments = sum_{t=1..M} g_B[t] = sum_{t=1}^M t(t+1)/2 = C(M+2,3). This matches the earlier result! And it's much simpler: we use prefix sums instead of suffix sums, and we process from leaves to root (which is reverse topological order of the original graph, or topological order of the reverse graph). So the DP direction is: root is the sink of the original functional graph (after contraction). Process in reverse topological order (i.e., from leaves towards root). For each node v, compute f_v[t] = product_{child c} (sum_{s=1..t} f_c[s]). Then answer = sum_t f_root[t] for each tree root, and multiply across trees? But wait, the original graph is a functional graph, which may have multiple components. Each component has exactly one cycle. After contracting, each component becomes a tree with a root (the cycle node). The trees are independent because there are no edges between components. So the total number of assignments is the product over all components of (number of assignments for that component's tree). But careful: the cycle node is a single node after contraction. In the original graph, the cycle has multiple nodes, but they are forced to have the same value. So the component is a cycle with trees attached. The cycle nodes have no outgoing edges in the contracted graph (since the cycle is contracted to a single node). The trees are attached to cycle nodes. So each component is a tree rooted at the cycle node. The DP above works for each such tree. The total number is the product over all components of (sum_t f_root[t] for that component's root). Since components are independent, the total is the product.

Let's verify with sample 1: N=3, A=[2,1,1]. SCCs: {1,2} (cycle), {3}. Component 1: cycle {1,2} contracted to one node, call it C. No trees attached. So it's just a single node. For a single node with no children, f_C[t] = 1. Sum = M = 3. Component 2: node 3 points to 1, so 3 is a leaf, and its child is C. In the tree rooted at C, node 3 is a leaf. So f_3[t] = 1. f_C[t] = sum_{s=1..t} f_3[s] = t. Sum over t: 1+2+3=6. Multiply across components: 3 * 6 = 18? That's not 6. Wait, sample 1 answer is 6. So the product over components is not correct. Why? Because the original graph is a single component! Let's check: N=3, A=[2,1,1]. Edges: 1->2, 2->1, 3->1. This is a single connected component: the cycle 1<->2, and node 3 points to 1. So there is only one component. The SCCs are {1,2} and {3}. But these two SCCs are connected by an edge 3->1. So after contracting, we have a graph with two nodes: C12 and C3, and an edge C3 -> C12. That is a tree with root C12 and leaf C3. So it's a single component (a tree). There is no separate component. The cycle is part of the same component. So the contracted graph is a forest of trees, each tree corresponds to one original connected component. In this case, the whole graph is one component, so it's one tree. The DP gives sum f_root[t] for that root (C12). f_C3[t] = 1. f_C12[t] = sum_{s=1..t} f_C3[s] = t. Sum = 6. That's the answer. So we don't multiply across components because each original component becomes one tree in the contracted graph. The product over components would be if there were multiple trees with no edges between them. But in the original graph, each component is a functional graph component. After contracting, each component is a single tree (with a root that is a sink). So the whole graph is a forest of trees, each tree being one original component. The answer is the product over these trees of (sum f_root[t]). But wait, in sample 1, there is only one tree, answer 6. Sample 2: N=4, A=[1,1,1,1]. Edges: 1->1, 2->1, 3->1, 4->1. This is one component: node 1 is a self-loop, others point to 1. SCCs: {1}, {2}, {3}, {4}. Contracted graph: 2->1, 3->1, 4->1. That's a tree with root 1, children 2,3,4. Leaves 2,3,4 have no children, so f_2[t]=1, etc. f_1[t] = product_{c=2,3,4} (sum_{s=1..t} 1) = t^3. Sum_{t=1..9} t^3 = (9*10/2)^2 = 2025. Matches sample 2.

Sample 3: N=10, M=5, A = [9,4,5,5,4,2,1,5,7,2]. We can trust it.

So the algorithm:
1. Find SCCs of the functional graph. Since N <= 2025, we can use Kosaraju or Tarjan.
2. Contract SCCs. For each node i, let comp[i] be its SCC id. For each edge i -> A[i], add edge from comp[i] to comp[A[i]] if they are different. This gives a DAG (actually a forest of trees directed towards roots). Note: the graph may have multiple roots (sinks in the DAG), but each root corresponds to a cycle in the original graph.
3. Topological sort of the contracted graph. We can do Kahn's algorithm. The graph is a forest, so we can also process in reverse topological order (from leaves to roots). Since the graph is a forest, we can simply do a DFS from each root (sink) to compute the DP, or process nodes in order of decreasing depth. But because the graph is a DAG, we can compute topological order.
4. For each node in reverse topological order (i.e., starting from nodes with out-degree 0 in the contracted graph? Wait, in the contracted graph, edges are from child to parent (since original edge i->A[i] means child to parent). The root has out-degree 0. The leaves have in-degree 0. In reverse topological order, we process from root to leaves? No, in the DP f_v[t] = product_{child c} (sum_{s=1..t} f_c[s]), we need the children's f_c to be computed before v. The children are the nodes that point to v. That is, in the contracted graph, if edge is u->v, then u is a child, v is a parent. So children have out-edges to their parents. So children come before parents in topological order? Let's check: topological order of a DAG is an ordering where for every edge u->v, u comes before v. In our graph, edges are child -> parent. So in topological order, children come before parents. So we can process nodes in topological order: start with leaves (in-degree 0), and move towards roots (out-degree 0). That is, we process in the order of the original edge direction. That works: for a leaf, no children, so f_leaf[t] = 1. For a parent, we already computed all its children, so we can compute f_parent[t]. At the end, for each root (out-degree 0), we have f_root[t]. The answer is the product over all roots of (sum_{t=1..M} f_root[t]).

Wait, is that correct? Let's test with the simple tree: B is root (out-degree 0), A is child, L is child of A. Edges: L->A, A->B. Topological order: L, A, B. Process L: f_L[t]=1. Process A: children = {L}, f_A[t] = sum_{s=1..t} f_L[s] = t. Process B: children = {A}, f_B[t] = sum_{s=1..t} f_A[s] = t(t+1)/2. Sum over t: sum t(t+1)/2 = C(M+2,3). Correct. So the DP is: process nodes in topological order (from leaves to roots). For each node v, compute f_v[t] for t=1..M as product over children c of (prefix sum of f_c up to t). Since M <= 2025, we can precompute prefix sums for each child. Total time: O(N * M + total edges * M). Total edges in contracted graph <= N. So O(N*M) ~ 4e6, fast.

Implementation details:
- N, M up to 2025.
- Use 0-indexed or 1-indexed carefully.
- Find SCCs: Kosaraju:
  - Build adjacency list of original graph: adj[i] = [A[i]].
  - Also build reverse graph: radj[A[i]].append(i).
  - DFS1 to get order (finish times).
  - DFS2 on reverse graph in reverse order to assign component ids.
- Contract: comp[i] for each i. Let C be number of components.
- Build contracted graph: for each i, if comp[i] != comp[A[i]], add edge comp[i] -> comp[A[i]]. Use a set or boolean matrix to avoid duplicate edges. Since N is small, we can use a list of sets or just a 2D boolean array, or we can use a list of lists and skip duplicates when iterating? Duplicate edges don't affect the DP because we will multiply over children. If we have duplicate edges, we would multiply the same child multiple times, which is wrong. So we must deduplicate. We can use a set of pairs or a boolean matrix. C <= N <= 2025, so a C x C boolean matrix is fine.
- Topological sort: Kahn's algorithm. Compute in-degree for each component. Queue nodes with in-degree 0. Process them, decreasing in-degree of their neighbors.
- DP: f is a list of lists: f[v][t] for t=1..M (0-indexed: t=0..M-1). Initialize f[v] for all v as size M.
- For each node v in topological order:
  - For each child c (i.e., for each edge v->c in contracted graph), compute prefix sums: prefix[t] = sum_{s=0..t} f[c][s] mod P.
  - Then f[v][t] = product over children of prefix[t] mod P.
  - If v has no children (leaf in the contracted graph, i.e., no outgoing edges in the contracted graph? Wait, in the contracted graph, edges are child -> parent. So leaves in the tree (in-degree 0) have no children? Actually, in the tree rooted at the cycle, the root has no outgoing edges (out-degree 0). The leaves have in-degree 0, and they have outgoing edges to their parent. So a leaf has out-degree 1 (to its parent), and no incoming edges. So in the DP, a leaf has no children? No, a leaf's children are the nodes that point to it. Since no one points to it, it has no children. So for a leaf (in-degree 0 in the contracted graph), we set f_leaf[t] = 1. That matches: f_leaf[t] = product over empty set = 1.
  - So we process in topological order. The first nodes in topological order are those with in-degree 0 (leaves). For them, f[v][t] = 1. Then we propagate.
- At the end, we need the product over all roots (out-degree 0 in the contracted graph) of (sum_t f_root[t]). But wait: are there multiple roots? In a functional graph, each component has exactly one cycle. After contracting, each component becomes a tree with a single root (the cycle node). So there is exactly one root per component. The whole graph is a forest of trees, each with one root. So we can find all roots (nodes with out-degree 0 in the contracted graph) and multiply their total sums.
- Alternatively, since the original graph is a single functional graph, it may have multiple components. Each component's cycle becomes a root. So we can just multiply over all roots.

Let's double-check with sample 1: components: C12 (cycle), C3. Edges: C3 -> C12. In-degree: C12: 1, C3: 0. Out-degree: C12: 0, C3: 1. Topological order: C3, C12. Process C3 (leaf): f[C3][t] = 1. Process C12: children = {C3}. prefix for C3: prefix[t] = t. f[C12][t] = t. Roots: C12 is root. Sum f[C12][t] = 1+2+3=6. Answer 6. Correct.

Sample 2: components: {1}, {2}, {3}, {4}. Edges: 2->1, 3->1, 4->1. In-degree: 1: 3, others: 0. Out-degree: 1: 0, others: 1. Topological order: 2,3,4,1. Process 2: f=1. Process 3: f=1. Process 4: f=1. Process 1: children = 2,3,4. For each child, prefix[t] = t. So f[1][t] = t*t*t = t^3. Sum t^3 = 2025. Correct.

Sample 3: we can trust.

So the algorithm is:
- Find SCCs.
- Build contracted DAG, deduplicate edges.
- Topological sort.
- DP from leaves to roots: for each node in topological order, compute f[v][t] = product_{c in children(v)} (sum_{s=1..t} f[c][s]) mod P.
- Answer = product_{v: out-degree(v)=0} (sum_{t=1..M} f[v][t]) mod P.

Complexity: O(N + M*N) ~ 4e6 operations. M and N up to 2025, so 2025*2025 = 4.1 million. Modulo 998244353.

Edge cases:
- N=1, M=1, A=[1]. SCC: {1}. Contracted: no edges. Root is 1. f[1][t] = 1. Sum = 1. Answer 1.
- N=1, A=[1], M=5. f[1][t]=1. Sum=5. Correct: x1 can be 1..5.
- All A_i = i: N self-loops. SCCs: each node alone. Contracted: no edges. Each node is a root. For each node, f[i][t] = 1. Sum = M. Answer = M^N. Because each node is independent (no constraints between them). Correct: x_i <= x_i is always true, so each can be chosen independently.
- A forms a single cycle of length N, with no trees. Then one SCC, one node, no edges. f[1][t]=1. Sum=M. Answer=M. Correct: all must be equal, so M choices.

Now, we need to implement this in Python. N, M up to 2025, so we can use lists of lists. Mod = 998244353.

Steps in code:
1. Read N, M.
2. Read A (1-indexed, convert to 0-indexed).
3. Build adjacency list: adj = [[] for _ in range(N)]; for i in range(N): adj[i].append(A[i]).
4. Build reverse adjacency: radj = [[] for _ in range(N)]; for i in range(N): radj[A[i]].append(i).
5. Kosaraju:
   - visited = [False]*N.
   - order = [].
   - def dfs1(v): visited[v]=True; for u in adj[v]: if not visited[u]: dfs1(u); order.append(v).
   - For i in range(N): if not visited[i]: dfs1(i).
   - comp = [-1]*N.
   - def dfs2(v, c): comp[v]=c; for u in radj[v]: if comp[u]==-1: dfs2(u, c).
   - c = 0; for v in reversed(order): if comp[v]==-1: dfs2(v, c); c+=1.
6. C = c (number of components).
7. Build contracted graph:
   - children = [[] for _ in range(C)] (list of children for each node).
   - out-degree = [0]*C.
   - in-degree = [0]*C.
   - Use a set to avoid duplicate edges: edge_set = set() or a 2D list. Since C <= 2025, we can use a list of sets: edges = [set() for _ in range(C)].
   - For i in range(N): u = comp[i]; v = comp[A[i]]; if u != v: if v not in edges[u]: edges[u].add(v); children[u].append(v); out-degree[u]+=1; in-degree[v]+=1.
   Actually, careful: the edge is from i to A[i]. So in the contracted graph, it's from u to v. The "children" in the DP are the nodes that point to the current node. In the DP, for a node v, we need its children: the nodes c such that c -> v. So we should build the reverse edges: parents[v] = list of c such that c -> v. But it's easier to just build the forward edges and then when processing v, we need the nodes that have an edge to v. So we can either build the reverse adjacency: rev[v] = list of u such that u -> v. Then in DP, for v, children = rev[v]. That's better.
   So:
   - rev = [[] for _ in range(C)].
   - For each edge u->v: rev[v].append(u). Also keep track of in-degree and out-degree for topological sort. In-degree of v in the DAG: number of edges into v. Out-degree of u: number of edges out of u.
   - For topological sort, we need the in-degree of each node in the DAG (edges from u to v). We can compute in-degree as the number of incoming edges.
   - Then we process in topological order: start with nodes with in-degree 0. When we process u, for each v in children[u] (i.e., v is a neighbor in the forward graph), we decrement in-degree of v. When in-degree becomes 0, we add to queue.
   - But in the DP, we need the children of v (nodes that point to v). So we need rev[v] (list of u such that u->v). So we will have:
     - forward: for each u, forward[u] = list of v.
     - rev: for each v, rev[v] = list of u.
   - Topological order: use in-degree based on forward edges. Queue in-degree 0.
   - DP: for u in topological order:
        f[u] = [1]*M
        for t in range(M): f[u][t] = 1
        For each child c in rev[u] (i.e., c -> u):
            Compute prefix sum of f[c] up to each t.
            Multiply to f[u][t].
   - Wait, the children are the nodes that point to u. So we need rev[u]. But in topological order, we process u before its parents? No, topological order processes u before v if u->v. So if u points to v, u is processed before v. In the DP, for v, we need the f of its children (u). Since u is processed before v, that's correct. So we can process in topological order (starting from in-degree 0 nodes). For a node u, its children are the nodes that have an edge to u. Those children have been processed already? Actually, if u has in-degree > 0, it has children pointing to it. Those children are the sources of edges into u. Since edges go from child to parent, the child has in-degree possibly >0? No, the child could have in-degree 0 (a leaf) or could have other children. But in any case, the child is a predecessor in the DAG. In topological order, all predecessors of u are processed before u. So yes, all children of u are processed before u. So we can just use the rev adjacency.

   Let's test: In the tree L->A->B. Forward: L->A, A->B. rev: A: [L], B: [A]. In-degree: L:0, A:1, B:1. Topological order: L, A, B.
   Process L: rev[L] is empty. f[L][t] = 1.
   Process A: rev[A] = [L]. prefix of f[L]: [1,2,3,...]. f[A][t] = t.
   Process B: rev[B] = [A]. prefix of f[A]: [1, 1+2=3, 1+2+3=6,...]. f[B][t] = t(t+1)/2.
   Sum at B: sum f[B][t] = C(M+2,3). Correct.

   So the DP is:
   - f = [[1]*M for _ in range(C)].
   - For u in topo_order:
        for c in rev[u]:
            # multiply f[u] by prefix sums of f[c]
            # compute prefix on the fly or precompute? M is small, we can compute prefix in a loop.
            # Since we need to do this for each child, we can precompute prefix[c] once, but we can just compute it inside the loop.
            # For efficiency, we can precompute prefix for each node after computing its f.
            # Actually, we can compute prefix in a separate array or just compute on the fly.
            # Since M is small, we can just do:
            #   running = 0
            #   for t in range(M):
            #       running = (running + f[c][t]) % mod
            #       f[u][t] = f[u][t] * running % mod
        # If rev[u] is empty, f[u] remains [1]*M.
   - After DP, roots are nodes with out-degree 0 (no forward edges). Answer = product over roots of (sum(f[root])) % mod.

   Wait, is the answer the product over roots? In the tree example, there is only one root (B). The answer is sum f[B]. If there are multiple trees (i.e., multiple components in the original graph), then they are independent, and the total number of assignments is the product of the number of assignments for each tree. But is it true that each tree's assignments are independent? Yes, because there are no edges between different trees. So the constraints don't link them. So the total is the product. So we multiply the sums for all roots.

   Let's verify with a case where the original graph has two separate components. N=2, A=[1,2] (two self-loops). M=2. Components: {1}, {2}. Contracted: no edges. Roots: 1 and 2. f[1][t]=1, f[2][t]=1. Sum f[1]=2, sum f[2]=2. Product = 4. The sequences: x1,x2 in [1,2]^2, constraints: x1<=x1 (always), x2<=x2 (always). So all 4 sequences. Correct.

   Another case: N=2, A=[1,1]. This is one component: 1 self-loop, 2->1. Contracted: 2->1. Roots: 1. f[2]=1. f[1][t] = sum_{s=1..t} 1 = t. Sum f[1] = 1+2=3. Total sequences: (x1,x2) with x2<=x1. For M=2: (1,1), (2,1), (2,2) -> 3. Correct.

   So the product over roots is correct.

Implementation details:
- N, M up to 2025. Use recursion for DFS? Python recursion limit might be an issue if N=2025? 2025 is fine for default recursion limit (1000)? Actually default is 1000. So we need to either set recursion limit higher or use iterative DFS. Let's use iterative or set sys.setrecursionlimit(10000).
- Use 0-indexing.
- Mod = 998244353.

Let's write the code structure:

```python
import sys
sys.setrecursionlimit(10000)

def solve():
    MOD = 998244353
    N, M = map(int, sys.stdin.readline().split())
    A = list(map(int, sys.stdin.readline().split()))
    A = [a-1 for a in A]
    
    # Build graph
    adj = [[] for _ in range(N)]
    radj = [[] for _ in range(N)]
    for i in range(N):
        adj[i].append(A[i])
        radj[A[i]].append(i)

## worker: Implement the solution: read N, M, A; build graph;
The topological sort logic is incomplete: we need forward adjacency to traverse the DAG. I should build `forward` adjacency as well, or traverse from `u` to its parents. Let's fix: we need to decrement in-degree of the node that `u` points to. In the contracted graph, edge is `u -> A_comp`. So for each `u`, we have a list of `v` such that `u -> v`. We can build that.

## worker: Implement the solution in Python: complete the top
The solution works as follows:
1. **SCC contraction**: The condition `x_i <= x_{A_i}` forces all nodes in a cycle to have equal values. So we find strongly connected components (SCCs) and contract them. The resulting graph is a DAG where each node has out-degree at most 1 (actually a forest of trees directed towards the roots).
2. **DP on DAG**: Process nodes in topological order (from leaves to roots). For each node `u`, let `f[u][t]` be the number of valid assignments to the subtree rooted at `u` (in the reverse direction) given that `x_u = t`. The recurrence is `f[u][t] = product_{child c of u} (sum_{s=1..t} f[c][s])`. This can be computed efficiently using prefix sums.
3. **Answer**: The roots of the DAG (nodes with out-degree 0) correspond to the contracted cycles. The total number of valid assignments is the product over all roots of `sum_{t=1..M} f[root][t]`, because different trees are independent.

The time complexity is `O(N * M)` after SCC computation, which is fast for `N, M <= 2025`.
