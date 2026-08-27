The operation rewrites all occurrences of one character `x` in S to another character `y`. This forms a functional graph from current characters to target characters — repeated operations allow chaining through intermediate letters. The reachable characters from any start form a set, and we need a mapping from each distinct character in S to its corresponding character in T, but we can use intermediate letters to "break" cycles.

Algorithm:
1. If S == T, answer is 0.
2. Build the required mapping `need[c]` = character `c` must become (the first occurrence where S[i] = c and T[i] != c, set target to T[i]). If we see two different targets for the same `c`, it's impossible (-1).
3. The dependency graph: for each character `c` where `need[c] = d` and `c != d`, `c` depends on being rewritten to `d` first.
4. The minimum number of operations is the number of edges in this functional graph. Each edge represents one rewrite. This is simply the count of pairs `(c, need[c])` where `c != need[c]`, because each such required transformation can be done independently in one operation (using any temporary letter if a cycle is involved — we can always break cycles using a fresh letter).

Wait — cycles of length > 1 can be resolved in `len(cycle)` operations by using an extra character, but the edge count equals the cycle length anyway. So the answer is simply the number of `(c, need[c])` pairs with `c != need[c]`.

Verification: Sample 1 — mapping: a→b, f→k, d→b, count=3? But answer is 4. Let me recount: S=afbfda, T=bkckbb.
- i=0: a→b
- i=1: f→k  
- i=2: b→c
- i=3: f→k (already set)
- i=4: d→b
- i=5: a→b (already set)

So edges: a→b, f→k, b→c, d→b. That's 4 edges, answer 4. ✓

Sample 4: S=abac, T=bcba.
- a→b, b→c, a→b, c→a. Edges: a→b, b→c, c→a = 3, but answer is 4.

Hmm. So the simple edge count is not always correct. Cycles of length > 1 (a→b→c→a) need an extra operation because you can't apply all three simultaneously — you need a temporary letter. The minimum is `cycle_length + 1` for a cycle of length ≥ 2.

So the correct formula: For each connected component of the dependency graph, if it's a tree (has a root with no outgoing edge), cost = number of edges. If it contains a cycle of length L ≥ 2, cost = number of edges + 1.

Actually, the standard result: answer = (number of edges with c ≠ need[c]) + (number of components that contain a cycle). Each such component needs one extra "temporary" operation.