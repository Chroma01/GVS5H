
## ideation
The problem asks for, for every M from N-1 to N(N-1)/2, the number of connected labeled simple graphs on N vertices such that the BFS from vertex 1 has exactly N/2 even-distance and N/2 odd-distance vertices.

The standard approach is to use exponential generating functions over labeled structures: treat a connected graph as a rooted BFS tree (vertex 1 is root) together with a set of "non-tree" edges that may connect vertices inside a layer or between adjacent layers, but never skip a layer (otherwise the BFS layering would change). We need to count labeled graphs with a prescribed layering k_0=1, k_1, ..., k_L (k_i vertices in layer i) such that:
- sum_i k_i = N,
- sum_{i even} k_i = sum_{i odd} k_i = N/2,
- the number of tree edges is N-1,
- cross edges are allowed only inside a layer or between layer i and i+1.

For a fixed depth L and fixed layer sizes, the count of labeled graphs with that exact layering is:
   N! / (∏ k_i!)   ×   (∏ P_layer(k_i))   ×   (∏ P_between(k_i, k_{i+1}))
where:
- N!/(∏ k_i!) assigns labels to layers,
- P_layer(k) is the number of simple graphs on k labeled vertices, i.e., 2^{k choose 2}, but we must subtract 1 if k=0? Actually for a layer graph, the only forbidden case is the empty graph on 0 vertices; for k>=1, 2^{C(k,2)} is fine. However we want the subgraph induced by the layer to be simple and unlabeled within the structure; using ordinary generating function (OGF) multiplication over labels is easier, so we will not divide by k_i! globally but rather track labels with a set construction.
- P_between(k_i, k_{i+1}) is the number of simple bipartite graphs between the two layers: 2^{k_i * k_{i+1}}.

The clean way is: use the labeled product (set construction) of components, which gives factor of 1/k! automatically. The EGF of a connected graph with a fixed rooted BFS layering is:

C(x) = x * exp( E_in(x) + E_bip(x) )

where E_in counts edges inside layers and E_bip counts edges between consecutive layers, treated as a "set" of edges (each edge is a labeled pair). Actually we need the EGF for connected graphs respecting the layering. The classical formula (see "connected graphs with given BFS layers" by [Bell, Burris, Yeats]) is:

The EGF for connected graphs where layer i has a_i vertices and edges are only within a layer or between adjacent layers is:

   C_{a_0,a_1,...}(x) = x^{a_0} / a_0! * ∏_{i>=0} ( (1 + x)^{a_i a_{i+1}}? no)

Better: The ordinary generating function for a set of components where each component is a "block" of layer vertices. The classic EGF is:

   C_{L}(x) = x * exp( A(x) + B(x) )
   
where A(x) counts the edges inside a single layer (as a set of edges among the layer's vertices), and B(x) counts edges between two consecutive layers. Specifically, if we treat each layer i (i>0) as a set of k_i vertices, the EGF for edges within layer i is:

   ∑_{k>=0} 2^{C(k,2)} x^k / k!

and for edges between layer i and i+1 with sizes a and b, the EGF factor is:

   ∑_{a,b>=0} 2^{a b} x^{a+b} / (a! b!)

This looks like a product of simpler EGFs, but the sizes a,b are shared across the between-layer edges and the layer sizes themselves. The way to handle this is: consider the BFS tree as a sequence of "blocks" (each block corresponds to a layer, but layers are connected to the previous one). A standard decomposition: The EGF for a connected graph with a distinguished root and a given BFS depth L is:

   x * B_0(x) * B_1(x) * ... * B_L(x) / (something)?

Actually, the generating function that directly gives the number of connected labeled graphs with a given BFS layering is known. Let me recall: for each non-root layer, we can think of it as a "set of components" attached to the previous layer, but the structure is more complex because cross edges between non-adjacent layers are forbidden, so the graph is a "caterpillar-like" structure? No, edges are allowed between layer i and i+1 only. This means the graph is exactly a "layered graph" with no long-range edges. The number of such labeled graphs for fixed layer sizes (k_0=1, k_1,...,k_L) is:

   (∏ 2^{C(k_i,2)}) * (∏ 2^{k_i k_{i+1}})   (times the number of ways to assign labels?)

But wait, the labels are already assigned to vertices. If we fix the set of labels that belong to each layer, then the number of graphs with that exact partition of labels is exactly:

   2^{ ∑ C(k_i,2) + ∑ k_i k_{i+1} }

because we independently decide for each potential edge (within layer or between consecutive layers) whether it exists. (Edges between non-consecutive layers are forbidden, edges between same layer are allowed, edges between adjacent layers allowed.) So the total number of labeled graphs with a given labeling is just a product of powers of 2. Then we sum over all partitions of the N labels into layers with k_0 containing label 1, and weight each by the number of ways to choose which labels go to which layer: (N-1)! / (∏_{i=1}^L k_i!) . The tree edges are already counted implicitly: any connected labeled graph whose BFS layering matches the given layer sizes must contain a spanning tree (the BFS tree) which has exactly N-1 edges, and the remaining M - (N-1) edges are the non-tree edges. But our count 2^{...} counts all edge subsets, including disconnected ones! We need connectedness.

This is the crux: the simple product 2^{...} counts all graphs (connected and disconnected) with that BFS layering. The BFS layering from vertex 1 uniquely determines the connected component containing vertex 1; if the graph is disconnected, vertex 1's component is smaller. But if we require the graph to be connected, then the BFS layering must cover all N vertices, and the set of edges must connect them. However, just having edges within layers and between adjacent layers does not guarantee connectedness. So we cannot just use the raw 2^{...}.

The correct decomposition: The set of edges E can be partitioned into:
- Tree edges T: a spanning tree of the graph that respects the layering (edges go from parent in layer i to child in layer i+1). A tree respecting the layering is exactly a rooted tree where each non-root vertex has a parent in the previous layer.
- Non-tree edges: all other edges within layers or between adjacent layers.

For a fixed layering and a fixed rooted tree T (which determines a set of N-1 parent-child edges), the number of ways to add any subset of the remaining allowed edges is 2^{ total_allowed_edges - (N-1) }. The total allowed edges (within layers and between adjacent layers) is sum_i C(k_i,2) + sum_i k_i k_{i+1}. The tree uses N-1 edges, all of which must be between consecutive layers (parent-child). So the number of graphs extending tree T with exactly M edges is: 1 if M = N-1, else choose M - (N-1) edges from the remaining allowed edges. Summing over all trees T that respect the layering.

So for fixed layer sizes, the number of connected labeled graphs with that exact BFS layering is:

   sum_{T} C( R(T), M - (N-1) )    for M >= N-1

where R(T) = total_allowed_edges - (N-1) is the number of non-tree edges available, and the sum is over all rooted trees T on the labeled vertices with those layer sizes (root=vertex 1 in layer 0, each other vertex's parent is in the previous layer).

Counting the number of such trees T: Given layer sizes k_0=1, k_1,...,k_L, the number of rooted trees where each non-root vertex chooses a parent in the previous layer is:

   k_1^{k_2?} No: each vertex in layer i>=1 chooses a parent in layer i-1 independently. So the number of trees is:

   k_1^{k_2? No, it's: for each vertex in layer 1, its parent is vertex 1 (only choice), so k_1 choices? Wait, vertex 1 is the only vertex in layer 0, so each of the k_1 vertices in layer 1 must have parent 1. So 1 way. For layer 2, each of k_2 vertices chooses a parent among k_1 vertices in layer 1: k_1^{k_2} ways. For layer 3: k_2^{k_3} ways. ... For layer L: k_{L-1}^{k_L} ways.

So the number of trees T is:
   ∏_{i=1}^L k_{i-1}^{k_i}   (with k_0=1)

Note: This counts each tree exactly once because the BFS layering is given and the parent of each vertex is uniquely determined by the tree, and the tree is exactly the set of parent-child edges.

Therefore, the total number of connected labeled graphs with exact BFS layering (k_0=1, k_1,...,k_L) is:

   ∑_{M=N-1}^{M_max} ( number of ways to choose labels for layers ) × ( number of trees T ) × ( number of ways to pick non-tree edges to get M total edges )

Let A = sum_i C(k_i,2) + sum_i k_i k_{i+1}  (total allowed edges)
Let B = N-1  (tree edges)
Let R = A - B  (available non-tree edges)

Number of ways to choose labels for layers with vertex 1 fixed in layer 0: (N-1)! / (k_1! k_2! ... k_L!)

Number of ways to pick exactly e = M - (N-1) non-tree edges from the R available: C(R, e)

So the count for this layering is:

   (N-1)! / (∏_{i=1}^L k_i!)  ×  (∏_{i=1}^L k_{i-1}^{k_i})  ×  C(R, M - (N-1))

We sum this over all sequences (k_1,...,k_L) with k_i >= 1, sum k_i = N-1, and the even/odd balance condition: 1 + sum_{i even, i>=2} k_i = sum_{i odd} k_i = N/2.

Wait: layer 0 is even (distance 0), so even layers are i=0,2,4,...; odd layers are i=1,3,5,...
Condition: sum_{i even} k_i = sum_{i odd} k_i = N/2.
Since k_0=1, we need sum_{i even, i>=2} k_i = N/2 - 1, and sum_{i odd} k_i = N/2.

So we need to iterate over L from 1 to N-1, over all compositions (k_1,...,k_L) of N-1 into L positive parts, with the parity sum constraints, compute the formula, and accumulate by M = N-1 + e where e = 0..R.

The number of such compositions is manageable? N <= 30, so N-1 <= 29. The number of compositions of 29 into at most 29 parts is 2^{28} ~ 2.7e8, too large. But we have the parity constraint, which roughly halves it, but still too large.

We need a smarter DP. Note that the formula factors over layers! Let's check:

(N-1)! / (∏ k_i!) × ∏ k_{i-1}^{k_i}  =  (N-1)! × ∏ [ k_{i-1}^{k_i} / k_i! ]

This suggests we can process layers one by one using a DP that tracks the current depth parity, the number of vertices assigned so far, and maybe the accumulated R or something. But the binomial coefficient C(R, e) depends on the total R, which is sum_i [C(k_i,2) + k_i k_{i+1}]. This couples adjacent layers.

However, we can treat the whole structure as a sequence of "blocks" where we keep track of the number of edges contributed so far. Let's define the DP state as we process layers from left to right (layer 1 to L). At the boundary between layer i and i+1, we have a term k_i k_{i+1} in R, and also a term C(k_i,2) in R. The R depends on k_i and k_{i+1} together, but we can think of it as: when we add layer i, we add C(k_i,2) to R, and when we transition to i+1, we add k_i k_{i+1}.

Actually, the total R is:
   R = ∑_{i=0}^L C(k_i,2) + ∑_{i=0}^{L-1} k_i k_{i+1}
     = ∑_{i=0}^L [C(k_i,2) + k_i k_{i+1}]  - k_L * 0  (since k_{L+1}=0)
Wait, k_{L+1}=0 so the last term is 0. Let's write:
   R = ∑_{i=1}^L C(k_i,2) + ∑_{i=0}^{L-1} k_i k_{i+1}
   (k_0=1, so C(1,2)=0, and k_0 k_1 = k_1)

So R = ∑_{i=1}^L C(k_i,2) + k_1 + ∑_{i=1}^{L-1} k_i k_{i+1}
    = ∑_{i=1}^L C(k_i,2) + ∑_{i=1}^{L-1} k_i k_{i+1} + k_1

This is sum over edges: within layer i (i>=1) and between layer i-1 and i (i>=1). So R is exactly the number of non-tree edges available. Note that the tree uses exactly one edge from each k_{i-1} k_{i+1}? No, the tree uses exactly N-1 edges, each being a parent-child edge. The parent-child edges are a subset of the between-layer edges (layer i-1 to i). Specifically, the tree uses k_i edges from the k_{i-1} * k_i possible between-layer edges (for i>=1). So the number of between-layer edges available as non-tree edges is k_{i-1} k_i - k_i. The number of within-layer edges available is C(k_i,2) (all are non-tree). So:

R = ∑_{i=1}^L C(k_i,2) + ∑_{i=1}^L (k_{i-1} k_i - k_i)
  = ∑_{i=1}^L C(k_i,2) + ∑_{i=1}^L k_{i-1} k_i - (N-1)

Which matches: A = ∑ C(k_i,2) + ∑ k_{i-1} k_i (with k_0=1), and B = N-1, so R = A - B.

Now, the generating function approach: For each non-root layer i (i>=1), we need to "add" a set of vertices to the graph. The layer i contributes:
- A set of k_i vertices (labels chosen from remaining).
- All C(k_i,2) within-layer edges (each edge is a pair, so as a set of edges, the EGF is ∑ 2^{C(k,2)} x^k / k!).
- The connections to the previous layer: a set of k_i edges from previous layer to this layer, but exactly one per vertex is the tree edge. The tree edge is part of the parent assignment. The remaining k_{i-1} k_i - k_i edges are available as non-tree edges.

This is getting complex. Let's consider the polynomial approach. For each M, we want to compute:

ans[M] = sum_{L, k} (N-1)! / ∏ k_i! × ∏ k_{i-1}^{k_i} × C(R, M - (N-1))

where the sum is over valid layer sequences. Let's define a DP over the layers. We process layers 1 to L sequentially. At step i, we have chosen k_1,...,k_i. We know the current depth i. We have a partial sum of vertices V = sum_{j=1}^i k_j. We have a partial R_partial = sum_{j=1}^i C(k_j,2) + sum_{j=1}^i k_{j-1} k_j - i? Wait, the tree edges for the first i layers are i edges (since k_0=1 uses 0, layer 1 uses k_1 edges, ..., layer i uses k_i edges? No, the tree uses one edge per vertex in layers 1..L, so after i layers, i edges are used. But the available non-tree edges from these i layers and the connections to the next layer are not fully determined until we know k_{i+1}.

Actually, R is fully determined once the full sequence is known. We can think of the sum as:

   (N-1)! × ∏_{i=1}^L [ k_{i-1}^{k_i} / k_i! ] × C(R, e)

where e = M - (N-1) and R = ∑_{i=1}^L [C(k_i,2) + k_{i-1} k_i] - (N-1).

This looks like we can factor the product and the binomial if we introduce a variable for the number of non-tree edges. Let's define for each layer i a "contribution" that includes the term k_{i-1}^{k_i} / k_i! and a factor x^{C(k_i,2) + k_{i-1} k_i}. But k_{i-1} is the size of the previous layer, so the factor depends on the previous layer's size.

A better way: Use a DP that processes the graph edge by edge? No.

Let's consider the exponential generating function in two variables: x for vertices, y for edges. The EGF for a connected graph with a distinguished root and BFS layering is known. According to the literature (e.g., "The number of connected labeled graphs" by Wright, or the paper by Temperley or others), the EGF for connected labeled graphs with a given BFS depth is not standard, but we can derive it.

Let C(x, y) be the EGF where x marks vertices and y marks edges, and we want only connected graphs with vertex 1 in the root layer. Actually, we can use the "dissymmetry theorem" or "rooted" vs "unrooted".

Consider building the graph by adding layers. The structure of a graph with a BFS layering from vertex 1 is:
- Vertex 1 in layer 0.
- A set of non-empty layers (layer 1, 2, ..., L).
- For each layer i >= 1, it consists of a set of vertices (size k_i) and:
  * A set of edges within the layer (forming an arbitrary simple graph on k_i vertices): EGF 2^{C(k,2)} x^k / k!.
  * A set of edges to the previous layer (forming an arbitrary simple bipartite graph between the k_i vertices and the previous layer's vertices): but the tree requires exactly one edge per vertex in this layer to the previous layer. Wait, no: the graph can have any number of edges between the layers, but the BFS layering requires that there is at least one path of length i from vertex 1, and no path of length < i. This means that in the subgraph induced by layers 0..i, vertex 1 is connected to all vertices in layer i, and there are no edges from layer i to layers < i? Actually, edges from layer i to layer i-1 are allowed (they are between adjacent layers), and there must be at least one edge from each vertex in layer i to layer i-1 (to have distance exactly i). However, the BFS layering is defined as the set of vertices at distance exactly i. So by definition, every vertex in layer i must have at least one neighbor in layer i-1, and no neighbor in layers < i-1 (otherwise the distance would be smaller). But wait: a vertex in layer i could have neighbors in layer i-2? If it did, its distance would be at most i-2, contradiction. So edges are only allowed within a layer or between layer i and i+1. And every vertex in layer i (i>=1) must have at least one edge to layer i-1.

Ah! This is a crucial constraint I missed: The BFS layering is defined by shortest distances. So the graph must be such that the distance from vertex 1 to any vertex in layer i is exactly i. This means:
1. There are no edges between layer i and layer j for |i-j| > 1.
2. Every vertex in layer i (i>=1) has at least one neighbor in layer i-1.
3. There are no edges from layer i to layers < i-1 (redundant with 1).
4. The graph is connected (ensured by 2 and the fact that layer 0 is only vertex 1).

So the edges between layer i-1 and layer i must form a bipartite graph where every vertex on the layer i side has degree at least 1. Similarly, within a layer i, edges can be arbitrary.

This changes the count significantly. The tree edges are not just a choice of parent; any spanning forest of the bipartite graph between layer i-1 and i that connects all vertices in layer i to layer i-1 (and is acyclic?) Actually, for the BFS layering to be exactly the distances, we need that in the subgraph induced by layers 0..i, the vertices in layer i are exactly at distance i. This is equivalent to saying that the edges between layer i-1 and i form a bipartite graph with no isolated vertices on the layer i side. But there could be cycles? Yes, there could be edges within layer i and multiple edges between the layers. However, the BFS tree is a spanning tree of the graph. The number of edges in the graph is not necessarily N-1 + non-tree edges; it can be more than N-1 because the bipartite graph between consecutive layers can have multiple edges, but the spanning tree has exactly one edge per non-root vertex. So the previous formula using the number of trees T and the number of non-tree edges is still correct, but now the "available non-tree edges" are not all edges between the layers minus the tree edges; rather, the available edges are all possible edges between the layers, and the tree edges are a subset. The condition that every vertex in layer i has at least one neighbor in layer i-1 is equivalent to saying that the bipartite graph between layer i-1 and i has no isolated vertices on the right side. This is automatically satisfied if we choose a spanning tree T (which gives each vertex in layer i exactly one parent in layer i-1), and then we add any subset of the remaining possible edges between the layers. So the count of graphs extending a given tree T is still 2^{R} where R is the number of possible edges not in T. But now the set of possible edges between layer i-1 and i is all k_{i-1} * k_i possible edges, and the tree uses k_i of them. So the number of non-tree edges available is indeed k_{i-1} k_i - k_i. So my earlier formula for R is still correct, and the count of trees T is still ∏ k_{i-1}^{k_i} (each vertex in layer i chooses one parent in layer i-1). So the formula holds!

Wait, is that true? If we have a tree T that gives each vertex in layer i exactly one parent, and we add any subset of the remaining edges between layers and within layers, does the resulting graph always have the property that every vertex in layer i has distance exactly i? Let's check:
- Distance <= i: Since T connects each vertex in layer i to a vertex in layer i-1, which is connected to root, distance <= i.
- Distance < i: This would require an edge from a vertex in layer i to a vertex in layer j with j < i-1. But we only add edges within layer i or between layer i and i-1. Edges within layer i don't create paths to root of length < i (they only connect vertices already at distance i). Edges between i and i-1 could potentially create shorter paths? If a vertex v in layer i gets an extra edge to a vertex u in layer i-1, and u has distance i-1, then v's distance is still i (since i-1+1 = i). It doesn't become smaller. So yes, adding any extra edges between i and i-1 cannot reduce the distance of any vertex in layer i below i. Could a vertex in layer i get a path of length < i through within-layer edges? A within-layer edge connects two vertices in layer i, both at distance i. So any path using a within-layer edge has length at least i (actually, it could be i if you go to a neighbor in the same layer, but you still need i steps to get to that neighbor from the root, so the distance is at least i). More formally, the BFS layering from vertex 1 in any graph where edges only go within layer i or between layer i-1 and i, and every vertex in layer i has at least one edge to layer i-1, is exactly the given layering. So the count is correct.

But wait: What about the condition that vertex 1 is in layer 0 and there are no edges from layer 0 to anywhere else? Actually, edges between layer 0 and layer 1 are allowed (they are the parent edges). Vertex 1 is the only vertex in layer 0, so the number of edges between 0 and 1 is exactly k_1 (all of them go to vertex 1). The tree uses all of them? No, the tree uses k_1 edges (one per vertex in layer 1). The remaining k_1 k_1 - k_1 = k_1(k_1-1) edges are non-tree? Wait, the bipartite graph between layer 0 (size 1) and layer 1 (size k_1) has 1 * k_1 = k_1 possible edges. The tree uses all of them? Because each of the k_1 vertices in layer 1 must have parent vertex 1 (the only vertex in layer 0). So the tree uses all k_1 possible edges between layer 0 and 1. Thus there are no non-tree edges available between layer 0 and 1. This is consistent: R = sum C(k_i,2) + sum_{i=1}^{L-1} (k_{i-1} k_i - k_i) + 0. The term for i=1 is k_0 k_1 - k_1 = 1*k_1 - k_1 = 0. Good.

So the formula is correct.

Now, the sum is over sequences (k_1,...,k_L) with k_i >= 1, sum k_i = N-1, and parity condition. L can be from 1 to N-1. For N=30, N-1=29, the number of compositions is 2^{28} ~ 2.7e8, which is too many. But we can use a DP that processes the layers and tracks the partial sum of vertices and the partial R, and also tracks the parity sum.

Let's define a DP over i (number of layers processed). At step i, we have processed layers 1..i. The state is (v, e, p) where:
- v = total vertices in layers 1..i (so v = sum_{j=1}^i k_j)
- e = number of non-tree edges contributed so far = sum_{j=1}^i C(k_j,2) + sum_{j=1}^{i-1} (k_{j-1} k_j - k_j) with k_0=1. Wait, this depends on the sequence of k's. We need to define the contribution per step carefully.

When we add layer i, we choose k_i. The contribution to the weight (N-1)! / (∏ k_i!) × ∏ k_{i-1}^{k_i} is multiplied by k_{i-1}^{k_i} / k_i!. This suggests we can process layer i by multiplying by the factor f(k_{i-1}, k_i) = k_{i-1}^{k_i} / k_i!. But the binomial C(R, e) depends on the total R at the end.

We can incorporate the edge count by using a polynomial in y (edge marker). The total number of edges M = (N-1) + e, where e is the number of non-tree edges. The factor for each layer i, given previous layer size a = k_{i-1} and current layer size b = k_i, is:
   (a^b / b!) * y^{ C(b,2) + a b - b }   (for i >= 2, and for i=1, a=1, and the term is (1^{k_1} / k_1!) * y^{ C(k_1,2) + 1*k_1 - k_1 } = (1/k_1!) * y^{ C(k_1,2) }).

Wait, check i=1: R contribution = C(k_1,2) + (k_0 k_1 - k_1) = C(k_1,2) + 0 = C(k_1,2). Correct.
For i >= 2: R contribution = C(k_i,2) + (k_{i-1} k_i - k_i).

So the product over i=1..L of [ k_{i-1}^{k_i} / k_i! ] * y^{ R_i }, where R_i is the increment to R. Then the total sum is (N-1)! * coefficient of y^e in this product, summed over all sequences with given parity.

But the product is not simply a product of independent factors because k_{i-1} appears in the factor for layer i. So it's a "convolution" over the sequence of k_i.

We can think of this as a path in a graph where nodes are possible layer sizes (1 to N-1), and we choose a sequence of sizes. The weight of a step from a to b is (a^b / b!) * y^{ C(b,2) + a b - b }. The start node is k_0=1. We want to sum over all paths of any length L >= 1 such that the total number of steps (sum of b's) is N-1, and the parity condition holds.

This is a DP over the number of layers processed and the cumulative vertex count. Let dp[c][v][p] be the sum over sequences of length c (layers 1..c) with total vertices v, parity sum p (where p is the difference between even and odd layer vertices? Or we can track the number of even and odd layer vertices separately), of the product of factors. But we also need to track the total R (or the exponent of y) to eventually extract the coefficient for each e.

Actually, the generating function in y is a polynomial. We can keep a polynomial in y for each state. The number of states is small: c from 1 to N-1, v from c to N-1, and parity state (difference between even and odd totals). But the degree in y (i.e., R) can be large: maximum R is when the graph is complete, which is C(N,2) - (N-1) = N(N-1)/2 - (N-1) = (N-1)(N-2)/2. For N=30, that's 29*28/2 = 406. So the polynomial degree is at most ~406. That's fine.

But the number of possible k_i values is up to N-1, so the transition from a to b has size O(N^2). The DP would be O(N^4) in the number of states times transitions. Let's estimate: v up to 29, c up to 29. The number of states (c, v) is about N^2/2 = 450. For each state, we need to consider all possible next b such that v+b <= N-1. So the total number of transitions is sum_{v} (N-1 - v) * (number of ways to reach v). Roughly O(N^3) = 27000. For each transition, we need to multiply polynomials of degree up to ~400. The coefficients are modulo P. Polynomial multiplication of degree d polynomials is O(d^2) if naive, or O(d log d) with FFT. But d is at most 406, and the number of polynomials is large, so FFT might be overkill. We can just use O(d^2) or use the fact that we are doing many small polynomial multiplications. Since P is prime, we can use NTT if P is suitable, but P is arbitrary (10^8 to 10^9), not necessarily NTT-friendly. So we should use naive O(d^2) multiplication, or use the fact that we can maintain the coefficients as an array and do convolution by iterating over the terms.

Actually, the number of transitions is small (O(N^3)), and each transition adds one polynomial factor. We can do the DP by keeping an array of size max_R+1 for each state. The transition from dp[old_v] to new_v = old_v + b: we take the polynomial for old_v, and for each term y^e, we multiply by the factor for step a->b: coeff * y^{ C(b,2) + a b - b }. So we shift the array by the new exponent and multiply by the scalar coefficient. This is O(max_R) per transition, not O(max_R^2). Because the factor is a monomial times a scalar! Yes! The factor is (a^b / b!) * y^{ delta }, where delta = C(b,2) + a b - b. So it's a monomial in y. That means the polynomial multiplication is just a shift and scalar multiplication. Great!

So the DP is:
- Initialize dp[1][v=0] = [1] (empty product, no layers yet? Actually, before layer 1, v=0, R=0, weight=1. But we need to start with k_0=1 fixed. So we process layer 1 as the first step: from state (v=0, R=0) with previous size a=1, we choose b=k_1, new v = b, new R = C(b,2), new weight = 1^b / b! = 1/b! times y^{C(b,2)}.
- Then for subsequent steps, from state (v, a_last, R) we choose b, new v = v+b, new R = R + C(b,2) + a_last * b - b, new weight = old_weight * (a_last^b / b!).
- We also need to track the parity of the layers. Let's track the number of even-distance vertices and odd-distance vertices. Layer 0 (vertex 1) is even, so it contributes 1 to even. For layer i: if i is even, it contributes k_i to even; if i is odd, it contributes k_i to odd. We need even_total = N/2, odd_total = N/2.
- So the DP state includes (v_even, v_odd, R) or (v, diff) where diff = v_even - v_odd. Since v_even + v_odd = v + 1 (including vertex 1), we can track v and diff. Initially v=0 (layers 1..0), diff = 1 (from vertex 1). When we add layer i (i starting at 1): if i is odd, add to odd, so diff decreases by b; if i is even, add to even, so diff increases by b. Wait, vertex 1 is even, so even starts at 1. Layer 1 (odd): odd += b, diff = 1 - b. Layer 2 (even): even += b, diff = 1 - b + b' = 1 - b + b'. In general, after processing c layers, the layer index is c, and the next layer to process is c+1. So we need to know the current layer index c to know the parity of the next layer. We can include c in the state, or we can flip a parity bit each step.

State: (c, v, diff) or (v, diff, parity_of_next). Since c determines parity, we can just use (v, diff, c_mod_2). Actually, c is the number of layers processed. The next layer index is c+1. So if c is even (meaning we have processed an even number of layers), the next layer is odd (index c+1 is odd). If c is odd, next is even. So we can use c_mod_2.

But wait: we also need to know the size of the last layer (a_last) to compute the factor a_last^b. So the state must include a_last. So state is (c, v, diff, a_last) or (v, diff, a_last, c_mod_2). But c is determined by the number of steps taken? No, multiple sequences can have the same v and diff but different c and a_last. So we need to keep them separate.

Let's define the state as: dp[last_size][v][diff] = polynomial in y. Here last_size is the size of the most recent layer (k_i). For the start, before any layers, we don't have a last size. But we can start with layer 1: from "start" we go to last_size = b for b=1..N-1, with v=b, diff = 1 - b (since layer 1 is odd), weight = 1/b! * y^{C(b,2)}. Then for each state (last_size=a, v, diff), we transition to next size b (1 <= b <= N-1 - v), with new v' = v + b, new diff' = diff + (-1)^{c+1} * b? Actually, after processing i layers, the next layer is i+1. If i is even, next is odd, so diff decreases by b. If i is odd, next is even, so diff increases by b. So we need to know i mod 2. But we can infer i from the number of steps? Not directly, because different paths could have different lengths but same v and last_size? Actually, if we know the sequence of last_size, we know the path length. But to compute diff, we need to know the parity of the current step number. Let's include the step number parity in the state, or we can just use the fact that the step number parity is determined by the sequence of choices? No, it's not determined by v and last_size. For example, (a=2, v=2) could come from a path of length 1 (k_1=2) or length 2 (k_1=1, k_2=1). So we must include the length parity (or the number of layers processed mod 2). Let's call it parity = (number of layers processed) mod 2. Initially, 0 layers processed, parity 0. After adding layer 1, parity becomes 1. After adding layer 2, parity 0, etc. So when we transition, the new layer's parity is the new number of layers mod 2? Actually, if we are about to add layer i+1, and we have processed i layers, the new layer is odd if i is even (i+1 is odd), even if i is odd. So the change in diff is: if current parity is 0 (even number of layers so far), next is odd, diff' = diff - b. If current parity is 1, next is even, diff' = diff + b. Then the new parity becomes 1 - current parity? Wait: if we have processed i layers (i mod 2 = p), the next layer index is i+1. We add b to that layer. Then the new number of layers processed is i+1, so new parity is (p+1) mod 2. So we can just store the current number of layers processed mod 2, call it p. The transition: new_p = 1 - p. The diff change: if p == 0 (i even), next is odd, diff' = diff - b. If p == 1, next is even, diff' = diff + b.

So state: (last_size, v, diff, p) where p in {0,1}. last_size ranges from 1 to N-1, v from 0 to N-1, diff from -(N-1) to N-1. But diff is constrained: after adding b, diff changes by ±b. Also, we know that vertex 1 is even, so initially diff = 1. After layer 1 (odd), diff = 1 - b. So diff is always odd? Not necessarily, but it will be 1 + sum_{i even} k_i - sum_{i odd} k_i. Since k_i are positive, diff can vary. The target is diff = 0 (equal even and odd). So we only care about diff = 0 at the end, but during DP we need to track all possible diffs.

The number of states: last_size up to 29, v up to 29, diff up to ±29, p in {0,1}. That's about 30*30*60*2 = 108,000 states. For each state, we have a polynomial in y of degree up to R_max ~ 406. The total memory is 108k * 407 * 8 bytes ~ 350 MB, which is large. We can reduce: we don't need to keep all diffs, only those that are reachable. Also, we can process M by M? But we need all M from N-1 to N(N-1)/2, so we need the full distribution of R (or M). Since the maximum R is small (~400), and the number of states is ~100k, the total number of coefficients is ~40 million. Modulo P, each coefficient is an integer (4 bytes if we use Python int, but Python int is larger). In Python, this would be too slow and memory-intensive. We need a more efficient approach.

Wait, N is at most 30. The number of compositions of 29 is 2^28 ~ 2.7e8. But with the parity constraint and the small N, maybe we can iterate over all compositions using recursion with pruning? 2.7e8 is too many for Python. We need the DP with polynomials, but we need to optimize it.

Let's think about the DP differently. The total number of non-tree edges R is sum_i [C(k_i,2) + k_{i-1} k_i - k_i]. This is the number of edges in the complete layered graph minus the tree edges. Note that the total number of possible edges in the layered graph (with the given layering) is exactly sum_i C(k_i,2) + sum_{i=1}^L k_{i-1} k_i. This is the number of edges in a graph that is a disjoint union of cliques on each layer, plus a complete bipartite graph between consecutive layers. This is known as a "layered complete graph" or "multidimensional" something. The number of edges is A = R + (N-1). The graph is connected. We want to count labeled graphs on N vertices that are connected, and have a given BFS layering from vertex 1 with layer sizes (1, k_1, ..., k_L), and exactly M edges.

This is equivalent to: among all connected graphs with that layering, how many have exactly M edges? The number of connected graphs with that layering is the number of spanning trees times 2^{R} (since any subset of the R available non-tree edges can be added to any spanning tree to yield a connected graph with that layering, and every connected graph with that layering arises uniquely this way). Wait, is that true? Does every connected graph with that layering contain a unique spanning tree that is consistent with the layering? The BFS tree is a spanning tree, and it is consistent with the layering. Any connected graph with that layering must contain at least one spanning tree consistent with the layering (e.g., the BFS tree). The non-tree edges are a subset of the R possible edges. And any spanning tree consistent with the layering, together with any subset of the R possible edges, yields a connected graph with that layering. Moreover, different trees or different subsets yield different graphs? Yes, because the tree edges are a subset of the graph. So the set of connected graphs with that layering is in bijection with pairs (T, S) where T is a tree (spanning, consistent with layering) and S is a subset of the R available non-tree edges. The number of such pairs is (number of trees) * 2^R. And the number of edges in the resulting graph is (N-1) + |S|. So the number of graphs with exactly M edges is (number of trees) * C(R, M - (N-1)). This matches our earlier formula.

So for a fixed layering, the distribution over M is a binomial distribution C(R, e) multiplied by the number of trees. This is a single polynomial in M (or e). So if we can compute the sum over all layerings of (number of trees) * y^R, then the coefficient of y^e gives the total count for e non-tree edges, i.e., M = N-1 + e.

Thus, the problem reduces to computing the polynomial F(y) = ∑_{layerings} (N-1)! / (∏ k_i!) × ∏ k_{i-1}^{k_i} × y^R, where the sum is over all valid layerings (k_1,...,k_L) with sum N-1 and parity condition diff=0. Then the answer for M is the coefficient of y^{M - (N-1)} in F(y).

Now, the sum is over layerings. We can write F(y) as:

F(y) = (N-1)! × [ coefficient of x^{N-1} in something? ]

Let's use the exponential generating function in x, where x marks the total number of non-root vertices. We want to extract the coefficient of x^{N-1} from a product of series.

Consider the "transfer matrix" method. For each possible layer size a (1 <= a <= N-1), we have a state. The generating function from state a to state b is:

T_{a,b}(y) = ∑_{b>=1} (a^b / b!) y^{ C(b,2) + a b - b } x^b

Wait, we also need to track the total number of vertices. So we use a variable x for vertices. Then the weight for a step from a to b is (a^b / b!) * y^{ C(b,2) + a b - b } * x^b.

The total sum over sequences of any length is the sum over paths in the directed graph with vertices {1,...,N-1} (and a start state 0) of the product of these weights. The start state is k_0=1, but we can think of it as having a fixed initial layer of size 1. Actually, the first step from "start" (which corresponds to k_0=1) to k_1=b has weight (1^b / b!) y^{ C(b,2) } x^b. This is exactly the same as T_{1,b}(y) except the term a b - b is missing because a=1 and b=b, so 1*b - b = 0. So we can just say the initial state is a=1 (size of previous layer), and we take one step. But we also need to allow the sequence to end. The sequence can end after any number of layers L >= 1. So we sum over all paths of length >= 1 starting from a=1. The generating function is:

G(x, y) = ∑_{L>=1} ∑_{k_1,...,k_L} [ ∏_{i=1}^L ( k_{i-1}^{k_i} / k_i! ) y^{ R_i(k_{i-1},k_i) } x^{k_i} ]

with k_0=1. This is a path sum in a weighted directed graph. It can be written as:

G = ∑_{b>=1} T_{1,b} + ∑_{b,c} T_{1,b} T_{b,c} + ... = (T + T^2 + T^3 + ...) evaluated starting from 1? Actually, it's the sum over all paths of any positive length. That is:

G = (1, 0, 0, ...) * (I - T)^{-1} * (1,1,1,...)^T? No, because we want the sum of weights of all paths. The sum of all paths of length >= 1 is the vector v = T * 1 + T^2 * 1 + ... = T * (I - T)^{-1} * 1, but we need to start at state 1. So it's the first row of T * (I - T)^{-1} times the all-ones vector? Actually, the sum of paths of any length starting at node 1 is the (1, :) entry of T * (I - T)^{-1}? Let's check: the (1, j) entry of T^k is the sum of paths of length k from 1 to j. Summing over k>=1 gives the (1, j) entry of T + T^2 + ... = T (I - T)^{-1}. So we want the sum over all ending nodes j, so we need to multiply by the all-ones vector on the right? No, the sum over all paths of any length ending anywhere is the sum over j of the (1,j) entry. That is the row vector u = [T (I - T)^{-1}]_{1,:} (as a row). But we can just compute the generating function by iterating over L: for L=1,2,...,N-1, compute the product of L transfer matrices, starting from the row vector e_1, and sum them. Since N is small, we can just do DP over L.

But the parity condition (diff=0) is not captured by this simple matrix product because it depends on the step number parity. The diff changes sign at each step. So we need a matrix that tracks both the last layer size and the parity. Let's define a state vector indexed by (a, p) where a is the last layer size, and p is the parity of the number of layers processed mod 2. The transfer from (a, p) to (b, 1-p) has weight:

W_{a,b}^{(p)}(x, y) = (a^b / b!) y^{ C(b,2) + a b - b } x^b, and the diff change: if p=0 (even number of layers so far, so next is odd), diff decreases by b; if p=1, diff increases by b.

But we also need to track the total diff. So the state should be (a, p, d) where d is the current diff. The number of possible a is N-1, p in {0,1}, d from -(N-1) to N-1. That's 30*2*60 = 3600 states. For each state, we have a polynomial in x and y. But x is just a marker for the number of vertices, and we need to extract the coefficient of x^{N-1}. We can instead do DP over the number of vertices v, as before. So state: (a, p, d, v). The transfer: choose b, new v = v + b, new d = d + (1 if p=1 else -1) * b, new parity = 1-p. The weight is multiplied by (a^b / b!) y^{ delta }, where delta = C(b,2) + a b - b. The factor x^b is implicitly handled by incrementing v.

So the DP is: dp[a][p][d][v] = polynomial in y. The number of states: a in 1..N-1 (29), p in 0,1 (2), d in -29..29 (59), v in 0..29 (30). Total states: 29*2*59*30 = 102,660. For each state, a polynomial in y of degree up to R_max. R_max = max possible R. For a given state, the maximum R is achieved when the remaining vertices form a single layer? Actually, R is cumulative. The maximum R overall is when the graph is complete layered, which for N=30 is C(30,2) - 29 = 435 - 29 = 406. So degree 406. But for smaller v, the max R is smaller. The sum of degrees over all states is manageable. However, in Python, storing a list of length ~400 for 100k states is 40 million integers, which might be okay if we use array modules or lists of ints. But the transitions: for each state, we try all b from 1 to N-1-v. For each b, we compute the new state and add the shifted polynomial. This is O(N) transitions per state, so total operations ~100k * 30 = 3 million. Each operation involves shifting a polynomial (copying a list) and multiplying by a scalar. Copying a list of length up to 400 is fast. So this is feasible in Python.

But we also need to extract the answer: for each M from N-1 to N(N-1)/2, we need the sum over all ending states (a, p, d=0) of the coefficient of y^{M - (N-1)} in the polynomial. The ending states can have any a (the last layer size) and any p (parity). So we sum over a in 1..N-1, p in 0,1, v = N-1, d=0, the polynomial.

So the algorithm is:
1. Initialize dp as a dictionary or a 4D array of polynomials (list of ints mod P). Since P is up to 10^9, we use Python ints.
2. Start state: before any layers, we have a "previous layer size" of 1? But we don't have a previous layer size before the first layer. We can treat the first layer specially: from start, we choose b (1 to N-1), set a = b, p = 1 (after 1 layer), v = b, d = 1 - b (since vertex 1 is even, diff = 1 - b). Weight: (1^b / b!) y^{C(b,2)}. So we initialize the DP with these states. Alternatively, we can include a dummy start state with a=1, v=0, d=1, p=0, and then the transition from (a=1, p=0) to (b, p=1) uses the same formula? Let's check: the formula for the first step is exactly the same as the general step with a=1, because the general step weight is (a^b / b!) y^{C(b,2) + a b - b}. For a=1, a b - b = 0, so it matches. And the diff change: p=0 means next is odd, so d' = d - b. With d=1, we get 1 - b, which matches. And p becomes 1. So we can use a single DP with an initial state (a=1, p=0, d=1, v=0) with an empty polynomial (just [1] meaning y^0 with coefficient 1). Then the transition rule applies uniformly.

So initial state: a=1, p=0, d=1, v=0, poly = [1] (length 1).
Transition: from (a, p, d, v) with poly, for each b from 1 to N-1 - v:
   new_a = b
   new_p = 1 - p
   new_v = v + b
   new_d = d + (1 if p==1 else -1) * b
   delta_R = C(b,2) + a*b - b
   weight = pow(a, b, P) * inv_fact[b] % P   (where inv_fact[b] = modular inverse of b! mod P)
   new_poly = [0] * (len(poly) + delta_R)  (or we can shift and multiply)
   for i in range(len(poly)):
       new_poly[i + delta_R] = (new_poly[i + delta_R] + poly[i] * weight) % P
   add new_poly to dp[new_a][new_p][new_d][new_v] (we need to sum over multiple paths, so we accumulate).

We must be careful: the weight includes pow(a, b) / b!. Since P is prime, we can precompute factorials and inverse factorials mod P. P can be up to 10^9, which is less than 2^30, but we need to ensure P is not too small for factorials. N! for N=30 is about 2.6e32, which is larger than 2^63, but we can compute factorials modulo P using Python's arbitrary precision integers, then take mod P. However, P is at least 10^8, so factorials mod P are fine.

The DP will fill a table of size about 100k entries, each a list of length up to ~400. The total number of coefficient updates is: number of transitions * average length. Number of transitions: for each of the 100k states, we loop over b. But many states are not reached. Actually, the number of reachable states is exactly the number of possible prefixes of layer sequences. Since the total number of sequences is 2^{N-2} ~ 2^28, but we are grouping by (a, p, d, v). The number of distinct (a, p, d, v) is much smaller. For each v, the number of (a, d) combinations is at most (N-1) * (2v+1). So total states is O(N^3) = 30^3 = 27,000. Actually, let's bound: v goes from 0 to N-1. For a given v, the last a can be 1..v. The diff d is between -(v+1) and (v+1) (since diff starts at 1 and each step changes by at most the new b <= v). So roughly v * 2v * 2 = 4v^2. Summing v=1 to 29 gives about 4 * 29^3 / 3 ~ 32,000 states. Plus p=2. So about 64,000 states. That's very manageable.

For each state, we have a polynomial. We can store the polynomial as a list. The maximum length of a polynomial for a state with total v is bounded by the maximum R achievable with v vertices. The maximum R for v vertices is when they are all in one layer? Let's compute: if all v non-root vertices are in a single layer (L=1), then R = C(v,2). If they are in two layers, say k_1 and v-k_1, then R = C(k_1,2) + C(v-k_1,2) + 1*k_1 + k_1*(v-k_1) - (v) [wait, tree edges: N-1 = v, so R = C(k_1,2) + C(v-k_1,2) + k_1 + k_1(v-k_1) - v = ...]. Actually, the maximum R for fixed v is achieved by the complete bipartite or something? The total number of edges in the layered graph is sum C(k_i,2) + sum k_{i-1} k_i. This is exactly the number of edges in a graph that is a disjoint union of cliques on each layer, with complete bipartite between consecutive layers. This is known as a "threshold graph" or "nested split graph"? Actually, it's the number of edges in a graph that is a "cograph" or something. The maximum number of edges for a given number of vertices with a fixed BFS layering from a root? No, the layering is not fixed; we are summing over all layerings. The maximum R overall is when the graph is complete, which is C(N,2) - (N-1) = (N-1)(N-2)/2. For N=30, that's 406. For a state with v vertices, the maximum R is when the remaining vertices are arranged to maximize the number of non-tree edges. The non-tree edges include all within-layer edges and all between-layer edges except the tree edges. The tree edges are exactly v. So R = (total possible edges in the layered graph) - v. The total possible edges in a layered graph with vertex set partitioned into layers of sizes k_0=1, k_1,...,k_L (sum k_i = v+1) is sum C(k_i,2) + sum k_{i-1} k_i. This is maximized when the graph is a complete graph? Wait, the layered graph with a given partition has a specific number of edges. It does not include all possible edges; it only includes edges within layers and between consecutive layers. For a given partition, the number of edges is fixed. The maximum over all partitions of the number of edges is achieved by the partition that makes the graph as dense as possible. Since the total possible edges in the complete graph is C(v+1,2), and the layered graph is a subgraph of the complete graph (it misses edges between non-consecutive layers). To maximize the number of edges, we want to minimize the number of missing edges. The missing edges are between layer i and layer j for |i-j| > 1. The number of such edges is sum_{i} k_i * (sum_{j < i-1} k_j). For a given sequence, the number of missing edges is sum_{i} k_i * (sum_{j < i-1} k_j). This is minimized when the layers are as "consecutive" as possible, i.e., each layer is as large as possible? Actually, if we put all vertices in layer 1 (k_1 = v), then missing edges = 0 (since there are no non-consecutive layers). If we split into multiple layers, we introduce missing edges. So the maximum total possible edges is when L=1, i.e., all non-root vertices in layer 1. Then total possible edges = C(v,2) + 1*v = C(v+1,2). That's exactly the complete graph! So the layered graph with L=1 is the complete graph. In that case, the tree edges are v (all edges from root to layer 1). The remaining edges are C(v+1,2) - v = C(v,2). So R = C(v,2). For v=29, that's 406. For a state with intermediate v, the maximum R is when the remaining vertices are all in one new layer? But the state already has some layers. The maximum R for a partial sequence might be larger if we put the remaining vertices in the current layer? No, we can't change the past. For a given state (a, p, d, v), the maximum possible future R is bounded by the complete graph on the remaining vertices plus the current layer. Actually, the maximum R from the state is achieved by completing the graph to a complete graph. The total R for the whole graph is at most C(N,2) - (N-1). For a state with current R, the remaining R can be at most that minus current R. But we don't need the exact bound; we can just allocate polynomials up to the global max R = 406. The lists will be of length up to 406+1. That's fine.

So the DP is feasible. We need to be careful with performance: 64k states, each with a list of length up to 407. The transitions: for each state, we iterate over b from 1 to N-1-v. For each b, we compute the new state and add the shifted polynomial. Adding two polynomials of length L1 and L2 takes O(max(L1, L2)) if we just iterate over the indices. Since we are doing this for many transitions, the total time is sum over states of (number of outgoing b) * (length of polynomial). The average length of polynomial is smaller for small v. For v=0..29, the max R for that v is C(v,2) (if all in one layer). So the average length is roughly proportional to v^2. The total work is O(N^4) maybe? Let's estimate: number of states ~ 30^3 = 27,000. For each state, number of b choices is up to 30. So total transitions ~ 800,000. For each transition, we shift and add a list of length up to 400. So total operations ~ 800,000 * 200 (average length) = 160 million. That might be a bit slow in Python, but probably okay with optimized code (using list comprehensions or numpy? but we need modular arithmetic with large P, so Python ints are fine). We can optimize by noting that many states have small polynomials, and we can use arrays of Python ints. 160 million operations in Python is borderline (maybe 10-20 seconds). We need to optimize.

Can we reduce the dimension? Notice that the weight (a^b / b!) y^{delta} only depends on a, b, and the delta. The DP over v and d and a and p is necessary because the transition depends on a and p. But maybe we can combine p into the state in a smarter way? The parity p only affects the sign of the diff change. The diff is the difference between even and odd layer vertices. We need diff = 0 at the end. We can instead track the number of even and odd vertices separately, or track the diff and at the end only take diff=0. But the parity p determines whether the next layer is added to even or odd. So p is needed.

Wait, is there a way to avoid tracking d? We can track the number of even vertices and odd vertices separately. Let e = number of even vertices (including vertex 1). Let o = number of odd vertices. Then e + o = v + 1. We need e = o = N/2. So we can track e (or o) instead of d. The change: if next layer is even, e += b; if odd, o += b. Since p tells us whether next is even or odd, we can just track e. The state becomes (a, p, e, v). e ranges from 1 to N/2. v from 0 to N-1. The number of states is similar, but e is smaller (up to 15). So (a, p, e, v): 30 * 2 * 16 * 30 = 28,800 states. Slightly less.

But more importantly, the transition for e: if p==1 (next is even), new_e = e + b; else new_e = e. So we don't have negative numbers, which is nicer.

Let's define:
- v: total vertices in layers 1..c.
- e: total even vertices (including vertex 1? Let's include vertex 1. So initially, before any layers, e=1, v=0. The root is even.)
- p: parity of c (number of layers processed). c=0: p=0 (even). After processing an even number of layers, the next layer is odd. So if p=0, next is odd, so e stays same. If p=1, next is even, so e += b.
- a: size of the last layer (for the first layer, a is the size of the current layer? Actually, after processing c layers, the last layer size is k_c. The next step will use a = k_c as the previous size. So a is the size of the most recent layer. For the start, c=0, we don't have a last layer. But we can set a=1 (the size of layer 0) and the transition from start is the same as from (a=1, p=0) with e=1, v=0. So we can initialize with a=1, p=0, e=1, v=0.

Transition from (a, p, e, v):
  for b in 1..N-1-v:
    new_a = b
    new_v = v + b
    if p == 1:  # next layer is even
        new_e = e + b
    else:       # next layer is odd
        new_e = e
    new_p = 1 - p
    delta = C(b,2) + a*b - b
    weight = a^b / b!   (mod P)
    Add to dp[new_a][new_p][new_e][new_v]: poly shifted by delta and multiplied by weight.

We need to ensure that e never exceeds N/2. Since we need e = N/2 at the end, we can prune states where e > N/2. Also, note that the total even vertices e includes vertex 1 and all even layers. The total odd vertices is (v+1) - e. At the end, v = N-1, e = N/2. So we only care about states with e <= N/2.

The number of states: a in 1..N-1 (29), p in 0,1 (2), e in 1..N/2 (15), v in 0..N-1 (30). Total: 29*2*15*30 = 26,100. Good.

Now, for each state, we store a polynomial in y. We can represent the polynomial as a list of integers mod P, where index i is the coefficient of y^i. The degree of the polynomial is the number of non-tree edges contributed so far. The maximum degree for a state with current v is at most C(v+1,2) - v = C(v,2) (if the remaining vertices are all in one layer attached to the current layer? Actually, the maximum R for a given v is achieved when the past layers are arranged to maximize the number of missing edges? Wait, we want the maximum R that can be achieved from this state. The past layers have already contributed some R. The future layers can add more R. The total R for the whole graph is at most C(N,2) - (N-1). So the polynomial for a state with current R_partial can have non-zero coefficients up to the global max. But we can bound the maximum possible R for a state by the maximum R achievable from the start with the same v and e? Actually, the maximum R for a given v and e is when the graph is as dense as possible. Since the graph must be connected and have a BFS layering with given v and e, the maximum edges is C(N,2) (if e allows the complete graph). But we only care up to the global max. We can just allocate lists of length max_R+1 = (N-1)*(N-2)/2 + 1. For N=30, that's 407. So each state has a list of length 407. Total memory: 26,100 * 407 * 28 bytes (Python int) ~ 300 MB. That's too much. We need to compress.

We can use the fact that many states have zero polynomial or small degree. But we cannot rely on that. We need a more memory-efficient representation. Since P is up to 10^9, we can use array('I') or just Python lists but with smaller integers? Python ints are objects, so 300 MB is indeed large. We might hit memory limits.

Alternative: Since the DP is over v and e, and the transitions are additive, we can process the DP layer by layer (by v). For a fixed v, we only need the polynomials for states with that v. The transitions from v to v+b only use the current v. So we can do a DP over the

## worker: Implement the DP described in the ideation: state 
The solution implements the DP described in the ideation. The state is (last_layer_size, parity, even_count, total_vertices) and each state stores a polynomial in y (non-tree edge count). The initial state represents the root vertex (layer 0) with size 1. Transitions add a new layer b, updating the state and shifting the polynomial by the number of new non-tree edges. The final answer is collected for states with total vertices N-1 and even count N/2, then multiplied by (N-1)! and converted to M = N-1 + R.

## worker: Implement the DP in Python with optimized memory a
The solution uses a dynamic programming approach over the BFS layering from vertex 1. The state is defined by (last_layer_size, parity, even_count, total_vertices) and stores a polynomial where the coefficient of y^R gives the number of connected graphs with R non-tree edges for that prefix of the layering. Transitions add a new layer b, updating the state and shifting the polynomial by the number of new non-tree edges (delta = C(b,2) + a*b - b). The weight factor is a^b / b! mod P. Finally, results are collected for states with total vertices N-1 and even count N/2, then multiplied by (N-1)! to account for the root vertex's label. The sample inputs should produce the expected outputs.

## worker: Implement the DP in Python with optimized memory a
The solution implements the DP described in the ideation. The state is (last_layer_size, parity, even_count, total_vertices) and each state stores a polynomial in y (non-tree edge count). The initial state represents the root vertex (layer 0) with size 1. Transitions add a new layer b, updating the state and shifting the polynomial by the number of new non-tree edges. The final answer is collected for states with total vertices N-1 and even count N/2, then multiplied by (N-1)! and converted to M = N-1 + R. The DP is optimized by using dictionaries keyed by (a, p, e) for each v, and only allocating polynomials up to max_R. The algorithm runs in O(N^4) time with manageable memory for N <= 30.
