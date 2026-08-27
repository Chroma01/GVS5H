
## ideation
The core difficulty is selecting disjoint pairs (top, bottom) with 2*top <= bottom to maximize count. Since sizes are sorted, an exchange argument shows that optimal pairs can be taken with tops from the smallest elements and bottoms from larger elements; pairing the smallest available top with the smallest feasible bottom is safe and optimal. A key pitfall is that tops and bottoms must be disjoint indices, so a simple count over all i of A[j] >= 2*A[i] could reuse the same element on both sides. The clean way is to cap possible pairs at floor(N/2) and match the K smallest tops against the K largest bottoms (or scan with two pointers while ensuring bottom index stays ahead of top region). Need O(N) or O(N log N); N up to 5e5, sizes up to 1e9, doubling fits in 64-bit and Python int anyway.

## worker: Implement and output the final Python solve() that
- The array is sorted ascending. Any valid pairing can use at most `floor(N/2)` pairs, so we only need to consider the `N//2` smallest mochi as candidate tops and the remaining larger half as candidate bottoms.
- Greedy: for the current smallest unmatched top `a[i]`, scan bottoms `a[j]` from the larger half. If `2*a[i] <= a[j]`, match them (using the smallest feasible bottom leaves bigger bottoms for bigger tops — exchange argument proves optimality) and advance both pointers; otherwise this bottom is too small for every remaining top, so advance `j`.
- Disjointness is guaranteed since `i < half <= j` always. Runs in O(N) time and O(N) memory for the input; sizes up to 1e9 so `2*a[i]` is safe.
- Verified against samples: sample1 → 3, sample2 → 0, sample3 → 6.
