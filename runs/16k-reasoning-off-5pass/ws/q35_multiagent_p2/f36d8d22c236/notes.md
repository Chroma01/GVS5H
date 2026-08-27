
## ideation
The core difficulty lies in correctly modeling the transformation process as a functional graph and understanding the cost associated with cycles versus paths in this graph.

1.  **Feasibility Check**: The operation replaces *all* occurrences of a character `x` with `y`. This implies a deterministic mapping. If two different characters in `S` (say `u` and `v`) map to the same character in `T` (i.e., `T[i] == T[j]` but `S[i] != S[j]`), it's impossible to distinguish them later or map them correctly because any operation on `u` would affect `v`'s position if they were ever merged, but more simply, the mapping from Source Char to Target Char must be a function. Specifically, if `S[i]` must become `T[i]`, then for any character `c` in `S`, all its occurrences must map to the same character in `T`. If `S[i] == S[j]` but `T[i] != T[j]`, it's impossible. This is the injectivity check (actually, it's checking if the relation is a well-defined function from S-chars to T-chars). Wait, the problem says "replace every occurrence of x in S with y". This means we define a mapping $M: \Sigma \to \Sigma$. For the transformation to be possible, for every index $i$, $M(S[i])$ must equal $T[i]$. This implies that if $S[i] == S[j]$, then $T[i]$ must equal $T[j]$. If this condition is violated, output -1.

2.  **Graph Construction**: Once feasibility is established, we have a mapping from each unique character in `S` to a unique character in `T`. Note that multiple characters in `S` might map to the same character in `T`? No, if $S[i] \neq S[j]$ but $T[i] == T[j]$, is that allowed? Yes. For example, S="ab", T="cc". Map: a->c, b->c. This is allowed. The mapping is from S-characters to T-characters. It is a function from the set of characters present in S to the set of characters present in T. It does not need to be injective on the domain of all 26 letters, but it must be a valid function. However, the reverse is not required.

3.  **Cost Calculation**:
    *   Each operation corresponds to changing the mapping for a specific source character $x$ to a new target $y$.
    *   We want to reach the target mapping $M_{target}$ where $M_{target}(c) = T[i]$ for any $i$ where $S[i]=c$.
    *   Let $U$ be the set of unique characters in $S$. For each $c \in U$, we have a required mapping $c \to M(c)$.
    *   If $c \to M(c)$ is already the identity (i.e., $c = M(c)$), no operation is needed for this character.
    *   If $c \neq M(c)$, we need to perform operations to change the mapping of $c$.
    *   The problem can be modeled as a directed graph where an edge exists from $u$ to $v$ if we need to change $u$ to $v$. Since each character $u$ has exactly one target $M(u)$, each node has out-degree at most 1.
    *   The graph consists of disjoint components, each being a tree rooted on a cycle or a path leading to a cycle or a fixed point.
    *   Actually, since we are relabeling, the standard result for this specific problem (AtCoder ABC 240 E is different, this is likely ABC 257 F or similar) is:
        *   Count the number of characters $c$ in $S$ such that $c \neq M(c)$. Let this be $E$ (edges that are not self-loops).
        *   Count the number of cycles in the functional graph defined by $c \to M(c)$. Let this be $C$.
        *   The minimum operations is $E + C$ if there is no "spare" character available to break cycles temporarily?
        *   Let's re-verify with Sample 4: S="abac", T="bcba".
            *   Map: a->b, b->c, c->a.
            *   Unique chars in S: {a, b, c}.
            *   $a \neq b$ (edge), $b \neq c$ (edge), $c \neq a$ (edge). $E=3$.
            *   Cycle: $a \to b \to c \to a$. One cycle. $C=1$.
            *   Result: $3 + 1 = 4$. Matches sample output.
        *   Sample 1: S="afbfda", T="bkckbb".
            *   Map: a->b, f->k, b->c, d->b.
            *   $a \neq b$, $f \neq k$, $b \neq c$, $d \neq b$. $E=4$.
            *   Graph: $a \to b \to c$. $f \to k$. $d \to b$.
            *   No cycles. $C=0$.
            *   Result: $4 + 0 = 4$. Matches sample output.
        *   Sample 2: S=T. $E=0, C=0$. Result 0.
        *   Sample 3: S="abac", T="abrc".
            *   $S[0]='a', T[0]='a'$. Map a->a.
            *   $S[1]='b', T[1]='b'$. Map b->b.
            *   $S[2]='a', T[2]='r'$. Map a->r.
            *   Conflict: a maps to 'a' and 'r'. Impossible. Output -1.

    *   Why $E + C$?
        *   Each edge $u \to v$ where $u \neq v$ represents a character that needs to be changed.
        *   In a path component (no cycle), we can resolve the mappings in $E$ operations by processing from the end of the chain backwards (or using a temporary if needed, but usually paths don't need extra ops beyond the edges themselves if we just apply the final mapping? No, we apply operations sequentially).
        *   Actually, the standard logic is:
            *   For a component that is a simple path (no cycle), the number of operations is equal to the number of non-identity edges.
            *   For a component that contains a cycle, we need an extra operation to break the cycle (to avoid overwriting a character that is needed later) unless we have a spare character.
            *   However, in this problem, we are replacing *all* occurrences.
            *   If we have a cycle $a \to b \to c \to a$, we cannot simply apply $a \to b$ because then all $a$'s become $b$'s, and we lose the original $a$'s which are needed to become $a$ at the end. We need a temporary.
            *   If we have a spare character (a character not present in S and not present in T? Or just not in S?), we can use it to break the cycle.
            *   Wait, does having a spare reduce the cost?
            *   In Sample 4, we had a spare (e.g., 'd' is not in S). The cost was 4, which is $E+C$. If the spare reduced the cost, it would be $E=3$. Since it is 4, the spare did *not* reduce the cost in this case?
            *   Let's check a case where a spare *does* help.
            *   S="a", T="b". Map a->b. E=1, C=0. Ans=1.
            *   S="ab", T="ba". Map a->b, b->a. E=2, C=1. Ans=3.
            *   Is there a case where Ans = E?
            *   Consider S="a", T="a". E=0, C=0. Ans=0.
            *   Consider S="abc", T="abd". Map a->a, b->b, c->d. E=1, C=0. Ans=1.
            *   It seems the formula $E + C$ is robust for this problem statement. The "spare" logic often applies to permutation cycles where you want to sort, but here the target mapping is fixed and we just relabel.
            *   Actually, I recall that if there is a cycle, you *always* need +1 operation for that cycle, regardless of spares, because you must break the cycle to resolve the dependencies. The only exception is if the cycle is of length 1 (self-loop), which is not counted in C.
            *   Therefore, the algorithm is:
                1. Validate mapping consistency.
                2. Build graph of unique chars in S.
                3. Count non-self-loop edges ($E$).
                4. Count cycles ($C$).
                5. Result is $E + C$.

## worker: (None)
1.  **Feasibility Check**: The operation replaces all occurrences of a character `x` in `S` with `y`. This implies a deterministic mapping. If two different characters in `S` (say `u` and `v`) map to the same character in `T`, it is allowed. However, if the same character in `S` (say `u`) maps to two different characters in `T` (i.e., `T[i] != T[j]` but `S[i] == S[j]`), it is impossible. We check this by building a dictionary `mapping` where `mapping[S[i]] = T[i]`. If a conflict arises, we print `-1`.

2.  **Graph Modeling**: We model the transformation as a directed graph where each unique character in `S` is a node, and there is a directed edge from `u` to `v` if `mapping[u] = v`. Since each character in `S` has exactly one target in `T`, each node has an out-degree of at most 1. This structure is a functional graph, consisting of disjoint components, each containing exactly one cycle or being a tree leading to a fixed point (self-loop).

3.  **Cost Calculation**:
    *   **Edges**: Each edge `u -> v` where `u != v` represents a character that needs to be changed. Let `E` be the count of such edges.
    *   **Cycles**: Each cycle in the graph represents a set of characters that depend on each other. To resolve a cycle, we need an extra operation to break the dependency chain (e.g., by temporarily mapping one character to a spare character, then resolving the rest, and finally mapping the spare to the correct target). Let `C` be the number of such cycles.
    *   **Formula**: The minimum number of operations is `E + C`. This holds because each non-identity mapping requires at least one operation, and each cycle requires an additional operation to break the circular dependency. This formula was verified against all sample cases, including Sample 4 where a cycle exists and the answer is `3 + 1 = 4`.

4.  **Complexity**:
    *   Time Complexity: $O(N)$ to read input and build the mapping. The graph traversal is over at most 26 nodes (unique lowercase English letters), so it is $O(1)$ effectively. Overall $O(N)$.
    *   Space Complexity: $O(1)$ for the mapping and graph structures (since alphabet size is fixed at 26).
