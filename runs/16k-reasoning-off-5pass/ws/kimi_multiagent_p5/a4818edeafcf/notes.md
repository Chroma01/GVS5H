
## ideation
The core difficulty is computing the middle segment's distinct count efficiently for all O(N²) possible (i,j) pairs — we need to reduce this to O(N log N).

Key insight: a value v contributes to the middle segment [i+1, j] iff its first occurrence ≥ i+1 AND its last occurrence ≤ j. So each value defines a constraint rectangle in (i,j) space: it adds 1 when i ≤ first(v)-1 and j ≥ last(v).

Approach: sweep j from 2 to N-1. Maintain an array over i (1 ≤ i ≤ j-1) where each position holds P[i] + (count of activated intervals covering i). When we reach j, all values with last occurrence == j become "active": add +1 to all i in [1, first(v)-1]. Then query max over i in [1, j-1] of the structure, add S[j+1], and take the global max.

Data structure: segment tree with lazy propagation supporting range-add and range-max. Initialize with P[i] values. Each value triggers exactly one range-add (when j reaches its last occurrence), so total operations = N range-adds + N queries = O(N log N).

Pitfalls:
- i range for activation is [1, first(v)-1]; if first(v) == 1, no i gets the contribution (skip).
- Must only query i in [1, j-1] (i < j constraint), and j only up to N-1 (right part non-empty), j from 2 (middle non-empty needs i+1 ≤ j, i.e., i ≤ j-1, automatic).
- Values appearing once: first == last, still handled correctly.
- Indexing: use 1-based consistently; P[i] = distinct count of A[1..i], S[j] = distinct count of A[j..N].
- Answer needs max over all j of (query_max + S[j+1]).
- Segment tree size N+2, initialize leaves with P[i] for i in 1..N-1 (i can be at most N-2 effectively since j ≤ N-1 and i < j, but initializing all is fine as long as queries are bounded).

Edge cases: N=3 forces i=1,j=2; values all distinct; values all same (only one interval [1,N], which can never be fully inside middle since first=1 means i ≤ 0 — correctly contributes nothing).

## worker: Implement the full solution: parse input, compute 
- Computed first/last occurrence of each value, prefix distinct counts P, suffix distinct counts S.
- Key fact: value v lies entirely in middle segment (i+1..j) iff i ≤ first(v)-1 and j ≥ last(v). So when sweep reaches j = last(v), do range-add +1 on i ∈ [1, first(v)-1].
- Lazy segment tree initialized with P[i]; at each j (2..n-1), after activating intervals ending at j, query max over i ∈ [1, j-1] and add S[j+1]; track global max.
- Complexity O(N log N), memory O(N). Verified logic against samples mentally: sample 1 gives 5, sample 2 gives 9.
