We need the number of connected labeled graphs on N vertices (N even, ≤30) with a given edge count M where the BFS layers from vertex 1 have equal size: exactly N/2 vertices at even distance and N/2 at odd distance. We split the problem into two parts:

1. **Unconditioned layer counts.** For each partition of vertices into sets E (even layer) and O (odd layer) with vertex 1 ∈ E, |E|=|O|=N/2, count all labeled graphs whose BFS layers (not necessarily connected) give exactly that partition. This depends only on the numbers of edges allowed inside E, inside O, and between E and O.

2. **Connectivity + root-isolation.** From those graphs we must subtract those where vertex 1 is disconnected, and then use the matrix-tree / inclusion–exclusion to keep only the connected ones (vertex 1 must be in the same component as all others, and its BFS parity must be as specified). The connectivity constraint is enforced by a standard deletion-contraction / Kirchhoff-style recurrence on edge subsets, which can be folded with the layer constraint.

We precompute binomial coefficients mod P, then iterate over all `(|E|,|O|)` partitions (there are C(N-1, N/2-1) of them, ≤ 5e8 in the worst case—too many for N=30), so we instead aggregate by counts of edges within E, within O, and across, using generating-function style DP across vertices.

Concretely: for each vertex v≠1 we decide whether it is in E or O. For each decision, when we add v we know how many new possible edges are added in each of the three categories, so we can polynomial-multiply contributions. This gives, for each triple (a,b,c) of edge counts (within E, within O, across), the number `T[a][b][c]` of labelings (with root in E) whose BFS layers respect the parity. Complexity is O(N * (Mmax)^3) but with careful compression (only relevant triangles) it fits N=30.

Then we need connected counts `C[a][b][c]`. Use DP by edges: `C = T - sum_{S⊂V\{1}, 1∈S} (connected on S) * T_on_rest`, implemented via a generating-function Möbius inversion on subsets. Because N is only 30, we can do a 2^(N-1) subset DP over vertices other than the root, which is 2^29 ≈ 5e8—too big.

So we exploit that the layer constraint only cares about parity. Define two groups G0 (even) and G1 (odd). We consider a graph restricted to one group only being connected, etc. A more efficient route: compute `T[a][b][c]` by a simple DP over vertices (treating root as already placed in G0). Then for connectivity we apply the formula

`C[a][b][c] = T[a][b][c] - Σ_{nonempty proper U⊂V, 1∈U} C_on_U * T_on_V\U`

but restricted to subsets U that are unions of parts consistent with parity (i.e., either U⊆G0, U⊆G1, or U contains whole G1 …). Because we never enumerated which specific vertices are in G0/G1, this direct subset DP is awkward.

**Alternative practical approach (chosen):** Iterate over all `C(N-1, N/2-1)` partitions. For N=30 this is about 155M, still too large to enumerate naively but small enough if we use a Gray-code enumeration and update counts incrementally, with O(N^2) per step—too slow.

**Better approach:** Since N≤30 we can use the subset DP on 2^(N/2) instead. We split the vertices into the even set E (size N/2) and odd set O (size N/2). The parity condition only distinguishes E and O; the actual labels inside each set do not matter for the counts `T`. So we do not enumerate individual labelings; we directly compute, for every (a,b,c), the number of graphs on the given bipartition (with root in E) that have those exact edge counts. This is a purely combinatorial count:

- Number of ways to place `a` edges inside E, `b` inside O, `c` across:  
  `C(C(N/2,2), a) * C(C(N/2,2), b) * C((N/2)^2, c)`.

- BUT we must restrict to graphs whose BFS from root produces exactly this E/O partition, i.e., no edge inside E connects a vertex at distance 0 to one at distance >0 in a way that would reclassify it. Actually the parity condition is simply: assign each vertex a label 0 (even) or 1 (odd) with root=0, and require that the BFS from root gives exactly these labels. This is equivalent to: every edge connects vertices of opposite parity OR connects two even-parity vertices both at distance ≥2 (i.e., not creating a shorter odd-distance vertex). The precise forbidden configuration is an edge from root (distance 0) to any vertex that we want to label odd—wait, root is even; edges from root must go to odd-labeled vertices. Edges within E are allowed only between vertices of even distance (≥2). Edges within O only between odd distance vertices. Edges across only between even and odd distance.

Since the BFS distance parity is a 2-coloring of the connected component containing root, ANY 2-coloring of a connected graph with root colored even is the BFS parity (unique). So the condition simply is: the connected component containing root is properly 2-colorable with root even, and we pre-assign every other vertex to be even or odd. Thus the count `C[a][b][c]` we need is exactly: the number of connected graphs on N labeled vertices with root 1, such that vertex 1 is in E, the other N/2-1 even-labeled vertices and N/2 odd-labeled vertices are as assigned, and the graph has `a` edges inside E, `b` inside O, `c` across.

Because the labeling of which specific vertices are even/odd is fixed once we choose the partition, the count for a particular partition is the same for all partitions. Hence

`Answer[M] = C(N-1, N/2-1) * C_connected[M]`

where `C_connected[M]` is the number of connected graphs on N labeled vertices with vertex 1 distinguished and a distinguished partition of the remaining N-1 vertices into two sets of sizes N/2-1 and N/2, with a edges in E-set, b in O-set, c across, summed appropriately.

But careful: different partitions give the same numbers a,b,c; they all contribute the same number of graphs because relabeling within E or within O doesn't change the count. So if we let `f(a,b,c)` be the number of connected graphs for one fixed partition (with specific vertex sets E,O), then total answer is `C(N-1, N/2-1) * Σ_{a+b+c=M} f(a,b,c)`.

So the problem reduces to computing `f(a,b,c)`: number of connected labeled graphs on a vertex set consisting of root 1 plus (k-1) even vertices and k odd vertices (where k=N/2), with a edges among evens, b among odds, c across, and the graph connected.

**Computing f(a,b,c) via inclusion-exclusion on edges:**
We can compute `g(a,b,c)` = total number of graphs (not necessarily connected) with those edge counts. Then
`f(a,b,c) = Σ_{S⊆E∪O, 1∈S, S proper nonempty} μ(S) * g_on_S * g_on_rest`,
where μ(S) is (-1)^{|S|} times connected count on S... Actually the standard formula:
`connected = total - Σ_{∅≠U⊂V, 1∈U} connected_on_U * total_on_V\U`.
This is a subset DP, again 2^N.

**Practical observation:** N≤30, but we can afford O(2^{N/2}) by splitting on parity again. Let A = even vertices (size k), B = odd vertices (size k). Any subset S containing 1 is a union of (S∩A) and (S∩B). Connectedness across the bipartition is not split easily.

However, 2^{N/2} = 2^{15} = 32768, which is very small! Wait N=30, N/2=15, so 2^15 = 32768, and 2^{N-1}=2^29 is huge. So if we treat the bipartition cleverly, we can do a DP on subsets of A (or B). Let's see:

We can do inclusion-exclusion on subsets of the even set A only. Fix a subset X ⊆ A that is the set of even vertices in the "root component" together with root. The root component must include some vertices from A and some from B. The structure of connectedness across the bipartition is captured by a bipartite connection.

Actually, since the graph is 2-colored (by parity), the connected component of root, if it contains all vertices, must contain at least one vertex from each color (root provides one color). The component's structure can be described by the bipartite adjacency between the A-side and B-side vertices in the component.

We can reformulate: we have a bipartite graph between A and B plus edges within A and within B. Connectedness of the whole graph to root can be checked via the bipartite adjacency structure.

**Use the principle of counting labeled connected graphs by edge subsets via deletion-contraction recurrence on the number of edges within each of the three categories.** This is complex.

**Alternative efficient route:** N≤30 is small enough that we can use a 2^{N-1} subset DP after all, because 2^29 ≈ 5×10^8 is too much. BUT we can reduce by noting symmetry: we only care about (|S∩A|, |S∩B|) and possibly the number of edges of each type within S. So we can do a DP over subsets indexed by (size_A, size_B, a, b, c) — but the number of connected subsets with given (size_A, size_B) is `C(size_A + size_B - 1, size_A - 1)` (choosing which A-vertices, with root fixed in A... wait root is in A, so size_A≥1, size_B≥0). The count of connected graphs on a specific labeled subset with given edge counts is what we need.

Hmm, this is getting complicated. Let me think of a cleaner way.

**Counting connected bipartite-within graphs via the inclusion-exclusion formula on edge count:**
`C(a,b,c) = Σ_{j=0}^{1} (-1)^j * Σ ...` No.

**Use the known formula for connected labeled graphs by edge count:**
The total number of connected labeled graphs on n vertices with m edges is given by a well-known recurrence, but here we have the additional bipartite constraint (vertex 1 in part A, fixed partition of remaining vertices into A and B). This is essentially counting connected graphs on n labeled vertices with a specified 2-coloring (root in color 0). The number of such graphs with m edges is the same for any 2-coloring with root in color 0, and equals the total number of connected graphs on n vertices with m edges, because every connected graph has exactly 2 BFS 2-colorings (swap the two colors), and we fix root in color 0, so it's exactly `connected_total(n, m) / 2` if n≥2 (the two colorings are distinct because root forces a choice). Wait, is that right?

Yes! For any connected graph, the BFS from vertex 1 gives a unique 2-coloring (even/odd distances). This 2-coloring is unique once we fix the color of vertex 1. So the set of connected graphs with vertex 1 distinguished and a pre-assigned partition (P_even, P_odd) such that the BFS gives that partition, is in bijection with the set of connected graphs where the BFS happens to give that specific partition.

But different partitions correspond to different subsets of connected graphs. The number of connected graphs giving a specific partition is `connected_total(n, m) / (number of valid partitions that could arise)`. However, not every partition can arise as a BFS coloring of some connected graph—e.g., the partition must be such that there exist edges making it connected. But actually, given any partition with |P_even|=|P_odd|=n/2 and root∈P_even, we can construct a connected graph realizing it (e.g., a path alternating between the two sets). So every such partition is realizable.

Moreover, for connected graphs, the BFS coloring is determined, and conversely the partition determines a unique set of connected graphs. The number of connected graphs giving a specific partition should be the same for all partitions by symmetry (relabeling vertices within P_even and within P_odd). So

`Answer[M] = C(N-1, N/2-1) * (connected_total(N, M) / 2)`?

Wait, that would mean the answer doesn't depend on the internal structure of the partition at all, just on whether connected_total(N,M) is divisible. But the sample for N=4, M=3: total connected graphs on 4 vertices with 3 edges = number of trees on 4 labeled vertices = 4^{4-2} = 16. Divided by 2 = 8. Times C(3,1)=3 gives 24. But the sample says 12. So my reasoning is off by a factor of 2.

Let me reconsider. The BFS from vertex 1 gives a partition. The number of partitions of {2,...,N} into even/odd sets with root in even is C(N-1, N/2-1). For each connected graph, vertex 1 is in some component... wait, for a connected graph, vertex 1 is in the whole graph, and the BFS gives a unique partition. So each connected graph corresponds to exactly one partition. Therefore, summing over all partitions, we get total connected graphs. By symmetry, each partition contributes the same number. So

`Answer[M] = C(N-1, N/2-1) * connected_total(N, M) / C(N-1, N/2-1) = connected_total(N, M)`.

That would mean the answer is just the number of connected labeled graphs on N vertices with M edges, regardless of parity. But the sample contradicts this: for N=4, M=3, connected trees = 16, but answer is 12. So the symmetry argument fails because not all partitions are equally likely to arise from a connected graph? Or my count of trees is wrong.

Number of labeled trees on n vertices: n^{n-2} = 4^2 = 16. Correct. So 16 connected graphs, but answer is 12. So the answer is not simply connected_total.

Hmm, let me recount. For a tree on 4 vertices with vertex 1, the BFS from vertex 1 gives a partition. The possible partitions (with root even) of {2,3,4} into even/odd with |even|=1, |odd|=2 are: {2}|{3,4}, {3}|{2,4}, {4}|{2,3}. That's 3 partitions. 16/3 is not integer, so partitions are not equally distributed.

Right, because the structure of the tree matters. A star centered at vertex 1 gives partition {1}|{2,3,4}—wait, in a star, vertex 1 is center, distance to others is 1 (odd), so the partition has |even|=1 (just root), |odd|=3. But we need |even|=|odd|=2. So the star partition is not in our set. So the condition |even|=|odd| restricts which connected graphs count.

So we need connected graphs where the BFS from vertex 1 has equal layer sizes. The symmetry is not complete because the partition sizes are fixed.

OK so back to the harder problem. Let me think about computing the answer directly for N≤30.

**Approach: subset DP on the odd set.**
Let A = even vertices (size k = N/2, includes root), B = odd vertices (size k). We do a subset DP over subsets of B. For each subset S ⊆ B, let T(S) = set of vertices in A that are connected to root via a path that stays within S ∪ (A-side vertices in the component), considering only edges from the graph. Hmm, this is getting complex.

**Simpler: use the formula for connected graphs via matrix-tree-like counting on the contracted graph.** The number of connected graphs on n labeled vertices with m edges is computed by a standard DP or by the formula involving Stirling numbers. But adding the bipartition constraint...

Let me look for known results or think differently. 

**Key insight: Use the deletion-contraction / recurrence on edges.** For a fixed bipartition (A, B) with root in A, the number of connected graphs `f(a,b,c)` with a edges in A, b in B, c across satisfies a recurrence obtained by picking a specific edge and applying inclusion-exclusion. But with three types of edges, we get a 3D recurrence.

Alternatively, **use the exponential generating function approach or known formulas for bipartite-connected graphs**.

Actually, here's a clean approach: The number of connected graphs on n labeled vertices with a specified 2-coloring (A, B), root in A, with a edges in A, b in B, c across, is:

`f(a,b,c) = Σ_{partition of vertex set into root-component and rest} (-1)^{...} * product of total counts on each part`.

Using inclusion-exclusion on the complement (disconnected from root), we have:

`f(a,b,c) = g(a,b,c) - Σ_{X⊂A\{1}, Y⊆B, not both empty} f_on_{1}∪X∪Y(a',b',c') * g_on_rest(a'',b'',c'')`

where the sum is over all nonempty proper subsets of the non-root vertices. This is O(3^n) naively, but we can compress by (|X|, |Y|, a', b', c').

The number of ways to choose a specific subset X of size i from A\{1} (which has k-1 vertices) is C(k-1, i), and Y of size j from B is C(k, j). The number of connected graphs on a specific labeled subset {1} ∪ X ∪ Y (with the induced bipartition) with edge counts (a', b', c') is `f(i+1, j, a', b', c')` (here i+1 = |A-part of subset|, j = |B-part|). And the number of all graphs on the complement with (a'', b'', c'') is `g(k-1-i, k-j, a-a', b-b', c-c')`.

So the DP is:
`f(nA, nB, a, b, c) = g(nA-1, nB, a, b, c) - Σ_{i,j,a',b',c'} C(k-1, i) * C(k, j) * f(i+1, j, a', b', c') * g(k-1-i, k-j, a-a', b-b', c-c')`

where i ranges 0..k-1, j 0..k, not both zero (i=j=0 gives the whole graph, which is what we solve for). The base case: if nA=1, nB=0, then a=b=c=0 and f=1; otherwise f=0 for nA=1, nB=0 with any edges.

Wait, for nA=1, nB=0: the only graph is the single vertex (root), with 0 edges. So f(1,0,0,0,0)=1, and f(1,0,a,b,c)=0 for (a,b,c)≠(0,0,0).

We want `F(M) = C(N-1, N/2-1) * Σ_{a+b+c=M} f(N/2, N/2, a, b, c)`.

This DP is feasible! The dimensions: nA, nB up to 15 each. a up to C(15,2)=105, b up to 105, c up to 15*15=225. So f is a 3D array (over a,b,c) of size ~105*105*225 ≈ 2.5M per (nA,nB). The number of (nA,nB) pairs is 16*16=256. Total memory would be huge if we store all, but we can compute bottom-up and only keep needed slices.

The recurrence: we compute f for smaller nA+nB first. For each (nA, nB), f depends on f for smaller nA or smaller nB (since i < nA or j < nB in the sum, because i ranges up to nA-1 and j up to nB). Specifically, i ranges 0..nA-1, j ranges 0..nB. So for fixed (nA, nB), we need f(i+1, j, ...) for i+1 ≤ nA and j ≤ nB, and also j=nB with i < nA-1 (so nB same, nA smaller). This means we need f(nA', nB') for all nA' ≤ nA, nB' ≤ nB except (nA, nB) itself. So a 2D DP over (nA, nB) in increasing order.

The sum over i, j, a', b', c' is a convolution. We can precompute g(nA, nB, a, b, c) = C(C(nA,2), a) * C(C(nB,2), b) * C(nA*nB, c).

Complexity: for each (nA, nB), we do O(nA * nB * 105 * 105 * 225) naively, which is 15*15*2.5M ≈ 560M per pair, times 256 = too much. But with convolution (FFT or just careful loops), we can do it. Actually, the convolution separates: Σ_{a',b',c'} f(i+1,j,a',b',c') * g(nA-1-i, nB-j, a-a', b-b', c-c') is a 3D convolution. We can precompute for each (i,j) the function h_{i,j}(a,b,c) = f(i+1,j,*,*,*), and then for each (nA, nB) compute f by subtracting convolutions. With the sizes involved (a≤105, b≤105, c≤225), the total per (nA,nB) is bounded.

Total work: Σ_{nA,nB} Σ_{i<nA, j≤nB} |f(i+1,j)| * |g(nA-1-i, nB-j)|. The arrays f and g are sparse (defined on a triangle a≤C(nA,2) etc.), but still the convolution cost is O(A*B*C) per pair. Let A_max=105, B_max=105, C_max=225, so ~2.5M ops per convolution. Number of (i,j,nA,nB) tuples: ~ (15^2)^2 / 2 ≈ 50000. 50000 * 2.5M = 1.25e11, too much.

We need a better way. Notice that the sum over a', b', c' is independent for a, b, c (it factorizes!):
Σ_{a'} f_a(i+1,j,a') * g_a(nA-1-i, nB-j, a-a')  [for a-part]
× similarly for b and c.

Wait, does it factorize? Let's see: g(nA', nB', a, b, c) = g_A(nA', a) * g_B(nB', b) * g_C(nA', nB', c), where g_A(nA, a) = C(C(nA,2), a), g_B similarly, g_C(nA, nB, c) = C(nA*nB, c). And f(nA, nB, a, b, c) — does it factorize? In general, f does NOT factorize because the connectivity couples the three types of edges. But let's check: the recurrence gives

f(nA, nB, a, b, c) = g(nA-1, nB, a, b, c) - Σ_{i,j} C(k-1,i) C(k,j) Σ_{a',b',c'} f(i+1,j,a',b',c') g(nA-1-i, nB-j, a-a', b-b', c-c').

If we define F_{nA,nB}(a,b,c) and the sum is a convolution ⊛, then yes the sum over a',b',c' is a full 3D convolution of f(i+1,j,*,*,*) with g(nA-1-i, nB-j, *,*,*). This does not factorize unless f factorizes, which it doesn't.

However, the total cost can be reduced. Note that for the final answer we only need the sum over a+b+c=M of f(N/2, N/2, a, b, c), i.e., the projection onto the total edge count. Let's define F(nA, nB, m) = Σ_{a+b+c=m} f(nA, nB, a, b, c), and similarly G(nA, nB, m) = Σ_{a+b+c=m} g(nA, nB, a, b, c).

But the recurrence involves a 3D convolution projected... hmm, the projection of a 3D convolution is the convolution of the projections only if the variables are independent. Since g factorizes, maybe we can use generating functions.

Define for fixed (nA, nB) the trivariate generating function F_{nA,nB}(x,y,z) = Σ f(nA,nB,a,b,c) x^a y^b z^c, and G_{nA,nB}(x,y,z) = G_A(x) G_B(y) G_C(z). Then the recurrence is:

F_{nA,nB} = G_{nA-1,nB} - Σ_{i,j} C(k-1,i) C(k,j) F_{i+1,j} · G_{nA-1-i, nB-j}

where · denotes the Hadamard product in the convolution sense, i.e., coefficient-wise product of generating functions (which corresponds to 3D convolution of coefficients). Wait, actually: (Σ_{a'} f_{a'} x^{a'}) (Σ_{a''} g_{a''} x^{a''}) = Σ_a (Σ_{a'} f_{a'} g_{a-a'}) x^a, so the coefficient of x^a is the convolution. So the product of generating functions gives the convolution. Therefore, the coefficient of x^a y^b z^c in F_{i+1,j} · G_{nA-1-i, nB-j} is exactly the 3D convolution we need. Good.

So if we work with the full trivariate generating functions as polynomials (with coefficients mod P), the recurrence is:
`F_{nA,nB}(x,y,z) = G_{nA-1,nB}(x,y,z) - Σ_{i=0}^{nA-1} Σ_{j=0}^{nB} C(nA-1, i) C(nB, j) F_{i+1,j}(x,y,z) * G_{nA-1-i, nB-j}(x,y,z)`

where * is polynomial multiplication in three variables (trivariate). This is exact.

Now, the final answer is `C(N-1, N/2-1) * [coefficient of x^M in F_{N/2, N/2}(x,y,z) evaluated at y=1, z=1]`? No wait: the answer is the sum over a+b+c=M of f(N/2, N/2, a, b, c), which is the coefficient of t^M in F_{N/2, N/2}(t, t, t). Because setting x=y=z=t gives Σ f a,b,c t^{a+b+c}.

So we need the coefficients of the polynomial H(t) = F_{nA,nB}(t,t,t), for all M.

But F_{nA,nB} is a trivariate polynomial, and we need its "diagonal" F(t,t,t). The recurrence for F involves products F_{i+1,j} * G_{nA-1-i,nB-j} (trivariate products). The diagonal of a product is not the product of diagonals. So this doesn't simplify directly.

However, we can still compute everything. The trivariate polynomials have degrees: deg_x ≤ C(nA,2) ≤ 105, deg_y ≤ 105, deg_z ≤ nA*nB ≤ 225. The number of monomials is at most 106*106*226 ≈ 2.5M per (nA,nB). The polynomial multiplication of two such polynomials is expensive (2.5M^2). But G factorizes: G = G_A(x) G_B(y) G_C(x,y,z? no, G_C depends on nA,nB). So G_{nA',nB'}(x,y,z) = G_A(nA', x) * G_B(nB', y) * G_C(nA',nB', z). And G_C(nA', nB', z) = Σ_c C(nA'*nB', c) z^c is a single-variable polynomial in z.

Now, the product F_{i+1,j}(x,y,z) * G_A * G_B * G_C:
= [F_{i+1,j}(x,y,z) * G_A(nA-1-i, x)] * G_B(nB-j, y) * G_C(nA-1-i, nB-j, z).

This is a product of three bivariate... no, x and y are separate from z in G, but F has mixed terms. So the product is still trivariate with no factorization of F.

But we can reduce the computation by noting that we only need the final diagonal F(t,t,t). The sum Σ_{a+b+c=M} f_{a,b,c} is what we want. 

**Alternative: use the known formula for the number of connected labeled graphs with a given degree sequence or just edge count, combined with the bipartition via a 2-variable generating function over the two color classes.**

Actually, there's a classical result: the number of connected graphs on n labeled vertices with m edges can be computed by a DP in O(n * m) using the formula with Stirling numbers of the second kind, or by the recurrence `C(n,m) = C(n,m-1) * (n(n-1)/2 - (m-1)) / m` ... no that's for trees? No.

The standard formula: Number of labeled connected graphs on n vertices with m edges is:
`c(n,m) = C(n(n-1)/2, m) - Σ_{k=1}^{n-1} C(n-1, k-1) * c(k, *) * C((n-k)(n-k-1)/2, m-*)`
with convolution. This is O(n^2 * M) where M = n(n-1)/2 ≤ 435 for n=30. This is feasible!

For our problem, we can extend this to the bipartite case. The number of connected graphs with a fixed bipartition (A, B), |A|=k, |B|=k, root in A, with a edges in A, b in B, c across, is:

`f(k,k,a,b,c) = g(k,k,a,b,c) - Σ_{(i,j) proper subset of (A∪B) containing root} f_on_subset * g_on_complement`

where the subset is defined by (i_A, i_B) = (|subset ∩ A|, |subset ∩ B|) with i_A ≥ 1 (contains root), and the complement has (k - i_A, k - i_B) vertices. The number of ways to choose the subset with given (i_A, i_B) is C(k-1, i_A-1) * C(k, i_B). So:

`f(k,k,a,b,c) = g(k-1, k, a, b, c) - Σ_{i_A=1}^{k} Σ_{i_B=0}^{k} C(k-1, i_A-1) C(k, i_B) * (sum over a',b',c' of f(i_A, i_B, a', b', c') * g(k-i_A, k-i_B, a-a', b-b', c-c'))`

where the outer sum excludes (i_A, i_B) = (k, k) (the whole set). Note f(1, 0, 0, 0, 0) = 1, f(1, 0, a, b, c) = 0 otherwise; f(0, *, *, *, *) = 0 (no root).

This is a recurrence on (i_A, i_B) increasing. We can compute all f(i_A, i_B, a, b, c) for i_A + i_B up to 2k.

The size of the state space: i_A ∈ [1, k], i_B ∈ [0, k], so up to k^2 = 225 states. For each state, f is a 3D array of size ~ C(i_A,2) × C(i_B,2) × i_A*i_B ≤ 105 × 105 × 225 ≈ 2.5M. Total memory 225 * 2.5M = 562M, too much.

But we can compute on the fly: for each target (i_A, i_B), we need f(i_A, i_B, a, b, c). The recurrence computes it from smaller (i_A, i_B) (since in the sum, either i_A < target i_A, or i_A = target i_A but i_B < target i_B, but wait the sum goes over all proper subsets, which have either i_A < k or i_B < k, not necessarily both < the current target. Actually, when computing f(I, J), the sum is over all (i_A, i_B) with 1 ≤ i_A ≤ I, 0 ≤ i_B ≤ J, EXCEPT (I, J), and the subset must be proper in the whole graph... Hmm, the complement has (k-i_A, k-i_B) vertices, which must be nonneg, so i_A ≤ k, i_B ≤ k. And proper means not (k,k). So when computing f(I, J) for I ≤ k, J ≤ k, the sum is over (i_A, i_B) with i_A ≤ I, i_B ≤ J, (i_A, i_B) ≠ (I, J), and (k-i_A, k-i_B) ≥ (0,0) so i_A ≤ k, i_B ≤ k. 

Wait, there's a subtlety. The recurrence is derived by: total graphs on the full set = connected + disconnected. For disconnected, the root is in some proper subset S. The number of graphs where root is in S and S is the root component (maximal) is: connected on S times total on complement. So:

`f(I, J) = g(I-1, J) - Σ_{S proper, 1∈S} [connected on S] [total on V\S]`

Here S is a subset of the full vertex set V (size 2k). |S ∩ A| = i_A, |S ∩ B| = i_B, with i_A ≥ 1. The number of such S is C(k-1, i_A-1) C(k, i_B). And connected on S is f(i_A, i_B, a', b', c'), total on complement is g(k - i_A, k - i_B, a-a', b-b', c-c'). The sum is over all (i_A, i_B) with i_A + i_B > 0 (so S nonempty), i_A ≤ k, i_B ≤ k, and (i_A, i_B) ≠ (k, k).

But note: when we compute f(I, J) for the full problem with I=J=k, we need this sum. For intermediate values, we compute f(I, J) for all I ≤ k, J ≤ k. The recurrence for general (I, J) (where we consider a graph on I even + J odd vertices, with root in the even part) is:

`f(I, J, a, b, c) = g(I-1, J, a, b, c) - Σ_{(i,j)≠(I,J), 1≤i≤I, 0≤j≤J} C(I-1, i-1) C(J, j) * [f(i,j) * g(I-i, J-j)](a,b,c)`

where the convolution is over (a,b,c). The base case f(1, 0) = 1 (only a=b=c=0), and f(I, J) = 0 if I=0 or (I=1 and J>0 is impossible since root needs even... wait if I=1, J=0, it's just root. If I=0, undefined.

So we compute f(I, J) for I = 1..k, J = 0..k. For each (I, J), the sum is over (i, j) with 1 ≤ i ≤ I, 0 ≤ j ≤ J, (i,j) ≠ (I,J). This means f(I,J) depends on f(i,j) for i ≤ I, j ≤ J, (i,j) ≠ (I,J). So we can compute in increasing order of I+J, and for same I+J in increasing I (or any order that ensures (i,j) < (I,J) in the product order). Actually, we need (i,j) ≤ (I,J) componentwise and (i,j) ≠ (I,J). So computing in increasing I, and for each I increasing J, works: when computing (I,J), all (i,j) in the sum have i ≤ I and j ≤ J, and if i=I then j < J (already computed since we go increasing J for fixed I), if i<I then (i,j) is computed earlier. Good.

Now, the computational cost. For each (I, J), the arrays have sizes: A_max = C(I,2) ≤ 105, B_max = C(J,2) ≤ 105, C_max = I*J ≤ 225. The convolution of two 3D arrays f(i,j) and g(I-i, J-j) of sizes (A1, B1, C1) and (A2, B2, C2) produces an array of size (A1+A2, B1+B2, C1+C2). The cost of 3D convolution is O(A*B*C * A2*B2*C2) naively, or using FFT O((ABC)^{1.34}) etc. But since the dimensions are small and we have mod P prime (not necessarily NTT-friendly), we do naive convolution.

The total cost: for each (I,J), for each (i,j) in the sum, we compute a 3D convolution. The number of (i,j) for a given (I,J) is O(I*J) ≤ 225. Total (I,J) pairs: 225. So total convolutions: 225 * 225 / 2 ≈ 25000. Each convolution size: the product of the output size. The worst convolution: f(k, k) has support A=105, B=105, C=225. g(0,0) has support (0,0,0), so convolution is trivial. The expensive ones are when both are large, e.g., f(i,j) and g(I-i, J-j) both around half. The product of supports is bounded. Actually, the convolution of arrays of sizes (a1,b1,c1) and (a2,b2,c2) costs O(a1*a2 * b1*b2 * c1*c2) in the worst case. Summed over all (i,j) for a given (I,J), the total is Σ C(I-1,i-1) C(J,j) * |f(i,j)| * |g(I-i,J-j)|, which is bounded by the product of total sizes. 

This is getting too heavy. Let me estimate the total operations. The number of (I,J) is 16*16=256 for k=15. For each, the sum over (i,j) has at most 256 terms, each a 3D convolution. 256^2 = 65536 convolutions. Each convolution up to 2.5M operations (for the largest), but most are small. Let's say average 100K operations per convolution. 65536 * 100K = 6.5e9, which might be borderline but possibly OK in C++ with optimization, but in Python it's too slow.

We need a faster method. **Key insight: the convolution over (a,b,c) factorizes after all?** Let's see. In the sum:
Σ_{a',b',c'} f(i,j,a',b',c') * g(I-i, J-j, a-a', b-b', c-c')
= [Σ_{a'} f_a(i,j,a') g_a(I-i,J-j, a-a')] * [same for b] * [same for c]?
NO, because f is not separable. The sum is a full 3D convolution.

But wait: the final answer only requires the sum over a+b+c=M, i.e., the "total" projection. If we could work with the 1D generating function H_{I,J}(t) = Σ_m f_{I,J}(m) t^m where f_{I,J}(m) = Σ_{a+b+c=m} f(I,J,a,b,c), then the recurrence for H is:
H_{I,J}(t) = G_{I-1,J}(t) - Σ C(...) H_{i,j}(t) * G_{I-i,J-j}(t)
where G_{I,J}(t) = G_A(I, t) G_B(J, t) G_C(I,J, t) = (1+t)^{C(I,2)} (1+t)^{C(J,2)} (1+t)^{I*J} = (1+t)^{C(I,2)+C(J,2)+I*J} = (1+t)^{I*(I-1)/2 + J*(J-1)/2 + I*J} = (1+t)^{(I+J)(I+J-1)/2 - I*J + I*J} wait: C(I,2)+C(J,2)+I*J = I(I-1)/2 + J(J-1)/2 + IJ = (I^2 - I + J^2 - J + 2IJ)/2 = ((I+J)^2 - (I+J))/2 = C(I+J, 2). So G_{I,J}(t) = (1+t)^{C(I+J, 2)}.

Interesting! So the total number of edges in the full graph on I+J vertices is C(I+J, 2), and g(I,J, a,b,c) summed over a+b+c=m is C(C(I+J,2), m). This is independent of the bipartition! So G_{I,J}(t) = (1+t)^{C(I+J,2)}.

Now, does the recurrence for H hold? H_{I,J}(m) = Σ_{a+b+c=m} f(I,J,a,b,c). The recurrence is:
f(I,J,a,b,c) = g(I-1,J,a,b,c) - Σ C(I-1,i-1)C(J,j) [f(i,j) * g(I-i,J-j)](a,b,c)
Summing over a+b+c = m:
H_{I,J}(m) = G_{I-1,J}(m) - Σ C(I-1,i-1)C(J,j) Σ_m' H_{i,j}(m') * G_{I-i,J-j}(m-m')
= G_{I-1,J}(m) - Σ C(...) [H_{i,j} * G_{I-i,J-j}](m).

So yes! The projection onto total edge count m satisfies exactly the same recurrence as the total number of connected labeled graphs on I+J vertices! Because G_{I,J} only depends on I+J, and the binomial coefficients C(I-1,i-1)C(J,j) with i+j = size of subset S... wait, no: the sum is over all (i,j), and the coefficient is C(I-1, i-1) C(J, j). But the number of ways to choose a subset of size s = i+j from I+J-1 non-root vertices is C(I+J-1, s). Here we have C(I-1, i-1) C(J, j) which is the number of ways to choose i-1 from the non-root even vertices and j from odd vertices, giving a subset of size (i-1)+j+1 = i+j. But the subset size is i+j, and the number of such subsets of size i+j is C(I+J-1, i+j-1), not the product. So the recurrence for H is NOT the standard connected-graph recurrence unless C(I-1,i-1)C(J,j) = C(I+J-1, i+j-1), which is not true in general.

So H_{I,J} does not satisfy the simple recurrence. The standard recurrence for connected labeled graphs on n vertices is:
c(n, m) = C(C(n,2), m) - Σ_{s=1}^{n-1} C(n-1, s-1) c(s, *) * C(C(n-s,2), m-*)
The coefficient is C(n-1, s-1). Here we have a product C(I-1, i-1) C(J, j) which is generally different from C(I+J-1, i+j-1). So the bipartition changes the counts. This makes sense: the number of connected graphs with a fixed bipartition and given total edge count depends on how the edges are distributed between the two parts and across, not just the total.

So we cannot avoid the 3D computation. But we can use the factorization of g to speed up the convolution.

**Optimized computation:**
We need to compute f(I, J, a, b, c) for all I∈[1,k], J∈[0,k], a∈[0, C(I,2)], b∈[0, C(J,2)], c∈[0, I*J].

The recurrence: f(I,J) = g(I-1,J) - Σ_{(i,j)≠(I,J)} C(I-1,i-1) C(J,j) * [f(i,j) ⊛ g(I-i, J-j)]

where ⊛ is 3D convolution. g(I', J', a, b, c) = C(C(I',2), a) C(C(J',2), b) C(I'*J', c).

Since g is a product of three 1D arrays (in a, b, c respectively), the 3D convolution of f and g factorizes if we represent f as a 3D array and g as outer product. Specifically:
(f ⊛ g)(a,b,c) = Σ_{a',b',c'} f(a',b',c') g_a(a-a') g_b(b-b') g_c(c-c')
= Σ_{a'} g_a(a-a') Σ_{b'} g_b(b-b') Σ_{c'} g_c(c-c') f(a',b',c')
= (1D conv in a) of (1D conv in b) of (1D conv in c) of f.

So the 3D convolution is separable! We can compute it as three successive 1D convolutions. The cost: for each of the three dimensions, the 1D convolution of two arrays of length L1 and L2 is O(L1*L2). Total cost per 3D convolution: O(A1*A2 + B1*B2 + C1*C2 + ... actually it's three 1D convolutions, but applied to the result of the previous. Let's see: define F_temp[a',b,c] = Σ_{c'} f(a',b,c') g_c(c-c'), then F_temp2[a',b',c] = Σ_{b'} F_temp(a',b',c) g_b(b-b'), then result[a,b,c] = Σ_{a'} F_temp2(a',b,c) g_a(a-a'). Each step is a 1D convolution along one axis. The total work is |f| * (|g_c| + |g_b| + |g_a|) roughly, but actually it's |f| * (size of g in each dim). Since g_c has length I'*J'+1, etc. This is much better than 3D convolution O(|f|*|g|).

Specifically, the work to compute f ⊛ g is O( A1*A2 * B1*C1 + A1*B1*B2*C1 + A1*B1*C1*C2 ) or similar. Actually, the algorithm:
1. Convolve f with g_c along axis c: for each (a,b), do 1D conv of length C1 and C2, producing array of size C1+C2-1. Cost: A1*B1 * (C1*C2).
2. Convolve result with g_b along axis b: for each (a,c), do 1D conv of length B1 and B2. The result of step 1 has size A1 × (B1+B2-1) × (C1+C2-1). Cost: A1 * (C1+C2-1) * (B1*B2).
3. Convolve with g_a along axis a: for each (b,c), do 1D conv of length A1 and A2. Size (A1+A2-1) × (B1+B2-1) × (C1+C2-1). Cost: (A1+A2-1) * (B1+B2-1) * (C1+C2-1) * (A1*A2)? No, the 1D conv along a for each (b,c) pair costs A1*A2, and there are (B1+B2-1)*(C1+C2-1) pairs. So cost: (B1+B2-1)(C1+C2-1) A1 A2.

Total cost ≈ A1 A2 B1 C1 + A1 B1 B2 (C1+C2) + A1 A2 (B1+B2)(C1+C2) ≈ dominated by A1 B1 C1 (A2+B2+C2). Since A2 = C(I-i,2) etc., and A1,B1,C1 are the dimensions of f(i,j).

For our case, f(i,j) has support A1=C(i,2) up to 105, B1=C(j,2) up to 105, C1=ij up to 225. g(I-i, J-j) has A2=C(I-i,2) ≤ 105, B2=C(J-j,2) ≤ 105, C2=(I-i)(J-j) ≤ 225. The cost of f(i,j) ⊛ g(I-i,J-j) is O(A1 B1 C1 (A2+B2+C2)) ≈ 2.5M * 300 = 750M in the worst case, which is still huge.

But note: many f(i,j) are small. Also, we sum over (i,j). The total cost for computing all f(I,J) can be bounded. Actually, the total work is Σ_{I,J} Σ_{i,j} cost(f(i,j)⊛g(I-i,J-j)). This is large.

**Better approach: change the order of summation or use generating functions over m=a+b+c.** But we saw that doesn't work simply.

**Alternative: use the fact that N≤30 is small enough to do 2^{N/2} DP.** Let's revisit. We have k even (including root) and k odd. We can do a DP over subsets of the odd set. For each subset S ⊆ B (odd vertices in root component), and a subset T ⊆ A (even vertices in root component, including root), we can compute the number of connected graphs where the root component is exactly T∪S. But this is again exponential.

Actually, since the graph is 2-colored, the connected component of root is a connected subgraph containing root. We can use the matrix-tree theorem or Prüfer sequences generalized.

**Use Prüfer-like encoding for connected graphs with 2-coloring.** A connected graph on n vertices with a specified 2-coloring (A, B) can be encoded... not simply.

**Use the deletion-contraction recurrence on the number of edges in A, B, and across.** This is the 3D recurrence. Given the small N (30), and the separable convolution, maybe we can do it efficiently in Python with numpy or just optimized loops, since the total number of (I,J) states is 256 and for each the sum over (i,j) is at most 256, and each 1D convolution is small.

Let me estimate more carefully. The array f(I,J) has size (A_I, B_J, C_{I,J}) where A_I = C(I,2)+1 ≤ 106, B_J = C(J,2)+1 ≤ 106, C_{I,J} = I*J+1 ≤ 226. Number of non-zero entries: actually f is defined for all (a,b,c) in range, but many are zero? The total number of graphs is C(C(I+J,2), total), so f(I,J,*,*,*) sums to the number of connected graphs on I+J labeled vertices (with the bipartition), which is roughly 2^{C(I+J,2)}. So f is dense in its support box. So size ~ 2.5M for (15,15).

Memory: 2.5M integers. 256 states would be 640M, too much. But we can free f(i,j) after they are no longer needed. Since we compute in increasing I, then for increasing J, when computing f(I,J) we need f(i,j) for i<I or (i=I and j<J). So we can discard f(I, j) for j < current J after we move to J+1? Actually, for fixed I, when computing J, we need f(I, j) for j < J. So we need to keep the current row I for all J up to current. And for i < I, we need all their f(i, *). So we keep all f(i,j) for i ≤ I, j ≤ k. The total memory is Σ_{i=1}^{I} Σ_{j=0}^{k} size(f(i,j)). For I=k=15, this is Σ_{i=1}^{15} Σ_{j=0}^{15} (C(i,2)+1)(C(j,2)+1)(ij+1). This is about 15*15 * 2.5M / 4 = 140M entries, which is 140M * 8 bytes = 1.1GB, too much for Python.

We need to be smarter. Notice that we only need the final f(k,k) and the intermediate ones to compute it. Can we compute f(k,k) without storing all? The recurrence for f(k,k) is:
f(k,k) = g(k-1,k) - Σ_{(i,j)≠(k,k)} C(k-1,i-1)C(k,j) [f(i,j) ⊛ g(k-i, k-j)]

This is a single equation! We don't need to compute f(k,k) for other k. We need all f(i,j) for i ≤ k, j ≤ k, (i,j) ≠ (k,k). But f(i,j) itself is defined by a similar recurrence involving smaller subsets. So we must compute all of them, or at least have access to them.

But we can compute f(i,j) on demand and cache. However, the number of states is 15*16=240, and each is a 3D array. We can't cache all 240 arrays of average size... let's compute average size. For (I,J), size is C(I,2) * C(J,2) * I*J. The sum over I=1..15, J=0..15 of C(I,2)C(J,2)I*J. Let's compute roughly: Σ_I C(I,2) I ≈ Σ I^3/2 ≈ (15^4)/8 ≈ 6000. Similarly for J. So total ~ 36M. That's manageable! 36M entries * 8 bytes = 288MB, still a lot for Python (a list of lists of lists would be much more). But in Python, a 3D list is inefficient. We need to use a flat array or numpy.

With numpy, we could store each f(I,J) as a 3D array. 36M floats is 288MB, might be OK but heavy. Alternatively, we can avoid storing the full 3D arrays by using the fact that the convolution is separable and we only need the final answer for (k,k).

**Use generating functions in one variable at a time.** Since the convolution is separable, we can think of f(I,J) as an element of the tensor product. But I think the most practical approach for N≤30 is to implement the DP with the 3D arrays using Python integers (since P can be up to 1e9, we need 64-bit) and rely on the small size.

Wait, P is prime but not necessarily small. 10^8 ≤ P ≤ 10^9. Multiplications of numbers up to P need 128-bit intermediate in Python? Python handles big ints natively, but it's slow. However, the numbers are bounded by P after mod.

Let me think of the sizes again. For (I,J) = (15,15), the array is 106 * 106 * 226 = 2,538,856 entries. For (15,14): C(15,2)=105, C(14,2)=91, 15*14=210. 105*91*210 = 2,006,550. Average over J: for I=15, J=0..15. C(J,2) is 0,0,1,3,6,10,15,21,28,36,45,55,66,78,91,105. J*15. The product C(15,2)*C(J,2)*15*J = 105 * 15 * C(J,2)*J. Σ_{J=0}^{15} C(J,2)*J = Σ_{j=2}^{15} j(j-1)/2 * j = (1/2)Σ j^2(j-1) = (1/2)(Σ j^3 - Σ j^2) ≈ (1/2)(15^4/4 - 15^3/3) ≈ (1/2)(12656 - 1125) = 5765. So for I=15, sum over J is 105*15*5765 ≈ 9M. Similarly for each I. Total over all I,J: 9M * 15 / 2 ≈ 67M. 67 million Python integers. Each Python int is ~28 bytes, so ~2GB. Too much.

We need to use arrays (bytearray or array module) or numpy. With numpy int64, 67M * 8 = 536MB. Might be OK on a system with enough RAM, but risky. We can compress: note that for small I or J, the array is small. The bulk is for I and J near 15. The number of states is 240. We can process and discard.

Since we compute in increasing I+J (or increasing I, then J), when we are at (I,J), we need all f(i,j) with i<I, or i=I and j<J. So we need to keep the entire "frontier" of computed f(i,j). This is all (i,j) with i+j < current, or i+j = current and i < I. The total size of this frontier grows. At the end, we have computed all 240 states. We can store them.

But maybe we can reduce the dimension: the final answer is F(M) = Σ_{a+b+c=M} f(k,k,a,b,c). We only need the "diagonal" of f(k,k). Can we compute the diagonal without computing the full 3D array? 

The recurrence for the diagonal: Let D_{I,J}(m) = Σ_{a+b+c=m} f(I,J,a,b,c). Then as derived:
D_{I,J} = G_{I-1,J} - Σ C(I-1,i-1)C(J,j) [D_{i,j} * G_{I-i,J-j}]
But G_{I,J}(m) = C(C(I+J,2), m). This is a 1D recurrence! And we need D_{k,k}(M) for M = N-1 to N(N-1)/2.

Wait, is this recurrence correct? Let's verify. We have:
f(I,J,a,b,c) = g(I-1,J,a,b,c) - Σ_{i,j} C(I-1,i-1)C(J,j) Σ_{a',b',c'} f(i,j,a',b',c') g(I-i,J-j, a-a',b-b',c-c')
Sum over a+b+c = m:
LHS = D_{I,J}(m)
RHS first term: Σ_{a+b+c=m} g(I-1,J,a,b,c) = G_{I-1,J}(m) = C(C((I-1)+J,2), m) = C(C(I+J-1,2), m).
Second term: Σ_{i,j} C(I-1,i-1)C(J,j) Σ_{a+b+c=m} Σ_{a',b',c'} f(i,j,a',b',c') g(I-i,J-j, a-a',b-b',c-c')
= Σ_{i,j} C(I-1,i-1)C(J,j) Σ_{a'+b'+c'=m'} D_{i,j}(m') * G_{I-i,J-j}(m-m')
= Σ_{i,j} C(I-1,i-1)C(J,j) [D_{i,j} * G_{I-i,J-j}](m).

So the recurrence for D is:
D_{I,J}(m) = G_{I-1,J}(m) - Σ_{(i,j)≠(I,J), i≤I, j≤J} C(I-1,i-1)C(J,j) [D_{i,j} * G_{I-i,J-j}](m)

where G_{I,J}(m) = C(C(I+J,2), m). This is EXACTLY the same form as the 3D recurrence, but now D and G are 1D arrays indexed by m (the total edge count), and the convolution is 1D convolution!

This is a huge simplification! We only need to compute 1D arrays D_{I,J} of length C(I+J,2) + 1 ≤ C(30,2)+1 = 436. The number of states (I,J) is 16*16=256 (with I≥1, J≥0, but some may be invalid). For each state, D has size ≤ 436. Total memory: 256 * 436 ≈ 112K entries. Tiny!

The work: for each (I,J), we sum over (i,j) < (I,J) in the partial order, and for each m, we do a convolution. The 1D convolution of D_{i,j} (length L1 = C(i+j,2)+1) and G_{I-i,J-j} (length L2 = C((I-i)+(J-j),2)+1) produces an array of length L1+L2-1. The cost of computing this convolution for all m is O(L1 * L2). So for each (i,j) in the sum, we pay O( C(i+j,2) * C(I+J-(i+j), 2) ). Summing over (i,j) for fixed (I,J): Σ_{i,j} C(i+j,2) C(I+J-(i+j), 2) where the sum is over proper subsets. Let s = i+j, then i ranges from max(1, s-J) to min(I, s), and j = s-i. The number of (i,j) with given s is min(...) - max(...) + 1. And we multiply by C(s,2) * C(I+J-s, 2). The total sum over s=1 to I+J-1 of [number of (i,j) with i+j=s] * C(s,2) * C(n-s,2) where n = I+J. The number of (i,j) with i+j=s is: i from max(1, s-J) to min(I, s), so count = min(I,s) - max(1, s-J) + 1 if this is positive. This is at most min(I, s, J, n-s) + 1. In the worst case, I=J=n/2, the count is roughly min(s, n-s) for s not too extreme. So the sum is at most Σ_s min(s, n-s) C(s,2) C(n-s,2). This is O(n^6) roughly? Let's compute: s ~ n/2, min(s,n-s) ~ n/2, C(s,2) ~ n^2/8, C(n-s,2) ~ n^2/8, so term ~ (n/2)*(n^4/64) = n^5/128. Sum over s ~ n terms gives n^6/128. For n=30, n^6/128 = 30^6/128 ≈ 7.29e8/128 ≈ 5.7e6. So per (I,J) state, the work is up to ~6M operations. Total states: 256. Total work: 256 * 6M = 1.5e9 operations. In Python, 1.5e9 is too slow (Python does ~10^7 simple ops/sec, so 150 seconds). We need to optimize.

We can precompute the convolution [D_{i,j} * G_{I-i,J-j}] for each (i,j) and reuse? No, G depends on I-i, J-j, so different for each (I,J). But the 1D convolution is cheap if we use FFT? But P may not support NTT. However, we can use the fact that the convolution is of a specific form: D_{i,j} is arbitrary, G_{I-i,J-j}(m) = C(C(n-s,2), m) where s=i+j, n=I+J. So the convolution is D_{i,j} * g_{n-s} where g_{n-s}(m) = C(C(n-s,2), m). We can precompute g_{r}(m) for all r and m.

The convolution D * g_r (m) = Σ_{m'} D(m') g_r(m-m'). This is a standard 1D convolution. With lengths up to C(s,2) and C(n-s,2), product up to ~100*100=10K, which is fast. The total number of convolutions: for each (I,J), number of (i,j) in sum is up to I*J+1 ≤ 226. So total convolutions over all (I,J): Σ_{I,J} I*J ≈ (Σ I)^2 / 4 = (120)^2/4 = 3600? Wait, Σ_{I=1}^{k} I = k(k+1)/2 = 120 for k=15. Σ_{I,J} I*J = (Σ I)(Σ J) = 120 * 120 = 14400 (including J=0, but J starts at 0, and I≥1). Actually for I=1..15, J=0..15, Σ I = 120, Σ J = 120, so Σ I*J = 14400. Each convolution costs O(L1*L2). Average L1 = C(s,2) for s average ~15, so ~100. Average L2 ~100. So 10K per convolution. Total: 14400 * 10K = 1.44e8. That's feasible in Python! (1.44e8 simple integer ops might be ~30-60 seconds, which is borderline but acceptable with optimization, especially since many ops are just mod addition/multiplication of small numbers, and we can use PyPy or numpy).

But we also need to compute the binomial coefficients C(C(n,2), m) mod P. Precompute all binomials mod P up to n=30, total edges 435, m up to 435. O(n^2) is trivial.

So the plan is:
1. Precompute binom(n, k) mod P for n up to 30, and for n up to 435 (number of edges in complete graph on 30 vertices). Actually we need C(C(n,2), m) for n up to 30. So precompute binom up to 435.
2. Compute G_{I,J}(m) = binom(C(I+J, 2), m) for all I,J.
3. Initialize D[1][0] as array of length 1: D[1][0][0] = 1, others 0. Wait, f(1,0) is the graph with just root, 0 edges, 1 graph. So D[1][0] = [1] (length C(1,2)=1? C(1,2)=0, so length 1, index 0). Yes.
4. For I from 1 to k, for J from 0 to k, compute D[I][J] using the recurrence:
   D[I][J] = G[I-1][J] - sum over (i,j) in {(i',j'): 1≤i'≤I, 0≤j'≤J, (i',j')≠(I,J)} of C(I-1, i'-1)*C(J, j') * conv(D[i'][j'], G[I-i'][J-j'])
   where conv is 1D convolution.
5. After computing D[k][k] (where k = N/2), the answer for M is C(N-1, N/2-1) * D[k][k][M] mod P.
6. Output D[k][k][M] for M = N-1 to N(N-1)/2, multiplied by C(N-1, N/2-1) mod P.

Wait, is that correct? D_{I,J}(m) = Σ_{a+b+c=m} f(I,J,a,b,c). And the answer is C(N-1, N/2-1) * D_{k,k}(M). Let's verify with N=4, k=2.
N=4, k=2. Vertices: root (even), one more even, two odd. Total vertices 4.
We compute D[2][2] and multiply by C(3,1)=3.
Let's compute manually or via the recurrence.
First, precompute G[I][J] for I+J up to 4.
G[1][0]: I+J=1, C(1,2)=0, so G[1][0] = [1] (only m=0).
G[2][0]: I+J=2, C(2,2)=1, G[2][0](0)=1, G[2][0](1)=C(1,1)=1? Wait C(C(2,2), m) = C(1, m). So G[2][0] = [1, 1] for m=0,1.
G[1][1]: I+J=2, same, [1,1].
G[3][0]: I+J=3, C(3,2)=3, G = [C(3,0), C(3,1), C(3,2), C(3,3)] = [1,3,3,1].
etc.

Now D[1][0] = [1].
D[2][0]: I=2, J=0. Recurrence: D[2][0] = G[1][0] - Σ_{(i,j)≠(2,0), i≤2, j≤0} C(1,i-1)C(0,j) D[i][j] * G[2-i][0-j].
The only (i,j) with j=0, i≤2, (i,j)≠(2,0) is (1,0). So:
D[2][0] = G[1][0] - C(1,