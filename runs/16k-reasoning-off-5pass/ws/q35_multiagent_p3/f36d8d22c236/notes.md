
## ideation
The core difficulty lies in correctly modeling the operation as a permutation problem and handling the "free character" optimization for cycles.

1.  **Feasibility Check**:
    *   The operation replaces *all* occurrences of a character `x` with `y`. This implies a functional mapping from characters in `S` to characters in `T`.
    *   If `S[i]` maps to `T[i]` and `S[j]` maps to `T[j]` with `S[i] == S[j]` but `T[i] != T[j]`, it's impossible (not a function).
    *   If `S[i]` maps to `T[i]` and `S[j]` maps to `T[j]` with `S[i] != S[j]` but `T[i] == T[j]`, it's impossible (not injective, because two different source characters would need to become the same target character, but we can only replace one source character at a time globally, and distinct sources must remain distinct unless they are merged, which this operation doesn't allow directly in a reversible way for the final state. More precisely, if `a->c` and `b->c`, we can't do both because replacing `a` with `c` makes all `a`s into `c`s, and then replacing `b` with `c` makes all `b`s into `c`s. But if we do `a->c` first, the original `a`s are now `c`s. If we later do `b->c`, the original `b`s become `c`s. The problem is that we need the final string to have specific characters. If `S="ab", T="cc"`, we need `a->c` and `b->c`. We can do `a->c` (S="cb"), then `b->c` (S="cc"). This works? Wait.
    *   Let's re-evaluate injectivity. The operation is `replace all x with y`. This is a permutation on the alphabet if we consider the set of characters present. However, if two different characters in `S` map to the same character in `T`, is it impossible?
        *   Example: S="ab", T="cc".
        *   Op 1: x='a', y='c' -> S="cb".
        *   Op 2: x='b', y='c' -> S="cc".
        *   This works! So injectivity is NOT required in the general sense?
        *   Wait, let's look at Sample 3: S="abac", T="abrc".
        *   Mapping: a->a, b->b, a->r (Conflict! a maps to both 'a' and 'r'). This is impossible.
        *   Let's look at a case where injectivity fails but mapping is functional: S="aa", T="ab".
        *   Op: x='a', y='b' -> S="bb". Then we need one 'a' and one 'b'. We can't create an 'a' from 'b' easily if we don't have another character.
        *   Actually, the standard constraint for this specific problem (AtCoder ABC 279 F or similar) is that the mapping must be a **bijection** on the set of characters involved if we want to reverse it, but here we just want to reach T.
        *   Key Insight: The operation `replace x with y` is not invertible if `y` already exists in the string. If `y` exists, the information about the original `x` is lost if we later need to distinguish it.
        *   However, the standard solution for this problem (often seen in competitive programming) relies on the fact that if the mapping is not a permutation (i.e., not injective), it might still be possible?
        *   Let's check Sample 4: S="abac", T="bcba".
        *   Pairs: (a,b), (b,c), (a,b), (c,a).
        *   Mapping: a->b, b->c, c->a. This is a cycle a->b->c->a. It is a bijection.
        *   Sample 1: S="afbfda", T="bkckbb".
        *   Pairs: (a,b), (f,k), (b,c), (f,c) -> Conflict! f maps to k and c? No.
        *   S[1]='f', T[1]='k'. S[3]='f', T[3]='c'.
        *   So 'f' maps to 'k' and 'c'. This is a conflict. But Sample 1 Output is 4.
        *   Let's re-read Sample 1 carefully.
        *   S: a f b f d a
        *   T: b k c k b b
        *   Indices:
            0: a->b
            1: f->k
            2: b->c
            3: f->k  (Consistent with index 1)
            4: d->b
            5: a->b  (Consistent with index 0)
        *   Mapping: a->b, f->k, b->c, d->b.
        *   Is it injective?
            *   a->b
            *   d->b
            *   Two different source characters (a and d) map to the same target character (b).
        *   The sample output is 4, so it IS possible.
        *   Therefore, **injectivity is NOT required**. My initial plan point 1 was partially wrong regarding injectivity.
        *   However, **functionality IS required**. If `S[i]` maps to `T[i]` and `S[j]` maps to `T[j]` with `S[i]==S[j]` but `T[i]!=T[j]`, it's impossible.

2.  **Correct Logic**:
    *   **Step 1**: Check if the mapping `S[i] -> T[i]` is well-defined (functional). If `S[i] == S[j]` but `T[i] != T[j]`, return -1.
    *   **Step 2**: Construct the directed graph where edges are `u -> v` for each unique pair `(u, v)` in the mapping.
    *   **Step 3**: Analyze the graph. Since each node has out-degree at most 1 (functional), the graph consists of components where each component is a set of trees rooted on a cycle, or just a tree leading to a sink (if the target character is not in the source set? No, the nodes are characters 'a'-'z').
    *   Actually, since the domain is finite (26 chars), and each node has out-degree <= 1, the structure is a collection of components. Each component contains exactly one cycle or is a tree leading to a node with out-degree 0 (a sink).
    *   Wait, if `u -> v` exists, `v` might not map to anything if `v` doesn't appear in `S`.
    *   **Step 4**: Count operations.
        *   We can perform operations in any order.
        *   If we have a cycle `a->b->c->a`, we need 3 operations if we don't have a free character. If we have a free character `z` (not in S, or not involved in a way that blocks us), we can do `a->z`, `b->a`, `c->b`, `z->c`? No.
        *   Standard trick: For a cycle of length L, we need L operations. If there is a "free" character (a character that does not appear in S, or appears in S but maps to itself and we can use it? No, it must be a character that is not currently being "pivoted" in a way that causes conflict), we can reduce the cost of *one* cycle by 1.
        *   Specifically, if there is any character `c` from 'a'-'z' that is **not present in S** at all, we can use it as a temporary buffer. This allows us to break one cycle with `L-1` operations instead of `L`.
        *   What if all characters 'a'-'z' are present in S? Then we can't use a free buffer.
        *   What if a character is present in S but maps to itself? Can we use it?
            *   Example: S="a", T="b". Mapping a->b. Cycle? No, just a->b. b is not in S. So b is a sink.
            *   Example: S="ab", T="ba". Mapping a->b, b->a. Cycle a<->b. Length 2. No free char. Ops: 2. (a->c, b->a, c->b? No, c not in S. If c is not in S, we have a free char. So we can do a->c (1), b->a (1), c->b (1). Total 3? But cycle length is 2. With free char, we can do: a->c, b->a, c->b. That's 3. Wait.
            *   Standard result: For a permutation cycle of length L, cost is L. If a free character exists, cost is L-1 for one cycle, L for others.
            *   So, Total Cost = (Sum of lengths of all cycles) - (1 if free character exists else 0).
            *   What about non-cycle components (trees)?
                *   If `u -> v` and `v` is not in the domain (doesn't map to anything), it's a path ending in a sink.
                *   Example: a->b. b not in S. We just do `a->b`. 1 op.
                *   Example: a->b, b->c. c not in S. Ops: `a->b`? No, if we do `a->b`, we get `bb`. Then `b->c` gives `cc`. 2 ops.
                *   Generally, a tree component with `k` edges requires `k` operations.
                *   So, we only care about **cycles**. The number of operations is equal to the number of edges in the mapping graph, MINUS the savings from free characters on cycles.
                *   Wait, is it just the number of edges?
                *   Let `E` be the number of unique mappings `u -> v` where `u != v`.
                *   If there are no cycles, cost is `E`.
                *   If there are cycles, each cycle of length `L` contributes `L` to the cost. If we have a free character, we can reduce one cycle's cost by 1.
                *   So, Cost = `E` - (1 if there is a free character AND there is at least one cycle else 0).
    
    *   **Refined Plan**:
        1.  Read N, S, T.
        2.  Build a map `mapping` from char in S to char in T.
        3.  Check for conflicts: If `S[i]` is already in `mapping` and `mapping[S[i]] != T[i]`, return -1.
        4.  Identify all unique characters in S that are part of a mapping where `u != v`.
        5.  Build the graph of these mappings.
        6.  Find all cycles in the graph.
        7.  Count total edges `E` where `u != v`.
        8.  Check if there is a "free" character. A character `c` is free if it does not appear in `S`. (Note: Characters in S that map to themselves don't help as buffers because they are "occupied" by their position, but actually, if `c` is in S and `c->c`, can we use it? No, because replacing `c` with something else would break the target `c`. So only characters NOT in S are safe buffers).
        9.  If there is at least one character in 'a'-'z' that is not in `S`, we have a free buffer.
        10. If there is a free buffer and there is at least one cycle, subtract 1 from the total count of operations.
        11. The total operations is simply the number of unique mappings `u -> v` where `u != v`, adjusted by the cycle saving.
            *   Wait, does a non-cycle component ever save? No. Only cycles can be broken by a temporary variable.
            *   So, `Ans = E - (1 if (has_free_char and has_cycle) else 0)`.

## worker: (None)
1.  **Feasibility**: The operation `replace all x with y` implies a functional mapping from characters in `S` to characters in `T`. If any character in `S` maps to two different characters in `T`, it's impossible. This is checked by building the `mapping` dictionary.
2.  **Graph Structure**: The valid mappings form a functional graph where each node has an out-degree of at most 1. Such a graph consists of components, each containing exactly one cycle or being a tree leading to a sink (a node with no outgoing edge in the mapping).
3.  **Operation Count**:
    *   Each edge `u -> v` with `u != v` represents a necessary substitution.
    *   If the graph has no cycles, each edge can be resolved independently in 1 operation. Total operations = number of edges.
    *   If the graph has cycles, resolving a cycle of length `L` normally takes `L` operations. However, if there is a "free" character (a character not present in `S`), we can use it as a temporary buffer to break one cycle, reducing the cost for that cycle by 1 (from `L` to `L-1`).
    *   Therefore, the total operations = (Total number of edges where `u != v`) - (1 if there is at least one cycle AND at least one free character exists, else 0).
4.  **Complexity**:
    *   Building the mapping: $O(N)$.
    *   Finding cycles: The graph has at most 26 nodes (characters 'a'-'z'). Traversal is $O(26) = O(1)$.
    *   Overall time complexity: $O(N)$, which fits within the constraints ($N \le 2 \times 10^5$).
