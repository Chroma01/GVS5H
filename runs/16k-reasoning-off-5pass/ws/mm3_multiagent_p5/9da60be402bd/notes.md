
## ideation
We need to compute the shortest walk from i to j whose edge labels form a palindrome. N ≤ 100, so N² = 10,000 pairs.

A walk with a palindromic label string can be seen as two synchronized walks:
- Forward from i to some middle state.
- Backward from j (walking edges in reverse) to the same middle state.
- The labels on both walks must match at every step.
This is exactly a BFS on the *product graph* whose vertices are ordered pairs (u, v) of original vertices. An edge (u, v) → (u', v') exists iff there is a label L with a forward edge u → u' and a reverse edge v' → v (both labeled L).

The shortest palindrome is found when the two halves meet:
- Even length 2k: meet at a vertex u, so we reach state (u, u) after k product-graph steps.
- Odd length 2k+1: meet at an edge u → v, so we reach state (u, v) with an original edge u → v after k product-graph steps.

Thus for every pair (i, j) we need the shortest distance in the product graph to the set of accepting states:
- Even targets: all (u, u).
- Odd targets: all (u, v) where the original graph has an edge u → v.

We can compute both distances simultaneously by a single multi-source BFS on the *reverse* product graph starting from all accepting states. The reverse product graph has an edge (u', v') → (u, v) iff there is a label L with u → u' and v' → v. Its total edge count is Σₗ |Eₗ|², bounded by about 3.85 million for N=100 (worst-case dense graph with even label distribution). This is very small and easily traversed once.

We run two BFS (or one BFS with two distance arrays) from the two types of accepting states on the reverse product graph. For each state (i, j) we obtain:
- d_even = shortest distance to any (u, u)
- d_odd = shortest distance to any (u, v) with edge u → v
Then the answer for (i, j) is:
- 0 if i == j (already covered by d_even = 0)
- else min(2·d_even, 2·d_odd + 1) if the corresponding distance is not -1.
- -1 if both are -1.

The BFS does not need to store the full product graph; we generate reverse neighbors on the fly using precomputed incoming adjacency lists grouped by label. Each state is processed at most once, giving total time O(Σₗ |Eₗ|²) ≈ 4·10⁶ operations and O(N²) memory.

## worker: Implement the solution in Python: read input, buil
The algorithm uses the standard "meet-in-the-middle" product‑graph BFS for shortest palindrome paths.  
Key points:  
- We run a BFS on the *reverse* product graph starting from all accepting states.  
- The reverse product graph has at most Σₗ |Eₗ|² edges (≈3.85M in worst case), which is tiny.  
- We store only incoming adjacency lists grouped by label, so generating reverse neighbors is fast.  
- Two BFS runs give `d_even` and `d_odd`; the answer is `min(2·d_even, 2·d_odd+1)` (with 0 for `i==j`).  
- Total time is well under a second for N=100.
