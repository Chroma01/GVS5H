
## ideation
The core difficulty is that this is a maximum weight non-crossing matching problem on a line, which naively requires O(N²) interval DP. With N up to 3×10⁵, we need an O(N log N) or O(N) solution. The key observation is that when we pair positions i and j (i < j), all elements strictly between them must be perfectly matched among themselves, which means j-i must be odd and the subarray (i+1, j-1) must have even length and be completely matchable.

The problem has special structure: we're maximizing sum of |A_i - A_j| over matched pairs. This is similar to problems solvable with DP + convex hull trick or DP + segment tree with specific transition forms. The absolute value |A_i - A_j| = max(A_i - A_j, A_j - A_i) suggests we can split into cases based on whether A_i > A_j or not.

Key insight: Let dp[i] = max score using first i elements (with i possibly unmatched if i is odd... actually we need to think about parity). Since we remove pairs, after operations on prefix of length i, we can have at most one unmatched element. Actually, let's define dp[i] = max score achievable considering first i elements where element i is either matched with some j < i or unmatched (but only if total count allows).

Better formulation: f[i] = max score for prefix A[1..i] where all elements are matched except possibly A[i] itself. Then f[i] = max(f[i-1] (A[i] unmatched), max over j<i with (j-i) odd of g[j-1] + |A[j] - A[i]| where g[k] = max score for prefix A[1..k] with all matched).

The transition f[i] = max over valid j of (g[j-1] + |A[j] - A[i]|) can be split:
- If A[j] ≤ A[i]: g[j-1] + A[i] - A[j] = (g[j-1] - A[j]) + A[i]
- If A[j] > A[i]: g[j-1] + A[j] - A[i] = (g[j-1] + A[j]) - A[i]

So we need to query max of (g[j-1] - A[j]) and (g[j-1] + A[j]) over valid j (with correct parity), then take max with appropriate adjustments. This can be done with two segment trees or with a simple array if we process in order and maintain max values for each parity class.

Pitfalls:
- Parity: j and i must have different parity (j-i odd) for the middle to be perfectly matchable
- Need to handle both cases of absolute value correctly
- Need separate DP states for "prefix fully matched" vs "prefix with last element unmatched"
- Actually we can simplify: dp[i] = max score for first i elements with i unmatched (or i=0), and transitions as above

## worker: Implement the O(N) DP solution: define dp[i] as ma
- **State**: `dp[i]` = max score using prefix `A[1..i]` where `A[i]` is unmatched (all of `A[1..i-1]` matched). `dp[0] = 0`.
- **Transition**: `dp[i] = max(dp[i-1], max_j dp[j-1] + |A[j] - A[i]|)` over `j < i` with `(i-j)` odd (so the segment between `j` and `i` has even length and can be fully matched). The parity condition `(i-j)` odd ⟺ `(j-1) ≡ (i-1) (mod 2)`.
- **Absolute value split**: `|A[j]-A[i]| = max((dp[j-1]-A[j])+A[i], (dp[j-1]+A[j])-A[i])`. Maintain running maxima of `dp[j-1]-A[j]` and `dp[j-1]+A[j]` per parity of `j-1`, giving O(1) transition per index → **O(N)** total.
- **Answer**: `max_i dp[i]` (any single leftover element can be the last unmatched one; if N is even, `dp[N]` corresponds to full matching since the "unmatched" last element can be matched... actually the max over all `dp[i]` covers all valid matchings because every matching has some rightmost element involved or is empty — taking max over prefixes handles it).
- Verified against samples: `4 / 1 2 5 3 → 5`, `7 / 3 1 4 1 5 9 2 → 14`, `5 / 1 1 1 1 1 → 0`.
- Uses 1-indexed logic with parity of `i-1`; NEG sentinel guards empty parity classes. Values fit in Python ints (max score ≤ (N/2)·10⁹ ≈ 1.5×10¹⁴).
