
## ideation
**Restating the task.** For every root‑to‑node chain (the current DFS stack path), we need the longest *contiguous suffix* of that chain whose node values are all distinct; among all such windows over all nodes, report (max total edge length, min node count as tie‑break).

**Core difficulty.**
1. Recognizing this is a *sliding window over the DFS stack*: the window's left boundary `start` is monotone non‑decreasing **along a single root‑to‑leaf chain**, but must be restored when backtracking so siblings are independent.
2. Doing it in O(n) without recomputation, and in Python without blowing the recursion limit (n up to 5·10⁴, tree can be a path ⇒ depth 5·10⁴).

**Correct formulation.**
- Maintain `distStack` where `distStack[i]` = distance from root to the chain node at depth index `i`, `distStack[0] = 0`.
- Maintain `lastIdx[value]` = chain index of the most recent (deepest) ancestor-or-self on the *current* chain holding that value; `-1`/absent if none.
- On entering node `u` at chain index `k` with inherited left boundary `start`:
  - `old = lastIdx[nums[u]]`; `start = max(start, old + 1)`;
  - set `lastIdx[nums[u]] = k`;
  - candidate: `length = distStack[k] - distStack[start]`, `nodes = k - start + 1`;
  - recurse into children with this `start` and index `k+1`.
- On exiting: restore `lastIdx[nums[u]] = old` (or delete) and pop `distStack`.
- Answer update: `if length > best or (length == best and nodes < bestNodes)`.

**Why only the maximal window per endpoint suffices.** All edge lengths ≥ 1, so any strictly shorter (sub‑)window ending at the same node has strictly smaller length; it can never tie the global maximum unless its own endpoint's maximal window already exceeds the maximum (contradiction). So we don't need to enumerate sub‑windows for the min‑nodes tie‑break.

**Indexing pitfall.** Be consistent: either `distStack[i]` = prefix distance to the i‑th chain node (then `length = distStack[k] - distStack[start]`, `nodes = k - start + 1`), or a `prefix` array of length depth+1 with `length = prefix[k+1] - prefix[start]`. Mixing the two off‑by‑one conventions is the most likely bug. Note the plan text mixes both (`prefix[k+1]-prefix[start]` with `nodes = k+1-start+1`), which is inconsistent with `nodes = k - start + 1`; verify against Example 1.

**Other pitfalls.**
- Recursion depth: must use an iterative DFS with explicit enter/exit events (or `sys.setrecursionlimit` + a big‑stack thread). Iterative is safer/faster.
- Restoring `lastIdx` **and** popping `distStack` at exit — forgetting either corrupts sibling subtrees.
- `start` must be carried per stack frame (not a global mutable), so backtracking automatically resets it.
- Initialize answer to `[0, 1]` (single node path). Example 2 (`n=2`, both values 2) must yield `[0,1]`.
- Values up to 5·10⁴ ⇒ use a preallocated list `lastIdx = [-1] * (max_val+1)` instead of a dict for speed.
- Undirected edges: build adjacency both ways, skip parent (or use visited).
- Avoid `List` import issue: `from typing import List`.

**Sanity check on Example 1.** edges: 0‑1(2), 1‑2(3), 1‑3(5), 1‑4(4), 2‑5(6); nums=[2,1,2,1,3,1]. Chain 0→1→4: values 2,1,3 distinct, length 2+4=6, nodes 3. Chain 0→1→2→5: values 2,1,2,1 — window for node 5 must start at index 2 (node 2) because nums[2]=2 duplicates nums[0]... actually at node 2 (value 2, dup of node 0 at idx 0) start becomes 1; at node 5 (value 1, dup of node 1 at idx 1) start becomes 2 ⇒ path 2→5, length 6, nodes 2. Max length 6, min nodes 2 ⇒ `[6,2]`. ✓

## worker: Implement the complete solution in one pass: build
- Built weighted adjacency list; ran a fully **iterative** DFS (explicit frames holding `(node, parent, start, value, oldIdx, child_iterator)`) so depth up to 5·10⁴ is safe.
- Fixed convention: `dist[i]` = root distance of the i-th chain node, `dist=[0]` for the root. Entering node at index `k`: `old = lastIdx[val]`, `start = max(start, old+1)`, `lastIdx[val] = k`, candidate `length = dist[k]-dist[start]`, `nodes = k-start+1`.
- `start` is stored per-frame (`s2` is passed to children), so sibling branches are independent; on exit we restore `lastIdx[val] = old` and pop `dist`, keeping the state exactly matching the current root-to-node chain.
- Only the maximal distinct-value window ending at each node is considered — valid because all edge lengths ≥ 1, so any shorter suffix window at the same endpoint has strictly smaller total length and can never tie the optimum.
- Answer initialized to `[0, 1]` (single-node path); verified Example 1 → `[6,2]` and Example 2 → `[0,1]` by hand trace.
- Complexity: O(n) time, O(n) memory.
