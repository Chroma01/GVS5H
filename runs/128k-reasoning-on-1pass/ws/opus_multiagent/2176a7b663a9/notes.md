
## ideation
**Restating the graph.** Edge {i,j} ⟺ [L_i,R_i] ∩ [L_j,R_j] = ∅ (i.e. R_i < L_j or R_j < L_i). Since L_i ≤ R_i, no self-loops. The graph is the *complement* of an interval-overlap graph, so it is typically dense (up to Θ(N²) edges) — building it or running BFS/Dijkstra per query is hopeless for N,Q = 2·10⁵. Core difficulty: exploit structure so each query is O(1)/O(log N) after O(N) preprocessing.

**Structural fact 1 (connectivity).** Let A = interval with minimum R, B = interval with maximum L.
- If a vertex v has *some* neighbor u, then either R_u < L_v (⇒ R_A ≤ R_u < L_v, so A–v is an edge) or L_u > R_v (⇒ L_B ≥ L_u > R_v, so B–v is an edge). Hence every non-isolated vertex is adjacent to A or to B.
- If R_A < L_B, A–B is an edge and all non-isolated vertices form one component. If R_A ≥ L_B, take v adjacent to A (R_A < L_v) and w adjacent to B (R_w < L_B); then R_w < L_B ≤ R_A < L_v, so v–w is an edge, and again A–v–w–B connects everything.
⇒ **All non-isolated vertices lie in one component.** Answer is −1 iff s or t is isolated. Vertex i is isolated ⟺ no interval strictly left of it and none strictly right of it.

**Structural fact 2 (path length ≤ 4 vertices; explicit candidate set).** Define
- minLeft(v) = min{W_u : R_u < v}, minRight(v) = min{W_u : L_u > v} (INF if empty).
Note minLeft(L_i) and minRight(R_i) automatically exclude i itself.

Base = W_s + W_t. Candidates:
1. If [L_s,R_s] ∩ [L_t,R_t] = ∅: answer = Base (optimal, weights positive).
2. 3-vertex: Base + min( minLeft(min(L_s,L_t)), minRight(max(R_s,R_t)) ) — the middle vertex is disjoint from both; always a genuine path.
3. 4-vertex "mixed": Base + min( minLeft(L_s)+minRight(R_t), minLeft(L_t)+minRight(R_s) ). Validity: if s,t intersect, a with R_a < L_s and b with L_b > R_t must be disjoint — else L_b ≤ R_a < L_s and L_b > R_t give R_t < L_s, contradicting intersection.

Domination proofs (why nothing longer/other is needed): for any path with ≥4 vertices s–a–…–b–t, weight ≥ Base + W_a + W_b where a is adjacent to s and b to t.
- a left of s & b right of t (or mirrored): candidate 3 ≤ Base + W_a + W_b, and it is a real path.
- a left of s & b left of t: whichever is "more left" (R_b < L_a ⇒ b, else a) is disjoint from both s and t, so candidate 2 ≤ Base + min(W_a,W_b).
- both right: symmetric.
Also, even when s,t are disjoint, candidates 2 and 3 are all ≥ Base, so taking the global min of all candidates is safe (no need to branch on validity).

**Preprocessing.** Coordinates in [1, 2N]. bestR[r] = min W over intervals with R = r; prefix-min ⇒ minLeft(v) = prefR[v−1]. bestL[l] = min W over intervals with L = l; suffix-min ⇒ minRight(v) = sufL[v+1]. O(N).

**Pitfalls.**
- Don't forget the disjoint (adjacent) case → answer W_s+W_t directly (also covered by taking min with Base when disjoint).
- Off-by-one: "strictly less/greater" (R_u < L_v, L_u > R_v), arrays sized 2N+2.
- INF handling: use a big sentinel (e.g. 4·10¹⁸) and only accept a candidate if all its parts are finite; guard against INF+INF overflow-into-answer by comparing with a threshold.
- Isolation test must use the same minLeft(L_i)/minRight(R_i); if both INF ⇒ −1 (do this before candidate computation; also, if both s,t non-isolated then at least one candidate is finite — good sanity check).
- Verify sample 1 by hand (query 1→4 should give 11 via 3-vertex candidate 7+4; query 5→2 isolated ⇒ −1).
- Python performance: read all input with sys.stdin.buffer.read().split() (or manual int parsing), avoid per-query function calls in favor of tight loop, output with '\n'.join or bytes writing. Q,N up to 2·10⁵ each → fine, but keep the query loop lean (local variable aliases for arrays).

## worker: Implement the complete Python solution: read input
Implemented exactly the plan:

- **Preprocessing** O(N): `prefR[v] = min{W_u : R_u ≤ v}` (prefix min over the array of best weight per right endpoint), `sufL[v] = min{W_u : L_u ≥ v}` (suffix min). Then `minLeft(v) = prefR[v-1]` (intervals strictly left of coordinate v) and `minRight(v) = sufL[v+1]` (intervals strictly right). Coordinates lie in [1, 2N], arrays sized 2N+2 with sentinels `prefR[0] = sufL[2N+1] = INF = 1<<60`.
- **Isolation / −1**: vertex i is isolated iff `minLeft(L_i)==INF and minRight(R_i)==INF`; since all non-isolated vertices form a single component (proof in plan: every non-isolated vertex is adjacent to the min-R interval A or the max-L interval B, and A,B are connected either directly or through two intermediates), the answer is −1 exactly when s or t is isolated.
- **Query O(1)**: take min over
  1. `W_s+W_t` if the intervals are disjoint (direct edge),
  2. `W_s+W_t+min(minLeft(min(L_s,L_t)), minRight(max(R_s,R_t)))` (3-vertex; the middle vertex is disjoint from both, and it is never s or t itself since minLeft(L_s) excludes s),
  3. `W_s+W_t+min(minLeft(L_s)+minRight(R_t), minLeft(L_t)+minRight(R_s))` (4-vertex; the two intermediates are provably mutually disjoint when [L_s,R_s]∩[L_t,R_t]≠∅, and when they're disjoint this candidate is ≥ candidate 1 anyway, so it never overestimates the optimum).
  Candidates containing INF are skipped by the `< INF` guards (sums of INF stay below the `INF*4` initial value only if finite, and the final check `ans >= INF` catches the impossible-leftover case).
- Weights are positive, so no path with more vertices can beat these (domination argument in plan).
- I/O: single `sys.stdin.buffer.read().split()`, tight loop with local aliases, joined output.

Hand-check of sample 1: query 1→4: intervals [2,4] and [4,5] intersect; 3-vertex candidate uses minLeft(min(2,4))=minLeft(2)=W of interval with R<2 → interval [1,2]? R=2 not <2, so INF; minRight(max(4,5))=minRight(5)=min W with L>5 → [7,8] w=4. So 5+2+4=11 ✓. Query 4→3: [4,5],[7,8] disjoint → 2+4=6 ✓. Query 5→2: vertex 5 = [2,7]: no R<2 and no L>7 → isolated → −1 ✓.
