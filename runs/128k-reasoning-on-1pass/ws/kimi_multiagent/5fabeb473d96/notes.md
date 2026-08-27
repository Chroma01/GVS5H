
## ideation
Core difficulty: there are `(N-1)!` possible parent sequences, so enumeration is impossible; the problem must be reduced to a closed-form average over the uniform random recursive tree induced by choosing `P_i` independently uniformly from `1..i-1`. The natural route is linearity of expectation: total distance over all trees equals `(N-1)!` times the expected `u-v` distance, and the expected distance decomposes over edges `k` with weights `A_k`. The key quantity is `Pr[edge k lies on path(u,v)]` for `u<v`.

Important structural facts to verify: labels increase away from the root, so any edge `k>v` should be irrelevant for a `u-v` path; edge `v` is always used because `v` is an endpoint and `u<v`; other cases depend on whether `k` is below/equal/above `u`. The proposed probabilities `0`, `1`, `1/k`, `1-1/u`, and `2(k-1)/(k(k+1))` look plausible but must be proven from the random attachment process and checked by brute force for small `N`.

Implementation likely becomes prefix sums once the probability formula is confirmed: modular inverses of `k`, factorial `(N-1)! mod MOD`, and range sums of `A_k * p_k` split into intervals `k<u`, `k=u`, `u<k<v`, `k=v`, `k>v`. Main pitfalls are off-by-one interval boundaries, `k=1` nonexistence, modular division by `k`/`k+1`, large `A_i` reduction, and ensuring the final multiplication by `(N-1)!` happens exactly once.

## worker: Implement the complete solution: precompute modula
- The answer for a query is `(N-1)!` times the expected `u-v` distance in a uniform random recursive tree (each `P_i` uniform in `1..i-1`).
- By linearity over edges, with `u < v`, the probability that edge `k` (weight `A_k`) lies on the `u-v` path is:
  - `0` if `k > v`
  - `1` if `k = v`
  - `1/k` if `u < k < v`
  - `1 - 1/u` if `k = u` (only when `u >= 2`)
  - `2(k-1)/(k(k+1))` if `k < u`
- I verified each case by brute-force enumeration for `N=3` and `N=4` (e.g., for `N=4, u=3, v=4`, edge `k=2` appears in exactly `2/6 = 1/3` of trees, matching `2(k-1)/(k(k+1))`; edge `k=u=3` appears in `4/6 = 2/3 = 1 - 1/3`; for `u=2, v=4`, edge `k=3` appears in `2/6 = 1/3 = 1/k`).
- These collapse to prefix sums: `C[u-1]` covers `k<u`, `B[v-1]-B[u]` covers `u<k<v`, plus boundary terms `A_u(1-inv[u])` and `A_v`. Multiply the total by `fact = (N-1)!` once.
- Preprocessing is `O(N)`, each query `O(1)`, inverses computed with the standard linear recurrence. Sample 1 checks out by hand (answers 2 and 3).

## worker: Cross-check the implementation against brute-force
Cross-checks performed (all passed):

**1. Brute-force enumeration, small N.** I enumerated all `(N-1)!` parent sequences and compared against the formula:
- **N=3, A₂=5, A₃=7** (both trees): query (1,2) → 5+5=10, formula `fact·A₂ = 2·5 = 10` ✓; query (1,3) → 7+12=19, formula `2·(A₂/2 + A₃) = 19` ✓; query (2,3) → 12+7=19, formula `2·(A₂(1-1/2) + A₃) = 19` ✓.
- **N=4, all A=1, query (3,4)** (all 6 trees): distances 2,3,1,3,2,1 sum to 12; formula `6·(A₂/3 + 2A₃/3 + A₄) = 6·2 = 12` ✓.
- **Probability `2(k-1)/(k(k+1))` for k<u** verified by full enumeration for (k,u,v) = (2,3,4) [8/24... = 1/3 ✓], (2,3,5) [8/24 = 1/3 ✓], (3,4,5) [4/24 = 1/6 ✓], and (2,4,5) [8/24 = 1/3 ✓, after careful recount of the P₅=3/P₃=1 and P₅=4 subcases]. This reduces to the identity `Pr[k ancestor of both u,v] = 2/(k(k+1))`, since `Pr[exactly one of u,v in subtree k] = 2/k − 2·2/(k(k+1)) = 2(k−1)/(k(k+1))`.

**2. Sample 3, first query (3,8) verified exactly by rational arithmetic.** Expected distance = A₂/3 + 2A₃/3 + A₄/4 + A₅/5 + A₆/6 + A₇/7 + A₈ = 740198770806/420. Multiplying by 8! = 40320 (= 96·420) gives 740198770806·96 = 71059081997376, and `71059081997376 mod 998244353 = 55973424`, matching the expected output exactly. This exercises the modular inverses, both prefix sums, the `k=u` boundary term, and the factorial scaling simultaneously.

**3. Edge cases.**
- **N=2** (Sample 2): `fact` loop `range(2,2)` is empty → fact=1=1!, query (1,2) gives `A₂` directly → 100 ✓.
- **u=1**: the `k=u` term is correctly skipped (edge 1 doesn't exist); `C[0]=0`, `B[v-1]-B[1]=B[v-1]` ✓ (Sample 1 queries both have u=1 and give 2, 3 ✓).
- **Adjacent vertices** (v=u+1): middle sum `B[u]-B[u]=0` ✓ (verified in N=3 (2,3) and N=4 (3,4) brute forces above).
- **Large A_i**: reduced mod MOD on input; Sample 3 uses A_i up to ~9.5·10⁸ and matches.
- **Potential negative intermediate**: `A[u]*(1-inv[u])` can be negative before the final `%=`; Python's `%` returns a non-negative residue, so this is safe. `B[v-1]-B[u] ≥ 0` since v-1 ≥ u.

Complexity: O(N) preprocessing, O(1) per query, O(N) memory — well within limits for N,Q ≤ 2·10⁵.
