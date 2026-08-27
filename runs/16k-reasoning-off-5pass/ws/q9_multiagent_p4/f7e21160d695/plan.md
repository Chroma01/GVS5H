The problem asks us to minimize the sum of bottleneck distances $f(A_i, B_i)$ by optimally permuting $B$. The function $f(u, v)$ is the minimum possible maximum edge weight on a path between $u$ and $v$, which is equivalent to the bottleneck distance in a Minimum Spanning Tree (MST). Since the bottleneck distance only depends on the MST, we first construct the MST of the given graph. Once we have the MST, the graph becomes a tree where $f(u, v)$ is the maximum edge weight on the unique path between $u$ and $v$. We can then use binary lifting (or similar techniques) to efficiently query $f(u, v)$. To minimize the sum, we sort both sequence $A$ and sequence $B$ based on their "cost profiles" or simply sort $B$ and greedily assign the smallest available $B_j$ to the $A_i$ that results in the smallest marginal increase, but a more robust approach for this specific structure is to realize that sorting $A$ and $B$ by their values in the MST might not be direct. However, a standard greedy strategy for minimizing $\sum f(A_i, B_{\pi(i)})$ when $f$ is a metric-like function on a tree often involves sorting. Actually, the optimal strategy here is to sort $A$ and $B$ by the value of $f(root, x)$ for an arbitrary root? No, that's not sufficient. The correct greedy approach for minimizing the sum of distances in a tree metric is to sort both arrays $A$ and $B$ based on their "depth" or distance from a specific node? Let's reconsider. The function $f(u,v)$ is the max edge on the path. If we sort $A$ and $B$ by some criteria, does it work?
Actually, the optimal permutation is achieved by sorting $A$ and $B$ such that we pair the "closest" elements. But "closest" is defined by the max edge.
Let's look at the constraints and properties. $f(u,v)$ is the bottleneck distance.
The standard solution for this specific problem (minimizing sum of bottleneck distances with permutation) is:
1. Construct the MST.
2. The problem reduces to pairing nodes in a tree to minimize the sum of max-edge-path-weights.
3. It turns out that sorting $A$ and $B$ by their distance from an arbitrary root (like node 1) in the MST does NOT work directly because the path between two arbitrary nodes $u, v$ depends on their LCA.
However, there is a known result: To minimize $\sum f(A_i, B_i)$, we should sort $A$ and $B$ based on the value of $f(root, x)$? No.
Let's re-evaluate the greedy strategy. Consider the edges in the MST sorted by weight. If we include an edge $e$ with weight $w$, it connects two components. Any path crossing this edge has cost at least $w$.
Actually, the optimal strategy is simply to sort $A$ and $B$ by the value of $f(1, x)$ (distance from root 1) and pair them?
Let's check Sample 1.
MST edges: (3,4,1), (1,3,2), (1,4,4) -> wait, (1,4) is 4, (2,4) is 5.
Edges sorted: (3,4,1), (1,3,2), (1,4,4), (2,4,5).
MST: (3,4,1), (1,3,2), (2,4,5)? No, (1,4) is 4, which is better than (2,4) for connecting 1 and 2?
Wait, Kruskal's:
1. (3,4) w=1. Sets: {3,4}, {1}, {2}.
2. (1,3) w=2. Sets: {1,3,4}, {2}.
3. (1,4) w=4. Cycle. Skip.
4. (2,4) w=5. Connects {2} to {1,3,4}. Sets: {1,2,3,4}.
MST Edges: (3,4,1), (1,3,2), (2,4,5).
Tree structure: 2 --(5)-- 4 --(1)-- 3 --(2)-- 1.
A = [1, 1, 3], B = [4, 4, 2].
Distances in MST:
f(1,2): path 1-3-4-2, max(2,1,5)=5.
f(1,4): path 1-3-4, max(2,1)=2.
f(3,4): path 3-4, max(1)=1.
We need to pair A=[1,1,3] with permuted B=[4,4,2].
Options:
1. (1,4), (1,4), (3,2) -> 2 + 2 + 5 = 9.
2. (1,4), (1,2), (3,4) -> 2 + 5 + 1 = 8.
3. (1,2), (1,4), (3,4) -> 5 + 2 + 1 = 8.
Min is 8.
Notice the values of $f(1, x)$:
$f(1,1)=0, f(1,2)=5, f(1,3)=2$.
Sorted A by $f(1, \cdot)$: 1 (0), 1 (0), 3 (2).
Sorted B by $f(1, \cdot)$: 4 (2), 4 (2), 2 (5).
Pairs: (1,4)->2, (1,4)->2, (3,2)->5. Sum=9. Not optimal.
So sorting by distance from root 1 is incorrect.

Correct approach:
The problem is equivalent to finding a minimum weight perfect matching in a bipartite graph where edge weights are $f(A_i, B_j)$. Since $N, K$ are up to $2 \cdot 10^5$, we need $O(N \log N)$ or similar.
There is a specific property for bottleneck distances on trees.
Actually, the optimal strategy is to sort $A$ and $B$ by the value of $f(u, v)$? No.
Let's reconsider the structure. $f(u,v)$ is the max edge on the path.
Is it possible that sorting $A$ and $B$ by the "depth" in the MST where depth is defined by the max edge from root?
Let $D(u) = f(root, u)$.
In Sample 1, root=1.
$D(1)=0, D(3)=2, D(4)=2, D(2)=5$.
A values: 1, 1, 3. Corresponding D: 0, 0, 2.
B values: 4, 4, 2. Corresponding D: 2, 2, 5.
If we sort A by D: [1, 1, 3] (D: 0, 0, 2).
Sort B by D: [4, 4, 2] (D: 2, 2, 5).
Pairing: (1,4)->2, (1,4)->2, (3,2)->5. Sum 9. Still 9.
Wait, the sample output says 8. The pairing that gives 8 is (1,4), (1,2), (3,4).
Here A indices: 1, 1, 3. B indices: 4, 2, 4.
Pairs: (1,4) cost 2. (1,2) cost 5. (3,4) cost 1.
Notice that for A=1, we paired with B=4 (cost 2) and B=2 (cost 5).
For A=3, we paired with B=4 (cost 1).
The costs are not monotonic with respect to $D$.

Alternative Idea:
Maybe we can process edges of the MST in increasing order of weight?
When we add an edge $e$ with weight $w$, it merges two components $C_1$ and $C_2$.
Any path between $u \in C_1$ and $v \in C_2$ must use an edge with weight $\ge w$.
Specifically, if we consider the MST edges sorted by weight, the value $f(u,v)$ is exactly the weight of the first edge (in sorted order) that connects the component containing $u$ and the component containing $v$.
This looks like we can use a greedy strategy with a data structure.
We want to minimize $\sum f(A_i, B_i)$.
Let's sort the edges of the MST by weight: $e_1, e_2, \dots, e_{N-1}$ with weights $w_1 \le w_2 \le \dots$.
Initially, each vertex is in its own component.
When we process edge $e_k = (u, v)$ with weight $w_k$, it merges component $S_u$ and $S_v$.
For any $x \in S_u$ and $y \in S_v$, the path between them now has a bottleneck of at most $w_k$. Before this edge, the bottleneck was $\ge w_k$ (actually infinity if disconnected).
So, $f(x, y) = w_k$ for all $x \in S_u, y \in S_v$ (assuming no smaller edge connected them, which is true by MST property).
We can maintain the sets of indices $I_A = \{i \mid A_i \in \text{some component}\}$ and $I_B = \{j \mid B_j \in \text{some component}\}$.
Actually, we can maintain for each component the count of $A$'s and $B$'s inside it.
When merging $S_u$ and $S_v$ with weight $w$:
We have a set of $A$'s in $S_u$ and $B$'s in $S_v$, and $A$'s in $S_v$ and $B$'s in $S_u$.
For any pair $(a \in S_u, b \in S_v)$, the cost is $w$.
For any pair $(a \in S_v, b \in S_u)$, the cost is $w$.
For pairs within $S_u$ or within $S_v$, the cost is determined by edges processed earlier (smaller weights).
This suggests we can calculate the total cost by summing contributions.
Total Cost = $\sum_{k} w_k \times (\text{number of pairs } (i, j) \text{ such that } A_i \in S_{u_k}, B_j \in S_{v_k} \text{ or vice versa, and they are matched})$.
Wait, this is not quite right because the matching is global. We are choosing a permutation.
This looks like a minimum cost perfect matching problem where the cost matrix has a specific structure (ultrametric-like).
However, there is a simpler greedy strategy for this specific "bottleneck sum" problem.
Sort $A$ and $B$ by the value of $f(root, x)$? We tried that.
What if we sort $A$ and $B$ by the "potential" of the node?
Actually, the correct greedy strategy for minimizing $\sum f(A_i, B_i)$ on a tree is:
Sort $A$ and $B$ by the value of $f(1, x)$? No.
Let's look at the contribution of each edge in the MST.
Edge $e$ with weight $w$ splits the tree into two sets of vertices $V_1, V_2$.
Any path from $u \in V_1$ to $v \in V_2$ has cost $\ge w$.
In fact, if $e$ is the highest weight edge on the path, the cost is $w$.
Since it's an MST, the path between any $u, v$ consists of edges with weights $\le w_{max}$.
The value $f(u,v)$ is the weight of the "highest" edge on the path.
Consider the edges of the MST sorted by weight descending.
Remove edges one by one. When we remove edge $e$ with weight $w$, the tree splits into two components.
For any $u$ in one component and $v$ in the other, $f(u,v) = w$.
So, if we have $cntA_1$ items of $A$ in component 1 and $cntB_1$ items of $B$ in component 1, and similarly $cntA_2, cntB_2$ in component 2.
The number of pairs $(A_i, B_j)$ that are separated by this cut is not fixed because we can permute $B$.
But we want to MINIMIZE the sum.
This means we want to AVOID pairing $A$'s and $B$'s across high-weight cuts if possible.
We should pair $A$'s and $B$'s such that they stay together in small components as much as possible.
This implies we should pair $A$'s and $B$'s that are "close" to each other.
Specifically, if we sort $A$ and $B$ by the value of $f(root, x)$, does it help?
Let's try a different root or a different metric.
Actually, the optimal strategy is to sort $A$ and $B$ by the value of $f(1, x)$?
Wait, in Sample 1, $f(1,1)=0, f(1,3)=2, f(1,4)=2, f(1,2)=5$.
A: 1, 1, 3. B: 4, 4, 2.
If we sort A by $f(1, \cdot)$: 1, 1, 3.
Sort B by $f(1, \cdot)$: 4, 4, 2.
Pairs: (1,4), (1,4), (3,2). Costs: 2, 2, 5. Sum 9.
But optimal is 8.
The optimal pairing was (1,4), (1,2), (3,4).
Costs: 2, 5, 1.
Notice that for A=3, we paired with B=4 (cost 1). $f(3,4)=1$.
For A=1, we paired with B=4 (cost 2) and B=2 (cost 5).
It seems we should pair the "smallest" available $B$ with the $A$ that has the "smallest" cost to it?
But the cost depends on the pair.
Let's re-read the problem carefully. "Permute B freely".
This is a minimum weight perfect matching in a complete bipartite graph with weight matrix $W_{ij} = f(A_i, B_j)$.
Since the graph is a tree, $f(u,v)$ has the property that $f(u,v) \le \max(f(u,w), f(w,v))$? No, $f(u,v) = \max(f(u,w), f(w,v))$ for any $w$ on the path.
This is an ultrametric space property?
Yes, the bottleneck distance on a tree satisfies the strong triangle inequality: $f(u,v) \le \max(f(u,w), f(w,v))$.
For ultrametric spaces, the minimum weight perfect matching can be found by sorting?
Actually, for ultrametric spaces, the optimal matching is obtained by sorting the elements by their "depth" or distance from a root?
Let's try sorting by $f(1, x)$ again but maybe the root matters?
What if we pick a root such that the "depths" are more spread out?
Or maybe we sort by the value of $f(x, y)$ for some fixed $y$?
Actually, there is a known result: For any ultrametric space, sorting the points by their distance from an arbitrary origin $r$ and pairing the $k$-th smallest $A$ with the $k$-th smallest $B$ minimizes the sum of distances?
Let's test this hypothesis on Sample 1.
Root = 1.
$D(A_1) = f(1,1) = 0$.
$D(A_2) = f(1,1) = 0$.
$D(A_3) = f(1,3) = 2$.
Sorted A (by D): 1, 1, 3.
$D(B_1) = f(1,4) = 2$.
$D(B_2) = f(1,4) = 2$.
$D(B_3) = f(1,2) = 5$.
Sorted B (by D): 4, 4, 2.
Pairing: (1,4), (1,4), (3,2). Costs: 2, 2, 5. Sum 9.
Still 9.
Why is the hypothesis wrong?
Maybe the root should be different?
Try Root = 3.
$D(1) = f(3,1) = 2$.
$D(2) = f(3,2) = \max(f(3,4), f(4,2)) = \max(1, 5) = 5$.
$D(4) = f(3,4) = 1$.
A: 1, 1, 3.
$D(A_1)=2, D(A_2)=2, D(A_3)=0$.
Sorted A: 3, 1, 1.
B: 4, 4, 2.
$D(B_1)=1, D(B_2)=1, D(B_3)=5$.
Sorted B: 4, 4, 2.
Pairing: (3,4), (1,4), (1,2).
Costs: $f(3,4)=1$, $f(1,4)=2$, $f(1,2)=5$. Sum = 8.
Bingo!
So the strategy is: Pick an arbitrary root (or maybe a specific one?), compute $f(root, x)$ for all $x$, sort $A$ and $B$ by these values, and pair them.
Does the choice of root matter?
In Sample 1, Root=1 gave 9, Root=3 gave 8.
Is there a root that always gives the optimal?
Or do we need to try all roots? $N$ is $2 \cdot 10^5$, trying all roots is $O(N^2)$, too slow.
However, note that the "depth" $f(root, x)$ is just the max edge on the path from root to $x$.
Is it possible that we should sort by $f(x, y)$ for a specific $y$ that minimizes the result?
Actually, the problem is symmetric.
Wait, if the space is ultrametric, the optimal matching is independent of the root?
Let's check the property.
In an ultrametric space, $d(x,y) \le \max(d(x,z), d(z,y))$.
Theorem: For any ultrametric space, the minimum weight perfect matching between two sets of points $A$ and $B$ (where $|A|=|B|$) is achieved by sorting $A$ and $B$ by their distance from an arbitrary point $r$?
No, the counterexample (Root=1 vs Root=3) suggests the root matters.
But wait, in Sample 1, the optimal sum is 8.
With Root=3, we got 8.
With Root=1, we got 9.
Why did Root=1 fail?
Maybe because the "center" of the distribution is not 1.
Is there a root that is "central"?
Actually, the optimal root might be one of the points in $A$ or $B$?
Or maybe we don't need a root.
Let's reconsider the structure.
We have a tree. We want to match $A$ and $B$.
The cost of matching $u$ and $v$ is the max edge on the path.
This is equivalent to: for each edge $e$ with weight $w$, if the cut defined by $e$ separates $k$ elements of $A$ and $l$ elements of $B$, then we must have at least $\min(k, l)$ pairs crossing this cut?
No, that's for the sum of distances in a metric space where distance is sum of edge weights. Here it's max.
For max metric: $f(u,v) = w$ if the path goes through $e$ and $e$ is the max weight edge.
Actually, $f(u,v) = \max_{e \in path(u,v)} w(e)$.
So $\sum f(A_i, B_i) = \sum_{i} \max_{e \in path(A_i, B_i)} w(e)$.
We can rewrite this as $\sum_{e \in MST} w(e) \times (\text{number of pairs } (A_i, B_i) \text{ such that } e \text{ is the max weight edge on their path})$.
Since edges are processed in increasing order of weight, an edge $e$ is the max weight edge for a pair if the pair is separated by $e$ in the MST when we remove all edges with weight $< w(e)$.
Let's process edges in increasing order of weight.
Initially, all vertices are isolated.
When we add edge $e=(u,v)$ with weight $w$, we merge two components $C_u$ and $C_v$.
Any pair $(a, b)$ with $a \in C_u, b \in C_v$ will have $f(a,b) = w$ (since all other edges on the path are $\le w$, and $e$ is the first one connecting them).
Wait, if there are multiple edges with the same weight, the order doesn't matter for the value, but we need to be careful.
Actually, the value $f(a,b)$ is the weight of the edge that connects the component of $a$ and the component of $b$ in the Kruskal's process.
So, if we have $cntA_u$ items of $A$ in $C_u$ and $cntB_u$ items of $B$ in $C_u$, and similarly for $C_v$.
The number of pairs $(A_i, B_j)$ that are connected by this edge $e$ (i.e., $A_i \in C_u, B_j \in C_v$ OR $A_i \in C_v, B_j \in C_u$) is NOT fixed.
We can choose to match $A$'s and $B$'s within $C_u$ as much as possible to avoid paying $w$.
To minimize the sum, we want to maximize the number of pairs that are matched within components before merging.
This is a flow/matching problem at each step?
Actually, at each step, we have $cntA_u$ and $cntB_u$ in $C_u$, and $cntA_v, cntB_v$ in $C_v$.
Total $A$'s available to be matched across the cut is $cntA_u + cntA_v$. Total $B$'s is $cntB_u + cntB_v$.
We want to maximize the number of pairs $(a,b)$ such that both $a$ and $b$ are in $C_u$ or both in $C_v$.
The number of such pairs is limited by the internal counts.
Let $x$ be the number of pairs formed within $C_u$, $y$ within $C_v$.
We want to maximize $x+y$.
The number of pairs crossing the cut is $(cntA_u + cntA_v) + (cntB_u + cntB_v) - 2(x+y)$? No.
Total pairs is $K$.
Number of pairs crossing the cut = Total pairs - (pairs within $C_u$) - (pairs within $C_v$).
To minimize the cost contribution of $w$, we need to minimize the number of crossing pairs.
So we maximize pairs within $C_u$ and $C_v$.
Max pairs within $C_u$ is $\min(cntA_u, cntB_u)$.
Max pairs within $C_v$ is $\min(cntA_v, cntB_v)$.
So the number of crossing pairs is $(cntA_u + cntA_v + cntB_u + cntB_v) - 2(\min(cntA_u, cntB_u) + \min(cntA_v, cntB_v))$?
Wait, the total number of pairs is $K$.
Let $S_A = cntA_u + cntA_v$, $S_B = cntB_u + cntB_v$.
We form $k_u = \min(cntA_u, cntB_u)$ pairs in $C_u$ and $k_v = \min(cntA_v, cntB_v)$ pairs in $C_v$.
The remaining $A$'s and $B$'s must be matched across the cut.
Remaining $A$'s: $S_A - (k_u + k_v)$? No.
Remaining $A$'s in $C_u$: $cntA_u - k_u$.
Remaining $B$'s in $C_u$: $cntB_u - k_u$.
Remaining $A$'s in $C_v$: $cntA_v - k_v$.
Remaining $B$'s in $C_v$: $cntB_v - k_v$.
Total remaining $A$'s = $(cntA_u - k_u) + (cntA_v - k_v)$.
Total remaining $B$'s = $(cntB_u - k_u) + (cntB_v - k_v)$.
These remaining must be matched across the cut.
Number of crossing pairs = Remaining $A$'s (which equals Remaining $B$'s).
Let $remA = (cntA_u - k_u) + (cntA_v - k_v)$.
Then the number of pairs crossing is $remA$.
Each such pair contributes $w$ to the sum.
So the contribution of edge $e$ is $w \times remA$.
Then we merge $C_u$ and $C_v$:
New $cntA = cntA_u + cntA_v$.
New $cntB = cntB_u + cntB_v$.
This greedy strategy works!
Algorithm:
1. Build MST.
2. Sort MST edges by weight ascending.
3. Use DSU to maintain components. For each component, store $cntA$ and $cntB$.
4. Initialize $cntA[v]=1$ if $v \in A$, else 0. Similarly for $B$.
5. Total cost = 0.
6. For each edge $(u, v)$ with weight $w$ in sorted order:
   - Find roots $ru, rv$.
   - If $ru == rv$, continue.
   - Calculate $k_u = \min(cntA[ru], cntB[ru])$.
   - Calculate $k_v = \min(cntA[rv], cntB[rv])$.
   - $rem = (cntA[ru] - k_u) + (cntA[rv] - k_v)$.
   - Total cost += $w \times rem$.
   - Merge $ru$ and $rv$: $cntA[new] = cntA[ru] + cntA[rv]$, $cntB[new] = cntB[ru] + cntB[rv]$.
7. Print total cost.

Let's trace Sample 1 with this algorithm.
MST edges: (3,4,1), (1,3,2), (2,4,5).
Initial:
1: A=1, B=0
2: A=0, B=1
3: A=1, B=0
4: A=0, B=2
(A indices: 1,1,3. B indices: 4,4,2. So A={1,3}, B={2,4,4}? No.
A sequence: 1, 1, 3. So A has 1 (twice), 3 (once).
B sequence: 4, 4, 2. So B has 4 (twice), 2 (once).
Counts:
Node 1: A=2, B=0
Node 2: A=0, B=1
Node 3: A=1, B=0
Node 4: A=0, B=2

Edge 1: (3,4) w=1.
ru=3, rv=4.
k_u = min(1,0) = 0.
k_v = min(0,2) = 0.
rem = (1-0) + (0-0) = 1.
Cost += 1 * 1 = 1.
Merge 3,4. New node (3,4): A=1, B=2.

Edge 2: (1,3) w=2. (Connects 1 to {3,4})
ru=1, rv=(3,4).
k_u = min(2,0) = 0.
k_v = min(1,2) = 1.
rem = (2-0) + (1-1) = 2.
Cost += 2 * 2 = 4. Total = 5.
Merge 1, (3,4). New node (1,3,4): A=2+1=3, B=0+2=2.

Edge 3: (2,4) w=5. (Connects 2 to {1,3,4})
ru=2, rv=(1,3,4).
k_u = min(0,1) = 0.
k_v = min(3,2) = 2.
rem = (0-0) + (3-2) = 1.
Cost += 5 * 1 = 5. Total = 10.
Wait, sample output is 8. My calculation gives 10.
Where is the error?
Ah, the logic "Max pairs within $C_u$ is $\min(cntA_u, cntB_u)$" assumes we can freely choose which $A$ and $B$ to pair.
But the pairing must be consistent globally.
The greedy choice at each step (maximize internal pairs) is locally optimal but might not be globally optimal?
Actually, for the bottleneck metric, the greedy strategy of "process edges from small to large, match as many as possible internally" IS correct.
Why did I get 10?
Let's re-check the counts.
A = [1, 1, 3]. B = [4, 4, 2].
Node 1: A=2, B=0.
Node 2: A=0, B=1.
Node 3: A=1, B=0.
Node 4: A=0, B=2.
Edge (3,4) w=1.
C3: A=1, B=0. C4: A=0, B=2.
Internal matches: min(1,0)=0 in C3, min(0,2)=0 in C4.
Crossing: (1-0)+(0-0) = 1. Cost 1.
New C34: A=1, B=2.
Edge (1,3) w=2. Connects 1 (A=2, B=0) and C34 (A=1, B=2).
Internal matches: min(2,0)=0 in C1, min(1,2)=1 in C34.
Crossing: (2-0) + (1-1) = 2. Cost 2*2=4.
New C134: A=3, B=2.
Edge (2,4) w=5. Connects 2 (A=0, B=1) and C134 (A=3, B=2).
Internal matches: min(0,1)=0 in C2, min(3,2)=2 in C134.
Crossing: (0-0) + (3-2) = 1. Cost 5*1=5.
Total 1+4+5=10.

But the sample output is 8.
The optimal pairing was (1,4), (1,2), (3,4).
Costs: 2, 5, 1. Sum 8.
Let's see the edges used in the optimal pairing.
(1,4): path 1-3-4. Edges (1,3) w=2, (3,4) w=1. Max=2.
(1,2): path 1-3-4-2. Edges (1,3) w=2, (3,4) w=1, (4,2) w=5. Max=5.
(3,4): path 3-4. Edge (3,4) w=1. Max=1.
Total cost 8.
My algorithm counted:
Edge (3,4) w=1: 1 pair. (This corresponds to (3,4)).
Edge (1,3) w=2: 2 pairs. (This corresponds to (1,4) and (1,2)? No, (1,4) uses (1,3) and (3,4). (1,2) uses (1,3), (3,4), (4,2)).
Wait, the definition of $f(u,v)$ is the MAX edge on the path.
So (1,4) contributes 2. (1,2) contributes 5. (3,4) contributes 1.
My algorithm says:
(3,4) contributes 1.
(1,3) contributes 2 for 2 pairs.
(4,2) contributes 5 for 1 pair.
Total 1 + 4 + 5 = 10.
The discrepancy is that (1,4) has max edge 2, but it also uses edge (3,4) with weight 1.
My algorithm counts the cost of (3,4) for (1,4)?
No, my algorithm counts the cost of an edge $e$ for a pair if $e$ is the "bottleneck" (max weight) edge?
No, my algorithm counts the cost of an edge $e$ for a pair if the pair is separated by $e$ in the Kruskal process.
In Kruskal, when we add (3,4) w=1, we connect 3 and 4.
Pair (3,4) is separated by (3,4)? Yes. Cost 1.
Pair (1,4): 1 is not in C3 or C4. So not separated by (3,4).
Pair (1,2): 1 not in C3/C4, 2 not in C3/C4. Not separated.
When we add (1,3) w=2. Connects 1 and {3,4}.
Pair (1,4): 1 in C1, 4 in C34. Separated. Cost 2.
Pair (1,2): 1 in C1, 2 in C2. Not separated by (1,3).
When we add (4,2) w=5. Connects 2 and {1,3,4}.
Pair (1,2): 1 in C134, 2 in C2. Separated. Cost 5.
So my algorithm counts:
(3,4): 1 pair (3,4). Cost 1.
(1,3): 1 pair (1,4). Cost 2.
(4,2): 1 pair (1,2). Cost 5.
Total 1+2+5 = 8.
Why did I calculate 10 earlier?
Ah, in step 2 (Edge 1,3 w=2):
C1: A=2, B=0.
C34: A=1, B=2.
k_u = min(2,0) = 0.
k_v = min(1,2) = 1.
rem = (2-0) + (1-1) = 2.
I calculated rem=2.
But which pairs are these?
The pairs are formed by matching remaining A's and B's.
Remaining A's in C1: 2. Remaining B's in C1: 0.
Remaining A's in C34: 0 (since 1 matched with 1 of the 2 B's). Remaining B's in C34: 1.
So we have 2 A's in C1 and 1 B in C34.
We must match them.
But we only have 1 B in C34. So we can only form 1 pair crossing?
Wait, the number of crossing pairs is NOT $remA$.
The number of crossing pairs is the number of pairs $(a,b)$ such that $a \in C1, b \in C34$ OR $a \in C34, b \in C1$.
We have 2 A's in C1, 0 B's in C1.
We have 0 A's in C34 (after matching 1), 1 B in C34.
Total A's available to cross: 2 (from C1).
Total B's available to cross: 1 (from C34).
We can only form $\min(2, 1) = 1$ pair crossing?
No, the total number of pairs is $K=3$.
We formed 1 pair in C34 (internal).
We formed 0 pairs in C1 (internal).
So we have 2 pairs left to form.
The available items are: 2 A's in C1, 1 B in C34.
Wait, we have 3 A's total, 3 B's total.
Used: 1 pair (1 A, 1 B) in C34.
Remaining: 2 A's (in C1), 2 B's (1 in C1? No, C1 had 0 B's initially. C34 had 2 B's, used 1, so 1 left).
So remaining: 2 A's in C1, 1 B in C34.
Total remaining A's = 2. Total remaining B's = 1.
This is impossible. We must have equal number of remaining A's and B's.
Ah, I see.
Initial: A=3, B=3.
After step 1 (3,4):
C3: A=1, B=0. C4: A=0, B=2.
Matched: 0.
Remaining: A=3, B=3.
After step 2 (1,3):
C1: A=2, B=0. C34: A=1, B=2.
Matched in C34: min(1,2)=1.
Matched in C1: min(2,0)=0.
Total matched: 1.
Remaining A: 3-1=2. Remaining B: 3-1=2.
Where are they?
A's: 2 in C1, 0 in C34.
B's: 0 in C1, 1 in C34.
Wait, 2 A's and 1 B?
Ah, C34 had 1 A and 2 B. Matched 1 pair (1 A, 1 B).
Remaining in C34: 0 A, 1 B.
C1 had 2 A, 0 B.
Total remaining: 2 A (in C1), 1 B (in C34).
This sums to 2 A and 1 B. But we started with 3 A and 3 B, matched 1. Should be 2 A and 2 B.
Where is the missing B?
Initial B counts: Node 2 has 1 B. Node 4 has 2 B's. Total 3.
In step 1, we merged 3 and 4.
C3: A=1, B=0.
C4: A=0, B=2.
C34: A=1, B=2.
Correct.
In step 2, we merge 1 and C34.
C1: A=2, B=0.
C34: A=1, B=2.
Total A: 3. Total B: 2.
Wait, where is the B from Node 2?
Node 2 is NOT in C1 or C34 yet.
Node 2 is separate.
So the components are: C1, C34, C2.
C1: A=2, B=0.
C34: A=1, B=2.
C2: A=0, B=1.
Total A=3, B=3.
Now we process edge (1,3) which merges C1 and C34.
New C134: A=3, B=2.
C2: A=0, B=1.
Internal matches in C1: min(2,0)=0.
Internal matches in C34: min(1,2)=1.
Total internal: 1.
Remaining: 2 A's (in C134), 2 B's (1 in C134, 1 in C2).
Wait, remaining A's = 3-1=2. Remaining B's = 3-1=2.
Where are they?
A's: 2 in C134 (since C1 had 2, C34 had 1, matched 1 from C34, so 2 left in C134? No.
C1: 2 A. C34: 1 A. Total 3 A.
Matched 1 from C34. So 2 A left in C134.
B's: C1: 0. C34: 2. Total 2.
Matched 1 from C34. So 1 B left in C134.
And C2 has 1 B.
So remaining: 2 A in C134, 1 B in C134, 1 B in C2.
Crossing pairs:
We need to match the 2 A's in C134 with the 2 B's (1 in C134, 1 in C2).
The B in C134 can be matched with an A in C134? No, that would be internal.
But we already maximized internal matches in C134.
So the remaining A's in C134 MUST be matched with B's outside C134 (i.e., in C2).
Number of such pairs = min(remaining A in C134, remaining B in C2)?
No, the B in C134 is also available to be matched with A in C2? No, C2 has no A.
So the B in C134 must be matched with an A in C134? But that would be internal.
But we said we maximized internal matches.
The issue is that "maximizing internal matches" is a greedy choice that might not be valid if it forces a high cost later.
However, in this specific problem, the greedy strategy IS correct.
The error in my manual trace was assuming that the remaining items must be matched across the cut immediately.
Actually, the number of crossing pairs is determined by the global matching.
But the formula $rem = (cntA_u - k_u) + (cntA_v - k_v)$ is the number of A's that are NOT matched internally in $u$ or $v$.
These A's MUST be matched with B's that are NOT matched internally in $u$ or $v$.
The number of such B's is $(cntB_u - k_u) + (cntB_v - k_v)$.
Since total A = total B, these two sums are equal.
Let $X = (cntA_u - k_u) + (cntA_v - k_v)$.
These $X$ A's are in $u \cup v$. They must be matched with $X$ B's.
Where are the $X$ B's?
Some are in $u$, some in $v$.
If a B is in $u$, it must be matched with an A in $v$ (crossing).
If a B is in $v$, it must be matched with an A in $u$ (crossing).
So ALL $X$ pairs are crossing pairs.
So the number of crossing pairs is indeed $X$.
In my trace:
Step 2: C1 (A=2, B=0), C34 (A=1, B=2).
k_u = 0, k_v = 1.
X = (2-0) + (1-1) = 2.
So 2 pairs cross.
Cost += 2 * 2 = 4.
Step 3: C134 (A=3, B=2), C2 (A=0, B=1).
k_u = min(3,2) = 2.
k_v = min(0,1) = 0.
X = (3-2) + (0-0) = 1.
Cost += 1 * 5 = 5.
Total 1 + 4 + 5 = 10.
Still 10.
Why is the sample 8?
Maybe the MST is different?
Edges: (3,4,1), (1,3,2), (1,4,4), (2,4,5).
Kruskal:
1. (3,4) w=1.
2. (1,3) w=2.
3. (1,4) w=4? No, 1 and 4 are already connected via 1-3-4.
4. (2,4) w=5.
MST is correct.
Is it possible that the optimal matching does not correspond to the greedy strategy?
Wait, the sample output explanation says:
f(1,2)=5, f(1,4)=2, f(3,4)=1. Sum 8.
My algorithm gives 10.
The difference is 2.
Where did I overcount?
In step 2, I counted 2 pairs crossing (1,3).
The pairs are (1,4) and (1,2)?
(1,4) uses (1,3). Cost 2.
(1,2) uses (1,3), (3,4), (4,2). Max is 5.
So (1,2) should NOT contribute 2 to the cost of (1,3).
The cost of (1,2) is 5, which is accounted for in step 3.
But my algorithm added 2 for (1,3) for the pair (1,2).
Why? Because in step 2, 1 and 2 were in different components (C1 and C2).
Wait, in step 2, we merged C1 and C34. C2 was separate.
The pairs crossing the cut (C1, C34) are pairs with one endpoint in C1 and one in C34.
(1,4): 1 in C1, 4 in C34. Crosses.
(1,2): 1 in C1, 2 in C2. Does NOT cross (C1, C34).
So why did my formula count (1,2)?
Because I calculated $X = (cntA_u - k_u) + (cntA_v - k_v)$.
This $X$ is the number of A's in $u \cup v$ that are not matched internally.
These A's must be matched with B's in $u \cup v$ that are not matched internally.
But the B's not matched internally could be in C2?
No, C2 is not part of the merge.
The merge is only between C1 and C34.
The B's not matched internally in C1 or C34 are:
In C1: 0.
In C34: 1 (since 2 B's, 1 matched).
So there is 1 B in C134 not matched.
And there are 2 A's in C134 not matched.
Wait, 2 A's and 1 B?
Ah, the B from C2 is not in C134.
So the 2 A's in C134 must be matched with B's.
One B is in C134 (internal to C134? No, not matched yet).
One B is in C2.
So we can match 1 A (from C134) with 1 B (from C134) -> Internal to C134.
And 1 A (from C134) with 1 B (from C2) -> Crossing (C134, C2).
But the edge (1,3) only connects C1 and C34. It does not connect to C2.
So the pair (A in C134, B in C2) does NOT cross the cut (C1, C34).
It crosses the cut (C134, C2) later.
So my formula $X$ is wrong because it assumes all unmatched A's must cross the current cut.
They only need to cross the current cut if the B they are matched with is on the other side of the cut.
But we don't know which B they are matched with.
However, we can choose to match them with B's on the same side to avoid crossing.
So we should maximize the number of pairs that stay on the same side.
This means we should match the unmatched A's with the unmatched B's on the same side as much as possible.
In C134, we have 2 unmatched A's and 1 unmatched B.
We can match 1 pair internally (A from C1, B from C34).
This leaves 1 unmatched A.
This A must be matched with the B in C2 later.
So the number of pairs crossing (C1, C34) is NOT 2.
It is the number of pairs that MUST cross.
Since we can choose the matching, we can minimize the crossing.
The minimum crossing is $\max(0, |A_{unmatched}| - |B_{unmatched\_same\_side}|)$?
Actually, the number of crossing pairs is $\max(0, cntA_u - cntB_u) + \max(0, cntA_v - cntB_v)$?
No.
Let's use the property: The number of pairs crossing the cut is $\max(0, (cntA_u - cntB_u) + (cntA_v - cntB_v))$? No.
The correct formula for the minimum number of pairs crossing a cut in a bipartite matching where we can choose the matching is:
Let $diff_u = cntA_u - cntB_u$.
Let $diff_v = cntA_v - cntB_v$.
Total diff = $diff_u + diff_v$.
The number of pairs crossing is $\max(0, diff_u + diff_v)$? No.
Actually, the number of pairs crossing is $\max(0, cntA_u - cntB_u) + \max(0, cntB_u - cntA_u)$? No.
The number of pairs crossing is $\max(0, (cntA_u - cntB_u) + (cntA_v - cntB_v))$?
Let's try:
C1: A=2, B=0. diff = 2.
C34: A=1, B=2. diff = -1.
Total diff = 1.
Crossing pairs = 1?
If crossing is 1, cost = 2 * 1 = 2.
Total cost = 1 + 2 + 5 = 8.
This matches!
So the formula is: $cross = \max(0, (cntA_u - cntB_u) + (cntA_v - cntB_v))$.
Wait, is it always $\max(0, \dots)$?
Actually, the number of crossing pairs is $\max(0, cntA_u - cntB_u) + \max(0, cntA_v - cntB_v)$?
C1: max(0, 2) = 2.
C34: max(0, -1) = 0.
Sum = 2.
This gives 2.
But we found 1 is possible.
The correct formula is: The number of pairs crossing is $\max(0, (cntA_u - cntB_u) + (cntA_v - cntB_v))$?
No, that would be 1.
Let's think.
We have $A_u, B_u$ in $u$, $A_v, B_v$ in $v$.
We want to match as many as possible within $u$ and within $v$.
Max within $u$: $m_u = \min(A_u, B_u)$.
Max within $v$: $m_v = \min(A_v, B_v)$.
Remaining $A$: $A_u - m_u + A_v - m_v$.
Remaining $B$: $B_u - m_u + B_v - m_v$.
These remaining must be matched across the cut?
No, they can be matched within $u$ if there are $B$'s left?
No, $m_u$ is the max possible within $u$.
So all remaining $A$'s in $u$ must be matched with $B$'s outside $u$.
Similarly for $v$.
So the number of pairs crossing is $(A_u - m_u) + (A_v - m_v)$.
In our case:
C1: $A=2, B=0, m=0$. Rem A = 2.
C34: $A=1, B=2, m=1$. Rem A = 0.
Total Rem A = 2.
So crossing = 2.
But we know we can do 1.
Why? Because the remaining B in C34 (1 B) can be matched with one of the remaining A's in C1.
This pair is crossing (C1, C34).
The other remaining A in C1 must be matched with the B in C2.
But the B in C2 is not in C34.
So the pair (A in C1, B in C2) does NOT cross (C1, C34).
So the number of pairs crossing (C1, C34) is the number of pairs $(a,b)$ such that $a \in C1, b \in C34$ or $a \in C34, b \in C1$.
We have 2 A's in C1, 0 B's in C1.
We have 0 A's in C34 (after matching 1), 1 B in C34.
We can match 1 A (from C1) with 1 B (from C34). This is 1 crossing pair.
The other A (from C1) must be matched with the B in C2. This is NOT a crossing pair for (C1, C34).
So the number of crossing pairs is $\min(remA_u, remB_v) + \min(remA_v, remB_u)$?
remA_u = 2, remB_v = 1. min = 1.
remA_v = 0, remB_u = 0. min = 0.
Total = 1.
Yes!
So the algorithm is:
1. Build MST.
2. Sort edges by weight.
3. DSU with $cntA, cntB$.
4. For each edge $(u,v)$ w:
   - $ru, rv$.
   - $remA_u = cntA[ru] - \min(cntA[ru], cntB[ru])$.
   - $remB_u = cntB[ru] - \min(cntA[ru], cntB[ru])$.
   - $remA_v = cntA[rv] - \min(cntA[rv], cntB[rv])$.
   - $remB_v = cntB[rv] - \min(cntA[rv], cntB[rv])$.
   - $cross = \min(remA_u, remB_v) + \min(remA_v, remB_u)$.
   - $cost += w * cross$.
   - Merge.

This should work.