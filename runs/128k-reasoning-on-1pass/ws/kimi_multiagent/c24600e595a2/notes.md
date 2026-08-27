
## ideation
Core difficulty: the flip costs are not independent; each operation’s price is the current weighted sum after that flip, so the order of flips changes the total even though the final set of flipped positions is fixed.

Key reduction: only indices with `A_i != B_i` need to be flipped, and in an optimal schedule each is flipped exactly once. Any index already equal should be flipped zero times; any mismatch flipped more than once creates extra positive-cost operations and can be reduced to one flip without increasing cost.

After fixing the set of flips, each flip has a signed delta to the weighted sum:
- `1 -> 0`: delta `-C_i`
- `0 -> 1`: delta `+C_i`

If there are `m` flips and initial sum is `S0`, then for deltas ordered as `d_1..d_m`, total cost is:
`m*S0 + sum_{r=1..m} (m-r+1) * d_r`.
Thus earlier deltas have larger coefficients, so deltas should be sorted increasingly: all negative/removal flips before positive/addition flips. Among removals, larger `C_i` is more negative and should go earlier; among additions, smaller `C_i` should go earlier so large increases are delayed.

Adjacent-swap proof sketch: swapping adjacent flips with deltas `d_p, d_q` changes cost by `d_p - d_q`, so the cheaper adjacent order puts the smaller delta first. This yields the greedy ordering above.

Pitfalls:
- Using the sum before the flip instead of after the flip.
- Flipping positions where `A_i == B_i`.
- Doing extra pairs of flips on the same index; all `C_i` are positive, so this cannot help.
- Reversing the addition order: additions should be ascending `C_i`, not descending.
- Overflow in languages with fixed-width ints; worst total is around `4e16`, so use 64-bit or Python ints.
- Avoid `O(N^2)` simulation over all states; sorting is enough.

## worker: Implement the final Python solution: read N, A, B,
- The mismatch-only plan is not sufficient: a position with `A_i = B_i = 1` may be worth turning off temporarily and turning back on. Example: `A=111`, `B=100`, `C=(1000,1,1)`; keeping the expensive common `1` costs `2001`, while turning it off and on costs `1003`.
- Correct structure: choose a set `K` of common `1`s to keep on throughout. All other initial `1`s are removed first in descending `C`; all final `1`s not in `K` are added afterward in ascending `C`. By an exchange argument, `K` can be taken as the cheapest `k` common `1`s.
- For fixed `k`, if `W` is the sum of kept common `1`s and `p,q` are the numbers of removal/addition operations, kept items contribute `(p+q)*W`. The remaining removal/addition contributions are maintained with Fenwick trees while moving common `1`s from “dropped” to “kept” in increasing `C`.
- Complexity: `O(N log N)` time, `O(N)` memory; Python integers avoid overflow.
