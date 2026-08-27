1. **Construct the Maximum Spanning Tree (MST)**: Since we want to minimize the maximum edge weight on the path, we can use the MST. However, note that the "bottleneck" path is minimized when we consider the Minimum Spanning Tree for the standard definition where path weight is max edge. Wait, let's re-verify. If we want to minimize the *maximum* edge weight on the path, this is equivalent to finding the path in the Minimum Spanning Tree? No.
   Let's clarify: The value $f(x, y)$ is the minimum over all paths of the maximum edge weight in the path. This is known as the minimax path problem. It is a well-known result that the minimax path between any two nodes in a graph is contained in the **Minimum Spanning Tree (MST)** of the graph. So, we should build the MST using Kruskal's or Prim's algorithm with standard edge weights (minimizing the sum, which also minimizes the bottleneck).
   
2. **Compute Distances in MST**: Once we have the MST, the value $f(x, y)$ is simply the maximum edge weight on the unique path between $x$ and $y$ in the MST. We can precompute these values efficiently. Since $N$ and $K$ are up to $2 \times 10^5$, we cannot compute all pairs. However, we only need the distances between specific pairs $(A_i, B_j)$.
   
3. **Formulate as Minimum Weight Perfect Matching**: We have $K$ vertices from set $A$ and $K$ vertices from set $B$. We need to pair each $A_i$ with a unique $B_j$ to minimize the sum of $f(A_i, B_j)$. This is a minimum weight perfect matching problem in a bipartite graph. However, $K$ can be up to $2 \times 10^5$, so general matching algorithms are too slow ($O(K^3)$ or even $O(K^2 \log K)$ might be too slow if the cost matrix is dense).
   
   Wait, is there a special structure? The cost $f(A_i, B_j)$ is the bottleneck distance in the MST. This doesn't immediately suggest a greedy strategy like sorting. However, note that the number of distinct edge weights in the MST is at most $N-1$. 
   
   Actually, let's look at the constraints again. $K \le N$. The bipartite matching with $K$ up to $2 \cdot 10^5$ is generally hard. But is the cost matrix special?
   
   Let's reconsider the problem. Is it possible that we can solve this greedily or with a simpler method?
   Consider the edges of the MST sorted by weight. The value $f(u, v)$ is the smallest $W$ such that $u$ and $v$ are connected in the subgraph of the MST containing only edges with weight $\le W$.
   
   This problem can be modeled as a minimum weight perfect matching in a bipartite graph where the cost is the bottleneck distance. Unfortunately, general minimum weight perfect matching is too slow.
   
   However, there is a known technique for this specific "bottleneck" assignment problem. We can use a **binary search on the answer** combined with a feasibility check, or more directly, we can use the structure of the MST.
   
   Actually, a simpler observation: The function $f(u, v)$ is the weight of the heaviest edge on the path in the MST.
   
   Let's try a different approach. Since $K$ is large, we need an efficient way to compute the matching.
   Is it possible that the optimal matching can be found by sorting? No, counter-examples exist.
   
   Let's look at similar problems. This is equivalent to the "Minimum Weight Perfect Matching in a Bipartite Graph with Bottleneck Costs".
   
   Wait, there is a specialized algorithm for this. We can use the **Hungarian algorithm** if $K$ is small, but $K$ is up to $2 \cdot 10^5$.
   
   Let's re-read carefully. "Permute B freely".
   
   Actually, there is a key property: The bottleneck distance satisfies the ultrametric inequality? No, it satisfies the triangle inequality for the bottleneck metric: $f(u, w) \le \max(f(u, v), f(v, w))$. This makes it an ultrametric if we define $d(u,v) = f(u,v)$. In an ultrametric space, the minimum weight perfect matching can be found greedily?
   
   In an ultrametric, the minimum weight perfect matching is not necessarily trivial, but the structure is hierarchical. We can use the **MST of the complete graph** on the $2K$ vertices? No.
   
   Let's use the property of the MST of the original graph. The values $f(A_i, B_j)$ are determined by the edges in the MST.
   
   Alternative Idea:
   Since $N, M, K \le 2 \cdot 10^5$, we need an $O(N \log N)$ or $O(N \log^2 N)$ solution.
   
   We can compute the "bottleneck distance" between all $A_i$ and $B_j$? No, that's $K^2$.
   
   However, we can process the edges of the MST in increasing order of weight. This builds a Union-Find structure. As we add edges, components merge.
   
   We can view this as a flow problem or matching problem on the tree.
   
   Actually, there is a known result: The minimum weight perfect matching in a bipartite graph where costs are ultrametric distances can be solved by a greedy strategy based on the hierarchical clustering (which is essentially the MST).
   
   Algorithm:
   1. Build the MST of the graph.
   2. Root the MST arbitrarily.
   3. The cost $f(u, v)$ is the weight of the LCA edge? No, it's the max edge on the path.
   
   Let's use the **Kruskal's reconstruction tree** (or just process MST edges from smallest to largest).
   We maintain a DSU structure. Initially, each node is a component.
   We also track the count of "A-nodes" and "B-nodes" in each component.
   
   When we merge two components with an edge of weight $w$, any pair $(a, b)$ with $a$ in one component and $b$ in the other will have $f(a, b) = w$ (assuming this is the first time they are connected, which is true for MST edges processed in increasing order).
   
   We want to minimize the total weight. This looks like we should match as many pairs as possible with smaller weights.
   
   This is equivalent to:
   Iterate through MST edges from smallest to largest weight $w$.
   Let the two components being merged be $C_1$ and $C_2$.
   Let $a_1, b_1$ be the number of A-nodes and B-nodes in $C_1$.
   Let $a_2, b_2$ be the number of A-nodes and B-nodes in $C_2$.
   
   We can form $\min(a_1, b_2)$ pairs between $A \in C_1$ and $B \in C_2$ with cost $w$.
   We can form $\min(a_2, b_1)$ pairs between $A \in C_2$ and $B \in C_1$ with cost $w$.
   
   Wait, is it optimal to match them immediately?
   Yes, because any pair matched within a component will have a cost $\le w$ (if matched earlier) or $> w$ (if matched later). But since we process from small to large, we want to match as many as possible with the current small weight $w$.
   
   Specifically, the number of pairs that *must* have cost $> w$ is determined by the imbalance of A and B nodes in the combined component.
   The number of pairs that can be formed with cost $\le w$ is limited by the total number of A and B nodes.
   
   Let's refine the greedy strategy:
   Total pairs = $K$.
   We process MST edges in increasing order of weight.
   For each edge connecting components $C_1$ and $C_2$ with weight $w$:
   - Calculate how many A-B pairs can be formed between $C_1$ and $C_2$.
   - The maximum number of pairs we can form with cost exactly $w$ (or less, but since they weren't connected before, it's exactly $w$ for these cross-component pairs) is $\min(a_1, b_2) + \min(a_2, b_1)$.
   - However, we must be careful. We want to minimize the sum. Matching now costs $w$. Matching later costs $> w$. So we should match as many as possible now.
   
   So, we add $\min(a_1, b_2) \times w$ and $\min(a_2, b_1) \times w$ to the answer.
   Then we update the counts for the new merged component:
   $a_{new} = a_1 + a_2$
   $b_{new} = b_1 + b_2$
   
   Is this correct?
   Let's trace Sample 1.
   MST Edges (sorted):
   1. (3,4) w=1. Components: {3}, {4}. A={1,1,3}, B={4,4,2}.
      Nodes: 1(A), 1(A), 3(A), 4(B), 4(B), 2(B).
      Initially:
      Comp 1: {1} -> a=2, b=0
      Comp 2: {2} -> a=0, b=1
      Comp 3: {3} -> a=1, b=0
      Comp 4: {4} -> a=0, b=2
      
      Edge (3,4) w=1: Merge Comp 3 and Comp 4.
      $a_1=1, b_1=0$ (Comp 3). $a_2=0, b_2=2$ (Comp 4).
      Pairs: $\min(1, 2) + \min(0, 0) = 1$.
      Add $1 \times 1 = 1$ to answer.
      New Comp {3,4}: a=1, b=2.
      
   2. Next edge (1,3) w=2. Merge Comp 1 ({1}) and Comp {3,4}.
      Comp 1: a=2, b=0.
      Comp {3,4}: a=1, b=2.
      Pairs: $\min(2, 2) + \min(1, 0) = 2$.
      Add $2 \times 2 = 4$ to answer.
      New Comp {1,3,4}: a=3, b=2.
      
   3. Next edge (1,4) w=4. Already connected? No, in MST, we skip edges that connect already connected components.
      The MST edges are (3,4), (1,3), (1,4) is not in MST if (1,3) and (3,4) connect 1,3,4.
      Wait, let's build MST properly.
      Edges: (3,4,1), (1,3,2), (1,4,4), (2,4,5).
      Sorted: 1, 2, 4, 5.
      1. Add (3,4). Sets: {3,4}, {1}, {2}.
      2. Add (1,3). Sets: {1,3,4}, {2}.
      3. Add (1,4). 1 and 4 are connected. Skip.
      4. Add (2,4). Sets: {1,2,3,4}.
      
      So next MST edge is (2,4) w=5.
      Merge Comp {2} and Comp {1,3,4}.
      Comp {2}: a=0, b=1.
      Comp {1,3,4}: a=3, b=2.
      Pairs: $\min(0, 2) + \min(3, 1) = 1$.
      Add $1 \times 5 = 5$ to answer.
      
      Total Answer: $1 + 4 + 5 = 10$.
      But Sample Output is 8.
      
      Where is the error?
      The error is in the assumption that we *must* match cross-component pairs immediately.
      In step 2, we matched 2 pairs with cost 2.
      The pairs were between A in {1} and B in {3,4}.
      A in {1}: {1, 1}. B in {3,4}: {4, 4}.
      Pairs: (1,4) and (1,4). Cost 2 each. Sum 4.
      
      In step 1, we matched 1 pair with cost 1.
      A in {3}: {3}. B in {4}: {4, 4}.
      Pair: (3,4). Cost 1.
      
      In step 3, we matched 1 pair with cost 5.
      A in {1,3,4}: remaining A?
      Let's track remaining nodes.
      Initially:
      A: {1, 1, 3} (vertices 1, 1, 3)
      B: {4, 4, 2} (vertices 4, 4, 2)
      
      Step 1 (w=1): Merge {3} and {4}.
      A in {3}: {3}. B in {4}: {4, 4}.
      We matched (3, 4). One B (4) remains in {3,4}.
      Remaining in {3,4}: A: {}, B: {4}.
      
      Step 2 (w=2): Merge {1} and {3,4}.
      A in {1}: {1, 1}. B in {3,4}: {4}.
      We matched (1, 4) and (1, 4)? No, only 1 B available.
      So we match 1 pair: (1, 4). Cost 2.
      Remaining in {1,3,4}: A: {1}, B: {}.
      
      Step 3 (w=5): Merge {2} and {1,3,4}.
      A in {2}: {}. B in {2}: {2}.
      A in {1,3,4}: {1}. B in {1,3,4}: {}.
      Match (1, 2). Cost 5.
      
      Total: $1 + 2 + 5 = 8$.
      
      My previous calculation failed because I didn't account for *remaining* nodes. The formula $\min(a_1, b_2) + \min(a_2, b_1)$ assumes we match *all possible* cross pairs. But we should only match as many as needed? No, we want to minimize sum, so we match as many as possible with small weights.
      
      The correct logic:
      At each merge, we form as many pairs as possible between the two components.
      Number of pairs formed = $\min(a_1, b_2) + \min(a_2, b_1)$.
      BUT, we must ensure we don't "use up" nodes that could be matched more cheaply? No, because this is the *cheapest* way to connect these specific sets of nodes. Any pair not formed here will be formed later with higher cost.
      
      So why did my manual trace give 10?
      In Step 2, I calculated pairs = 2.
      $a_1=2, b_1=0$. $a_2=1, b_2=2$.
      $\min(2, 2) + \min(1, 0) = 2$.
      This implies we match 2 pairs.
      But there is only 1 B in Comp 2 ({3,4} had 1 B left? No, initially {3,4} had 2 Bs. We used 1. So 1 left).
      And 2 As in Comp 1.
      So we can match 1 pair (since only 1 B).
      $\min(2, 1) + \min(1, 0) = 1$.
      
      Ah, the counts $a$ and $b$ must represent the **remaining unmatched** A and B nodes in the component.
      
      Correct Algorithm:
      1. Build MST.
      2. Initialize DSU. For each node $i$, if $i \in A$, $a_i=1, b_i=0$. If $i \in B$, $a_i=0, b_i=1$. Else 0,0.
      3. Sort MST edges by weight.
      4. For each edge $(u, v)$ with weight $w$:
         Find roots $r_u, r_v$.
         If $r_u \neq r_v$:
           $pairs = \min(a_{r_u}, b_{r_v}) + \min(a_{r_v}, b_{r_u})$
           $ans += pairs \times w$
           $a_{new} = a_{r_u} + a_{r_v} - pairs$ ? No.
           
           Let's trace the flow of nodes.
           We match $k_1 = \min(a_{r_u}, b_{r_v})$ pairs between $A_{r_u}$ and $B_{r_v}$.
           We match $k_2 = \min(a_{r_v}, b_{r_u})$ pairs between $A_{r_v}$ and $B_{r_u}$.
           
           Remaining $A$ in $r_u$: $a_{r_u} - k_1 - k_2$? No.
           The $A$ nodes in $r_u$ are matched with $B$ nodes in $r_v$.
           The $A$ nodes in $r_v$ are matched with $B$ nodes in $r_u$.
           
           So, remaining $A$ in merged component:
           $a_{rem} = (a_{r_u} - k_1) + (a_{r_v} - k_2)$?
           Wait, $k_1$ uses $A$ from $r_u$ and $B$ from $r_v$.
           $k_2$ uses $A$ from $r_v$ and $B$ from $r_u$.
           
           So remaining $A$ in $r_u$ part: $a_{r_u} - k_1$.
           Remaining $A$ in $r_v$ part: $a_{r_v} - k_2$.
           Total remaining $A$: $(a_{r_u} - k_1) + (a_{r_v} - k_2)$.
           
           Similarly for B:
           Remaining $B$ in $r_u$ part: $b_{r_u} - k_2$.
           Remaining $B$ in $r_v$ part: $b_{r_v} - k_1$.
           Total remaining $B$: $(b_{r_u} - k_2) + (b_{r_v} - k_1)$.
           
           Let's re-verify with Sample 1.
           Init:
           1: A=2, B=0
           2: A=0, B=1
           3: A=1, B=0
           4: A=0, B=2
           
           Edge (3,4) w=1:
           $r_3: A=1, B=0$. $r_4: A=0, B=2$.
           $k_1 = \min(1, 2) = 1$. (A from 3, B from 4)
           $k_2 = \min(0, 0) = 0$.
           Ans += 1*1 = 1.
           Rem A: $(1-1) + (0-0) = 0$.
           Rem B: $(0-0) + (2-1) = 1$.
           New Comp {3,4}: A=0, B=1.
           
           Edge (1,3) w=2:
           $r_1: A=2, B=0$. $r_{34}: A=0, B=1$.
           $k_1 = \min(2, 1) = 1$. (A from 1, B from 34)
           $k_2 = \min(0, 0) = 0$.
           Ans += 1*2 = 2. Total 3.
           Rem A: $(2-1) + (0-0) = 1$.
           Rem B: $(0-0) + (1-1) = 0$.
           New Comp {1,3,4}: A=1, B=0.
           
           Edge (2,4) w=5:
           $r_2: A=0, B=1$. $r_{134}: A=1, B=0$.
           $k_1 = \min(0, 0) = 0$.
           $k_2 = \min(1, 1) = 1$. (A from 134, B from 2)
           Ans += 1*5 = 5. Total 8.
           Rem A: $(0-0) + (1-1) = 0$.
           Rem B: $(1-1) + (0-0) = 0$.
           
           Result 8. Correct.