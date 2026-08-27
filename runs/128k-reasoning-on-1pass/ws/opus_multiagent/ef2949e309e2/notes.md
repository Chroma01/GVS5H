
## ideation
**Restating the count.** A size‑5 subsequence is determined by choosing an index `i` for the middle slot plus 2 indices `< i` and 2 indices `> i`. Different middle indices give different index‑sets, so summing over `i` (from 2 to n‑3) never double counts. Let `x = nums[i]`, `L = i`, `R = n-1-i`, `a = cntL[x]`, `b = cntR[x]`, `L' = L-a`, `R' = R-b`.

**Case analysis on k = multiplicity of x in the 5 chosen (k ≥ 1, includes the middle).**
- k = 1: the other 4 elements are non‑x; at best they are all distinct, giving a 5‑way tie for mode (count 1 each) → never a unique mode. Always bad.
- k = 2: the 3 non‑x elements must be pairwise distinct (else some value hits count 2 → tie, or 3 → beats x). Good ⟺ 3 distinct values.
- k ≥ 3: the ≤2 remaining elements can reach count at most 2 < 3 → always good.

So per `i`: `good(i) = C(L,2)C(R,2) − C(L',2)C(R',2) − bad2(i)` (complementary counting; the k≥3 cases are automatically kept).

**bad2(i)** = choose exactly one x among the 4, and the 3 non‑x elements are NOT all distinct.
- x taken from left (`a` ways): remaining = 1 left non‑x + 2 right non‑x. Repetition happens either (i) the two right ones are equal: `L'·Σ_{y≠x} C(cntR[y],2)`, or (ii) the two right ones differ but one equals the left one: `Σ_{y≠x} cntL[y]·cntR[y]·(R'−cntR[y])`. These are disjoint (right pair equal vs. unequal) and exhaustive.
- x taken from right (`b` ways): mirror image with L/R swapped.

I verified this against Example 2 by hand (i=2 gives 2, i=3 gives 2 → total 4 ✓) and Example 1 (all‑ones: only k=5 survives, total C(5,2)... check: for each i with L,R≥2, total=C(L,2)C(R,2), L'=R'=0, bad2=0 since all non‑x counts are 0; Σ over i=2..3 of C(i,2)C(5-i,2) = C(2,2)C(3,2)+C(3,2)C(2,2)=3+3=6 ✓).

**Core difficulty.** Not the combinatorics per se, but (1) getting the disjoint decomposition of "3 non‑x elements contain a repeat" right without double counting, and (2) keeping it efficient. The inner sum over distinct values y is O(d) per i → O(n·d) ≤ 10^6 for n=1000, which is borderline but acceptable in Python (~0.5–1.5 s); an O(n) version is available by maintaining aggregates.

**Aggregate sums for O(n)** (updated in O(1) when a single value's `cntL`/`cntR` changes as `i` advances: add `nums[i]` to left, remove `nums[i+1]` from right):
- `A = Σ_y C(cntR[y],2)`, `B = Σ_y cntL[y]·cntR[y]`, `C3 = Σ_y cntL[y]·cntR[y]²`
- `A' = Σ_y C(cntL[y],2)`, `D3 = Σ_y cntR[y]·cntL[y]²`
Then, excluding y=x by subtracting its own term:
- left‑case sum = `L'·(A − C(b,2)) + (R'·(B − a·b) − (C3 − a·b²))`
- right‑case sum = `R'·(A' − C(a,2)) + (L'·(B − a·b) − (D3 − b·a²))`
and `bad2 = a·(left‑case) + b·(right‑case)`.

**Pitfalls to watch.**
- Only iterate `i` in `[2, n-3]`; C(m,2)=0 for m<2 handles edges anyway.
- Subtractions can go negative before mod → take `% MOD` at the very end (or use exact Python ints throughout and mod once; n≤1000 keeps ints small enough).
- `R'` in the term `(R'−cntR[y])` must be the non‑x right count, not `R`.
- Don't forget y ranges over all values ≠ x, including values present on only one side (their terms vanish, so a Counter over the whole array or union of keys both work).
- Values can be negative / up to 1e9 → use dict/Counter (no array indexing) or compress.
- Equal values at different indices are distinct subsequences; count by index positions only.

## worker: *Task 2 (Core implementation):** Write `subsequenc
Implemented the O(n) aggregate sweep (strictly better than the required O(n·d), same formulas).

- Sweep `i` as the middle index. Before processing `i`, remove `nums[i]` from `cntR`; after processing, add it to `cntL`. So `cntL` = counts strictly left, `cntR` = counts strictly right.
- Per `i`: `good = C(L,2)C(R,2) − C(L',2)C(R',2) − bad2`, with
  - `bad2 = a·[L'·Σ_{y≠x}C(cntR[y],2) + Σ_{y≠x} cntL[y]cntR[y](R'−cntR[y])] + b·[mirror]`.
  - Using aggregates `A, Ap, B, C3, D3` the inner sums become `L'(A−C(b,2)) + (R'(B−ab) − (C3−ab²))` and `R'(Ap−C(a,2)) + (L'(B−ab) − (D3−ba²))`.
- Aggregate O(1) updates: removing one copy from right (`r→r−1`, left count `l`): `A −= r−1`, `B −= l`, `C3 −= l(2r−1)`, `D3 −= l²`. Adding one to left (`l→l+1`, right count `r`): `Ap += l`, `B += r`, `C3 += r²`, `D3 += r(2l+1)`.
- Exact Python ints throughout (values stay well below huge magnitudes for n≤1000), single `% MOD` at the end, avoiding negative-intermediate mod issues.
- Hand-verified examples 1 and 2 term-by-term (i=2 → 2, i=3 → 2 for example 2; 3+3=6 for example 1), plus edge cases `[1,1,2,2,3] → 0` and `[1,2,2,2,3] → 1`.
- The `__main__` block asserts the three examples and randomly cross-checks against a brute force over `C(n,5)` subsets (only runs when executed directly, not when imported by a judge).
