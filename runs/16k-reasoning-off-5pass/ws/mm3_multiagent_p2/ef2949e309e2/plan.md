We need to count subsequences of length 5 where the middle element (index 2) is the unique mode. For each position `i` chosen as the middle, we must count ways to pick 2 elements before `i` and 2 elements after `i` such that the value at `i` appears strictly more times than any other value in the chosen 5-tuple.

Approach: For each index `i` as middle, let `v = nums[i]`. Count pairs `(a,b)` with `a < i < b` where the multiset `{nums[a], nums[b], v, x, y}` has `v` strictly dominating. We can split into cases based on whether the other elements equal `v` or not.

A clean way: For each `i`, count all `C(L,2) * C(R,2)` ways to pick 2 left and 2 right, then subtract "bad" selections where some other value ties or beats `v`. Use inclusion-exclusion over the other value `u != v`: count selections where `u` appears at least as often as `v`.

Concretely, for fixed `i` and value `u != v`:
- Let `cl` = count of `u` in left side, `cr` = count of `u` in right side.
- Let `L` = number of left positions, `R` = number of right positions.
- We need to subtract selections where the count of `u` in the chosen 2 left + 2 right is `>=` count of `v` in chosen 2 left + 2 right.
- Count of `v` in chosen left = `kL` (0..2), chosen right = `kR` (0..2), with `kL + kR = count_v_chosen`. Count of `u` chosen = `jL + jR`.

This becomes complex. Better approach: iterate over the "second most frequent" value.

Alternative cleaner approach (standard for this problem):
For each `i` as middle, let `v = nums[i]`. The middle is unique mode iff in the chosen 2 left + 2 right elements, the number of `v`'s is strictly greater than the count of any other single value.

We can count by enumerating how many `v`'s appear among the 4 other positions: `k = 0,1,2`. For each `k`, count ways to pick `k` copies of `v` from left/right, and ensure no other value appears `>= k+1` times (since `v` appears `k+1` total including middle).

For `k=2`: both other positions are `v`. Count = `C(cnt_v_left,2)*C(cnt_v_right,0) + C(cnt_v_left,1)*C(cnt_v_right,1) + C(cnt_v_left,0)*C(cnt_v_right,2)`. Always valid since no other value can tie.

For `k=1`: one other `v`, three other positions must not contain any value appearing 2+ times. Count ways to pick 1 `v` from left/right, then pick 3 from remaining positions such that no value appears twice.

For `k=0`: no other `v`, the 4 positions must have all distinct values (since any duplicate would tie with `v` at count 1).

This is still complex. Let me use the known solution pattern:

**Known solution**: For each `i`, count total ways `C(L,2)*C(R,2)`. Subtract ways where some other value `u` appears at least as many times as `v` in the 4 chosen positions.

For each `u != v`, let `cl = count of u in left`, `cr = count of u in right`, `vl = count of v in left`, `vr = count of v in right`, `L = i`, `R = n-1-i`.

We need to subtract selections where `u` count in chosen >= `v` count in chosen. Use inclusion-exclusion over pairs of values? No, use the principle: for each `u`, subtract selections where `u` is "at least as frequent as v", but add back overlaps where two values both tie.

Actually the cleanest known method: For each `i`, iterate over all possible "competitor" values `u` (including `v` itself for the `k>=2` case handled separately), and use a formula.

Let me use a different, well-known approach:

**Final approach**: For each index `i` as middle:
- Let `v = nums[i]`, `L = i`, `R = n-1-i`.
- Total ways to pick 2 left and 2 right: `C(L,2) * C(R,2)`.
- For each other value `u`, count "bad" selections where `u` appears at least as many times as `v` among the 4 chosen positions. Sum over `u`, subtract, but this overcounts when two values both tie.

Use inclusion-exclusion with pairs? Too expensive.

**Better**: Direct enumeration of the "second mode" value. For each `i`, for each value `u` (could equal `v`), count selections where `u` is the value that ties or beats `v`. If `u == v`, this counts selections where `v` appears >=2 times among the 4 (which is always fine, so we want to count these as good). Hmm.

Let me restructure: Count good selections directly.

For each `i`, value `v = nums[i]`:
- Good selections = selections where `v` appears strictly more than any other value among the 5.
- Equivalently: max count of any value among the 4 chosen positions is `<= count of v among 4 chosen + 1`, and `v` achieves the max.

Count by cases on `k` = number of `v`'s among the 4 chosen:
- `k=2`: always good. Ways = `C(vl,2) + vl*vr + C(vr,2)`.
- `k=1`: need the other 3 chosen to have no value appearing 2+ times. So among the 3 non-`v` chosen, all distinct.
- `k=0`: need all 4 chosen to be distinct.

For `k=1`: pick 1 `v` from left or right (vl + vr ways for position, then choose which side). Actually: choose 1 position for the extra `v`: `vl + vr` choices. Then from remaining positions (excluding that chosen `v` position and the middle), pick 3 positions such that all 3 values are distinct and none equals `v`.

This is getting complex but doable with precomputation.

Given the complexity, I'll use the **standard competitive programming solution** for this exact problem (LeetCode 3395):

For each `i`, compute:
- `total = C(L,2) * C(R,2)` (all ways)
- For each value `u`, compute `bad[u]` = ways where `u` appears >= count of `v` among the 4 chosen.
- Answer for `i` = `total - sum_u bad[u] + sum_{u1<u2} bad_both[u1,u2] - ...`

This inclusion-exclusion is too expensive.

**Actual known solution** (from LeetCode editorial): 
For each `i`, iterate over the "second most frequent" value `u` in the subsequence (could be `v` itself meaning no second). For each `u`, count subsequences where `u` is the value with the maximum count among non-`v` values, and that max is `<= count of v`.

Let me just implement the direct enumeration approach which is `O(n^2)` per middle, too slow for `n=1000`.

**Pragmatic solution**: `n <= 1000`, so `O(n^2)` total might work. For each pair `(i, j)` with `i < j`, treat them as... no.

Let me think again. `n=1000`, we can do `O(n^2)` or `O(n^2 log n)`.

**Clean O(n^2) solution**: For each `i` (middle), we want to count pairs of left indices `(a,b)` and right indices `(c,d)` with `a<b<i<c<d` such that `nums[i]` is unique mode.

For each `i`, let's count by the value `u` that is the "runner-up" (second most frequent, could tie with others but we handle).

Actually, here's a clean approach: For each `i`, for each value `u` (including `u = nums[i]`), count the number of 5-element subsequences with middle `i` where `u` is the most frequent value (or tied). Then use inclusion-exclusion.

Given time, let me implement the **known working approach**:

For each `i`:
1. Count `total = C(L,2)*C(R,2)`.
2. For each value `u != v`, count selections where `u` count >= `v` count in the 4 chosen. Subtract these.
3. But selections where two different `u1, u2` both have count >= `v` count are subtracted twice; add back.

Since values are up to `n=1000` distinct, and we iterate `i` from 0 to n-1, we can maintain frequency maps incrementally.

**Incremental approach**: Sweep `i` from left to right. Maintain for each value `u`: `cntL[u]` = occurrences in left, `cntR[u]` = occurrences in right (which is total - left - middle).

For each `i`, we need to compute for each `u`:
`bad[u] = sum over (jL, jR, kL, kR) with jL+jR >= kL+kR of C(cntL[u], jL)*C(cntR[u], jR) * C(cntL[v], kL)*C(cntR[v], kR)`

where `jL+jR+kL+kR = 4`, `jL<=2, jR<=2, kL<=2, kR<=2`.

This is a convolution-like computation per `u`, which is `O(distinct values)` per `i`, total `O(n * distinct)`. With `n=1000`, this is `O(n^2)` = 10^6, feasible.

Let me precompute `C(x, y)` for `x` up to 1000.

For each `i`, for each `u`:
- Enumerate `jL in 0..min(2, cntL[u])`, `jR in 0..min(2, cntR[u])`, `kL in 0..min(2, cntL[v])`, `kR in 0..min(2, cntR[v])` with `jL+jR+kL+kR=4` and `jL+jR >= kL+kR`.
- Sum `C(cntL[u],jL)*C(cntR[u],jR)*C(cntL[v],kL)*C(cntR[v],kR)`.

Then `good_i = total - sum_{u != v} bad[u] + sum_{u1 < u2} bad_both[u1,u2] - ...`

The inclusion-exclusion over pairs is needed when two values both tie. This is complex.

**Simpler**: Count good directly by iterating over the "winning competitor" value.

For each `i`, for each value `u` (the value that is the second most frequent, or `u = v` if no competitor):
- Count selections where `u` is the max among non-`v` values, and that max is `<= count of v`.
- If `u = v`: count selections where `v` appears >= 2 times among 4 (always good). = `C(vl,2)+vl*vr+C(vr,2)`.
- If `u != v`: count selections where `u` appears `m` times (m = 1 or 2), `v` appears `k` times with `k+1 > m`, and all other values appear `< m` times.

This is still complex.

**Let me just implement the brute-force O(n^2) with hash maps** since n=1000:

For each `i`, iterate over all pairs of left indices and pairs of right indices? That's `C(L,2)*C(R,2)` per `i`, total `O(n^4)` = 10^12, too slow.

**Final decision**: Implement the per-`i` enumeration over competitor value `u`, using the formula:

For each `i`, for each value `u` (iterate over all distinct values in nums):
- Compute `bad[u]` = number of ways where `u` count in 4 chosen >= `v` count in 4 chosen.
- `good_i = total - sum_{u != v} bad[u] + sum_{u1 != v, u2 != v, u1<u2} (ways where both u1 and u2 count >= v count) - ...`

Inclusion-exclusion to depth 2 might suffice if we argue that 3 values can't all tie with v when v appears at most 2 times... actually they can.

Hmm. Let me look up the actual editorial approach.

**Actual editorial approach** (LeetCode 3395):
For each index `i` as middle:
- Let `v = nums[i]`.
- Count `ans_i` = number of valid subsequences with middle `i`.
- `ans_i = total - sum_{u} f(u) + sum_{u1 < u2} f(u1, u2) - ...`
where `f(u1, ..., uk)` = ways where all of `u1,...,uk` have count >= v count in the 4 chosen.

But this is inclusion-exclusion over all subsets, expensive.

**Simpler editorial approach**: 
`ans_i = sum over partitions of the 4 chosen positions by value, where v is unique max`.

Directly enumerate the multiset of the 4 chosen positions. The 4 positions have some value distribution. We need v's count > any other value's count.

Cases for the 4 chosen:
- (2,1,1): two of one value `u`, one each of two other values. v must appear 3+ times, impossible (only 4 positions, v appears 3 means one other). So v appears 3, other appears 1: (3,1). v appears 4: (4).
- (2,2): two values each appearing twice. v must appear 3+, impossible.
- (2,1,1) with v=3: impossible since v appears 3, one other value appears 1, but we said two other values each 1, contradiction. So v appears 3 means (3,1) distribution.
- (1,1,1,1): all distinct. v appears 1, others 1 each. v is NOT unique mode (all tie). Bad.
- (2,1,1): v appears 2, one other value appears 2. Tie. Bad.
- (2,2): v appears 2, another appears 2. Tie. Bad.
- (3,1): v appears 3, one other appears 1. v unique mode. Good.
- (4): v appears 4. Good.
- (2,1,1) where v=2 and others are 1,1: tie between v and the value appearing 2. Bad.

Wait, I need to reconsider. The 4 chosen positions + middle = 5 positions. Middle is `v`. So total count of `v` in the 5 = 1 + (count of v in 4 chosen). For v to be unique mode, we need:
- count_v_in_4 + 1 > count_u_in_4 for all u != v.

Let `k = count_v_in_4` (0,1,2,3,4). Then need `k+1 > count_u_in_4` for all u.

- k=4: others have 0. Always good.
- k=3: others have 1 total, so one other value with count 1. Good (3 > 1).
- k=2: others have 2 total. Need no other value to have count 2. So the 2 non-v positions must be two different values (each count 1). Good iff the 2 non-v are distinct values.
- k=1: others have 3 total. Need no other value to have count 2. So among the 3 non-v positions, all distinct values.
- k=0: others have 4 total. Need no other value to have count 1... wait, need `1 > count_u`, so count_u = 0 for all u. But there are 4 non-v positions, so some u has count >= 1. Impossible. So k=0 is always bad.

So good cases:
- k=4: all 4 chosen are v.
- k=3: 3 chosen are v, 1 is some u != v.
- k=2: 2 chosen are v, 2 chosen are two distinct values (both != v).
- k=1: 1 chosen is v, 3 chosen are three distinct values (all != v, and all distinct from each other).
- k=0: impossible.

Now count each:

Let `vl = count of v in left of i`, `vr = count of v in right of i`, `L = i`, `R = n-1-i`.

**k=4**: Choose 2 from left (both v) + 2 from right (both v), or 1 left + 1 right, or 0 left + 2 right, etc. Actually we need 4 v's total from left+right with 2 from each side.
- Ways = `C(vl,2)*C(vr,2) + C(vl,2)*C(vr,1)*C(R-vr,1) + ...` 

Wait, we need exactly 2 from left and 2 from right. So:
- 2 v from left, 2 v from right: `C(vl,2)*C(vr,2)`.
- 2 v from left, 1 v from right + 1 non-v from right: `C(vl,2)*vr*(R-vr)`.
- 1 v from left + 1 non-v from left, 2 v from right: `vl*(L-vl)*C(vr,2)`.
- 1 v + 1 non-v from left, 1 v + 1 non-v from right: `vl*(L-vl)*vr*(R-vr)`.
- 0 v from left, 2 v from right: `C(L-vl,2)*C(vr,2)`. Wait, we need 2 from left total, so if 0 v from left, 2 non-v from left: `C(L-vl,2)*C(vr,2)`.
- 0 v from left, 1 v + 1 non-v from right: `C(L-vl,2)*vr*(R-vr)`.
- 2 non-v from left, 0 v from right: `C(L-vl,2)*C(R-vr,2)`.

Hmm wait, for k=4, ALL 4 chosen must be v. So:
- 2 from left must both be v: `C(vl,2)`.
- 2 from right must both be v: `C(vr,2)`.
- Total: `C(vl,2)*C(vr,2)`.

I confused myself. k=4 means 4 of the chosen are v. Since we pick 2 from left and 2 from right, both left picks must be v and both right picks must be v. So `C(vl,2)*C(vr,2)`.

**k=3**: 3 v's and 1 non-v among the 4 chosen. The non-v can be in left or right.
- Non-v in left: 1 v from left, 1 non-v from left, 2 v from right: `vl * (L-vl) * C(vr,2)`.
- Non-v in right: 2 v from left, 1 non-v from right, 1 v from right: `C(vl,2) * (R-vr) * vr`.

**k=2**: 2 v's and 2 non-v's. The 2 non-v's must be distinct values. 
- Split of 2 v's: (2 left, 0 right), (1 left, 1 right), (0 left, 2 right).
- Split of 2 non-v's: (2 left, 0 right), (1 left, 1 right), (0 left, 2 right).
- For each split, the non-v positions must contain 2 distinct values.

This requires knowing, for each side, the count of distinct values and pairs of distinct values. Complex.

**k=1**: 1 v and 3 non-v's, all 3 non-v's distinct.

This is getting very complex to compute per `i`.

**Let me use a different, simpler approach**: Since `n <= 1000`, and we have at most `n` middles, and for each middle we can do `O(n)` work, total `O(n^2) = 10^6`, feasible.

For each `i` as middle, iterate over all possible 4-element selections? No, `C(n,4)` is too large.

**Alternative**: For each `i`, iterate over pairs `(a, c)` where `a < i < c`, and count completions. Still complex.

**Let me just implement the known solution pattern from competitive programming**:

For each `i`:
- Maintain frequency maps of left and right sides.
- For each value `u`, compute `bad[u]` = selections where `u` count >= `v` count in 4 chosen.
- Use the formula with inclusion-exclusion, but truncate: since `n <= 1000` and values are bounded, we can do inclusion-exclusion over all values, but that's `O(2^distinct)` per `i`, too expensive.

**Pragmatic final approach**: 
For each `i`, compute `good_i` by iterating over the "second mode" value `u`:
- For each `u` (including `u = v`), count selections where `u` is the value with maximum count among non-`v` values, and that max is `<= count of v`.
- If `u = v`: count selections where v appears >= 2 times in 4 chosen (these are always good). = `C(vl,2) + vl*vr + C(vr,2)` ... wait this counts selections with exactly 2 v's, but we want >=2.

Hmm, let me reconsider. For `u = v`, this means "no other value beats v", which is equivalent to "v is unique mode". So we'd be double-counting.

**Cleanest formulation**: 
`good_i = total - bad_i`
where `bad_i` = selections where some value `u != v` has count >= count of v in the 4 chosen.

`bad_i = union over u of {selections where count_u >= count_v}`.

By inclusion-exclusion:
`bad_i = sum_u bad[u] - sum_{u1<u2} bad[u1,u2] + ...`

where `bad[u1,...,uk]` = selections where all of `u1,...,uk` have count >= count_v.

For `n=1000`, inclusion-exclusion over all subsets is infeasible. But note: in the 4 chosen positions, at most 4 distinct values can appear. So at most 4 values can have count >= 1. The condition `count_u >= count_v` with `count_v <= 4` means we only care about values with sufficient counts.

**Key insight**: `count_v` in 4 chosen is at most 4. For `u` to have `count_u >= count_v`, we need `count_u >= 1` (if count_v=1), etc. But more importantly, the number of values with `count >= 1` in 4 chosen is at most 4.

**Truncation**: We only need inclusion-exclusion up to depth 4 (since at most 4 distinct values in 4 positions). But iterating over all 4-subsets of distinct values is `O(distinct^4)` per `i`.

Given `n=1000` and `distinct <= 1000`, this is `10^9` per `i`, too slow.

**Better truncation**: For each `i`, only values that actually appear in left or right with sufficient count matter. The number of such values is bounded by `L + R = n-1`, but typically much less.

**Let me just implement the direct enumeration for k=2 and k=1 cases carefully**:

For k=2 (2 v's, 2 non-v's distinct):
- Need to count pairs of non-v positions (one in left, one in right, or both in same side) with distinct values.
- This requires, for each side, the number of ways to pick 2 positions with distinct values.

Let `L` = left positions, `R` = right positions. Let `freqL[x]` = count of value x in left, `freqR[x]` = count of value x in right.

Number of ways to pick 2 from left with distinct values:
`distinct_pairs_L = C(L,2) - sum_x C(freqL[x], 2)`

Similarly for right.

Number of ways to pick 1 from left and 1 from right with distinct values:
`cross_distinct = L*R - sum_x freqL[x]*freqR[x]`

For k=2:
- 2 v from left, 2 non-v distinct from right: `C(vl,2) * distinct_pairs_R`.
- 2 v from right, 2 non-v distinct from left: `C(vr,2) * distinct_pairs_L`.
- 1 v from left, 1 v from right, 1 non-v from left, 1 non-v from right, distinct: `vl * vr * cross_distinct`.
- 2 v from left, 1 non-v from left, 1 non-v from right, distinct: `C(vl,2) * (L-vl) * (R-vr) - (correction for same value)`.

Wait, this is getting complicated because the non-v positions need to have distinct values, and they can be in the same side or different sides.

Let me define:
- `pick2L_distinct` = ways to pick 2 positions from left with distinct values.
- `pick2R_distinct` = ways to pick 2 positions from right with distinct values.
- `pick1L_1R_distinct` = ways to pick 1 from left and 1 from right with distinct values.

For k=2, the 2 v positions can be distributed as (2L, 0R), (1L, 1R), (0L, 2R). The 2 non-v positions similarly. But the non-v positions must have distinct values.

Cases:
1. 2v in L, 2 non-v in L (distinct): `C(vl,2) * pick2L_nondistinct_from_nonv`. 
   - Non-v positions in L: choose 2 from `L - vl` positions with distinct values.
   - `pick2L_nonv_distinct = C(L-vl, 2) - sum_{x != v} C(freqL[x], 2)`.
2. 2v in L, 2 non-v in R (distinct): `C(vl,2) * pick2R_nonv_distinct`.
3. 2v in L, 1 non-v in L, 1 non-v in R (distinct): `C(vl,2) * (L-vl) * (R-vr) - sum_{x != v} freqL[x] * freqR[x]`. Wait, we need the non-v in L and non-v in R to have distinct values. So subtract cases where they're the same value.
4. 1v in L, 1v in R, 2 non-v in L (distinct): `vl * vr * pick2L_nonv_distinct`.
5. 1v in L, 1v in R, 2 non-v in R (distinct): `vl * vr * pick2R_nonv_distinct`.
6. 1v in L, 1v in R, 1 non-v in L, 1 non-v in R (distinct): `vl * vr * pick1L_1R_nonv_distinct`.
7. 0v in L, 2v in R, 2 non-v in L: `C(vr,2) * pick2L_nonv_distinct`.
8. 0v in L, 2v in R, 2 non-v in R: `C(vr,2) * pick2R_nonv_distinct`.
9. 0v in L, 2v in R, 1 non-v in L, 1 non-v in R: `C(vr,2) * pick1L_1R_nonv_distinct`.
10. 2v in L, 0v in R, 1 non-v in L, 1 non-v in R: `C(vl,2) * pick1L_1R_nonv_distinct`.

This is 10 cases but many are symmetric. Let me organize by (v-dist, nonv-dist):

v-dist can be (2L,0R), (1L,1R), (0L,2R).
nonv-dist can be (2L,0R), (1L,1R), (0L,2R).

For each combination, compute the count.

This requires knowing for each side:
- `vl`, `vr`, `L`, `R`.
- `pick2L_nonv_distinct`, `pick2R_nonv_distinct`, `pick1L_1R_nonv_distinct`.

And:
- `pick2L_nonv_distinct = C(L-vl, 2) - sum_{x != v} C(freqL[x], 2)`.
- `sum_{x != v} C(freqL[x], 2) = sum_x C(freqL[x], 2) - C(vl, 2)`.
- `sum_x C(freqL[x], 2) = C(L,2) - pick2L_distinct`. So `pick2L_nonv_distinct = C(L-vl, 2) - (C(L,2) - pick2L_distinct - C(vl,2)) = C(L-vl,2) - C(L,2) + pick2L_distinct + C(vl,2)`.

Hmm, let me just compute directly:
- `pick2L_distinct = C(L,2) - sum_x C(freqL[x], 2)`.
- `pick2L_nonv_distinct = C(L-vl, 2) - sum_{x != v} C(freqL[x], 2) = C(L-vl, 2) - (sum_x C(freqL[x],2) - C(vl,2))`.

Similarly for R.

`pick1L_1R_nonv_distinct = (L-vl)*(R-vr) - sum_{x != v} freqL[x]*freqR[x]`.
`sum_{x != v} freqL[x]*freqR[x] = sum_x freqL[x]*freqR[x] - vl*vr`.

OK this is computable. Let me also handle k=1 and k=3, k=4.

**k=4**: `C(vl,2)*C(vr,2)`.

**k=3**: 
- 3v in chosen, 1 non-v. The non-v can be in L or R.
- 2v in L, 1v in R, 1 non-v in R: `C(vl,2)*vr*(R-vr)`.
- 1v in L, 2v in R, 1 non-v in L: `vl*(L-vl)*C(vr,2)`.

**k=1**: 1v in chosen, 3 non-v distinct.
- 1v in L, 3 non-v in L (distinct): `vl * pick3L_nonv_distinct`.
- 1v in L, 3 non-v in R (distinct): `vl * pick3R_nonv_distinct`.
- 1v in L, 2 non-v in L, 1 non-v in R (distinct): `vl * pick2L_nonv_distinct * (R-vr) - correction`. 
  - Need the 2 in L to be distinct from each other AND from the 1 in R.
  - `vl * [pick2L_nonv_distinct * (R-vr) - sum_{x != v} C(freqL[x],2) * freqR[x]]`.
  - Hmm, the correction is for when the 1 in R equals one of the 2 in L.
- ... this gets very complicated.

**Let me reconsider**. Given the complexity, and that `n <= 1000`, let me use a different strategy:

**Strategy**: For each `i` as middle, iterate over all pairs `(a, b)` with `a < i < b` (the "cross" pair), and for each, count completions with 1 more from left and 1 more from right. Total work per `i`: `O(L * R) = O(n^2)`, total `O(n^3) = 10^9`, too slow.

**Strategy**: For each `i`, iterate over pairs in left `(a,b)` and for each, count valid right pairs. `O(L^2 * R)`, too slow.

**Strategy**: For each `i`, precompute for left: for each value `u`, count of `u` and pairs. Similarly for right. Then use formulas.

Given the time I've spent, let me implement the **k=2, k=3, k=4** cases carefully (which are the main contributors) and handle k=1 with a simpler bound or skip if too complex.

Actually wait. Let me reconsider the problem. The answer for example 1 is 6, which is `C(6,5) = 6`. For example 2, answer is 4. For example 3, answer is 0.

Let me reconsider whether k=1 cases are common. In random arrays, k=0 dominates (no v in chosen), but k=0 is always bad. k=1 requires 3 distinct non-v values, which is common. k=2 requires 2 distinct non-v values.

**Let me implement the full solution with all cases**. I'll precompute for each `i`:
- `vl, vr, L, R`.
- `sumC2L = sum_x C(freqL[x], 2)`, `sumC2R`.
- `sumProd = sum_x freqL[x] * freqR[x]`.
- `pick3L_distinct = C(L,3) - sum_x (freqL[x] * C(freqL[x]-1, 2) * 3 + ...)`. 

Actually `pick3_distinct` = number of ways to pick 3 positions with all distinct values = `C(L,3) - sum_x [ways to pick 3 with at least 2 from value x]`.

Ways to pick 3 with at least 2 from value x: `C(freqL[x], 2) * (L - freqL[x]) + C(freqL[x], 3)`.

So `pick3L_distinct = C(L,3) - sum_x [C(freqL[x],2)*(L-freqL[x]) + C(freqL[x],3)]`.

This is computable.

Similarly `pick3R_distinct`.

For k=1, the 3 non-v positions must be distinct. They can be distributed as (3L, 0R), (2L, 1R), (1L, 2R), (0L, 3R).

- (3L, 0R): `vl * pick3L_nonv_distinct`.
- (0L, 3R): `vr * pick3R_nonv_distinct`.
- (2L, 1R): `vl * [pick2L_nonv_distinct * (R-vr) - sum_{x!=v} C(freqL[x],2)*freqR[x]]`.
  - The 2 in L are distinct non-v, the 1 in R is non-v, and the 1 in R value differs from both in L.
  - Total without distinct constraint: `pick2L_nonv_distinct * (R-vr)`.
  - Subtract cases where the 1 in R equals one of the 2 in L: `sum_{x!=v} C(freqL[x],2) * freqR[x]`.
- (1L, 2R): `vr * [pick2R_nonv_distinct * (L-vl) - sum_{x!=v} freqL[x]*C(freqR[x],2)]`.

And the 1 v can be in L or R, giving factors `vl` or `vr`.

Wait, for k=1, exactly 1 of the 4 chosen is v. So:
- v in L, 3 non-v: `vl * [ways to pick 3 non-v from L and R with all distinct]`.
- v in R, 3 non-v: `vr * [ways to pick 3 non-v from L and R with all distinct]`.

Ways to pick 3 non-v from L∪R with all distinct values:
- (3L, 0R): `pick3L_nonv_distinct`.
- (2L, 1R): `pick2L_nonv_distinct * (R-vr) - sum_{x!=v} C(freqL[x],2)*freqR[x]`.
- (1L, 2R): `(L-vl) * pick2R_nonv_distinct - sum_{x!=v} freqL[x]*C(freqR[x],2)`.
- (0L, 3R): `pick3R_nonv_distinct`.

So `k=1` total = `(vl + vr) * [above]`.

This is computable! Let me code it up.

**Summary of computation per `i`**:

Precompute for left side (positions 0..i-1) and right side (positions i+1..n-1):
- `L = i`, `R = n-1-i`.
- `vl = count of v in left`, `vr = count of v in right`.
- `freqL[x]`, `freqR[x]` for all values.

Compute:
- `sumC2L = sum_x C(freqL[x], 2)`.
- `sumC2R = sum_x C(freqR[x], 2)`.
- `sumC3L = sum_x C(freqL[x], 3)`.
- `sumC3R = sum_x C(freqR[x], 3)`.
- `sumProd = sum_x freqL[x] * freqR[x]`.
- `sumC2L_prod_R = sum_{x!=v} C(freqL[x],2) * freqR[x]`.
- `sumC2R_prod_L = sum_{x!=v} freqL[x] * C(freqR[x],2)`.
- `sumC2L_prod_C2R_same = sum_{x!=v} C(freqL[x],2) * C(freqR[x],2)`. (for k=2 case where 2 non-v in L and 2 non-v in R, all 4 distinct... wait no, for k=2 the 2 non-v just need to be distinct from each other, not from v).

Wait, for k=2, the 2 non-v positions must have distinct values (from each other), but they can equal v? No, they're non-v, so they can't equal v. And they must be distinct from each other.

Let me redefine:
- `pick2L_nonv_distinct` = ways to pick 2 positions from left, both non-v, with distinct values.
  = `C(L-vl, 2) - sum_{x!=v} C(freqL[x], 2)`.
- `pick2R_nonv_distinct` = `C(R-vr, 2) - sum_{x!=v} C(freqR[x], 2)`.
- `pick1L_1R_nonv_distinct` = ways to pick 1 from left (non-v) and 1 from right (non-v) with distinct values.
  = `(L-vl)*(R-vr) - sum_{x!=v} freqL[x]*freqR[x]`.
- `pick3L_nonv_distinct` = ways to pick 3 from left, all non-v, all distinct values.
  = `C(L-vl, 3) - sum_{x!=v} [C(freqL[x],2)*(freqL[x]-2) + C(freqL[x],3)]`.
  
  Wait: ways to pick 3 from positions with value x, at least 2 from x: `C(freqL[x], 2) * (freqL[x] - 2) + C(freqL[x], 3)`.
  Actually: pick 3 with at least 2 from value x = (pick 2 from x and 1 from non-x) + (pick 3 from x) = `C(freqL[x],2) * (L - freqL[x]) + C(freqL[x], 3)`.
  
  But we want all 3 to be non-v. So we restrict to non-v positions: `L - vl` positions. Among these, value x (x!=v) has `freqL[x]` positions.
  
  `pick3L_nonv_distinct = C(L-vl, 3) - sum_{x!=v} [C(freqL[x],2)*(L-vl-freqL[x]) + C(freqL[x],3)]`.

- `pick3R_nonv_distinct` = similarly.

For k=1, the 3 non-v positions distributed across L and R:
- (3L, 0R): `pick3L_nonv_distinct`.
- (0L, 3R): `pick3R_nonv_distinct`.
- (2L, 1R): pick 2 distinct non-v from L, pick 1 non-v from R, and the R value differs from both L values.
  - Without distinct constraint between L and R: `pick2L_nonv_distinct * (R-vr)`.
  - Subtract: the R value equals one of the 2 L values. For each x!=v: `C(freqL[x],2) * freqR[x]`.
  - So: `pick2L_nonv_distinct * (R-vr) - sum_{x!=v} C(freqL[x],2)*freqR[x]`.
- (1L, 2R): `(L-vl) * pick2R_nonv_distinct - sum_{x!=v} freqL[x]*C(freqR[x],2)`.

Total non-v distinct triples = sum of above 4.

Then `k=1` contribution = `(vl + vr) * total_nonv_distinct_triples`.

For k=2, the 2 non-v positions must be distinct. Distributed as (2L,0R), (1L,1R), (0L,2R):
- (2L, 0R): `pick2L_nonv_distinct`.
- (0L, 2R): `pick2R_nonv_distinct`.
- (1L, 1R): `pick1L_1R_nonv_distinct`.

Total non-v distinct pairs = sum.

The 2 v positions distributed as (2L,0R), (1L,1R), (0L,2R):
- (2L, 0R): `C(vl, 2)`.
- (0L, 2R): `C(vr, 2)`.
- (1L, 1R): `vl * vr`.

`k=2` contribution = sum over (v-dist, nonv-dist) of `ways(v-dist) * ways(nonv-dist)`.

This is a convolution: `(C(vl,2) + vl*vr + C(vr,2)) * (pick2L_nonv_distinct + pick1L_1R_nonv_distinct + pick2R_nonv_distinct)`.

Wait, is that right? The v-dist and nonv-dist are independent (v positions and non-v positions are disjoint). Yes! So:

`k=2` = `ways_to_pick_2_v * ways_to_pick_2_nonv_distinct`.

Where `ways_to_pick_2_v = C(vl,2) + vl*vr + C(vr,2)` (pick 2 from left∪right that are v).

And `ways_to_pick_2_nonv_distinct = pick2L_nonv_distinct + pick1L_1R_nonv_distinct + pick2R_nonv_distinct`.

Great, this simplifies things!

Similarly for k=1:
`ways_to_pick_1_v = vl + vr`.
`ways_to_pick_3_nonv_distinct = pick3L_nonv_distinct + [pick2L_nonv_distinct*(R-vr) - sum C2L*R] + [(L-vl)*pick2R_nonv_distinct - sum L*C2R] + pick3R_nonv_distinct`.

`k=1` = `ways_to_pick_1_v * ways_to_pick_3_nonv_distinct`.

For k=3:
`ways_to_pick_3_v = C(vl,2)*vr + vl*C(vr,2)` (pick 3 v's: 2 from one side, 1 from other).
`ways_to_pick_1_nonv = (L-vl) + (R-vr)`.
`k=3` = `ways_to_pick_3_v * ways_to_pick_1_nonv`.

For k=4:
`ways_to_pick_4_v = C(vl,2)*C(vr,2)`.
`k=4` = `ways_to_pick_4_v`.

Total good for middle `i` = k=1 + k=2 + k=3 + k=4.

This is `O(distinct)` per `i` to compute the sums, total `O(n * distinct)`. With `n=1000`, feasible.

**Implementation plan**:
1. Coordinate compress values.
2. For each `i` from 0 to n-1:
   a. Compute `freqL` and `freqR` for all values.
   b. Compute the required sums.
   c. Compute good_i using formulas.
3. Sum good_i modulo 1e9+7.

To compute freqL and freqR efficiently, we can sweep `i` and update incrementally:
- When moving `i` to `i+1`, the element at `i` moves from left to middle, and element at `i+1` is the new middle... actually let me think.

Sweep: fix `i` as middle. Left = [0, i-1], Right = [i+1, n-1].
- Start with `i=0`: left empty, right = nums[1:].
- Move to `i=1`: left = [nums[0]], right = nums[2:].
- ...
- Move to `i+1`: left gains nums[i], right loses nums[i+1].

So we can maintain `freqL` and `freqR` incrementally in `O(1)` per step (update two values).

But we also need `vl = freqL[v]` and `vr = freqR[v]` where `v = nums[i]`. When `i` changes, `v` changes, so we need to look up the new `v`'s counts.

Also, the sums `sumC2L`, `sumC3L`, `sumProd`, etc., need to be updated incrementally. When `freqL[x]` changes by `+1` (adding nums[i] to left), `sumC2L` changes by `freqL[x]` (new C(f+1,2) - C(f,2) = f). Similarly `sumC3L` changes by `C(f+1,3) - C(f,3) = C(f,2)`.

When `freqR[x]` changes by `-1` (removing nums[i+1] from right), similar updates.

This is doable. Let me code it.

Actually, for simplicity and given `n=1000`, I can recompute freqL and freqR from scratch for each `i` in `O(n)` time, total `O(n^2) = 10^6`. That's fine and simpler.

Let me code the `O(n^2)` solution:

```python
class Solution:
    def subsequencesWithMiddleMode(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        n = len(nums)
        
        # Precompute C[x][y] for x up to n
        C = [[0]*(n+1) for _ in range(n+1)]
        for i in range(n+1):
            C[i][0] = 1
            for j in range(1, i+1):
                C[i][j] = (C[i-1][j-1] + C[i-1][j]) % MOD
        
        def comb(x, y):
            if y < 0 or y > x: return 0
            return C[x][y]
        
        ans = 0
        for i in range(n):
            v = nums[i]
            L = i
            R = n - 1 - i
            
            # Build freqL and freqR
            freqL = {}
            freqR = {}
            for j in range(L):
                freqL[nums[j]] = freqL.get(nums[j], 0) + 1
            for j in range(i+1, n):
                freqR[nums[j]] = freqR.get(nums[j], 0) + 1
            
            vl = freqL.get(v, 0)
            vr = freqR.get(v, 0)
            
            # Compute sums
            sumC2L = sum(comb(c, 2) for c in freqL.values())
            sumC2R = sum(comb(c, 2) for c in freqR.values())
            sumC3L = sum(comb(c, 3) for c in freqL.values())
            sumC3R = sum(comb(c, 3) for c in freqR.values())
            sumProd = sum(freqL[x] * freqR.get(x, 0) for x in freqL)
            # Actually need sum over all x in freqL ∪ freqR
            all_vals = set(freqL.keys()) | set(freqR.keys())
            sumProd = sum(freqL.get(x,0) * freqR.get(x,0) for x in all_vals)
            
            sumC2L_prod_R = sum(comb(freqL[x], 2) * freqR.get(x, 0) for x in freqL if x != v)
            sumC2R_prod_L = sum(freqL.get(x, 0) * comb(freqR[x], 2) for x in freqR if x != v)
            
            # pick2L_nonv_distinct
            pick2L_nonv_distinct = comb(L - vl, 2) - sum(comb(freqL[x], 2) for x in freqL if x != v)
            pick2R_nonv_distinct = comb(R - vr, 2) - sum(comb(freqR[x], 2) for x in freqR if x != v)
            pick1L_1R_nonv_distinct = (L - vl) * (R - vr) - sum(freqL.get(x,0) * freqR.get(x,0) for x in all_vals if x != v)
            
            # pick3L_nonv_distinct
            pick3L_nonv_distinct = comb(L - vl, 3) - sum(comb(freqL[x],2)*(L-vl-freqL[x]) + comb(freqL[x],3) for x in freqL if x != v)
            pick3R_nonv_distinct = comb(R - vr, 3) - sum(comb(freqR[x],2)*(R-vr-freqR[x]) + comb(freqR[x],3) for x in freqR if x != v)
            
            # k=4
            k4 = comb(vl, 2) * comb(vr, 2) % MOD
            
            # k=3
            ways_3v = comb(vl, 2) * vr + vl * comb(vr, 2)
            ways_1nonv = (L - vl) + (R - vr)
            k3 = ways_3v * ways_1nonv % MOD
            
            # k=2
            ways_2v = comb(vl, 2) + vl * vr + comb(vr, 2)
            ways_2nonv_distinct = pick2L_nonv_distinct + pick1L_1R_nonv_distinct + pick2R_nonv_distinct
            k2 = ways_2v * ways_2nonv_distinct % MOD
            
            # k=1
            ways_1v = vl + vr
            # 3 non-v distinct, distributed (3L,0R),(2L,1R),(1L,2R),(0L,3R)
            triple_3L_0R = pick3L_nonv_distinct
            triple_0L_3R = pick3R_nonv_distinct
            triple_2L_1R = pick2L_nonv_distinct * (R - vr) - sumC2L_prod_R
            triple_1L_2R = (L - vl) * pick2R_nonv_distinct - sumC2R_prod_L
            ways_3nonv_distinct = triple_3L_0R + triple_0L_3R + triple_2L_1R + triple_1L_2R
            k1 = ways_1v * ways_3nonv_distinct % MOD
            
            good_i = (k1 + k2 + k3 + k4) % MOD
            ans = (ans + good_i) % MOD
        
        return ans
```

Let me verify with examples.

**Example 1**: nums = [1,1,1,1,1,1], n=6.
For each `i`, v=1, vl=i, vr=5-i.
- i=0: L=0, R=5. vl=0, vr=5. All freqL empty, freqR={1:5}.
  - k4 = C(0,2)*C(5,2) = 0.
  - k3 = (C(0,2)*5 + 0*C(5,2)) * (0+0) = 0.
  - k2 = (0+0+10) * (0+0+0) = 0. (pick2R_nonv_distinct = C(5,2) - C(5,2) = 0).
  - k1 = 0 * ... = 0.
  - good = 0.
- i=1: L=1, R=4. vl=1, vr=4.
  - freqL={1:1}, freqR={1:4}.
  - k4 = C(1,2)*C(4,2) = 0*6 = 0.
  - k3 = (C(1,2)*4 + 1*C(4,2)) * (0+0) = (0+6)*0 = 0.
  - k2 = (0+4+6) * (0+0+0) = 10*0 = 0.
  - k1 = (1+4) * ... = 5 * 0 = 0.
  - good = 0.
- i=2: L=2, R=3. vl=2, vr=3.
  - k4 = C(2,2)*C(3,2) = 1*3 = 3.
  - k3 = (C(2,2)*3 + 2*C(3,2)) * (0+0) = (3+6)*0 = 0.
  - k2 = (1+6+3) * 0 = 0.
  - k1 = 5 * 0 = 0.
  - good = 3.
- i=3: L=3, R=2. vl=3, vr=2.
  - k4 = C(3,2)*C(2,2) = 3*1 = 3.
  - k3 = (C(3,2)*2 + 3*C(2,2)) * (0+0) = (6+3)*0 = 0.
  - k2 = (3+6+1) * 0 = 0.
  - k1 = 5 * 0 = 0.
  - good = 3.
- i=4: L=4, R=1. vl=4, vr=1.
  - k4 = C(4,2)*C(1,2) = 6*0 = 0.
  - k3 = (C(4,2)*1 + 4*C(1,2)) * (0+0) = (6+0)*0 = 0.
  - k2 = (6+4+0) * 0 = 0.
  - k1 = 5 * 0 = 0.
  - good = 0.
- i=5: L=5, R=0. vl=5, vr=0.
  - k4 = C(5,2)*C(0,2) = 10*0 = 0.
  - good = 0.

Total = 3 + 3 = 6. ✓

**Example 2**: nums = [1,2,2,3,3,4], n=6.
Expected: 4.

Let me compute for each i:
- i=0: v=1, L=0, R=5. vl=0, vr=0 (1 not in right). 
  - freqL={}, freqR={2:2,3:2,4:1}.
  - All k=0 since vl=vr=0 and no v available.
  - good=0.
- i=1: v=2, L=1, R=4. freqL={1:1}, freqR={2:1,3:2,4:1}. vl=0, vr=1.
  - k4 = C(0,2)*C(1,2) = 0.
  - k3 = (0*1 + 0*0) * (1+3) = 0.
  - k2 = (0+0+0) * ... = 0.
  - k1 = (0+1) * ... = 1 * [pick3 non-v distinct].
    - pick3L_nonv: C(1,3)=0.
    - pick3R_nonv: C(3,3) - [C(2,2)*1 + C(2,3) + C(1,2)*2 + C(1,3)] = 1 - [1*1+0+0+0] = 0.
    - triple_2L_1R: pick2L_nonv * (R-vr) - sumC2L_prod_R. pick2L_nonv = C(1,2)-0 = 0. So 0.
    - triple_1L_2R: (L-vl)*pick2R_nonv - sumC2R_prod_L. pick2R_nonv = C(3,2) - [C(1,2)+C(2,2)+C(1,2)] = 3 - [0+1+0] = 2. (L-vl)=1. sumC2R_prod_L: for x!=2, C(freqR[x],2)*freqL[x]. x=3: C(2,2)*0=0. x=4: C(1,2)*0=0. x=1: freqR[1]=0. So 0. triple_1L_2R = 1*2 - 0 = 2.
    - ways_3nonv = 0+0+0+2 = 2.
  - k1 = 1*2 = 2.
  - good = 2.

Hmm, but the expected answer is 4 total. Let me continue.

- i=2: v=2, L=2, R=3. freqL={1:1,2:1}, freqR={3:2,4:1}. vl=1, vr=0.
  - k4 = C(1,2)*C(0,2) = 0.
  - k3 = (C(1,2)*0 + 1*C(0,2)) * (1+3) = 0.
  - k2 = (0+0+0) * ... = 0.
  - k1 = (1+0) * ... = 1 * [pick3 non-v distinct].
    - pick3L_nonv: C(1,3)=0 (L-vl=1).
    - pick3R_nonv: C(3,3) - [C(2,2)*1 + 0 + C(1,2)*2 + 0] = 1 - 2 = -1. 

Wait, that's negative. Let me recheck.

`pick3R_nonv_distinct = C(R-vr, 3) - sum_{x!=v} [C(freqR[x],2)*(R-vr-freqR[x]) + C(freqR[x],3)]`.

R-vr = 3. freqR={3:2,4:1}. x!=2: x=3: C(2,2)*(3-2)+C(2,3) = 1*1+0=1. x=4: C(1,2)*(3-1)+C(1,3) = 0*2+0=0. Sum=1.
pick3R_nonv_distinct = C(3,3) - 1 = 1 - 1 = 0.

OK so 0. Let me redo:
    - pick3L_nonv: L-vl=1, C(1,3)=0.
    - pick3R_nonv: 0.
    - triple_2L_1R: pick2L_nonv*(R-vr) - sumC2L_prod_R. pick2L_nonv = C(1,2)-[C(freqL[1],2)] = 0-0=0. So 0.
    - triple_1L_2R: (L-vl)*pick2R_nonv - sumC2R_prod_L. pick2R_nonv = C(3,2)-[C(2,2)+C(1,2)] = 3-1=2. (L-vl)=1. sumC2R_prod_L: x!=2, freqL[x]*C(freqR[x],2). x=1: 1*C(0,2)=0. x=3: 0*C(2,2)=0. x=4: 0*C(1,2)=0. So 0. triple_1L_2R = 1*2 = 2.
    - ways_3nonv = 0+0+0+2 = 2.
  - k1 = 1*2 = 2.
  - good = 2.

- i=3: v=3, L=3, R=2. freqL={1:1,2:2}, freqR={3:1,4:1}. vl=0, vr=1.
  - k4 = 0.
  - k3 = 0 * (3+1) = 0.
  - k2 = 0 * ... = 0.
  - k1 = (0+1) * [pick3 non-v distinct].
    - pick3L_nonv: C(3,3) - [C(2,2)*1 + C(2,3) + C(1,2)*2 + C(1,3)] = 1 - [1+0+0+0] = 0.
    - pick3R_nonv: C(1,3)=0.
    - triple_2L_1R: pick2L_nonv*(R-vr) - sumC2L_prod_R. pick2L_nonv = C(3,2)-[C(2,2)+C(1,2)] = 3-1=2. R-vr=1. sumC2L_prod_R: x!=3, C(freqL[x],2)*freqR[x]. x=1: 0*0=0. x=2: C(2,2)*0=0. x=4: 0*1=0. So 0. triple_2L_1R = 2*1 = 2.
    - triple_1L_2R: (L-vl)*pick2R_nonv - sumC2R_prod_L. pick2R_nonv = C(1,2)-0=0. So 0.
    - ways_3nonv = 0+0+2+0 = 2.
  - k1 = 1*2 = 2.
  - good = 2.

- i=4: v=3, L=4, R=1. freqL={1:1,2:2,3:1}, freqR={4:1}. vl=1, vr=0.
  - k4 = C(1,2)*C(0,2) = 0.
  - k3 = (C(1,2)*0 + 1*0) * (3+1) = 0.
  - k2 = (0+0+0) * ... = 0.
  - k1 = (1+0) * [pick3 non-v distinct].
    - pick3L_nonv: C(3,3) - [C(2,2)*1 + 0 + 0 + 0] = 1-1=0.
    - pick3R_nonv: C(1,3)=0.
    - triple_2L_1R: pick2L_nonv*(R-vr) - sumC2L_prod_R. pick2L_nonv = C(3,2)-[C(2,2)+C(1,2)+C(1,2)] = 3-[1+0+0]=2. R-vr=1. sumC2L_prod_R: x!=3, C(freqL[x],2)*freqR[x]. x=1: 0*0=0. x=2: 1*0=0. x=4: 0*1=0. So 0. triple_2L_1R = 2.
    - triple_1L_2R: (L-vl)*pick2R_nonv - sumC2R_prod_L. pick2R_nonv = C(1,2)-0=0. So 0.
    - ways_3nonv = 0+0+2+0 = 2.
  - k1 = 1*2 = 2.
  - good = 2.

- i=5: v=4, L=5, R=0. vl=0, vr=0.
  - good = 0.

Total = 0+2+2+2+2+0 = 8. But expected is 4!

Hmm, discrepancy. Let me re-examine.

The subsequences with unique middle mode from example 2 are:
- [1,2,2,3,4] with middle 2 (i=2? no, middle is index 2 of subsequence, which is the 3rd element). The subsequence [1,2,2,3,4] has middle 2. In nums, positions: 1 at idx 0, 2 at idx 1 or 2, 2 at the other, 3 at idx 3 or 4, 4 at idx 5. Middle is 2.
- [1,2,3,3,4] with middle 3.

So there are 2 distinct subsequences, each can be formed in multiple ways.

[1,2,2,3,4]: 1 at idx 0 (forced), 4 at idx 5 (forced), 2,2 at idx 1,2 (1 way), 3 at idx 3 or 4 (2 ways). Total 2 ways.
[1,2,3,3,4]: 1 at idx 0, 4 at idx 5, 2 at idx 1 or 2 (2 ways), 3,3 at idx 3,4 (1 way). Total 2 ways.

Total = 4. ✓

But my computation gives 8. Let me find the error.

For i=1 (v=2): I got k1=2. The subsequences with middle at i=1 (value 2):
- Need 1 v from left+right, 3 non-v distinct.
- vl=0, vr=1. So the 1 v must come from right (idx > 1).
- 3 non-v distinct from left∪right excluding the chosen v.
- Left has {1}, right has {2,3,3,4} minus the chosen v.
- If chosen v is at idx 2 (value 2): right becomes {3,3,4}. 3 non-v distinct from {1}∪{3,3,4}: need 3 distinct. {1,3,4} - pick 1 from left (1) and 2 from right distinct. From right {3,3,4}, pick 2 distinct: {3,4}. So 1 way. But wait, we need 3 non-v: 1 from left + 2 from right distinct = 1 * 1 = 1. Or 0 from left + 3 from right distinct. From {3,3,4}, pick 3 distinct: impossible (only 2 distinct values). Or 2 from left + 1 from right: left has only 1 element. Or 3 from left: impossible.
  - So 1 way.
- If chosen v is at idx 3 or 4 (value 3): right becomes {2,3,4} or {2,3,4}. 3 non-v distinct from {1}∪{2,3,4}: pick 3 distinct from {1,2,3,4}. C(4,3)=4 ways.
  - But we need to pick 2 from left and 1 from right (since left has 1 element, we pick 1 from left and 2 from right, or 0 from left and 3 from right).
  - Wait, we pick 2 from left and 2 from right total. 1 is v (from right). So 2 from left + 1 non-v from right, or 1 from left + 1 non-v from right + ... wait.
  
  Let me re-examine. We pick 2 from left and 2 from right. Among these 4, exactly 1 is v (from right, since vl=0). So:
  - 2 from left (both non-v) + 1 v from right + 1 non-v from right.
  - Left has 1 element (value 1), so we pick both: 1 way. The 2 from left are {1,1}, but they must be distinct! Wait, no, for k=1, the 1 v is separate. The 2 from left are non-v, and we need them to be distinct values. But left has only 1 position with value 1, so we can't pick 2 distinct from left.
  
  Hmm, so for k=1 with vl=0, vr=1, the 1 v is from right. The remaining 3 non-v are picked from left (2 positions) and right (1 non-v position). But left has only 1 position, so we can pick at most 1 from left. So the 3 non-v must be: 1 from left + 2 from right (distinct), or 0 from left + 3 from right (distinct).
  
  Wait, we pick 2 from left and 2 from right. 1 of the 4 is v (from right). So the other 3 are: 2 from left + 1 from right, or