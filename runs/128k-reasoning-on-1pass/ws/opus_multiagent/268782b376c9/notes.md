
## ideation
**Restating the mechanics.** A walk starts at −1 and takes ≤ m steps; each step (either direction) lands on some index i and adds points[i] to gameScore[i]. So gameScore[i] = points[i] · visits(i). We need to maximize min_i points[i]·visits(i).

**Core difficulty.** m up to 1e9 so we can't simulate; we must (a) turn "maximize the minimum" into a feasibility test via binary search on the answer T, and (b) find a *provably optimal* minimum-move schedule for given required visit counts need[i] = ceil(T / points[i]).

**Structure of an optimal walk (derivation).** Model edge i as the edge between i−1 and i (edge 0 = −1↔0), with r_i rightward and l_i leftward traversals. Then
- visits(i) = r_i + l_{i+1},
- total moves = Σ(r_i + l_i),
- if the walk ends at index e: r_i = l_i + 1 for i ≤ e, r_i = l_i for i > e.

So cost = (e+1) + 2·Σ l_i. Consequence: the only useful "extra" operation is a *bounce* i → i+1 → i (2 moves, +1 visit to both i and i+1); backward wandering beyond that is pure waste. Also, the walk should end at n−1 **or** at n−2 (the last bounce from n−2 can be truncated: you may end at n−1 without returning, or you may reach n−1 only via a bounce and stop at n−2). Ending earlier than n−2 never helps.

**Greedy check(T) (left-to-right, with carry).** carry = visits already granted to the current index by bounces at the previous index. For i = 0..n−1:
- need = ceil(T/points[i]) − carry
- if need ≤ 0: cost += 1 (the forward step onto i, needed only to continue right), carry = 0. **Special case: if i == n−1, cost += 0** (no need to step onto the last index at all — it was already covered by bounces from n−2, and we stop at n−2).
- else: cost += 1 + 2·(need−1) = 2·need − 1, carry = need − 1. (Step onto i gives 1 visit; each of the remaining need−1 visits costs a 2-move bounce, which also grants 1 visit to i+1. At i = n−1 the "bounce" is n−1 → n−2 → n−1, same cost, extra visits to n−2 harmless.)
- abort early if cost > m.

Feasible iff cost ≤ m.

**Why minimal carry is optimal:** an extra bounce at i costs 2 and gives 1 visit to i+1; satisfying that visit with a bounce at i+1 also costs 2 but additionally grants a free visit to i+2. So deferring is weakly better ⇒ take the minimum forced carry at each step (exchange argument).

**Sanity checks.**
- Example 1 (points=[2,4], m=3): T=4 → need=[2,1]. i=0: need'=2 → cost=3, carry=1. i=1 (last): need'=0 → +0. cost=3 ≤ 3 ✓. T=5 → need=[3,2]: i=0 cost=5>3 ✗. Answer 4 ✓.
- Example 2 (points=[1,2,3], m=5): T=2 → need=[2,1,1]: 3, then +1 (=4, carry 0), then last need'=1 → +1 = 5 ≤ 5 ✓. T=3 → need=[3,2,1]: 5, then need'=0 → +1 = 6 > 5 ✗. Answer 2 ✓.

**Pitfalls.**
- Forgetting the last-index special case (the "0 moves" branch) gives an off-by-one and fails Example 1.
- T = 0 must be reported feasible (cost 0), even though the loop would compute n−1 > m when m < n ⇒ handle T==0 as a base case / start binary search with lo = 0 known-good.
- Upper bound: total visits ≤ m ⇒ min visits ≤ m//n ⇒ answer < (m//n + 1)·max(points). Use hi = (m//n + 1)·max(points) as a known-infeasible bound (search may span ~5e14 ⇒ ~50 iterations).
- Performance: n = 5e4 × ~50 iterations = 2.5e6 inner steps in Python — need a tight loop (local vars, `-(-T//p)` for ceil, early `break` on cost > m). Consider precomputing nothing fancy; avoid function-call overhead per element.
- Careful that binary search returns the largest feasible T (invariant: lo feasible, hi infeasible).

## worker: Implement the complete `Solution.maxScore`: the ca
Implemented exactly the planned algorithm.

- `check(T)` for `T > 0`: sweep left to right with `carry` = free visits to the current index already granted by bounces at the previous index. For index `i`, `need = ceil(T/points[i]) - carry`. If `need <= 0`, the index is already satisfied and we only pay 1 move to step forward onto it (needed to continue rightwards), resetting `carry = 0`. Otherwise we pay `1 + 2*(need-1) = 2*need - 1` moves (one forward step plus `need-1` bounces `i -> i+1 -> i`), and each bounce also grants a free visit to `i+1`, so `carry = need - 1`.
- The last index is handled outside the loop: if its requirement is already fulfilled by the carry from index `n-2`, we pay **0** extra moves (we simply stop at `n-2`, never stepping onto `n-1`). This is the off-by-one that Example 1 hinges on (`points=[2,4], m=3, T=4` costs exactly 3).
- Early `return False` inside the loop keeps infeasible probes cheap.
- `T = 0` is never probed: binary search maintains invariant `lo` feasible (starting at 0, trivially feasible with 0 moves) and `hi` infeasible. `hi = (m//n + 1) * max(points)` is infeasible because total visits ≤ m ⇒ min visits ≤ m//n ⇒ answer ≤ (m//n)*max(points) < hi.
- Verified both examples by hand (see plan) and the loop's early abort keeps the worst case ~n·log(range) ≈ 5e4 × 50 = 2.5e6 simple operations.
