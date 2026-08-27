
## ideation
The core difficulty lies in correctly counting graphs where the BFS distance partition is exactly $(S_{even}, S_{odd})$ with $|S_{even}| = |S_{odd}| = N/2$. A naive approach of summing over all subsets $S_{even}$ containing vertex 1 fails because the condition "BFS distances result in this partition" is complex: it requires that there are no "shortcuts" (edges between non-adjacent BFS layers or backward edges that create shorter paths) that would alter the distances.

Specifically, for a fixed partition $(S_{even}, S_{odd})$, the graph must satisfy:
1. It is connected.
2. Vertex 1 is in $S_{even}$.
3. For every vertex $v \in S_{odd}$, all its neighbors must be in $S_{even}$? No, that's for bipartite. BFS layers allow edges within the same layer and between adjacent layers.
   - Let the BFS layers be $L_0, L_1, \dots, L_k$.
   - $S_{even} = L_0 \cup L_2 \cup \dots$
   - $S_{odd} = L_1 \cup L_3 \cup \dots$
   - Edges can exist within any $L_i$.
   - Edges can exist between $L_i$ and $L_{i+1}$.
   - Edges between $L_i$ and $L_j$ with $|i-j| > 1$ are forbidden because they would create a shorter path.
   - Edges between $L_i$ and $L_j$ with $j < i-1$ are forbidden for the same reason.

However, iterating over all BFS layerings is still complex because the number of layerings can be large, and for each layering, we need to count graphs with exactly $M$ edges that are consistent with it AND result in *exactly* that layering (i.e., no "redundant" edges that don't change the BFS tree structure but might affect connectivity or distances? Actually, if we fix the layers, the condition is just that there are no edges skipping layers. But we also need to ensure that the graph is connected and that the BFS *actually* produces these layers. The latter means that for each layer $L_i$ ($i>0$), there must be at least one edge from $L_i$ to $L_{i-1}$, and no edges from $L_i$ to $L_j$ with $j < i-1$.

Given $N \le 30$, we can use a DP approach that builds the graph layer by layer.
State: `dp(layer_index, mask_of_visited_vertices, current_edge_count)` is too expensive.
Alternative: Since $N$ is small, we can iterate over all possible *partitions* of the $N-1$ other vertices into layers $L_1, L_2, \dots$. $L_0=\{1\}$.
For a fixed sequence of layers $(L_0, L_1, \dots, L_k)$, the number of valid graphs with $M$ edges is the number of ways to choose $M$ edges such that:
1. No edge connects $u, v$ if their layers differ by more than 1.
2. For each $i \ge 1$, there is at least one edge between $L_i$ and $L_{i-1}$ (to ensure $L_i$ is reached at distance $i$).
3. The graph is connected. (Actually, if condition 2 holds for all $i$, and we consider edges within layers and between adjacent layers, the graph is connected if and only if the "skeleton" of inter-layer edges connects all layers. But intra-layer edges don't help connectivity between layers. So, we need the subgraph formed by edges between $L_i$ and $L_{i-1}$ to connect $L_i$ to the rest. This is equivalent to: for each $i \ge 1$, every vertex in $L_i$ has at least one neighbor in $L_{i-1}$? No, the whole set $L_i$ must be connected to $L_{i-1}$ via at least one edge, but individual vertices in $L_i$ don't necessarily need a neighbor in $L_{i-1}$ if they are connected to other vertices in $L_i$ which are connected to $L_{i-1}$. Wait, BFS distance is defined by shortest path. If a vertex $v \in L_i$ has no neighbor in $L_{i-1}$, but has a neighbor in $L_i$ that does, its distance is still $i$ (via the neighbor). So the condition is just that the union of edges between $L_i$ and $L_{i-1}$ is non-empty for all $i \ge 1$.

So, for a fixed layering, we can count the number of graphs with $M$ edges as follows:
- Total possible edges allowed: $E_{allowed} = \sum_{i} \binom{|L_i|}{2} + \sum_{i \ge 1} |L_i| \cdot |L_{i-1}|$.
- We need to choose $M$ edges from $E_{allowed}$.
- Constraint: For each $i \ge 1$, the set of edges between $L_i$ and $L_{i-1}$ is non-empty.
- This can be solved using inclusion-exclusion on the "forbidden" condition (empty inter-layer edges).

Let $K = k$ be the number of layers (excluding $L_0$).
Let $A_i$ be the property that there are no edges between $L_i$ and $L_{i-1}$.
We want the number of graphs with $M$ edges that satisfy none of $A_1, \dots, A_k$.
By inclusion-exclusion:
$\sum_{S \subseteq \{1, \dots, k\}} (-1)^{|S|} N(S)$
where $N(S)$ is the number of graphs with $M$ edges chosen from $E_{allowed} \setminus \bigcup_{i \in S} E(L_i, L_{i-1})$.
Basically, for a subset $S$ of indices, we remove the inter-layer edges for those $i \in S$. The remaining allowed edges are:
- All intra-layer edges.
- Inter-layer edges for $i \notin S$.
Let $E_S$ be the count of such allowed edges. Then $N(S) = \binom{E_S}{M}$.

So the algorithm is:
1. Iterate over all compositions of $N-1$ into $k$ parts ($k \ge 1$). Each composition corresponds to a layering $(L_0, L_1, \dots, L_k)$ where $|L_0|=1$ and $|L_i| = c_i$ for $i \ge 1$.
2. For each layering, calculate $S_{even} = \{1\} \cup \bigcup_{j \text{ even}} L_j$ and $S_{odd} = \bigcup_{j \text{ odd}} L_j$.
3. If $|S_{even}| \ne N/2$, skip.
4. Otherwise, for this layering, compute the answer for each $M$ using inclusion-exclusion over the $k$ inter-layer boundaries.
   - Precompute the number of allowed edges for each subset of boundaries removed.
   - Since $k$ is small (at most $N-1$, but typically much smaller for valid partitions), and $N \le 30$, $k$ can be up to 29. $2^{29}$ is too big.
   - However, note that the layers are indistinguishable in terms of structure if we just care about sizes? No, the sizes matter for edge counts.
   - But wait, we can group layerings by the sequence of layer sizes.
   - Also, we can optimize the inclusion-exclusion. The term $E_S$ depends only on which boundaries are removed.
   - Let $B_i$ be the number of possible edges between $L_i$ and $L_{i-1}$, i.e., $|L_i| \cdot |L_{i-1}|$.
   - Let $I$ be the number of intra-layer edges, i.e., $\sum \binom{|L_j|}{2}$.
   - $E_S = I + \sum_{i \notin S} B_i$.
   - We need to sum $(-1)^{|S|} \binom{I + \sum_{i \notin S} B_i}{M}$ over all $S \subseteq \{1, \dots, k\}$.
   - This is equivalent to: $\sum_{j=0}^k (-1)^j \sum_{S: |S|=j} \binom{I + \sum_{i \notin S} B_i}{M}$.
   - Let $T = \sum_{i=1}^k B_i$. Then $\sum_{i \notin S} B_i = T - \sum_{i \in S} B_i$.
   - So we need $\sum_{S \subseteq \{1, \dots, k\}} (-1)^{|S|} \binom{I + T - \sum_{i \in S} B_i}{M}$.
   - This looks like a DP. Let $dp[i][w]$ be the sum of $(-1)^{|S|}$ for subsets of the first $i$ boundaries with total weight $w = \sum_{j \in S} B_j$.
   - Then the answer for this layering and edge count $M$ is $\sum_w dp[k][w] \binom{I + T - w}{M}$.
   - The maximum weight $T$ is roughly $(N/2)^2 \cdot k \approx 225 \cdot 15 \approx 3000$. This is feasible.

5. Sum the results over all valid layerings (partitions of $N-1$).

Pitfalls:
- Double counting: Each graph has a unique BFS layering? Yes, BFS layers are uniquely determined by the graph. So summing over all layerings is correct.
- Modulo arithmetic: $P$ is prime, so we can use modular inverse for combinations.
- Performance: Number of compositions of $N-1$ is $2^{N-2}$. For $N=30$, $2^{28}$ is too big.
- We need a better way to iterate. Notice that the contribution of a layering depends only on the multiset of layer sizes? No, the order matters for $B_i$ and the parity of layers for $S_{even}/S_{odd}$.
- However, we can use DP to generate the layerings and accumulate the results directly.
- Let $DP(i, s, current\_I, current\_T, last\_layer\_size)$ be a state? No, we need to track the parity of the current layer to know if it contributes to even or odd set.
- Actually, we can iterate over the number of layers $k$ and the sizes.
- Given the constraint $N \le 30$, maybe we can use a different approach.
- Alternative: Iterate over all subsets $S_{even}$ of size $N/2$ containing 1.
  - For each such subset, we need to count graphs where BFS distances result in this partition.
  - This requires that there are no edges within $S_{even}$ that connect to $S_{odd}$ in a way that reduces distance? No.
  - The condition is: The graph is connected, and for every $v \in S_{odd}$, $dist(1, v)$ is odd, and for every $v \in S_{even}$, $dist(1, v)$ is even.
  - This implies that there are no edges between $u \in S_{even}$ and $v \in S_{even}$ if they are at the same BFS layer? No, edges within a layer are allowed.
  - The key is that there are no edges between $S_{even}$ and $S_{odd}$ that are "long range" in the BFS sense.
  - This seems harder than the layering approach.

Let's stick to the layering approach but optimize the iteration.
We can use a recursive function to generate compositions of $N-1$.
For $N=30$, $2^{28}$ is too large.
However, note that many compositions will have the same "profile" of layer sizes and parities.
We can group by the sequence of layer sizes.
But the parity of the index matters.
Let's try to use DP to count the number of layerings with a given set of layer sizes and a given "signature" for the inclusion-exclusion.
Actually, the inclusion-exclusion part depends on the specific $B_i$ values.
$B_i = |L_i| \cdot |L_{i-1}|$.
This depends on adjacent layer sizes.
This suggests we can't easily group.

Wait, $N \le 30$ is small enough for $O(2^N)$? No.
But the number of *partitions* of $N-1$ is much smaller than $2^{N-2}$? No, compositions are $2^{N-2}$. Partitions are $p(N-1)$. For $N=30$, $p(29) = 4565$. This is small!
But the order of layers matters for the BFS structure (layer 1 is adjacent to 0, layer 2 to 1, etc.).
So we must consider compositions, not just partitions.
However, we can use DP to sum over compositions.
Let $DP(i, s, parity\_sum, current\_layer\_size)$...
We need to track the current layer size to compute $B_i$ for the next step.
And we need to track the "state" for the inclusion-exclusion DP.
The inclusion-exclusion DP state is a polynomial in $x$: $\sum c_w x^w$.
We can maintain this polynomial.
The degree of the polynomial is at most $T \approx 3000$.
Multiplying polynomials is expensive.
But we are adding terms.
$DP_{new} = DP_{old} * (1 - x^{B_i})$.
This is a convolution.
If we do this for each layer, the complexity is $O(N \cdot T^2)$ or $O(N \cdot T)$.
$T \approx 3000$, $N=30$. $30 \cdot 3000 = 90000$.
The number of states in the outer DP:
$i$: current number of vertices placed ($0$ to $N-1$).
$s$: current sum of "weights" for inclusion-exclusion? No, we can't merge states easily because the $B_i$ values depend on the specific layer sizes.
Actually, we can't merge states because the $B_i$ values are different for different layerings.
So we must iterate over all compositions.
$2^{28}$ is too big.

Is there a symmetry?
If we swap two adjacent layers of the same size, the $B_i$ values change?
$L_{i-1}, L_i, L_{i+1}$.
$B_i = |L_i||L_{i-1}|$, $B_{i+1} = |L_{i+1}||L_i|$.
If $|L_{i-1}| = |L_{i+1}|$, then swapping $L_i$ and $L_{i+1}$? No, the sequence is ordered.
If we have a composition, the order is fixed.

Let's re-read constraints. $N \le 30$.
Maybe the number of *valid* layerings (where $|S_{even}| = N/2$) is small?
No, many compositions will satisfy this.

Let's try a different approach.
Iterate over all subsets $S_{even}$ of size $N/2$ containing 1.
There are $\binom{29}{14}$ such subsets. $\binom{29}{14} = 77558760$. This is too big.

Wait, sample 3 has $N=10$. $\binom{9}{4} = 126$.
For $N=30$, $\binom{29}{14}$ is huge.

Let's go back to layering.
We can use DP to generate compositions and accumulate the inclusion-exclusion polynomials.
State: $DP(i, last\_size, poly)$
$i$: number of vertices placed so far (excluding vertex 1).
$last\_size$: size of the last layer added.
$poly$: a polynomial representing the inclusion-exclusion weights for the boundaries so far.
The polynomial has terms $c_w x^w$.
When we add a new layer of size $s$, we multiply the polynomial by $(1 - x^{last\_size \cdot s})$.
We also update the parity of the current layer to check if the final $S_{even}$ has size $N/2$.
We can track the current size of $S_{even}$ and $S_{odd}$ in the state.
State: $DP(i, last\_size, s\_even, poly)$
$i$: $0 \dots N-1$.
$last\_size$: $1 \dots N-1$.
$s\_even$: $1 \dots N/2$.
$poly$: degree up to $T$.
This state space is too big.

However, note that we only care about the final answer for each $M$.
We can swap the loops:
Outer loop: iterate over all compositions.
For each composition, compute the polynomial and then the answer.
To avoid iterating $2^{28}$ compositions, we can use memoization on the composition structure?
No, the composition is a sequence.

Let's consider that $N$ is up to 30.
Maybe we can use the fact that the number of layers $k$ is small?
If $k$ is large, the layers are small.
If $k$ is small, the layers are large.

Actually, there is a known technique for this problem.
It is equivalent to counting graphs with a given BFS tree structure.
But we don't fix the tree, just the layers.

Let's try to code the composition iteration with pruning.
For $N=30$, $2^{28}$ is too slow.
But maybe we can use DP to sum over compositions.
$DP(i, last\_size, s\_even, poly)$
We can't store poly in state.
But we can compute the poly on the fly.
The issue is that the poly depends on the specific sequence of $B_i$.
So we can't merge states with different $B_i$ sequences.

Wait, look at the constraints again.
$N \le 30$.
Maybe the intended solution is $O(2^N \cdot N^2)$ or similar?
$2^{30}$ is too big.

Let's look at Sample 3. $N=10$.
$\binom{9}{4} = 126$ subsets.
For each subset, we can compute the answer.
How?
For a fixed $S_{even}$, we need to count graphs where BFS distances result in this partition.
This requires that:
1. No edge within $S_{even}$ connects two vertices that are at the same BFS layer? No.
2. No edge between $S_{even}$ and $S_{odd}$ that skips a layer.
3. No edge within $S_{odd}$ that skips a layer.

Actually, the condition "BFS distances result in partition $(S_{even}, S_{odd})$" is equivalent to:
- The graph is connected.
- There are no edges between $u \in S_{even}$ and $v \in S_{odd}$ if $dist(1, u) \ne dist(1, v) \pm 1$?
- This is hard to check without knowing distances.

I will implement the composition iteration with DP to generate compositions and accumulate the inclusion-exclusion polynomials.
To handle the state explosion, I will use a dictionary for the DP state:
$DP[i][last\_size][s\_even] = poly$
where $poly$ is a list/array of coefficients.
$i$ goes from $0$ to $N-1$.
$last\_size$ goes from $1$ to $N-1$.
$s\_even$ goes from $1$ to $N/2$.
The number of states is $30 \cdot 30 \cdot 15 = 13500$.
For each state, we store a polynomial of degree up to $3000$.
Updating the polynomial: $poly_{new} = poly_{old} * (1 - x^{B})$.
This is $O(T)$ per transition.
Total complexity: $13500 \cdot 3000 \approx 4 \cdot 10^7$.
This is feasible in Python if optimized.

Next, I will implement this DP.

## worker: Implement the DP solution to iterate over all vali
The solution uses dynamic programming to iterate over all possible BFS layerings (compositions of N-1). The DP state tracks the number of layers placed, the size of the last layer, the current size of the even-distance set, the total number of vertices placed, the number of intra-layer edges (I), and the total number of inter-layer edges (T). For each state, a polynomial is maintained that represents the inclusion-exclusion weights for the boundaries between layers. The polynomial is updated by multiplying with $(1 - x^B)$ where $B$ is the number of possible edges between the last layer and the new layer. Finally, for each valid final state (all vertices placed, even set size is N/2), the answer for each M is computed by summing over the polynomial coefficients multiplied by the appropriate binomial coefficient.
