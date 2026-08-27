
## ideation
<analysis>

## worker: Implement the full solution in Python: parse input
The solution works as follows:

1. **Conflict detection**: For each letter `c` appearing in `S`, all positions where `S[i] == c` must end up as the same letter in `T`. If two positions with the same source letter require different targets, it's impossible → output `-1`.

2. **Graph construction**: Build a functional mapping `target[c]` for each source letter. This defines a directed graph on the 26 letters where each node has out-degree at most 1.

3. **Component analysis via DSU**: Union each source letter with its target letter. This groups letters into connected components (undirected). For each component:
   - If it contains a "fixed point" (a letter `c` with `target[c] == c`), we can map every other letter directly to its final target in `size` operations.
   - If it has no fixed point (pure cycle), we need `size + 1` operations: one extra operation to temporarily map some letter to itself (or an unused letter) to break the cycle, then map the rest.

4. **Complexity**: O(N + 26·α(26)) time, O(26) space.
