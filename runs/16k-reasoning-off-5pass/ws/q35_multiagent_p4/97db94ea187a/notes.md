
## ideation
The core difficulty lies in correctly characterizing the set of graphs where the BFS layers from vertex 1 are exactly a specific partition $(S, T)$ with $1 \in S$, $|S|=|T|=N/2$, and then summing over all such partitions while ensuring the graph is connected and has exactly $M$ edges.

Key observations:
1. **BFS Layer Constraints**: For the shortest distance parity to match the partition $(S, T)$:
   - Vertex 1 is at distance 0 (even).
   - Vertices in $T$ must be at odd distances (1, 3, ...).
   - Vertices in $S \setminus \{1\}$ must be at even distances (2, 4, ...).
   
   This implies:
   - There must be at least one edge between 1 and $T$ (so vertices in $T$ are reachable at distance 1).
   - There must be at least one edge between $T$ and $S \setminus \{1\}$ (so vertices in $S \setminus \{1\}$ are reachable at distance 2).
   - No edge can exist between 1 and $S \setminus \{1\}$ (otherwise those vertices would be at distance 1, contradicting they are in $S$).
   - Edges within $S$ and within $T$ are allowed, but they must not create shorter paths that would change the BFS layering. However, since we only care about parity, and the minimal distances are constrained by the bipartite-like structure between layers, the critical constraints are:
     - No edge between 1 and $S \setminus \{1\}$.
     - The subgraph induced by $S \cup T$ must be connected.
     - The BFS tree must reach all vertices. Specifically, every vertex in $T$ must be adjacent to some vertex in $S$ at a distance one less (which is 1 for the first layer of $T$), and every vertex in $S \setminus \{1\}$ must be adjacent to some vertex in $T$ at a distance one less.

2. **Simplification via Inclusion-Exclusion**:
   Instead of directly enforcing the exact BFS layering, we can use the following approach:
   - Iterate over all subsets $S$ containing 1 with $|S| = N/2$. Let $T = V \setminus S$.
   - For a fixed partition $(S, T)$, count the number of connected graphs with $M$ edges such that:
     - No edge exists between 1 and $S \setminus \{1\}$.
     - The graph is connected.
     - Every vertex in $T$ has at least one neighbor in $S$ (to ensure distance from 1 is odd, specifically 1 if we consider the first layer, but actually we need to ensure the shortest path parity is correct. The condition "shortest distance is odd" for $v \in T$ means the shortest path from 1 to $v$ has odd length. Since 1 is in $S$, any path from 1 to $v \in T$ must have odd length. The shortest such path will be odd. Similarly for $S \setminus \{1\}$, paths from 1 must have even length.
     - The key constraint is: **No edge between 1 and $S \setminus \{1\}$**. This ensures that vertices in $S \setminus \{1\}$ are not at distance 1. They must be reached via $T$, so distance $\ge 2$ (even). Vertices in $T$ are adjacent to 1 (directly or via other nodes in $T$? No, if a vertex in $T$ is not adjacent to 1, its distance is at least 2, which is even, contradicting it's in $T$. So every vertex in $T$ must have a neighbor in $S$? Not necessarily 1. But if a vertex in $T$ has no neighbor in $S$, it's disconnected from 1. So connectivity + no edge 1 to $S \setminus \{1\}$ implies:
       - All vertices in $T$ must be connected to $S$.
       - All vertices in $S \setminus \{1\}$ must be connected to $T$.
   
   Actually, a simpler characterization:
   The condition "number of vertices at even distance = number at odd distance" with $1 \in \text{Even}$ is equivalent to:
   - The set of even-distance vertices is exactly $S$ (with $1 \in S, |S|=N/2$).
   - The set of odd-distance vertices is exactly $T$.
   
   This requires:
   1. No edge between 1 and $S \setminus \{1\}$.
   2. The graph is connected.
   3. Every vertex in $T$ has a neighbor in $S$ (specifically, the shortest path to any $v \in T$ must be odd, so it must come from an even-distance node. Since 1 is the only even-distance node at distance 0, and others in $S$ are at distance $\ge 2$, the first step from 1 must go to $T$. Then from $T$ to $S \setminus \{1\}$. So we need:
      - At least one edge between 1 and $T$.
      - At least one edge between $T$ and $S \setminus \{1\}$.
      - No edge between 1 and $S \setminus \{1\}$.
   
   However, this is not sufficient. We need to ensure that no vertex in $T$ is reached via a path of even length (which would make its shortest distance even). This is guaranteed if there are no edges within $T$ that create a shortcut? No.
   
   Let's use the standard technique for counting graphs with specific BFS properties:
   For a fixed partition $(S, T)$ with $1 \in S, |S|=N/2$:
   - Allowed edges:
     - Between 1 and $T$: allowed.
     - Between $T$ and $S \setminus \{1\}$: allowed.
     - Within $T$: allowed.
     - Within $S \setminus \{1\}$: allowed.
     - Between 1 and $S \setminus \{1\}$: **forbidden**.
   - Disallowed edges:
     - Any edge between 1 and $S \setminus \{1\}$.
   
   But we also need to ensure that the BFS layers are exactly $S$ and $T$. This means:
   - Every vertex in $T$ must have a neighbor in $S$ (to be reachable at odd distance).
   - Every vertex in $S \setminus \{1\}$ must have a neighbor in $T$ (to be reachable at even distance $\ge 2$).
   - Vertex 1 must have a neighbor in $T$ (to start the BFS).
   
   If these conditions are met, and no edge exists between 1 and $S \setminus \{1\}$, then:
   - Distance to 1 is 0 (even).
   - Distance to any $v \in T$ is odd (since it's connected to $S$, and the path from 1 to $S \setminus \{1\}$ is even, so 1 to $T$ is 1, then $T$ to $S \setminus \{1\}$ is 2, etc.).
   - Distance to any $v \in S \setminus \{1\}$ is even.
   
   So the problem reduces to:
   For each partition $(S, T)$ with $1 \in S, |S|=N/2$:
   - Count connected graphs with $M$ edges such that:
     - No edge between 1 and $S \setminus \{1\}$.
     - Every vertex in $T$ has at least one neighbor in $S$.
     - Every vertex in $S \setminus \{1\}$ has at least one neighbor in $T$.
     - Vertex 1 has at least one neighbor in $T$.
   
   Note: The "connected" condition is implied by the neighbor conditions? Not necessarily. We need the entire graph to be connected. However, if every vertex in $T$ is connected to $S$ and every vertex in $S \setminus \{1\}$ is connected to $T$, and 1 is connected to $T$, then the graph is connected.
   
   So we can count:
   - Total graphs with $M$ edges, no edge between 1 and $S \setminus \{1\}$, satisfying the "at least one neighbor" conditions.
   
   Let $E_{allowed}$ be the set of allowed edges.
   Let $A$ be the property that 1 has a neighbor in $T$.
   Let $B_v$ be the property that $v \in T$ has a neighbor in $S$.
   Let $C_v$ be the property that $v \in S \setminus \{1\}$ has a neighbor in $T$.
   
   We need to count graphs with $M$ edges in $E_{allowed}$ that satisfy $A$ and all $B_v, C_v$.
   
   This can be done using inclusion-exclusion on the properties $A, B_v, C_v$.
   
   Since $N \le 30$, $|S| = 15$, $|T| = 15$. The number of subsets is $\binom{29}{14}$, which is large ($\approx 77 \times 10^6$). We cannot iterate over all subsets.
   
   Alternative approach:
   Use generating functions or DP.
   
   Let's reconsider the structure. The condition is symmetric for all partitions.
   The number of valid partitions is $\binom{N-1}{N/2 - 1}$.
   
   For a fixed partition, the number of allowed edges is:
   - Edges within $S$: $\binom{N/2}{2}$.
   - Edges within $T$: $\binom{N/2}{2}$.
   - Edges between $S$ and $T$: $(N/2) \times (N/2)$.
   - Forbidden: edges between 1 and $S \setminus \{1\}$. There are $N/2 - 1$ such edges.
   
   So total allowed edges $K = \binom{N/2}{2} + \binom{N/2}{2} + (N/2)^2 - (N/2 - 1)$.
   
   We need to count graphs with $M$ edges from these $K$ edges such that:
   - 1 is connected to $T$.
   - Each $v \in T$ is connected to $S$.
   - Each $v \in S \setminus \{1\}$ is connected to $T$.
   
   This is a problem of counting graphs with specific degree constraints (at least one edge to a specific set).
   
   Given the complexity and $N \le 30$, we might need a more efficient method.
   
   However, note that the constraints on $M$ are from $N-1$ to $N(N-1)/2$.
   
   Let's try to compute the answer for each $M$ using inclusion-exclusion on the "forbidden" non-edges (i.e., vertices not connected to their required sets).
   
   For a fixed partition, let $U$ be the set of allowed edges.
   Let $F$ be the set of "bad" events:
   - $E_0$: 1 has no neighbor in $T$.
   - $E_v$ for $v \in T$: $v$ has no neighbor in $S$.
   - $E_w$ for $w \in S \setminus \{1\}$: $w$ has no neighbor in $T$.
   
   We want to count graphs with $M$ edges in $U$ that avoid all events in $F$.
   By inclusion-exclusion:
   $$ \sum_{J \subseteq F} (-1)^{|J|} N(J, M) $$
   where $N(J, M)$ is the number of graphs with $M$ edges in $U$ that satisfy all events in $J$ (i.e., for each event in $J$, the corresponding vertex has no edges to the required set).
   
   If a set of events $J$ is satisfied, it means certain edges are forbidden. Specifically:
   - If $E_0 \in J$, then no edges between 1 and $T$ are allowed.
   - If $E_v \in J$ for $v \in T$, then no edges between $v$ and $S$ are allowed.
   - If $E_w \in J$ for $w \in S \setminus \{1\}$, then no edges between $w$ and $T$ are allowed.
   
   The number of available edges $K_J$ depends on $J$.
   $N(J, M) = \binom{K_J}{M}$ if $K_J \ge M$, else 0.
   
   The number of terms in inclusion-exclusion is $2^{|F|} = 2^{1 + (N/2) + (N/2 - 1)} = 2^N$.
   For $N=30$, $2^{30} \approx 10^9$, which is too large.
   
   However, we can group terms by the number of vertices in $T$ and $S \setminus \{1\}$ that are "bad".
   Let $i$ be the number of vertices in $T$ with no neighbor in $S$.
   Let $j$ be the number of vertices in $S \setminus \{1\}$ with no neighbor in $T$.
   Let $k$ be 1 if 1 has no neighbor in $T$, else 0.
   
   The number of ways to choose which vertices are bad is $\binom{N/2}{i} \binom{N/2 - 1}{j} \binom{1}{k}$.
   
   For a fixed $i, j, k$, we need to calculate $K_{i,j,k}$, the number of allowed edges when:
   - $k=1$: no edges between 1 and $T$.
   - $i$ specific vertices in $T$ have no edges to $S$.
   - $j$ specific vertices in $S \setminus \{1\}$ have no edges to $T$.
   
   The edges are partitioned into:
   1. Edges within $S$: always allowed. Count: $\binom{N/2}{2}$.
   2. Edges within $T$: always allowed. Count: $\binom{N/2}{2}$.
   3. Edges between $S$ and $T$:
      - Between 1 and $T$: allowed unless $k=1$. If $k=1$, 0 edges. Else, $N/2$ edges (but wait, 1 is in $S$, so edges between 1 and $T$ are part of $S-T$ edges).
      - Between $S \setminus \{1\}$ and $T$:
        - For the $j$ bad vertices in $S \setminus \{1\}$, no edges to $T$.
        - For the remaining $N/2 - 1 - j$ vertices in $S \setminus \{1\}$, edges to $T$ are allowed.
        - For the $i$ bad vertices in $T$, no edges to $S$ (which includes 1 and $S \setminus \{1\}$).
   
   Let's refine the count of $S-T$ edges:
   Total potential edges between $S$ and $T$ is $(N/2)^2$.
   
   If $k=1$, edges between 1 and $T$ are removed. Remaining: $(N/2 - 1) \times (N/2)$ edges between $S \setminus \{1\}$ and $T$.
   If $k=0$, all $(N/2)^2$ edges are potentially allowed, but subject to $i$ and $j$.
   
   For the edges between $S \setminus \{1\}$ and $T$:
   - There are $(N/2 - 1) \times (N/2)$ such edges.
   - The $j$ bad vertices in $S \setminus \{1\}$ have no edges to $T$. So edges incident to them are removed.
   - The $i$ bad vertices in $T$ have no edges to $S$. So edges incident to them are removed.
   
   The number of allowed edges between $S \setminus \{1\}$ and $T$ is:
   $$ (N/2 - 1 - j) \times (N/2 - i) $$
   
   If $k=1$, we also remove edges between 1 and $T$.
   The number of allowed edges between 1 and $T$ is:
   - If $k=1$: 0.
   - If $k=0$: The edges between 1 and $T$ are allowed unless the vertex in $T$ is bad (i.e., in the set of $i$ bad vertices).
     So, if $k=0$, allowed edges between 1 and $T$ is $N/2 - i$.
   
   So, total allowed edges $K_{i,j,k}$:
   $$ K_{i,j,k} = \binom{N/2}{2} + \binom{N/2}{2} + \text{edges}(S \setminus \{1\}, T) + \text{edges}(1, T) $$
   $$ \text{edges}(S \setminus \{1\}, T) = (N/2 - 1 - j)(N/2 - i) $$
   $$ \text{edges}(1, T) = \begin{cases} 0 & k=1 \\ N/2 - i & k=0 \end{cases} $$
   
   The coefficient for $(i, j, k)$ in the inclusion-exclusion sum is:
   $$ (-1)^{i + j + k} \binom{N/2}{i} \binom{N/2 - 1}{j} \binom{1}{k} $$
   
   The number of partitions is $\binom{N-1}{N/2 - 1}$.
   
   So the answer for a fixed $M$ is:
   $$ \binom{N-1}{N/2 - 1} \sum_{i=0}^{N/2} \sum_{j=0}^{N/2 - 1} \sum_{k=0}^{1} (-1)^{i+j+k} \binom{N/2}{i} \binom{N/2 - 1}{j} \binom{1}{k} \binom{K_{i,j,k}}{M} $$
   
   This is $O(N^2)$ per $M$, and there are $O(N^2)$ values of $M$. Total complexity $O(N^4)$, which is fine for $N=30$.

## worker: (None)
The solution uses inclusion-exclusion to count the number of valid graphs for each edge count $M$. 

1. **Partitioning**: We iterate over all possible partitions of vertices into even-distance set $S$ (containing vertex 1) and odd-distance set $T$. The number of such partitions is $\binom{N-1}{N/2-1}$.

2. **Edge Constraints**: For a fixed partition $(S, T)$, the valid graphs must satisfy:
   - No edge between vertex 1 and $S \setminus \{1\}$.
   - Vertex 1 has at least one neighbor in $T$.
   - Every vertex in $T$ has at least one neighbor in $S$.
   - Every vertex in $S \setminus \{1\}$ has at least one neighbor in $T$.

3. **Inclusion-Exclusion**: We use inclusion-exclusion on the "bad" events (violations of the "at least one neighbor" conditions). The bad events are:
   - $E_0$: Vertex 1 has no neighbor in $T$.
   - $E_v$ for $v \in T$: Vertex $v$ has no neighbor in $S$.
   - $E_w$ for $w \in S \setminus \{1\}$: Vertex $w$ has no neighbor in $T$.

4. **Counting Available Edges**: For a given set of bad events (characterized by $i$ bad vertices in $T$, $j$ bad vertices in $S \setminus \{1\}$, and $k$ indicating if vertex 1 is bad), we calculate the number of available edges $K_{i,j,k}$.

5. **Summation**: For each $K$, we precompute the inclusion-exclusion coefficient. Then for each $M$, we sum over all $K \ge M$: $\text{ie\_sum\_by\_K}[K] \times \binom{K}{M}$.

6. **Complexity**: The inclusion-exclusion has $O(N^2)$ terms. Computing the final answers for all $M$ takes $O(N^4)$ time, which is feasible for $N \le 30$.
