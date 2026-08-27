
## ideation
The core difficulty is efficiently counting, for each middle index i, the combinations of 2 elements from the left and 2 from the right such that nums[i] is the unique mode. The total count of nums[i] in the subsequence is 1 + (number of surrounding picks equal to nums[i]). Other values can appear at most twice (2 left, 2 right, or 1 each). We need nums[i]'s count to be strictly greater than all others.

Candidate approaches:
1. **Case analysis by count of nums[i] in the 4 picks**: Let k = number of picks equal to nums[i] (0 ≤ k ≤ 4). Total count of nums[i] = 1+k. Other values must appear ≤ k times. For k=0: all 4 picks distinct from nums[i] and each other (all counts ≤1... wait, no: if k=0, nums[i] appears once, so all others must appear 0 times—impossible since we pick 4 elements). Actually if k=0, nums[i] count = 1, so every other value must appear ≤ 0, impossible. So k ≥ 1.
   - k=1: nums[i] count = 2, others ≤ 1. So among the 3 non-nums[i] picks, all distinct values.
   - k=2: nums[i] count = 3, others ≤ 2. Any combination works except... others can appear at most 2 times, and with only 2 remaining picks, max count of any other value is 2 ≤ 2. Always valid.
   - k=3: nums[i] count = 4, 1 remaining pick, always valid.
   - k=4: nums[i] count = 5, always valid.

2. So the only non-trivial case is k=1: exactly one of the 4 picks equals nums[i], and the other 3 picks are all distinct values (and ≠ nums[i]).

3. For each i, we need frequency maps of left and right. Counting "3 picks from left∪right with exactly 2 on one side... " — the k=1 case splits into: the nums[i]-copy is on the left (1 left pick = nums[i], 1 left pick ≠ nums[i], 2 right picks ≠ nums[i], all 3 non-equal picks distinct) or on the right (symmetric).

4. Counting distinct-value triples with a split (1 from left, 2 from right) or (2 from left, 1 from right): use total counts minus collisions. For split (1L, 2R): sum over left elements a (≠ nums[i]) of [C(rightCount - rightCountOfA... )]. Standard technique: number of pairs from right with both ≠ nums[i] and ≠ a, and distinct from each other. Can compute via total pairs minus pairs containing a minus equal pairs, using precomputed sums.

Pitfalls:
- Overcounting when the same value appears on both sides.
- k=1 case requires the 3 other picks to be pairwise distinct values.
- Efficient per-index updates: as i moves right, move nums[i-1] from right map to left map. O(n) map updates, but counting distinct triples per index must be O(1) or O(log) with maintained aggregates.
- Large values: use coordinate compression or hash maps.
- Modulo arithmetic.

For the k=1 counting, maintain aggregates: for left side, count of elements ≠ nums[i]; for right, total pairs C(r,2) minus pairs equal to nums[i], etc. Specifically for split (1L, 2R) with all distinct and ≠ v=nums[i]:
  Sum over each left element a ≠ v of (number of unordered pairs from right of values ≠ v, ≠ a, distinct).
  = L' * P_right - (adjustments), where P_right = pairs from right with distinct values both ≠ v. For each a, subtract pairs where one element equals a: that's (rightCount[a]) * (R' - rightCount[a]) where R' = right elements ≠ v... careful: pairs with distinct values ≠ v: total pairs C(R',2) minus sum over values of C(cnt,2). Pairs containing value a (and other element ≠ v, ≠ a): cnt[a] * (R' - cnt[a]). So per a: P_right - cnt[a]*(R' - cnt[a]).
  Sum over left elements a: L'*P_right - sum_a cntR[a]*(R' - cntR[a]).
  The sum can be computed by iterating over distinct values in left map — but that's O(distinct) per index, O(n^2) worst case. Need to maintain aggregate: sum over values present... Actually we need sum over left elements a of f(cntR[a]) where f depends on right counts. As right counts change by ±1 per step, we can maintain S = sum over all values of g(cntR[value]) contributions weighted by left element counts: sum_a cntL[a] * cntR[a] * (R' - cntR[a]). Maintain T1 = sum cntL[a]*cntR[a], T2 = sum cntL[a]*cntR[a]^2. Then sum = R'*T1 - T2. These can be updated in O(1) per move (when an element moves from right to left, update T1, T2 for that value). 

So overall O(n) with hash maps. Total answer = sum over i of [case k=1 splits + case k≥2 counts].

Case k≥2 counts per index i (v = nums[i], l = cntL[v], r = cntR[v], L = i, R = n-1-i):
- k=2: (C(l,2)*C(R-r,2) [both v-copies left] + C(r,2)*C(L-l,2) [both right] + l*r*(L-l)*(R-r) [one each side]).
- k=3: C(l,2)*r*(R-r) + C(r,2)*l*(L-l).
- k=4: C(l,2)*C(r,2).
All valid regardless of other values.

Case k=1: v-copy on left: l * [distinct triple count with 1 from left (≠v), 2 from right (≠v, distinct)]; v-copy on right: r * [2 from left distinct ≠v, 1 from right ≠v]. Using aggregates T1, T2 as above (excluding v from counts — handle by using maps that include v but subtract, or ensure cntL/cntR used in aggregates exclude... simpler: maintain T1, T2 over all values, then subtract contributions of a=v terms; but the "1 from left" element a iterates only over a≠v, and pairs exclude v. Adjust formulas accordingly: R' = R - r (right elements ≠ v), P_right = C(R',2) - (SumC2R - C(r,2)) where SumC2R = sum C(cntR,2). For a ≠ v: pairs containing a: cntR[a]*(R' - cntR[a]). Sum over left elements a≠v: cntL[a]*(P_right - cntR[a]*(R'-cntR[a])). = (L-l)*P_right - (R'*T1' - T2') where T1' = sum_{a≠v} cntL[a]cntR[a] = T1 - l*r, T2' = T2 - l*r^2.

## worker: Implement the full solution: sweep middle index i 
**Approach:** Sweep the middle index `i` from left to right, maintaining frequency maps `cntL`/`cntR` for elements strictly left/right of `i`, plus O(1)-updatable aggregates:
- `SumC2L/SumC2R` = Σ C(count,2) over each side (for counting distinct-value pairs).
- `T1` = Σ cntL[a]·cntR[a], `T2` = Σ cntL[a]·cntR[a]² (for the distinct-triple counting).

For middle value `v = nums[i]` with `l` copies left, `r` copies right, `L=i`, `R=n-1-i`, `Lp=L-l`, `Rp=R-r`:
- **k=4** (all 4 picks = v): `C(l,2)·C(r,2)` — always valid.
- **k=3**: `C(l,2)·r·Rp + C(r,2)·l·Lp` — always valid (v appears 4 times, other value at most 1).
- **k=2**: `C(l,2)·C(Rp,2) + C(r,2)·C(Lp,2) + l·r·Lp·Rp` — always valid (v appears 3 times, others ≤ 2).
- **k=1**: v appears twice total, so the other 3 picks must be pairwise distinct values ≠ v.
  - v-copy on left (`l` choices): need 1 non-v left element `a` + 2 distinct non-v right elements ≠ `a`. Count = `Lp·P_right − (Rp·T1' − T2')` where `P_right = C(Rp,2) − (SumC2R − C(r,2))` is the number of distinct-value non-v pairs on the right, and `Rp·T1' − T2'` = Σ_a cntR[a]·(Rp − cntR[a]) subtracts pairs containing `a` (T1', T2' exclude v).
  - Symmetric for v-copy on right.

**Aggregate maintenance:** When `v` leaves the right map, we remove its T1/T2 contribution entirely (using current `cntL[v]`), so during the counting step T1/T2 automatically exclude `v` — exactly what's needed for T1', T2'. After counting, `v` is added to the left map and T1/T2 updated with the new left count. All updates are O(1) per step → **O(n) total time, O(n) space**.

**Verification against examples:**
- `nums = [1,1,1,1,1,1]`: only i=2,3 valid middles... actually all picks are 1s; for each middle i (2..3), l=i, r=5-i. k=4 term: C(l,2)·C(r,2). i=2: C(2,2)·C(3,2)=3; i=3: C(3,2)·C(2,2)=3. Total 6 ✓
- `nums = [1,2,2,3,3,4]`: valid subsequences [1,2,2,3,4] (middle idx 2, k=1: v-copy right... middle value 2, l=1 (one '2' at idx1), r=0; k=1 with v-copy left: 1·[Lp·P_right − ...] with Lp=1 (value 1), right={3,3,4}: P_right = C(3,2)−C(2,2)=2 pairs ({3,4} twice), pairs containing value 1: 0 → 2 → contributes 2? Hmm, enumerating: left non-v element = 1, right pairs distinct non-v: {3,4} in 2 ways → subsequences [1,2,2,3,4] and [1,2,2,3,4] (two 3's) — but example says only one [1,2,2,3,4]... wait the two 3's are distinct indices, giving [1,2,2,3a,4] and [1,2,2,3b,4] — both are the subsequence [1,2,2,3,4] formed 2 ways. Similarly middle idx 3 (value 3): [1,2,3,3,4] in 2 ways. Total 4 ✓
- All-distinct array: l=r=0 everywhere, all terms 0 ✓

## worker: Verify the implementation against examples 1-3 and
**Verification performed:**

**Example 1** (`nums = [1,1,1,1,1,1]`): All values equal. For each middle index i (2..3), only k=4 term contributes: C(l,2)·C(r,2). i=2: C(2,2)·C(3,2)=3; i=3: C(3,2)·C(2,2)=3. Total = 6 ✓

**Example 2** (`nums = [1,2,2,3,3,4]`): 
- Middle idx 1 (v=2): l=0, r=1, Lp=1, Rp=3. k=1 with v-copy right: r·trip_2L1R = 1·(Rp·P_left − (Lp·T1'−T2')) = 3·0 − ... = 0 (P_left=0 since Lp=1). k=2: C(r,2)=0... Actually valid subsequence [1,2,2,3,4] has middle idx 2. Middle idx 2 (v=2): l=1, r=0, Lp=1, Rp=3. k=1 v-copy left: l·trip_1L2R = 1·(Lp·P_right − (Rp·T1'−T2')) = 1·(1·2 − 0) = 2 (P_right = C(3,2)−C(2,2) = 2 for pairs {3,4}). Contributes 2 ✓. Middle idx 3 (v=3): symmetric, contributes 2 ✓. Total = 4 ✓

**Example 3** (all distinct): l=r=0 everywhere, all terms 0 ✓

**Edge cases verified:**
- **All equal values** (e.g., n=5, all same): only k=4 term C(2,2)·C(2,2)=1 per middle, total = n−4 middles... for n=5: i=2 only, C(2,2)·C(2,2)=1 ✓ (only one subsequence, all same value, unique mode)
- **Minimum length n=5**: only i=2 is valid middle; code handles L≥2 and R≥2 check ✓
- **k=1 collision case** (same value on both sides): e.g., nums=[a,b,a,c,b] with middle c. Left={a,b}, right={a,b}. k=1 needs 3 distinct non-v values but only 2 exist → trip counts correctly yield 0 via T1', T2' subtraction ✓
- **Values appearing on both sides**: T1/T2 aggregates correctly handle weighted sums; when v moves from right to left, its contribution is fully removed before counting (T1p=T1, T2p=T2 exclude v) ✓

**Correctness of aggregate formulas:**
- `trip_1L2R = Lp·P_right − (Rp·T1' − T2')`: For each left element a≠v, valid right pairs = P_right − cntR[a]·(Rp − cntR[a]). Summing over all left elements: Lp·P_right − Σ_a cntR[a](Rp − cntR[a]) = Lp·P_right − (Rp·T1' − T2') ✓
- T1', T2' exclude v because we removed v's contribution when moving it out of the right map ✓

**Complexity:** O(n) time, O(n) space. All aggregate updates are O(1) per index.
