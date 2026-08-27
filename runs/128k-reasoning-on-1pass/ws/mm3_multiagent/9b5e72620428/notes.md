
## ideation
**Core difficulty** – We have two sequences with some entries known (non‑negative) and some “‑1” (free to be set to any non‑negative integer). Additionally, the whole array `A` may be permuted arbitrarily. The goal is to make all pairwise sums `A[i] + B[i]` equal to a common value `C`. The challenge is to determine whether the fixed numbers force a particular `C`, and whether the remaining free positions are sufficient to accommodate the fixed values while respecting the non‑negativity constraint.

**Key observations**  

1. If any position has both `A[i]` and `B[i]` fixed, the sum at that position is fixed, and consequently **all** sums must equal that value (call it `C0`).  
2. If no position has both numbers fixed, we can always pick a large enough `C` (e.g., `max(max fixed A, max fixed B, 0)`) and fill the missing numbers to achieve that `C`.  
3. When `C0` is forced, we must check that every fixed `A` and fixed `B` is ≤ `C0` (otherwise a negative partner would be required).  
4. Positions where only `A` is fixed (and `B = -1`) act as “free B slots”. Positions where only `B` is fixed (and `A = -1`) act as “free A slots”.  
5. The only restriction is that enough disjoint pairs `(a, b)` with `a + b = C0` must be formed using fixed `A` values and fixed `B` values, so that the remaining fixed `A` values can be placed on free B slots.  
6. The minimum number of such required pairs is `need = max(0, cntBoth - cntNone)`, where `cntBoth` is the number of both‑fixed positions and `cntNone` is the number of both‑`-1` positions.  
7. The maximum number of pairs we can actually form for a given `C0` is `pairs(C0) = Σ_a min(cntA[a], cntB[C0 - a])`, where `cntA` and `cntB` are the frequencies of fixed `A` and `B` values.  
8. A feasible configuration exists **iff** `pairs(C0) ≥ need`.

**Pitfalls to watch for**  

- Forgetting to verify that all both‑fixed positions share the same sum; otherwise the answer is immediately “No”.  
- Not checking the non‑negativity condition (`C0 ≥ max fixed A` and `C0 ≥ max fixed B`).  
- Miscomputing `need` or the number of free B slots.  
- Double‑counting pairs when iterating over values in `cntA`; the formula `Σ min(cntA[a], cntB[C0 - a])` is correct because each pair is associated with the `A` value and uses a distinct `B` value.  
- Edge cases: `N = 2`, all `-1`, or one side completely fixed, etc.  
- Using `int` overflow (not an issue in Python, but good to keep in mind).  

**Candidate approaches**  

- The described counting‑based method (frequencies + pair counting) runs in `O(N)` time and `O(N)` space, which is optimal for `N ≤ 2000`.  
- Alternative methods (e.g., greedy assignment, bipartite matching) are unnecessary given the simple arithmetic conditions derived above.

## worker: Implement the solution in Python based on the deri
The algorithm follows the reasoning in the plan:

1. If there is a position with both `A[i]` and `B[i]` fixed, the common sum `C` is forced to be that value (`C0`). All such positions must share the same sum.
2. When `C0` is forced we must also have `C0 ≥ max(fixed A)` and `C0 ≥ max(fixed B)`, otherwise a fixed value would need a negative partner.
3. The number of “free” `B = -1` positions is `cntAonly + cntNone`. To place all fixed `A` values we need at least `need = max(0, cntBoth - cntNone)` of them to be paired with a fixed `B` (forming a pair `(a, b)` with `a + b = C0`).  
4. The maximum number of such pairs is `pairs(C0) = Σ_a min(cntA[a], cntB[C0 - a])`. If `pairs(C0) ≥ need` we can realise the required pairs; the remaining fixed `A` go to `B = -1` positions and we set `B = C0 - a` (non‑negative because of step 2).  
5. If no position has both numbers fixed, we can always pick a large enough `C` and fill the missing numbers, so the answer is always “Yes”.

The implementation is linear in `N` (reading, building counters, and a single pass over distinct `A` values). The pair‑counting step is actually redundant because `pairs(C0) ≥ cntBoth ≥ need` always holds when the basic checks pass, but it is kept for completeness and does not affect correctness.
