The problem asks us to minimize the sum of bottleneck distances $f(A_i, B_i)$ by optimally permuting the sequence $B$. The value $f(u, v)$ represents the minimum maximum edge weight on a path between $u$ and $v$, which is equivalent to the distance in the Minimum Spanning Tree (MST) of the graph. Since $f(u, v)$ depends only on the MST, we first construct the MST. The problem then reduces to matching two sets of vertices ($A$ and $B$) to minimize the sum of their distances in the MST. We can solve this by sorting both sequences based on their distances from an arbitrary root in the MST (or more simply, by sorting the values $f(A_i, \text{root})$ and $f(B_i, \text{root})$ if the metric was additive, but here it's not). However, a more robust approach for general bottleneck matching on a tree involves sorting the queries. Actually, since the cost function $f(u,v)$ is the path max edge, and we want to minimize $\sum f(A_i, B_{\pi(i)})$, we can observe that if we sort the array $A$ and array $B$ based on some property related to their positions in the MST, the optimal matching is often between corresponding sorted elements. Specifically, if we consider the edges of the MST in increasing order of weight, we can use a greedy strategy or simply sort both $A$ and $B$ by their "depth" or distance from a root? No, bottleneck distance isn't additive. 
Correct approach: The optimal strategy for minimizing $\sum f(A_i, B_{\pi(i)})$ on a tree is to sort both sequences $A$ and $B$ based on their distance from an arbitrary root? No, that doesn't work for bottleneck. 
Let's reconsider. $f(u,v)$ is the weight of the highest edge on the unique path in the MST. This is equivalent to: $f(u,v) \le W$ if and only if $u$ and $v$ are in the same connected component when considering only edges with weight $\le W$. 
We can iterate through the edges of the MST in increasing order of weight. As we add edges, components merge. For a specific weight $W$, let $S_W$ be the set of pairs $(A_i, B_j)$ such that $f(A_i, B_j) \le W$. We want to maximize the number of pairs matched with cost $\le W$, then $\le W'$, etc. This is a maximum matching problem in a dynamic graph.
However, there is a simpler observation: The function $f(u,v)$ is the distance in the MST. The problem is to find a permutation $\pi$ minimizing $\sum d_{bottleneck}(A_i, B_{\pi(i)})$. 
Actually, the optimal strategy is to sort both $A$ and $B$ based on their distance from an arbitrary root? No. 
Let's look at the structure. If we root the MST at vertex 1, $f(u,v)$ is not simply $|depth(u) - depth(v)|$. 
Wait, there is a known result: To minimize $\sum f(A_i, B_{\pi(i)})$, we should sort $A$ and $B$ based on the value $f(A_i, \text{root})$? No. 
Let's try a different angle. Consider the edges of the MST sorted by weight. We can use a Disjoint Set Union (DSU) to maintain components. We process edges from smallest to largest. When an edge $(u, v)$ with weight $w$ is added, $u$ and $v$ merge into a component. Any $A_i$ in the component of $u$ and any $B_j$ in the component of $v$ (and vice versa) now have a path with max weight $\le w$. 
Actually, the optimal matching is achieved by sorting $A$ and $B$ based on their "potential" to be connected. 
Let's re-evaluate the sample. 
Sample 1: MST edges: (3,4,1), (1,3,2), (1,4,4) [Wait, 1-4 is 4, 2-4 is 5. Path 1-2 via 4 is 5. Path 1-2 via 3 is 1-3(2)-4(1)-2(5) -> max 5. Direct 1-4 is 4. So 1-2 is 5. Correct. MST edges: (3,4,1), (1,3,2), (1,4,4) is not MST because 1-4(4) connects 1 to {3,4}. 2-4(5) connects 2. So MST edges are (3,4,1), (1,3,2), (2,4,5). 
Distances: 
A = {1, 1, 3}, B = {4, 4, 2}.
Pairs:
(1,4): path 1-3-4, max(2,1)=2.
(1,4): same, 2.
(3,2): path 3-4-2, max(1,5)=5.
Sum = 2+2+5 = 9.
Sample output says 8 with B permuted to (2, 4, 4).
Pairs: (1,2)->5, (1,4)->2, (3,4)->1. Sum=8.
So we matched A[1]=1 with B[perm]=2 (cost 5), A[2]=1 with B[perm]=4 (cost 2), A[3]=3 with B[perm]=4 (cost 1).
Notice that 1 is connected to 4 with cost 2. 3 is connected to 4 with cost 1. 1 is connected to 2 with cost 5.
The key is that we want to match "close" nodes together. 
Is it true that if we sort $A$ and $B$ by their distance from some root, the sum is minimized? 
Let's try sorting by distance from node 1 in MST.
MST: 2-5-4-1-2-3 (weights 5,1,2). 
Dist from 1:
1: 0
3: 2
4: 2 (path 1-3-4, max 2)
2: 5 (path 1-3-4-2, max 5)
A = {1, 1, 3} -> dists: {0, 0, 2}. Sorted: 0, 0, 2.
B = {4, 4, 2} -> dists: {2, 2, 5}. Sorted: 2, 2, 5.
Sum of sorted pairs: 0+2 + 0+2 + 2+5 = 2+2+7 = 11. Not 8.
So simple distance sorting doesn't work.

Alternative approach: 
The cost $f(u,v)$ is the weight of the edge that connects the component containing $u$ and the component containing $v$ in the Kruskal's process (when considering edges in increasing order).
Actually, the problem is equivalent to: We have a set of points $A$ and $B$. We want to pair them up. The cost of a pair $(u,v)$ is the weight of the edge that merges the component of $u$ and the component of $v$ in the MST construction.
This looks like we can solve it greedily. 
Sort all edges of the MST by weight. Iterate from smallest to largest.
Maintain the count of unmatched $A$'s and $B$'s in each component.
When an edge $(u, v)$ with weight $w$ merges component $C_u$ and $C_v$:
Any unmatched $A$ in $C_u$ can be matched with any unmatched $B$ in $C_v$ (and vice versa) with cost $w$.
To minimize the total cost, we should greedily match as many pairs as possible using the current edge weight $w$.
Specifically, let $cntA(C)$ be the number of unmatched $A$'s in component $C$, and $cntB(C)$ be the number of unmatched $B$'s.
When merging $C_u$ and $C_v$ with weight $w$:
New $cntA = cntA(C_u) + cntA(C_v)$.
New $cntB = cntB(C_u) + cntB(C_v)$.
The number of pairs we can form with cost $w$ is $\min(cntA(C_u), cntB(C_v)) + \min(cntA(C_v), cntB(C_u))$.
Wait, is it that simple?
Suppose $C_u$ has 2 A's and 0 B's. $C_v$ has 0 A's and 2 B's. We can match 2 pairs with cost $w$.
Suppose $C_u$ has 2 A's and 1 B. $C_v$ has 1 A and 2 B's.
We can match $A(C_u)$ with $B(C_v)$ -> 1 pair.
We can match $A(C_v)$ with $B(C_u)$ -> 1 pair.
Total 2 pairs with cost $w$.
Remaining: $A(C_u)$ has 1, $B(C_u)$ has 0. $A(C_v)$ has 0, $B(C_v)$ has 1.
These remain for larger edges.
Yes, this greedy strategy works because any pair formed later will have a cost $\ge w$. By forming as many pairs as possible now, we minimize the contribution of higher weights.
This is a standard technique for bottleneck matching on trees (or graphs).