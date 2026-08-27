
## ideation
The problem asks for the number of ways to pair $N$ White vertices with $N$ Black vertices in a directed graph with edges $i \to i+1$ for all $i$, such that the resulting graph is strongly connected.

**Key Observations:**
1.  **Structure**: The base graph is a simple path $1 \to 2 \to \dots \to 2N$. The added edges are from White vertices to Black vertices.
2.  **Strong Connectivity Condition**: A directed graph containing a Hamiltonian path (the base path) is strongly connected if and only if there are no "cuts" that isolate a prefix of the vertices from the rest in a way that prevents return flow. Specifically, the graph is NOT strongly connected if and only if there exists a $k \in \{1, \dots, 2N-1\}$ such that all added edges go from $\{1, \dots, k\}$ to $\{k+1, \dots, 2N\}$ or from $\{k+1, \dots, 2N\}$ to $\{1, \dots, k\}$? 
    Actually, a more precise structural decomposition applies: The condensation graph of SCCs is a DAG. Since the base edges go $i \to i+1$, the topological order of SCCs must respect the vertex indices. The first SCC in the topological order (containing vertex 1) must be a prefix $\{1, \dots, k\}$. For this prefix to be a source SCC (no incoming edges from outside), there must be no added edges from any vertex $u > k$ to any vertex $v \le k$. Since added edges go from White to Black, this means no Black vertex in $\{1, \dots, k\}$ can be paired with a White vertex in $\{k+1, \dots, 2N\}$. Consequently, all Black vertices in $\{1, \dots, k\}$ must be paired with White vertices in $\{1, \dots, k\}$. This implies that the prefix $\{1, \dots, k\}$ must contain an equal number of White and Black vertices.

3.  **Combinatorial Recurrence**:
    Let $Total[m]$ be the total number of valid pairings for a balanced prefix of length $2m$ (where the number of Ws equals the number of Bs), ignoring strong connectivity.
    Let $Ans[m]$ be the number of strongly connected pairings for a balanced prefix of length $2m$.
    
    Any valid pairing of a balanced prefix of length $2m$ can be uniquely decomposed into a first strongly connected component of length $2k$ (where $1 \le k \le m$) followed by a valid pairing of the remaining $2(m-k)$ vertices.
    Thus:
    $$ Total[m] = \sum_{k=1}^{m} Ans[k] \times Total[m-k] $$
    With $Total[0] = 1$.
    
    We can invert this to find $Ans[m]$:
    $$ Ans[m] = Total[m] - \sum_{k=1}^{m-1} Ans[k] \times Total[m-k] $$

4.  **Computing $Total[m]$**:
    $Total[m]$ is the number of perfect matchings between the White vertices and Black vertices in the first $2m$ positions. We can compute this using dynamic programming.
    Let $dp[i][j]$ be the number of ways to pair the first $i$ vertices such that there are $j$ unmatched White vertices.
    - If $S[i] == 'W'$: The $i$-th vertex is White. It cannot be paired immediately. It adds to the pool of unmatched Whites.
      $dp[i][j] = dp[i-1][j-1]$
    - If $S[i] == 'B'$: The $i$-th vertex is Black. It must be paired with one of the currently unmatched Whites. There are $j$ choices (where $j$ is the number of unmatched whites before this step, so we transition from state $j+1$ unmatched whites at step $i-1$ to $j$ at step $i$? No, let's be careful).
      
      Let's redefine state: $dp[i][j]$ = number of ways to process first $i$ vertices with $j$ *unmatched* White vertices.
      - Start: $dp[0][0] = 1$.
      - For $i$ from 1 to $2N$:
        - If $S[i] == 'W'$:
          $dp[i][j] = dp[i-1][j-1]$ (for $j \ge 1$)
        - If $S[i] == 'B'$:
          $dp[i][j] = dp[i-1][j+1] \times (j+1)$ (for $j \ge 0$). The term $(j+1)$ is the number of choices to pair the current Black vertex with one of the $j+1$ unmatched Whites from the previous step.
      
      $Total[m] = dp[2m][0]$.

5.  **Algorithm**:
    - Read $N$ and $S$.
    - Compute $dp[i][j]$ for $i=0 \dots 2N$. Note that $j$ ranges from $0$ to $N$.
    - Extract $Total[m] = dp[2m][0]$ for $m=0 \dots N$.
    - Compute $Ans[m]$ for $m=1 \dots N$ using the recurrence:
      $Ans[m] = Total[m] - \sum_{k=1}^{m-1} Ans[k] \times Total[m-k] \pmod{998244353}$.
    - Output $Ans[N]$.

6.  **Complexity**:
    - DP for Total: $O(N^2)$. Since $N \le 2 \times 10^5$, $O(N^2)$ is too slow ($4 \times 10^{10}$ ops).
    - Wait, is $O(N^2)$ acceptable? No. We need a faster way to compute $Total[m]$ or the final answer.
    
    Let's re-examine $Total[m]$.
    The DP for $Total[m]$ is essentially counting the number of matchings in a bipartite graph defined by the positions.
    Actually, there is a closed form or a faster way?
    The DP state $dp[i][j]$ looks like it's related to Catalan-like numbers but constrained by the specific string $S$.
    However, notice that the transitions are local.
    Is there a combinatorial formula for $Total[m]$?
    $Total[m]$ is the number of bijections $f: W \cap \{1..2m\} \to B \cap \{1..2m\}$ such that... wait, there are no restrictions on the pairing other than W to B.
    So $Total[m]$ is simply the number of perfect matchings between the set of White indices in $1..2m$ and Black indices in $1..2m$.
    Let $W_m$ be the set of indices of Ws in $1..2m$ and $B_m$ be the set of indices of Bs in $1..2m$.
    If $|W_m| = |B_m| = m$, then $Total[m] = m!$.
    **Wait!** The problem says "Partition the 2N vertices into N pairs, each consisting of one white vertex and one black vertex."
    It does NOT say that a White vertex at index $i$ can only be paired with a Black vertex at index $j$ if some condition holds. It just says we add an edge.
    So, ANY White vertex can be paired with ANY Black vertex.
    Therefore, the number of ways to pair the first $2m$ vertices (assuming they have $m$ Ws and $m$ Bs) is simply $m!$?
    
    Let's check Sample 1: N=2, S=BWBW.
    Vertices: 1(B), 2(W), 3(B), 4(W).
    Prefix 1..2: B, W. 1 W, 1 B. $Total[1] = 1! = 1$.
    Prefix 1..4: B, W, B, W. 2 Ws, 2 Bs. $Total[2] = 2! = 2$.
    
    Let's check the recurrence with $Total[m] = m!$.
    $Ans[1] = Total[1] = 1$.
    $Ans[2] = Total[2] - Ans[1] \times Total[1] = 2 - 1 \times 1 = 1$.
    Output 1. Matches Sample 1.
    
    Let's check Sample 2: N=4, S=BWWBWBWB.
    Check if prefix 1..8 has equal Ws and Bs.
    S: B W W B W B W B
    Ws: 2,3,5,7 (4 Ws). Bs: 1,4,6,8 (4 Bs).
    $Total[4] = 4! = 24$.
    
    We need $Ans[4]$.
    $Ans[1] = 1! = 1$.
    $Ans[2] = 2! - Ans[1] \times 1! = 2 - 1 = 1$.
    $Ans[3] = 3! - (Ans[1] \times 2! + Ans[2] \times 1!) = 6 - (1 \times 2 + 1 \times 1) = 6 - 3 = 3$.
    $Ans[4] = 4! - (Ans[1] \times 3! + Ans[2] \times 2! + Ans[3] \times 1!) = 24 - (1 \times 6 + 1 \times 2 + 3 \times 1) = 24 - (6+2+3) = 24 - 11 = 13$.
    
    But Sample 2 Output is 0.
    Why?
    The recurrence assumes that the graph can be decomposed into a first SCC which is a prefix.
    This decomposition is valid ONLY IF the prefix is "balanced" (equal Ws and Bs).
    In Sample 2, are there balanced prefixes?
    Prefix 1..2: B, W. Balanced.
    Prefix 1..4: B, W, W, B. Balanced.
    Prefix 1..6: B, W, W, B, W, B. Balanced.
    Prefix 1..8: Balanced.
    
    So why is the answer 0?
    Let's re-read the strong connectivity condition.
    "The graph is strongly connected if and only if it is possible to travel from any vertex to any vertex".
    
    Is it possible that $Ans[m]$ is not just determined by the prefix balance?
    The decomposition $Total[m] = \sum Ans[k] Total[m-k]$ relies on the fact that the first SCC is a prefix $1..2k$.
    This is true if and only if there are no edges from $V \setminus \{1..2k\}$ to $\{1..2k\}$.
    Edges are $i \to i+1$ and $W \to B$.
    Edges from outside to inside:
    - Base edges: $i \to i+1$. If $i \ge 2k$, $i+1 > 2k$. No base edges enter $1..2k$ from outside.
    - Added edges: $u \to v$ with $u \in W, v \in B$.
      We need no edges from $u > 2k$ to $v \le 2k$.
      This requires that no Black vertex in $1..2k$ is paired with a White vertex in $2k+1..2N$.
      This implies all Black vertices in $1..2k$ are paired with White vertices in $1..2k$.
      This implies $|W \cap 1..2k| = |B \cap 1..2k|$.
      
    So the decomposition holds.
    
    Why is Sample 2 output 0?
    Maybe my calculation of $Ans$ is wrong?
    Or maybe $Total[m]$ is not $m!$?
    "Partition the 2N vertices into N pairs...".
    The pairs are formed globally.
    When we say "Total[m] is the number of ways to pair the first 2m vertices", we mean:
    Consider the subproblem on vertices $1..2m$. We pair the $m$ Whites in this range with the $m$ Blacks in this range.
    The number of such pairings is indeed $m!$.
    
    Let's re-read Sample 2 carefully.
    N=4, S=BWWBWBWB.
    Output 0.
    
    Is it possible that for some $k$, the "first SCC" is not a prefix?
    No, the topological sort argument holds.
    
    Is it possible that the graph is never strongly connected?
    Let's check if there is ANY valid pairing for Sample 2.
    Ws at 2,3,5,7. Bs at 1,4,6,8.
    We need to pair each W with a B.
    Condition for strong connectivity:
    1. No cut at $k=2$ (prefix 1,2). B at 1, W at 2.
       Prefix 1..2 has 1 W, 1 B.
       For this to NOT be a source SCC, there must be an edge from outside to inside.
       Outside: 3,4,5,6,7,8.
       Inside: 1,2.
       Edges from outside to inside:
       - Base: None.
       - Added: $u \to v$ with $u > 2, v \le 2$.
       $v$ must be Black. Only B in prefix is 1.
       So we need a pair $(u, 1)$ with $u > 2$ and $u$ is White.
       Ws outside: 3,5,7.
       If 1 is paired with 3, 5, or 7, then there is an edge into 1 from outside.
       If 1 is paired with 2 (the only W inside), then there is NO edge from outside to inside (since 2 is inside).
       So, if 1 is paired with 2, the prefix 1..2 is a source SCC (or part of one).
       If 1 is paired with 3,5,7, then there is an incoming edge.
       
    For the whole graph to be strongly connected, the FIRST SCC must be the whole graph.
    This means there should be NO $k < 2N$ such that the prefix $1..2k$ is a source SCC.
    Prefix $1..2k$ is a source SCC iff all Blacks in $1..2k$ are paired with Whites in $1..2k$.
    
    So, the graph is strongly connected IFF for all $k \in \{1, \dots, N-1\}$ such that prefix $1..2k$ is balanced, there is at least one Black in $1..2k$ paired with a White in $2k+1..2N$.
    
    In Sample 2:
    Balanced prefixes at $k=1$ (len 2), $k=2$ (len 4), $k=3$ (len 6).
    We need:
    - For $k=1$ (prefix 1,2): B at 1, W at 2.
      Condition: 1 must NOT be paired with 2.
      So 1 must be paired with 3, 5, or 7.
    - For $k=2$ (prefix 1..4): Bs at 1,4. Ws at 2,3.
      Condition: NOT (1 paired with 2 or 3 AND 4 paired with 2 or 3).
      i.e., At least one of 1 or 4 is paired with a White in 5,7.
    - For $k=3$ (prefix 1..6): Bs at 1,4,6. Ws at 2,3,5.
      Condition: At least one of 1,4,6 is paired with a White in 7.
      
    Let's count the number of permutations $\sigma$ of Ws to Bs that satisfy these.
    Ws: $w_1=2, w_2=3, w_3=5, w_4=7$.
    Bs: $b_1=1, b_2=4, b_3=6, b_4=8$.
    
    Condition 1: $b_1$ (1) is NOT paired with $w_1$ (2).
    Condition 2: The set of Bs $\{1,4\}$ is NOT fully covered by Ws $\{2,3\}$.
    Condition 3: The set of Bs $\{1,4,6\}$ is NOT fully covered by Ws $\{2,3,5\}$.
    
    Let's use inclusion-exclusion or just iterate? N=4 is small.
    Total permutations: 24.
    
    Let $A_1$ be the set of pairings where prefix 1..2 is a source SCC (1 paired with 2).
    Let $A_2$ be the set of pairings where prefix 1..4 is a source SCC (1,4 paired with 2,3).
    Let $A_3$ be the set of pairings where prefix 1..6 is a source SCC (1,4,6 paired with 2,3,5).
    
    We want $Total - |A_1 \cup A_2 \cup A_3|$.
    
    $|A_1|$: 1 paired with 2. Remaining 3 Ws (3,5,7) paired with 3 Bs (4,6,8). $3! = 6$.
    $|A_2|$: 1,4 paired with 2,3. $2!$ ways to pair them. Remaining 2 Ws (5,7) paired with 2 Bs (6,8). $2!$ ways. Total $2! \times 2! = 4$.
    $|A_3|$: 1,4,6 paired with 2,3,5. $3!$ ways. Remaining 1 W (7) paired with 1 B (8). $1!$ way. Total $3! \times 1! = 6$.
    
    Intersections:
    $A_1 \cap A_2$: 1 paired with 2 (from $A_1$). And 1,4 paired with 2,3 (from $A_2$).
    Since 1 is paired with 2, this is consistent with $A_2$'s requirement that {1,4} map to {2,3}.
    So $A_1 \cap A_2$ is just $A_2$?
    Wait. $A_2$ requires {1,4} $\to$ {2,3}. $A_1$ requires 1 $\to$ 2.
    If 1 $\to$ 2, then 4 must $\to$ 3.
    So $A_1 \cap A_2$ is the set where 1$\to$2, 4$\to$3, and remaining 5,7 $\to$ 6,8.
    Number of ways: $1 \times 1 \times 2! = 2$.
    
    $A_1 \cap A_3$: 1 $\to$ 2. And {1,4,6} $\to$ {2,3,5}.
    Since 1 $\to$ 2, 4,6 must map to 3,5.
    Remaining 7 $\to$ 8.
    Ways: 1$\to$2 (1 way). 4,6 $\to$ 3,5 ($2!$ ways). 7$\to$8 (1 way). Total 2.
    
    $A_2 \cap A_3$: {1,4} $\to$ {2,3} AND {1,4,6} $\to$ {2,3,5}.
    This implies 6 $\to$ 5 (since 1,4 take 2,3).
    Ways: {1,4} $\to$ {2,3} ($2!$). 6 $\to$ 5 (1). 7 $\to$ 8 (1). Total 2.
    
    $A_1 \cap A_2 \cap A_3$:
    1 $\to$ 2.
    4 $\to$ 3 (from $A_2$ given 1$\to$2).
    6 $\to$ 5 (from $A_3$ given 1,4 take 2,3).
    7 $\to$ 8.
    Total 1 way.
    
    By Inclusion-Exclusion:
    $|A_1 \cup A_2 \cup A_3| = |A_1| + |A_2| + |A_3| - (|A_1 \cap A_2| + |A_1 \cap A_3| + |A_2 \cap A_3|) + |A_1 \cap A_2 \cap A_3|$
    $= 6 + 4 + 6 - (2 + 2 + 2) + 1 = 16 - 6 + 1 = 11$.
    
    Valid pairings = $24 - 11 = 13$.
    
    But Sample 2 output is 0.
    Why?
    
    Re-read Sample 2: "BWWBWBWB".
    My manual count gave 13.
    Is it possible that strong connectivity requires MORE than just no source SCCs?
    No, for a graph with a Hamiltonian path, being strongly connected is equivalent to the condensation graph being a single node.
    
    Wait, look at Sample 2 Output again. 0.
    Is it possible that NO pairing is strongly connected?
    
    Let's check a specific pairing.
    Try to satisfy the conditions.
    1. 1 not paired with 2.
    2. Not (1,4 paired with 2,3).
    3. Not (1,4,6 paired with 2,3,5).
    
    Let's try:
    1 $\to$ 4.
    2 $\to$ 1.
    3 $\to$ 6.
    5 $\to$ 8.
    7 $\to$ ?
    Ws: 2,3,5,7. Bs: 1,4,6,8.
    Pairs: (2,1), (3,6), (5,8), (7,4).
    Edges: 2$\to$1, 3$\to$6, 5$\to$8, 7$\to$4.
    Base: 1$\to$2, 2$\to$3, 3$\to$4, 4$\to$5, 5$\to$6, 6$\to$7, 7$\to$8.
    
    Check connectivity:
    1$\to$2$\to$1 (Cycle 1-2).
    2$\to$3$\to$6$\to$7$\to$4$\to$5$\to$6...
    Can we go 1 $\to$ 3? 1$\to$2$\to$3. Yes.
    Can we go 3 $\to$ 1? 3$\to$4$\to$5$\to$6$\to$7$\to$4... stuck in 4-5-6-7 loop?
    7$\to$4. 4$\to$5. 5$\to$6. 6$\to$7.
    From 3, we go 3$\to$4. Then we are in the cycle 4-5-6-7.
    Can we exit the cycle to 1?
    Edges from 4,5,6,7 to 1,2,3?
    4$\to$5 (base).
    5$\to$6 (base).
    6$\to$7 (base).
    7$\to$4 (added).
    No edges from 4,5,6,7 to 1,2,3.
    So once we enter 4, we can't go back to 1,2,3.
    So 3 cannot reach 1.
    Not strongly connected.
    
    It seems very hard to connect the "left" part to the "right" part and back.
    
    Actually, there is a known result for this problem.
    If the string $S$ does not start with 'W' and end with 'B' (or similar constraints), the answer might be 0.
    Sample 2 starts with B and ends with B.
    Sample 1 starts with B and ends with W.
    
    Condition for non-zero answer:
    The first vertex must be Black? No, if first is White, it has no incoming base edge. It must have an incoming added edge.
    If $S_1 = W$, it must be paired with a B. But it has no incoming base edge. So it must have an incoming added edge from some $u > 1$.
    If $S_{2N} = B$, it has no outgoing base edge. It must have an outgoing added edge? No, added edges are W to B. So B has no outgoing added edges. It relies on base edges.
    If $S_{2N} = B$, it has no outgoing edges (base $2N \to 2N+1$ doesn't exist, added edges are TO B).
    So if $S_{2N} = B$, vertex $2N$ has out-degree 0?
    Base edges: $i \to i+1$. Vertex $2N$ has no base outgoing edge.
    Added edges: $W \to B$. Vertex $2N$ is B, so it is a target, not a source.
    So if $S_{2N} = B$, vertex $2N$ has out-degree 0.
    Thus, the graph cannot be strongly connected (cannot leave $2N$).
    
    Sample 2 ends with B. So Answer 0.
    Sample 1 ends with W. Answer 1.
    
    So, a necessary condition is $S_{2N} = W$.
    Similarly, $S_1$ must be B?
    If $S_1 = W$, it has in-degree 0 from base. It must have an incoming added edge.
    This is possible.
    However, if $S_1 = W$, then vertex 1 is White.
    
    Let's check if $S_{2N}=W$ is sufficient?
    No, Sample 3: BWWBWBBBWWBWBBWWBW. Ends with W. Output 240792.
    
    So, if $S_{2N} \neq W$, output 0.
    
    What about the DP approach?
    The DP approach $Ans[N]$ derived from $Total[m]=m!$ gave 13 for Sample 2.
    But we established Sample 2 is 0 because $S_{2N}=B$.
    Does the DP account for this?
    The DP counts pairings where the first SCC is the whole graph.
    If $S_{2N}=B$, can the graph be strongly connected?
    No, because vertex $2N$ has out-degree 0.
    So $Ans[N]$ should be 0 if $S_{2N}=B$.
    
    Why did my DP give 13?
    Because the DP assumes that if the prefix $1..2N$ is balanced, we can form a strongly connected component.
    But it doesn't check the out-degree of the last vertex.
    The decomposition into SCCs works for the structure, but the "strongly connected" definition requires every vertex to have in-degree $\ge 1$ and out-degree $\ge 1$.
    The DP counts matchings that form a single SCC in the condensation graph sense (i.e., no cuts).
    However, if a vertex has out-degree 0, it cannot be part of a cycle, so it cannot be in a strongly connected component of size $>1$?
    Actually, if a vertex has out-degree 0, it is a sink.
    If the graph is strongly connected, every vertex must have out-degree $\ge 1$.
    
    So, if $S_{2N}=B$, the answer is 0.
    
    Is this the only case?
    What if $S_1=W$?
    Vertex 1 has in-degree 0 from base. It must have an incoming added edge.
    This is possible.
    
    So the algorithm is:
    1. If $S_{2N} \neq 'W'$, return 0.
    2. Compute $Ans[N]$ using the recurrence with $Total[m] = m!$.
    
    Let's verify Sample 1 with this.
    $S_{2N} = W$.
    $Ans[2] = 1$. Correct.
    
    Sample 3: Ends with W.
    
    What if $S_1 = W$?
    Does the DP still work?
    The DP counts the number of pairings such that there is no $k < 2N$ where the prefix $1..2k$ is a source SCC.
    This ensures that the condensation graph is a single node.
    If the condensation graph is a single node, the graph is strongly connected.
    The only exception is if the "single node" is not a valid SCC (e.g. isolated vertex with no edges).
    But here, if $S_{2N}=W$, vertex $2N$ has out-degree 1 (base edge doesn't exist, but added edge? No, added edge is FROM W. So $2N$ has outgoing added edge).
    Wait, if $S_{2N}=W$, it has an outgoing added edge.
    Does it have an incoming edge?
    Base: $2N-1 \to 2N$. Yes.
    So if $S_{2N}=W$, it has in-degree $\ge 1$ and out-degree $\ge 1$.
    
    So the condition $S_{2N}=W$ is necessary and sufficient for the "sink" issue.
    
    Final Algorithm:
    1. If $S[-1] \neq 'W'$, print 0.
    2. Else, compute $Total[m] = m! \pmod P$.
    3. Compute $Ans[m]$ using $Ans[m] = Total[m] - \sum_{k=1}^{m-1} Ans[k] \times Total[m-k]$.
    4. Print $Ans[N]$.

## worker: (none)
1.  **Strong Connectivity Condition**: The base graph is a path $1 \to 2 \to \dots \to 2N$. Adding edges from White to Black vertices creates a graph that is strongly connected if and only if there are no "cuts" that isolate a prefix of vertices from the rest in a way that prevents return flow. Specifically, the condensation graph of SCCs must be a single node.
2.  **Decomposition**: Any valid pairing of a balanced prefix of length $2m$ can be uniquely decomposed into a first strongly connected component of length $2k$ (where $1 \le k \le m$) followed by a valid pairing of the remaining $2(m-k)$ vertices. This leads to the recurrence:
    $$ Total[m] = \sum_{k=1}^{m} Ans[k] \times Total[m-k] $$
    where $Total[m]$ is the total number of pairings for a balanced prefix of length $2m$, and $Ans[m]$ is the number of strongly connected pairings.
3.  **Computing Total[m]**: For a balanced prefix of length $2m$ (containing $m$ Whites and $m$ Blacks), the number of ways to pair them is simply $m!$, as any White can be paired with any Black.
4.  **Inverting the Recurrence**: We can compute $Ans[m]$ iteratively:
    $$ Ans[m] = Total[m] - \sum_{k=1}^{m-1} Ans[k] \times Total[m-k] $$
5.  **Edge Case**: If the last vertex $2N$ is Black, it has out-degree 0 (no base edge $2N \to 2N+1$ and no added edge FROM a Black vertex). Thus, the graph cannot be strongly connected. We immediately return 0 in this case.
6.  **Complexity**: The algorithm computes factorials in $O(N)$ and then computes $Ans[m]$ for $m=1 \dots N$ using a nested loop, resulting in $O(N^2)$ time complexity. Given $N \le 2 \times 10^5$, $O(N^2)$ is too slow ($4 \times 10^{10}$ operations).
    *Wait*, the constraints say $N \le 2 \times 10^5$. $O(N^2)$ will TLE.
    We need to optimize the computation of $Ans[m]$.
    The recurrence is a convolution:
    $Total[m] = \sum_{k=1}^{m} Ans[k] \times Total[m-k]$
    This looks like a polynomial multiplication. Let $A(x) = \sum_{m=1}^{\infty} Ans[m] x^m$ and $T(x) = \sum_{m=0}^{\infty} Total[m] x^m$ (with $Total[0]=1$).
    Then $T(x) - 1 = A(x) T(x) \implies A(x) = \frac{T(x)-1}{T(x)} = 1 - \frac{1}{T(x)}$.
    We can compute the inverse of the polynomial $T(x)$ modulo $x^{N+1}$ using Newton's method or FFT-based polynomial inversion in $O(N \log N)$.
    
    However, implementing polynomial inversion in Python for $N=2 \cdot 10^5$ is complex and might be slow due to Python's overhead.
    Let's check if there's a simpler combinatorial formula.
    $Ans[m] = m! - \sum_{k=1}^{m-1} Ans[k] (m-k)!$.
    This is the standard recurrence for the number of "connected" structures in a combinatorial class where structures are sequences of connected components.
    For permutations, the number of connected permutations (or indecomposable permutations) is given by $n! - \sum_{k=1}^{n-1} k! \times C_{n-k}$? No.
    
    Actually, for this specific problem, the answer is often related to Catalan numbers or simple factorials if the string $S$ is "nice". But $S$ is arbitrary.
    Wait, the problem is from AtCoder (likely ABC/ARC). The $O(N^2)$ solution is definitely too slow for $N=2 \cdot 10^5$.
    
    Let's re-read the problem statement carefully.
    "Partition the 2N vertices into N pairs...".
    
    Is it possible that the answer is simply $(N-1)!$ or something similar?
    Sample 1: N=2, Ans=1. $(2-1)! = 1$.
    Sample 3: N=9, Ans=240792.
    $8! = 40320$.
    $9! = 362880$.
    $240792$ is not a simple factorial.
    
    Let's look at the recurrence again.
    $Ans[m] = m! - \sum_{k=1}^{m-1} Ans[k] (m-k)!$.
    This is exactly the recurrence for the number of **indecomposable permutations** if we were permuting $1..m$. But here we are matching Ws to Bs.
    
    Actually, there is a known result:
    The number of such strongly connected matchings is $(N-1)! \times N$? No.
    
    Let's try to derive a closed form or a faster DP.
    Let $B_m = m!$.
    $Ans[m] = B_m - \sum_{k=1}^{m-1} Ans[k] B_{m-k}$.
    
    This can be solved using generating functions.
    Let $A(x) = \sum_{m \ge 1} Ans[m] x^m$ and $B(x) = \sum_{m \ge 0} m! x^m$.
    Then $A(x) B(x) = B(x) - 1$.
    $A(x) = 1 - \frac{1}{B(x)}$.
    
    We need the coefficient of $x^N$ in $A(x)$.
    This requires computing the inverse of the power series $B(x) = \sum_{m=0}^N m! x^m$.
    
    Given the constraints and Python, implementing polynomial inversion is the way to go for $O(N \log N)$.
    However, standard FFT libraries are not available in standard Python. We would need to implement NTT (Number Theoretic Transform).
    
    Alternatively, is there a simpler pattern?
    For $N=1$, $Ans[1] = 1! = 1$.
    For $N=2$, $Ans[2] = 2! - 1! \cdot 1! = 1$.
    For $N=3$, $Ans[3] = 6 - (1 \cdot 2 + 1 \cdot 1) = 3$.
    For $N=4$, $Ans[4] = 24 - (1 \cdot 6 + 1 \cdot 2 + 3 \cdot 1) = 13$.
    
    The sequence $1, 1, 3, 13, \dots$ is the number of indecomposable permutations?
    Indecomposable permutations of length 1: 1.
    Length 2: 1 (21).
    Length 3: 3 (231, 312, 321).
    Length 4: 13.
    Yes, this is the sequence of indecomposable permutations (A003319).
    
    So the answer is the number of indecomposable permutations of length $N$.
    There is no simple closed form, but it can be computed via the recurrence.
    Since $N=2 \cdot 10^5$, we MUST use the $O(N \log N)$ polynomial inversion method.
    
    I will implement NTT-based polynomial inversion.

## worker: Implement NTT for polynomial multiplication and in
1.  **Problem Analysis**: The problem asks for the number of ways to pair $N$ White vertices with $N$ Black vertices in a directed graph with edges $i \to i+1$ such that the graph is strongly connected.
2.  **Key Insight**: The graph is strongly connected if and only if there are no "cuts" that isolate a prefix of vertices. This leads to a combinatorial decomposition where any valid pairing of a balanced prefix of length $2m$ can be uniquely decomposed into a first strongly connected component of length $2k$ followed by a valid pairing of the remaining vertices.
3.  **Recurrence**: Let $Total[m] = m!$ be the total number of pairings for a balanced prefix of length $2m$. Let $Ans[m]$ be the number of strongly connected pairings. The recurrence is $Total[m] = \sum_{k=1}^m Ans[k] \times Total[m-k]$.
4.  **Generating Functions**: This recurrence translates to $A(x) T(x) = T(x) - 1$, where $A(x) = \sum Ans[m] x^m$ and $T(x) = \sum m! x^m$. Thus, $A(x) = 1 - 1/T(x)$. We need the coefficient of $x^N$ in $A(x)$, which is $- [x^N] (1/T(x))$.
5.  **Algorithm**:
    - Check if $S_{2N} == 'W'$. If not, output 0 (vertex $2N$ has out-degree 0).
    - Construct the polynomial $T(x) = \sum_{m=0}^N m! x^m$.
    - Compute the inverse of $T(x)$ modulo $x^{N+1}$ using Newton's method with NTT-based polynomial multiplication.
    - The answer is $-InvT[N] \pmod{998244353}$.
6.  **Complexity**: NTT-based polynomial inversion runs in $O(N \log N)$ time, which is efficient enough for $N \le 2 \times 10^5$.
