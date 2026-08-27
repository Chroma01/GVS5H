
## ideation
**Core Difficulty**: The problem asks for the minimum number of global character replacement operations to transform string $S$ into string $T$. The key constraints are:
1.  **Global Replacement**: Replacing 'a' with 'b' changes *all* occurrences of 'a' in the current string. This implies a functional dependency: if $S[i]$ needs to become $T[i]$, then all positions $j$ where $S[j] == S[i]$ must also eventually become $T[j]$.
2.  **Consistency Check**: If $S[i] == S[j]$ but $T[i] \neq T[j]$, it's impossible because a single character in $S$ cannot map to two different characters in $T$.
3.  **Cycle Detection**: If the required mappings form a cycle (e.g., $a \to b$, $b \to c$, $c \to a$), we can never resolve the first character to its target without breaking the target of the second, etc. In such cases, it's impossible.
4.  **Counting Operations**: We need to count the minimum steps. Since one operation can change all instances of a character, we want to group the necessary changes into the fewest steps.

**Candidate Approaches**:
1.  **Graph Construction & DFS**:
    *   Build a directed graph where an edge $u \to v$ exists if every occurrence of character $u$ in $S$ must become character $v$ in $T$.
    *   First, validate consistency: For each char $c$ in 'a'-'z', check if it maps to exactly one target char. If it maps to multiple or none (if not present in S but needed? No, only chars in S matter), proceed.
    *   Detect cycles in this graph. If a cycle exists, output -1.
    *   Count operations: The number of operations is the number of nodes in the graph that have an outgoing edge (i.e., $mapping[c] \neq c$). Wait, is it just the count of edges?
        *   Let's re-evaluate the counting logic based on Sample 1:
            *   $S$: afbfda, $T$: bkckbb
            *   Mappings derived from indices:
                *   'a' (at 0, 4) -> 'b' (at 0, 4). So $a \to b$.
                *   'f' (at 1) -> 'c' (at 1). So $f \to c$.
                *   'b' (at 2, 3) -> 'k' (at 2, 3). So $b \to k$.
                *   'd' (at 5) -> 'b' (at 5). So $d \to b$.
            *   Graph: $a \to b$, $f \to c$, $b \to k$, $d \to b$.
            *   Are there cycles? No.
            *   Operations needed:
                1.  Replace 'b' with 'k' (S becomes afkfkda). Now 'b' is gone, 'k' is there.
                2.  Replace 'a' with 'b' (S becomes bfcfdb).
                3.  Replace 'f' with 'c' (S becomes bkckdb).
                4.  Replace 'd' with 'b' (S becomes bkckbb).
            *   Total 4.
            *   Notice that $a \to b$ and $d \to b$ both target 'b'. Can we do them together? No, because replacing 'a' affects 'a's, replacing 'd' affects 'd's. They are independent sources.
            *   However, consider if we had $a \to b$ and $b \to c$.
                *   If we do $a \to b$ first, we get more 'b's. Then $b \to c$ converts original 'b's AND the new 'b's (from 'a') to 'c'. This is allowed and efficient.
                *   If we do $b \to c$ first, original 'b's become 'c'. Then $a \to b$ converts 'a's to 'b'. Result: 'b's and 'c's. Correct.
                *   Does the order matter for the count? No, the count is simply the number of characters in $S$ that need to change. Why? Because each character $x$ in $S$ that needs to become $y$ ($x \neq y$) requires exactly one operation "replace $x$ with $y$". Even if $x$ is part of a chain ($x \to y \to z$), we still need one operation for $x$ and one for $y$.
                *   Wait, is it possible to optimize? "Choose x, y and replace every occurrence of x with y".
                *   If we have $a \to b$ and $b \to c$.
                    *   Op 1: $a \to b$. (Count = 1)
                    *   Op 2: $b \to c$. (Count = 2)
                    *   Total 2.
                    *   Is it possible to do it in 1? No, we need to change 'a' to 'b' AND 'b' to 'c'. One op changes one letter type.
                *   So the answer is simply the number of unique characters $c$ in $S$ such that $mapping[c] \neq c$.
    *   Wait, let's double check Sample 4: $S=$ abac, $T=$ bcba.
        *   Indices:
            *   0: a->b
            *   1: b->c
            *   2: a->c (Conflict! 'a' maps to 'b' at index 0 and 'c' at index 2).
            *   Output: -1.
        *   My logic holds: Check consistency first.
    *   Sample 3: $S=$ abac, $T=$ abrc.
        *   0: a->a
        *   1: b->b
        *   2: a->r (Conflict with 0: a->a).
        *   Output: -1.

    **Refined Algorithm**:
    1.  Initialize a map `mapping` from char to char, initially empty.
    2.  Iterate $i$ from 0 to $N-1$:
        *   $u = S[i]$, $v = T[i]$.
        *   If $u$ is already in `mapping`:
            *   If `mapping[u]` != $v$, return -1 (Inconsistent mapping).
        *   Else:
            *   `mapping[u] = v`.
    3.  Check for cycles in the `mapping` graph.
        *   The graph consists of nodes 'a' through 'z'. Edges are defined by `mapping`.
        *   Since there are only 26 nodes, we can use DFS or Union-Find or simple iteration.
        *   Actually, since it's a functional graph (each node has at most 1 outgoing edge), cycles are easy to detect.
        *   We need to detect if there is a cycle reachable from any node that is part of a required change?
        *   Actually, if there is a cycle anywhere in the mapping of characters present in $S$, is it always impossible?
            *   Example: $S=$ "ab", $T=$ "ba".
                *   $a \to b$, $b \to a$. Cycle.
                *   Op 1: $a \to b$. $S$ becomes "bb". Target "ba". Fail.
                *   Op 1: $b \to a$. $S$ becomes "aa". Target "ba". Fail.
                *   Impossible. Return -1.
            *   So yes, any cycle involving characters that need to change makes it impossible.
            *   What if the cycle is $a \to b \to a$ but neither $a$ nor $b$ appear in $S$? Then it doesn't matter. We only care about characters present in $S$.
            *   So, detect cycles in the subgraph induced by characters present in $S$.
    4.  If no cycles and consistent:
        *   Count how many characters $c$ in `mapping` satisfy `mapping[c] != c`.
        *   Note: Only count characters that actually exist in $S$. If a char is in mapping but not in $S$, it's irrelevant (though our construction ensures we only add to mapping if $S[i]$ is encountered).
        *   Wait, is it possible that a character in $S$ maps to itself? Yes ($a \to a$). That costs 0 operations.
        *   So result = count of $c \in \text{keys}(\text{mapping})$ where $mapping[c] \neq c$.

## worker: Read the input values $N$, $S$, and $T$ from stand
1.  **Consistency Check**: The first step iterates through the strings $S$ and $T$. If a character $x$ in $S$ appears at multiple positions, it must map to the same character $y$ in $T$ at all those positions. If $S[i] == S[j]$ but $T[i] \neq T[j]$, the transformation is impossible, so we output -1.
2.  **Cycle Detection**: The mapping forms a directed graph where each node (character) has at most one outgoing edge. If there is a cycle (e.g., $a \to b \to c \to a$), we cannot resolve the characters to their targets because replacing one would break the target of another or create an infinite loop of dependencies. We use DFS with a `state` array (0: unvisited, 1: visiting, 2: visited) to detect cycles. If a cycle is found involving any character present in $S$, we output -1.
3.  **Counting Operations**: If the graph is consistent and acyclic, the minimum number of operations is simply the count of unique characters in $S$ that are not already equal to their target character in $T$. Each such character $x$ (where $x \neq mapping[x]$) requires exactly one operation "replace $x$ with $mapping[x]$". The order of operations can be chosen (e.g., topological sort order) to ensure correctness, but the count remains the number of non-fixed-point characters.

## worker: Run the code against the provided sample inputs to
The code implements the logic derived in the thought process:
1.  **Consistency Check**: Iterates through $S$ and $T$. If a character $u$ in $S$ maps to different characters in $T$ at different positions, it prints -1.
2.  **Cycle Detection**: Uses DFS with a `state` array (0: unvisited, 1: visiting, 2: visited) to detect cycles in the functional graph formed by the mappings. If a cycle is found involving any character present in $S$, it prints -1.
3.  **Counting Operations**: Counts the number of unique characters in $S$ where the mapped character is different from the original character. This count represents the minimum operations required.

The logic handles the constraints ($N \le 2 \times 10^5$) efficiently because the consistency check is $O(N)$ and the cycle detection is $O(26)$ (constant time relative to $N$).
