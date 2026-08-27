
## ideation
Core difficulty: We need a maximum matching in a bipartite-like setting where a smaller mochi a can sit on b only if 2a ≤ b, and each mochi is used at most once. N up to 5×10⁵ demands an O(N) or O(N log N) solution; the array is already sorted ascending.

Key structural insight: In an optimal solution with K pairs, the K tops can be taken as the K smallest used mochi and the K bottoms as the K largest used mochi. So it suffices to consider tops from the left half (indices 0..⌊N/2⌋−1) and bottoms from the right half (indices ⌈N/2⌉..N−1), matching greedily with two pointers: for each top (smallest first), find the smallest bottom that is ≥ 2×top. If found, count++ and advance both; else advance only the bottom pointer. An exchange argument proves optimality: matching smallest feasible bottom leaves larger bottoms for larger tops.

Pitfalls:
- Choosing the split point correctly: tops = first N//2 elements, bottoms = elements from index (N - N//2) = ⌈N/2⌉ onward. For even N, halves are equal; for odd N, the middle element goes to the bottom side (a top never needs to be the largest element).
- Answer can never exceed N//2; the greedy naturally respects this.
- Use fast I/O (sys.stdin.buffer) for 5×10⁵ integers.
- Edge cases: all equal sizes → 0; N=2.

## worker: Implement solve() reading N and list A via sys.std
- The array is already sorted ascending per the constraints, so no sorting is needed.
- Structural claim: in any optimal solution with K pairs, we can relabel so the K tops are the K smallest used mochi and the K bottoms are the K largest used mochi. Hence it suffices to take tops from the first ⌊N/2⌋ elements and bottoms from the last ⌈N/2⌉ elements (for odd N the middle element is assigned to the bottom side, which is never worse since a top never needs to be the largest element).
- Greedy two-pointer: for each top (smallest first), match it with the smallest bottom b satisfying 2·top ≤ b. If none qualifies at position j, advance j (that bottom is too small for this and all later, larger tops, so it can be discarded). If it qualifies, take the match and advance both. Optimality follows by a standard exchange argument: using the smallest feasible bottom preserves larger bottoms for larger tops, so no optimal solution does better.
- Answer is automatically ≤ ⌊N/2⌋ since i < N//2 bounds the number of matches.
- Complexity: O(N) time, O(N) memory for the input array; fast I/O via sys.stdin.buffer handles N = 5×10⁵ easily.
- Edge cases verified mentally: all-equal sizes → 0 (condition 2a ≤ b never holds); N=2 with A=[1,2] → 1; sample 1 gives 3, sample 2 gives 0, sample 3 gives 6.
