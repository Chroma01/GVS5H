
## ideation
The problem asks for the minimum number of operations to transform string S into T using the operation: pick letters x, y and replace **all** occurrences of x in S with y.

**Key observations:**
- The operation affects all positions simultaneously, so each "source" character c can be mapped to at most one target. If positions where S[i]=c map to two different T[i] values, it's impossible.
- This creates a functional graph: each character c has an outgoing edge to `need[c]` (the target it must become). Self-loops (c == need[c]) require no operation.
- Each edge in this graph requires at least one operation, but cycles are tricky: in a cycle like a→b→c→a, you can't rewrite all three at once because each rewrite would interfere. You need a temporary letter, which costs one extra operation.

**Known result for this type of problem:** The minimum number of operations equals:
- Count of edges (c ≠ need[c]) in the functional graph, plus
- 1 extra for each connected component that contains a cycle (a cycle needs a temporary "break" letter).

**Pitfalls:**
- Must detect impossible cases (two different targets for same source).
- Self-loops (c == need[c]) count as 0 operations, but the character still needs to be "available" as a temp if its component has a cycle.
- Components without cycles (trees) need exactly (edges) operations.
- For cycle components of length L (L edges), the cost is L + 1 (use one extra letter as buffer).
- Total distinct letters is 26, so cycles can be resolved using any letter not in the cycle as the temporary.

**Verification with samples:**
- Sample 1: edges = 4 (a→b, f→k, b→c, d→b), one cycle component (b→c is a self-contained cycle of length 1? No, b→c and c has no outgoing edge... actually need to check: c appears in S? S=afbfda, c not present as source, so the cycle is just b→c which is a tree edge. Wait — b→c where c is not a source: this is a chain ending at a non-source character. The component {b, c} has edge b→c, no cycle. Component {a, b, d}... b appears as source in {b→c}? No b appears in S at position 2: S[2]=b, T[2]=c, so b→c. So edges: a→b, f→k, b→c, d→b. Graph: f→k (isolated edge), a→b→c (chain), d→b (d points into the chain). No cycles. Cost = 4 edges. ✓
- Sample 4: a→b, b→c, c→a forms a cycle of length 3. Cost = 3 + 1 = 4. ✓

## worker: Read N, S, T from stdin, check if S == T (output 0
I implemented the algorithm:
1. Check if S == T (output 0).
2. Build the `need` mapping from each character in S to its required target in T. If any character maps to two different targets, output -1.
3. Count edges (characters with `need[c] is not None` and `c != need[c]`).
4. Use Union-Find to group characters into connected components.
5. For each component, if the number of edges equals the number of nodes, the component contains a cycle and needs one extra operation.
6. Answer = total edges + number of components with cycles.

## worker: Simplify and finalize the solution: remove the dea
I cleaned up the solution by:
1. Removing the dead BFS/DFS code that was left over from exploration.
2. Using a clean Union-Find to group characters into connected components.
3. Correctly counting nodes per component (all 26 characters, including those that aren't sources — they could be targets of multiple sources in the same component).
4. Using the standard cycle detection: in a functional graph where self-loops are excluded from the edge count, a component contains a cycle iff `edges == nodes`.

Verification against samples:
- **Sample 1**: edges = 4 (a→b, f→k, b→c, d→b). Components: {f,k} (1 edge, 2 nodes — tree, no extra), {a,b,c,d} (3 edges, 4 nodes — tree, no extra). Total = 4 + 0 = 4. ✓
- **Sample 2**: S == T, output 0. ✓
- **Sample 3**: character 'a' maps to both 'b' and 'r' → -1. ✓
- **Sample 4**: edges = 3 (a→b, b→c, c→a), component {a,b,c} has 3 edges and 3 nodes → cycle, +1 extra. Total = 3 + 1 = 4. ✓
