
## ideation
The problem: partition a tree with NK vertices into N vertex-disjoint paths, each containing exactly K vertices (K-1 edges). Despite the phrase "length K", the N×K matrix and Sample 1 (K=2 → paths of 2 vertices) confirm K = number of vertices per path.

Core difficulty: deciding feasibility without enumerating partitions. Tree structure suggests a bottom-up DFS greedy.

Key idea: Root the tree arbitrarily. DFS(u) returns the number of vertices in an "unfinished" path ending at u that must extend upward to its parent (0 means the subtree is fully decomposed). Return values are in {0, 1, ..., K-1}.

At node u, collect non-zero return values from children. Each such value `a` is a dangling path of `a` vertices ending at a child of u. Using u as a connector:
- Two dangling paths a, b from different children can be completed through u iff a + 1 + b == K, i.e., a + b == K-1.
- At most one dangling path may continue upward through u (since u has only one parent edge); it becomes a+1. If a+1 == K, it completes and we return 0.
- If no child value continues up, u itself starts a new dangling path of length 1 (return 1). Special case K=1: every node is its own path; always "Yes".

Pairing strategy: since valid pairs must sum exactly to K-1, greedy pairing via a frequency map (or sorted two-pointer) is optimal: pair each value a with K-1-a. After all possible pairings, at most one value may remain; if ≥2 remain, answer is No. Edge cases: value a where a+a == K-1 needs pairing within its own count (pair count//2, leftover count%2).

At the root, there is no parent, so the returned value must be 0 (everything completed). If root returns non-zero, No.

Pitfalls:
- Recursion depth: NK up to 2×10^5 → use iterative DFS or sys.setrecursionlimit with care (Python recursion may still be risky; iterative post-order is safer).
- K=1 edge case: each path is a single vertex; always Yes (tree has N vertices).
- K=2: pairing values a=1 with b where a+b=1 → b=0 doesn't exist; so each node can have at most one child returning 1, and it returns 0 (1+1=2 completes). Actually a+b=K-1=1 needs (0,1) but 0 isn't collected... wait, values returned are ≥1, so for K=2, K-1=1, pairs need a+b=1 with a,b≥1 — impossible. So each child returning 1 must be extended: 1+1=2=K → completes, return 0. So a node with two children both returning 1 fails. Correct: star with center + 3 leaves (N=2,K=2, 4 vertices... center+3 leaves = 4 vertices) — paths of 2 vertices: center pairs with one leaf, other two leaves can't connect → No. Matches logic.
- Must ensure the "pass up" value: if leftover a exists, new value = a+1; if a+1 == K return 0 else return a+1. If no leftover, return 1 (unless K==1, handled separately).
- Pairing greedily: for each value v, pair with complement K-1-v. Process values in any order using counts; leftover detection: total unpaired count must be ≤1.

Complexity: O(NK) time, fine for 2×10^5.

## worker: Implement the complete solution: parse input, buil
- Interpretation: each path has exactly K vertices (confirmed by the N×K matrix and Sample 1 where K=2 gives 2-vertex paths).
- Algorithm: root tree at 1, iterative post-order DFS. `ret[u]` = length of unfinished path ending at u that must extend to parent (0 = subtree fully decomposed).
- At each node: collect non-zero child returns, greedily pair values a with K-1-a via frequency counts (exact-sum pairing makes greedy optimal). After pairing, at most one leftover value may remain (else No). Leftover a → return a+1 (0 if it reaches K). No leftover → return 1 (start new path at u).
- K=1 handled specially: always Yes.
- Root must return 0, else No.
- Complexity O(NK) time and memory; iterative DFS avoids recursion limits.
- Verified mentally on samples: Sample 1 → Yes; Sample 2 → No (node 3 gets two child values 1 from leaves 4 and 6... actually leaves return 1, node 3 has children 4,6 both returning 1, K-1=1, no pairing possible, two leftovers → No).
