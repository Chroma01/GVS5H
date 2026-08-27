
## ideation
The core difficulty is proving which mochi should serve as tops and bottoms while ensuring that no mochi is reused. Since the sizes are sorted, an optimal solution can be arranged so that smaller mochi are tops and larger mochi are bottoms. For a fixed K, feasibility requires matching K tops against K distinct bottoms, with each top at most half its corresponding bottom. The candidate pairs must be chosen from disjoint portions, so K cannot exceed floor(N/2).

A useful monotonicity property is that if K pairs are possible, then any smaller number of pairs is also possible. This permits binary search, provided the feasibility check is correct. For a fixed K, use the K smallest mochi as candidate tops and the K largest mochi as candidate bottoms; matching them in sorted order is sufficient. If even this arrangement fails, no alternative matching can succeed, while if it succeeds, K pairs are directly constructed.

Care is needed with equality: a top of size a is valid when 2a is at most the bottom size. Also, the two selected groups must be disjoint, and integer arithmetic should avoid floating-point division.

## worker: Implement the solution using a two-pointer greedy 
The first `N // 2` mochi can be treated as candidate tops, and the remaining mochi as candidate bottoms. This is optimal because replacing any chosen top with a smaller unused mochi and any chosen bottom with a larger unused mochi cannot invalidate a pair.

Process both groups in ascending order. If `2 * top <= bottom`, pair them. Otherwise, the current bottom is too small for the current top and all later tops, so it can be skipped. The greedy scan runs in `O(N)` time and uses `O(N)` memory for the input array.
