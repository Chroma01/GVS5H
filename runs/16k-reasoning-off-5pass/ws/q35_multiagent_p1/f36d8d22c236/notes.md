
## ideation
The core difficulty lies in correctly counting the minimum operations while handling cycles in the character mapping graph.

1.  **Feasibility Check**:
    *   We must establish a mapping from each character `s` in `S` to the corresponding character `t` in `T` at the same position.
    *   If `S[i] != T[i]`, we require `S[i] -> T[i]`.
    *   **Conflict 1**: If `S[i]` is already mapped to a different character `T'[i]`, it's impossible (return -1).
    *   **Conflict 2**: If two different characters in `S` map to the same character in `T` (e.g., `S[i]='a'->'b'` and `S[j]='c'->'b'`), it's impossible because 'a' and 'c' would both become 'b', making them indistinguishable. So the mapping from S-char to T-char must be injective.

2.  **Counting Operations**:
    *   Each edge in the mapping graph (`s -> t`) represents one operation to change all occurrences of `s` to `t`.
    *   However, if there is a cycle in the mapping (e.g., `a -> b` and `b -> a`), we cannot simply apply these operations sequentially because applying `a->b` first destroys the original 'a's needed for the `b->a` step (or vice versa).
    *   To break a cycle of length $L$, we need $L+1$ operations if we use a temporary character. But wait, let's look closer.
    *   Actually, the standard result for this problem is:
        *   Count the number of distinct mappings (edges).
        *   If there is a cycle in the functional graph defined by the mappings, we need **one extra operation** to break the cycle.
        *   Why? Because in a cycle like $a \to b \to c \to a$, if we just do $a \to b$, then $b \to c$, we lose the original $a$'s before we can turn them into $c$'s (which is what the $c \to a$ part would have done if it were a cycle, but here the cycle is in the *required* mapping).
        *   More precisely: The graph consists of nodes 'a'-'z'. Edges are $u \to v$ if we need to change $u$ to $v$. Since each node has out-degree $\le 1$ (from the injective constraint on sources) and in-degree $\le 1$ (from the injective constraint on targets), the graph is a collection of disjoint paths and cycles.
        *   For a path, the number of operations is the number of edges.
        *   For a cycle, we need `number of edges + 1` operations because we need a temporary character to break the cycle.
        *   Therefore, the total operations = (total number of edges) + (1 if there is at least one cycle, else 0).

3.  **Algorithm**:
    *   Read N, S, T.
    *   If S == T, output 0.
    *   Build the mapping: `map[s] = t`. Check for conflicts.
        *   If `s` is already in map and `map[s] != t`, return -1.
        *   If `t` is already a target of some other `s'` (i.e., `t` is in the set of values of the map) and `s != s'`, return -1.
    *   Build the graph based on the valid mappings.
    *   Detect if there is any cycle. Since each node has out-degree $\le 1$, we can just traverse.
    *   Count edges. Let $E$ be the number of mappings.
    *   If there is a cycle, answer is $E + 1$. Else, answer is $E$.

## worker: Implement the feasibility check by building the ma
The solution first checks if S and T are identical, returning 0 if so. It then builds a mapping from characters in S to characters in T, ensuring that the mapping is a function (each S-char maps to at most one T-char) and injective (each T-char is mapped to by at most one S-char). If any conflict arises, it outputs -1.

After building the valid mapping, the problem reduces to counting the minimum operations to apply these character substitutions. Each mapping `s -> t` requires one operation. However, if the mapping graph contains a cycle, we need an extra operation to break the cycle using a temporary character. The graph is a collection of disjoint paths and cycles because each node has out-degree at most 1 and in-degree at most 1. The total operations are the number of edges (mappings) plus 1 if there is at least one cycle.
