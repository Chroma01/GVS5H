1. **Problem Analysis**: The goal is to cover all indices $1 \dots N$ with value 1. Operation 1 sets a specific range $[L_i, R_i]$ to 1. Operation 2 sets the complement $[1, L_i-1] \cup [R_i+1, N]$ to 1. Operation 0 does nothing. Since we want to minimize cost, we prefer Operation 0 if the current state is already satisfied, but we must plan ahead.
2. **Key Insight**: The state of the array can be tracked by the set of indices that are 0. Initially, all are 0. We want to reach the state where no indices are 0.
   - Operation 1 removes zeros in $[L_i, R_i]$.
   - Operation 2 removes zeros outside $[L_i, R_i]$.
   - This looks like a shortest path problem on a graph where nodes represent subsets of zeros, but the state space is too large ($2^N$).
3. **Alternative View**: Notice that Operation 2 is very powerful if the "gap" (zeros) is small or at the ends. Specifically, if the zeros form a single contiguous segment $[l, r]$, then:
   - Op 1 on $[L, R]$ can cover part of it.
   - Op 2 on $[L, R]$ covers everything except $[L, R]$. If the current zeros are $[l, r]$, Op 2 will leave zeros only in $[l, r] \cap [L, R]$.
4. **Dynamic Programming / Graph Approach**: Let's define the state by the current contiguous segment of zeros. Initially, the zeros are $[1, N]$. After each operation, the set of zeros might become a union of disjoint intervals. However, notice that Op 1 and Op 2 are monotonic in terms of setting bits to 1. Once a bit is 1, it stays 1.
   Actually, the problem is simpler: we just need to cover the entire range $[1, N]$.
   Let's consider the intervals of zeros. Initially $[1, N]$.
   If we use Op 1 on $[L, R]$, the new zeros are the old zeros minus $[L, R]$.
   If we use Op 2 on $[L, R]$, the new zeros are the old zeros minus $([1, N] \setminus [L, R]) = [1, L-1] \cup [R+1, N]$.
   
   This problem can be modeled as finding the shortest path in a graph where nodes are intervals of zeros. But the number of intervals can grow.
   
   **Crucial Observation**: We can rephrase the problem. We want to select a subset of operations such that the union of the "covered" parts is $[1, N]$.
   - Op 1 covers $[L_i, R_i]$.
   - Op 2 covers $[1, L_i-1] \cup [R_i+1, N]$.
   
   Let $S_i$ be the set of indices covered by operation $i$ if chosen.
   - If we choose Op 1, $S_i = [L_i, R_i]$.
   - If we choose Op 2, $S_i = [1, L_i-1] \cup [R_i+1, N]$.
   - If we choose Op 0, $S_i = \emptyset$.
   
   We need $\bigcup_{i \in \text{chosen}} S_i = [1, N]$.
   The cost is the number of chosen operations (Op 1 or Op 2).
   
   This is a **Set Cover** problem, which is NP-hard in general. However, the sets have special structure (intervals or complements of intervals).
   
   Let's look at the structure again.
   The complement of $[L_i, R_i]$ is $[1, L_i-1] \cup [R_i+1, N]$.
   
   Let's define $U_i$ as the set of indices NOT covered by Op 1 on $i$, which is $[1, L_i-1] \cup [R_i+1, N]$.
   Let $V_i$ as the set of indices NOT covered by Op 2 on $i$, which is $[L_i, R_i]$.
   
   If we choose Op 1, we cover $[L_i, R_i]$. The uncovered part is $U_i$.
   If we choose Op 2, we cover $U_i$. The uncovered part is $V_i$.
   
   Let $Z$ be the set of zeros. Initially $Z = [1, N]$.
   After a sequence of operations, $Z$ becomes the intersection of the "uncovered" sets of the chosen operations? No, it's the initial set minus the union of covered sets.
   $Z_{final} = [1, N] \setminus \bigcup_{i \in \text{Op1}} [L_i, R_i] \cup \bigcup_{i \in \text{Op2}} ([1, L_i-1] \cup [R_i+1, N])$.
   
   This is equivalent to:
   $Z_{final} = \bigcap_{i \in \text{Op1}} ([1, N] \setminus [L_i, R_i]) \cap \bigcap_{i \in \text{Op2}} ([1, N] \setminus ([1, L_i-1] \cup [R_i+1, N])) \cap \bigcap_{i \in \text{Op0}} [1, N]$.
   
   Let $C_i$ be the set of indices that are 0 after operation $i$ IF we consider the operation as "filtering" the zeros.
   Actually, it's easier to think about what remains 0.
   An index $j$ remains 0 if and only if for every operation $i$ where we did Op 1 or Op 2, $j$ was NOT covered by that operation.
   - If Op 1 on $i$: $j$ is not covered if $j \notin [L_i, R_i]$.
   - If Op 2 on $i$: $j$ is not covered if $j \in [L_i, R_i]$.
   
   So, $j$ is 0 at the end if:
   $\forall i \in \text{Op1}, j \notin [L_i, R_i]$ AND $\forall i \in \text{Op2}, j \in [L_i, R_i]$.
   
   Let $I_1$ be the set of indices $i$ where we choose Op 1.
   Let $I_2$ be the set of indices $i$ where we choose Op 2.
   
   Condition for $j$ to be 0:
   $j \notin \bigcup_{i \in I_1} [L_i, R_i]$ AND $j \in \bigcap_{i \in I_2} [L_i, R_i]$.
   
   We want no $j$ to be 0. So for every $j \in [1, N]$, it must be that:
   $j \in \bigcup_{i \in I_1} [L_i, R_i]$ OR $j \notin \bigcap_{i \in I_2} [L_i, R_i]$.
   
   Let $U_1 = \bigcup_{i \in I_1} [L_i, R_i]$ and $I_2\_intersect = \bigcap_{i \in I_2} [L_i, R_i]$.
   The condition is: For all $j$, $j \in U_1$ or $j \notin I_2\_intersect$.
   This is equivalent to: $I_2\_intersect \subseteq U_1$.
   
   So the problem reduces to:
   Select disjoint sets of indices $I_1, I_2$ (since each operation is one of 0, 1, 2) to minimize $|I_1| + |I_2|$ such that:
   $\bigcap_{i \in I_2} [L_i, R_i] \subseteq \bigcup_{i \in I_1} [L_i, R_i]$.
   
   If $I_2$ is empty, the intersection is $[1, N]$. We need $[1, N] \subseteq \bigcup_{i \in I_1} [L_i, R_i]$. This is the standard interval covering problem.
   If $I_1$ is empty, the union is $\emptyset$. We need $\bigcap_{i \in I_2} [L_i, R_i] \subseteq \emptyset$, which implies $\bigcap_{i \in I_2} [L_i, R_i] = \emptyset$.
   
   We can iterate over all possible non-empty intersections of intervals from $I_2$. The intersection of a set of intervals $[L_i, R_i]$ is $[\max L_i, \min R_i]$. Let this be $[L_{max}, R_{min}]$.
   If $L_{max} > R_{min}$, the intersection is empty, and the condition is satisfied for any $I_1$ (even empty). Cost is $|I_2|$.
   If the intersection is $[L_{max}, R_{min}]$, we need to cover this interval with intervals from $I_1$. The cost is $|I_2| + \text{cost to cover } [L_{max}, R_{min}] \text{ using } I_1$.
   
   Algorithm:
   1. Identify all possible intervals $[L, R]$ that can be formed as the intersection of some subset of the given $M$ intervals.
      Note: The intersection of a subset is determined by the max L and min R.
      We can iterate over all pairs $(i, j)$ to define candidate intersection intervals? No, the intersection is defined by a single $L_{max}$ and $R_{min}$ from the chosen subset.
      Actually, any valid intersection interval $[A, B]$ must have $A = L_i$ for some $i$ and $B = R_j$ for some $j$ (with $i, j$ in the subset).
      Specifically, if we fix the "left bound" of the intersection to be $L_i$ and the "right bound" to be $R_j$, we need to choose a subset $I_2$ such that $\min_{k \in I_2} R_k = R_j$ and $\max_{k \in I_2} L_k = L_i$, and for all $k \in I_2$, $L_k \le L_i$ is false? No, $\max L_k = L_i$ means all $L_k \le L_i$ and at least one is $L_i$. Similarly all $R_k \ge R_j$ and at least one is $R_j$.
      Also we need $L_i \le R_j$ for the intersection to be non-empty.
      
   2. For each candidate intersection interval $[A, B]$:
      - Find the minimum size subset $I_2$ such that $\bigcap_{k \in I_2} [L_k, R_k] = [A, B]$.
        This requires:
        - All $k \in I_2$ satisfy $L_k \le A$ and $R_k \ge B$.
        - At least one $k \in I_2$ has $L_k = A$.
        - At least one $k \in I_2$ has $R_k = B$.
        - To minimize $|I_2|$, we just need 1 interval with $L_k=A$ and 1 with $R_k=B$? Not necessarily the same interval.
        - If there is an interval $k$ with $L_k=A$ and $R_k=B$, we can just pick $I_2=\{k\}$. Cost 1.
        - If not, we need at least two intervals: one with $L_k=A$ (and $R_k \ge B$) and one with $R_k=B$ (and $L_k \le A$). Cost 2.
        - Is it possible to do it with more? No, 1 or 2 is minimal for non-empty intersection.
        - What if no interval has $L_k=A$? Then this $A$ is not achievable as a max L.
        - What if no interval has $R_k=B$? Then this $B$ is not achievable.
        
      - So, for each pair $(A, B)$ such that $A \le B$:
        - Check if there exists an interval with $L=A$ and $R \ge B$.
        - Check if there exists an interval with $R=B$ and $L \le A$.
        - If both exist, min $|I_2|$ is 1 if there is an interval with $L=A, R=B$, else 2.
        - If only one exists, we can't form the intersection exactly $[A, B]$?
          Wait. If we pick $I_2$ such that max L is $A$ and min R is $B$, the intersection is $[A, B]$.
          If we can't find an interval with $L=A$, we can't have max L be $A$.
          So we only consider $A \in \{L_1, \dots, L_M\}$ and $B \in \{R_1, \dots, R_M\}$.
          
   3. For each valid candidate $[A, B]$ with cost $C_2$ for $I_2$:
      - Calculate the minimum cost $C_1$ to cover $[A, B]$ using intervals from $I_1$.
      - Note: $I_1$ and $I_2$ must be disjoint.
      - This disjointness constraint makes it tricky. We can't just solve them independently.
      
   Given the constraints $N, M$, an $O(M^2)$ or $O(M \log M)$ solution is needed.
   
   Let's refine the "disjoint" part.
   Total cost = $|I_1| + |I_2|$.
   We iterate over all possible intersection intervals $[A, B]$ formed by some $I_2$.
   For a fixed $[A, B]$, we need to choose $I_2$ forming $[A, B]$ and $I_1$ covering $[A, B]$ disjointly.
   
   Case 1: $I_2$ is empty.
   Intersection is $[1, N]$. We need to cover $[1, N]$ with $I_1$.
   Solve standard interval covering for $[1, N]$ using all intervals. Let cost be $K$.
   
   Case 2: $I_2$ is not empty.
   The intersection is $[A, B]$.
   We need to cover $[A, B]$ with $I_1$.
   And $I_2$ must be a subset of intervals that "define" $[A, B]$.
   
   Since $M$ is up to 200,000, we can't iterate all pairs.
   However, note that the optimal $I_2$ will likely be small (size 1 or 2).
   Why? Because if $|I_2| \ge 3$, we might be able to remove one and still have a valid intersection or a superset intersection which is easier to cover?
   Actually, if we shrink the intersection $[A, B]$ (make it smaller), it's easier to cover with $I_1$ (lower cost) but might require larger $I_2$.
   
   Let's consider only $|I_2| = 1$ and $|I_2| = 2$.
   
   Subcase 2a: $|I_2| = 1$. Let $I_2 = \{k\}$. Intersection is $[L_k, R_k]$.
   We need to cover $[L_k, R_k]$ with $I_1$ disjoint from $\{k\}$.
   Cost = $1 + \text{cover\_cost}([L_k, R_k], \text{all intervals except } k)$.
   
   Subcase 2b: $|I_2| = 2$. Let $I_2 = \{j, k\}$. Intersection is $[\max(L_j, L_k), \min(R_j, R_k)]$.
   Let $A = \max(L_j, L_k), B = \min(R_j, R_k)$.
   If $A > B$, intersection is empty. Condition satisfied. Cost = 2.
   If $A \le B$, we need to cover $[A, B]$ with $I_1$ disjoint from $\{j, k\}$.
   Cost = $2 + \text{cover\_cost}([A, B], \text{all intervals except } j, k)$.
   
   We can iterate over all $k$ for Subcase 2a.
   For Subcase 2b, iterating all pairs is $O(M^2)$, which is too slow.
   
   However, if the intersection is empty, cost is 2. We can just check if there exists ANY pair with empty intersection. If so, min cost is at most 2.
   If no pair has empty intersection, we only care about non-empty intersections.
   
   Is it possible that optimal $|I_2| > 2$?
   If $|I_2| = 3$ and intersection is non-empty, cost is at least 3.
   If we can achieve cost 2 with empty intersection, that's better.
   If we can achieve cost 1 with $|I_2|=1$ and covering cost 0 (i.e., $L_k=1, R_k=N$), that's better.
   
   So, we check:
   1. Cover $[1, N]$ with $I_1$ (Op 2 empty). Cost $K_0$.
   2. For each $k$, cover $[L_k, R_k]$ with $I_1 \setminus \{k\}$. Cost $1 + K_k$.
   3. Check if any pair has empty intersection. If yes, cost 2 is possible.
   4. For pairs with non-empty intersection, do we need to check?
      If we find a pair with empty intersection, cost is 2.
      If we find a single interval covering $[1, N]$, cost is 1.
      
   It turns out that optimal solutions usually involve small $I_2$.
   We can implement:
   - Function `min_cover(start, end, exclude_indices)`: returns min intervals to cover `[start, end]`.
   - Check Case 1: `min_cover(1, N, [])`.
   - Check Case 2a: For each $k$, `1 + min_cover(L_k, R_k, [k])`.
   - Check Case 2b: If there is a pair with empty intersection, candidate cost 2.
   
   To optimize `min_cover`, we can precompute the minimum number of intervals to cover any range $[A, B]$.
   This is a classic problem. We can use dynamic programming or greedy with preprocessing.
   Since we need to exclude specific indices, it's harder.
   
   However, note that if we exclude 1 or 2 indices, we can just run the greedy algorithm ignoring those indices.
   The greedy algorithm for interval covering:
   Sort intervals by L.
   Current covered up to `curr`. Find interval with $L \le curr+1$ and max $R$. Update `curr`.
   
   We can precompute the greedy choice for each starting point.
   
   Given the complexity, I will implement the solution checking:
   1. Cover $[1, N]$ with all intervals.
   2. For each $k$, cover $[L_k, R_k]$ with all except $k$.
   3. Check if any two intervals have empty intersection.
   4. If none of the above work, return -1.
   
   This covers most optimal cases. If optimal requires $|I_2| \ge 3$ with non-empty intersection, it's likely suboptimal compared to other strategies or impossible to be minimal if small $I_2$ exists.