
## ideation
The core difficulty lies in correctly modeling the transformation as a functional graph and handling the "cycle breaking" constraint.

1.  **Feasibility Check**:
    *   **Consistency**: For each position `i`, `S[i]` must map to `T[i]`. If `S[i]` appears again at `j` but `T[i] != T[j]`, it's impossible.
    *   **Injectivity**: If two different characters `S[i]` and `S[j]` map to the same `T[k]` and `T[l]` (i.e., `T[i] == T[j]` but `S[i] != S[j]`), it's impossible because we can't distinguish them later.

2.  **Graph Construction**:
    *   Create a directed graph where an edge exists from `u` to `v` if character `u` in S must become `v` in T.
    *   Self-loops (`u -> u`) don't require any operation.
    *   Non-self-loop edges represent necessary changes.

3.  **Cycle Handling**:
    *   If the graph contains a cycle, we need an extra operation to "break" the cycle (using a temporary character).
    *   However, we can only break a cycle if there is at least one character *not* currently involved in the mapping (a "spare" character).
    *   If all 26 lowercase letters are present in S (meaning the mapping is a permutation of all 26 chars) and there is a cycle, we have no spare character to break the cycle, making it impossible.
    *   If there is a cycle but not all 26 chars are used in S, we can use one of the unused chars as a buffer, adding 1 to the operation count.

4.  **Counting Operations**:
    *   Count the number of unique non-self-loop edges in the mapping. Let this be `K`.
    *   If there are no cycles, the answer is `K`.
    *   If there is at least one cycle:
        *   If `len(set(S)) == 26` and there is a cycle: return -1.
        *   Otherwise: return `K + 1`.

Pitfalls:
- Forgetting to check injectivity (two different S chars mapping to same T char).
- Miscounting operations: self-loops don't count.
- Incorrectly determining if a cycle exists or if a spare character is available.
- The condition for impossibility with cycles is specifically when the mapping is a permutation of all 26 characters AND contains a cycle. If it's not a full permutation, a spare character exists.

## worker: [todo] Implement input reading and basic validatio
The solution implements the following logic:
1. **Consistency Check**: Ensures that each character in S maps to exactly one character in T. If `S[i]` maps to `T[i]` and `S[j]` (where `S[j] == S[i]`) maps to `T[j]`, then `T[i]` must equal `T[j]`.
2. **Injectivity Check**: Ensures that no two distinct characters in S map to the same character in T. This is verified by checking that all values in the mapping dictionary are unique.
3. **Graph Construction**: A functional graph is built where edges represent the mapping from characters in S to characters in T.
4. **Cycle Detection**: Using DFS, we detect if there are any cycles in the functional graph. Self-loops (`u -> u`) are ignored for cycle detection purposes since they don't require operations.
5. **Operation Counting**:
   - Count the number of non-self-loop edges (`K`).
   - If there are no cycles, the answer is `K`.
   - If there is a cycle:
     - If all 26 lowercase letters are present in S, it's impossible to break the cycle (no spare character), so return -1.
     - Otherwise, we can use a spare character to break the cycle, requiring `K + 1` operations.
