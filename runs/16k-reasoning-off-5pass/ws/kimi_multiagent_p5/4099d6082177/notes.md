
## ideation
The problem: partition a tree of NK vertices into N vertex-disjoint paths of exactly K vertices each (K-1 edges per path).

Core difficulty: deciding feasibility without exponential search. This is a known AtCoder problem (typical "tree path decomposition" greedy). The structure: root the tree anywhere, process bottom-up. Each subtree may leave at most one "dangling" (incomplete) path that must extend upward through the parent — because a path in the tree intersects a subtree in a connected segment, and at most one such segment can touch the parent edge.

Key greedy invariant: DFS returns to parent the length (in vertices) of the single unfinished path ending at the current node, or 0 if none. At node v:
- Collect lengths l_i returned by children (ignore zeros — those subtrees are fully resolved).
- v itself is one vertex. We can:
  - Pair two child paths through v: lengths a, b combine into a+b+1 vertices; valid only if a+b+1 == K (complete path formed). If a+b+1 > K it's invalid (paths can't overlap v twice); if < K it would create a "branch" that can never be completed later (since after passing v we can't come back) — actually a+b+1 < K joined through v creates a path with both ends below v... no wait, joining two child paths through v makes a path whose both endpoints are in subtrees; it can never be extended further, so it must be exactly K. Correct.
  - At most one child path can be extended by v (v appended, length l+1), passed upward. If l+1 == K, it completes and v returns 0.
  - If no child path is extended, v starts a new path of length 1 (returns 1), unless K==1 (then v alone is complete, returns 0).

Pairing strategy (two pointers on sorted lengths): smallest s and largest l.
- If s + l + 1 == K: pair them (complete path), remove both.
- If s + l + 1 > K: l cannot pair with anything (s is minimal), so l must be the one extended upward. But we can only extend one — so if this happens, l becomes the candidate to pass up; continue pairing the rest. If a second unpairable appears → impossible.
- If s + l + 1 < K: s cannot pair with anything (l is maximal), so s must be extended upward — same logic: at most one such survivor allowed.

So: at most one leftover after pairing; if leftover exists, extend it (l+1); if that equals K, return 0 else return l+1. If no leftover, return 1 (start new path at v) — but careful: if K==1, return 0. Also if leftover l+1 > K impossible (can't happen since l ≤ K-1 enforced: any child returning K would have been cut to 0 already... child returns l+1 only if < K, so l ≤ K-1; but pairing condition a+b+1==K with both ≥1 means each ≤ K-1, fine).

Edge cases: K=1 → always Yes (each vertex its own path). N=1 → tree must itself be a path of K vertices (the greedy handles this: root must return 0). Root final check: root's returned value must be 0 (no dangling path), else No.

Pitfalls:
- Recursion depth up to 2e5 → use iterative DFS or sys.setrecursionlimit with care (Python recursion at 2e5 risky; use iterative post-order).
- Sorting child lists: total work sum of deg log deg ≤ O(V log V), fine.
- The leftover logic: when s+l+1 != K, the unpairable one must be the unique survivor; track survivor count, fail if >1.
- When extending survivor: if survivor+1 == K return 0, else return survivor+1. Note survivor+1 < K required to pass up; if survivor+1 > K impossible (can't happen as argued).
- Also need: if there's a survivor AND we could also just not extend... no — survivor must be extended through v, no choice. And if no survivor, v starts fresh path of length 1 (return 1, or 0 if K==1).

Wait, subtle: when no child lengths at all (leaf), return 1 (or 0 if K==1). Correct.

Another subtlety: when s+l+1 < K, s must survive — but actually could s be extended and l also be... no, only one path can pass through v upward. Correct.

Complexity: O(V log V). V = NK ≤ 2e5. Fine.

## worker: Implement the complete solution: read input, build
- Root tree at 1, iterative post-order (avoids recursion limit at 2e5).
- Each node returns length of one dangling path (0 = subtree fully decomposed). At most one dangling path can cross the parent edge, so any unpairable child path must be the unique survivor; a second one → impossible.
- Two-pointer pairing on sorted child lengths: sum+1==K completes a path; >K forces the large one to be the survivor; <K forces the small one.
- Survivor extended by current vertex (+1); if it reaches K it's completed (return 0). No survivor → start a fresh path of length 1.
- K==1 trivially Yes. Final answer Yes iff no failure and root returns 0.
- Complexity O(V log V) from per-node sorts (sum bounded by O(V log V)).

## worker: Verify the greedy solution against samples and edg
- Verified the greedy on the provided samples mentally and by case analysis:
  - Sample 1 (path-ish tree 1-2-3-4, 2-5-6, N=3,K=2): leaves return 1; node 3 gets child 4's 1 → 1+1=2=K → completes, returns 0; node 5 similarly completes with 6; node 2 gets child 3's 0 and 5's 0 → returns 1; root 1 gets 1 → completes → Yes.
  - Sample 2 (edges 1-2,2-3,3-4,2-5,3-6): node 3 has children 4 and 6 both returning 1 → 1+1+1=3 > K=2, so one must survive; the other also can't pair → second survivor → fail → No. Correct.
- Edge cases checked:
  - K=1: trivially Yes (handled early).
  - N=1: tree must itself be a simple path of K vertices. On a path, each internal node has exactly one child with nonzero up-value, which becomes the survivor and gets extended; a branching node yields ≥2 survivors → fail. Root must return 0. Correct.
  - Star graph with K=2: center pairs leaf 1's two at a time (1+1=K); with even number of leaves (N even) → Yes, odd → center left with one survivor extended to 2=K → up[root]=0... wait: odd leaves means V = leaves+1 must equal NK=2N → leaves odd → V even → consistent; one leftover 1 at center, extended → 2=K → returns 0 → Yes. E.g., star with 3 leaves (V=4, N=2, K=2): pairs (1,1) and center+leaf → Yes. Correct.
  - Deep chain (V=2e5, K large): iterative DFS avoids recursion limits; each node has ≤1 nonzero child, O(V) total.
- Bug check on the survivor logic: when `i == j` (odd count leftover), that element must be the survivor; if a survivor already exists → impossible. Correct. When `s+l+1 > K`, `l` is unpairable with the minimum `s`, hence with anything; it must survive. When `< K`, symmetric for `s`. At most one survivor ever allowed because only one path can cross the edge to the parent.
- Input parsing switched to `sys.stdin.buffer.read().split()` for speed and safety with the final line lacking newline.
- Complexity: O(V log V) from per-node sorting (sum of deg log deg ≤ O(V log V)); V ≤ 2e5.
- One subtlety verified: a child can never return a value ≥ K (values only increment when < K, and reset to 0 at K), so survivor+1 ≤ K always; no overflow case needed.
