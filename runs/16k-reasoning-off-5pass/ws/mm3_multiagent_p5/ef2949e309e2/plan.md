We need to count length-5 subsequences where the middle element (index 2) is the unique mode. For each position `i` that can serve as the middle, we count ways to pick 2 elements before `i` and 2 elements after `i`. Let `a = nums[i]`. Let `L = i` (elements before), `R = n-1-i` (elements after). The middle is the unique mode iff: (1) the number of `a` among the 4 other chosen elements is `c` where `c <= count_a` (where `count_a` = 1 for the middle), and (2) no other value appears `>= count_a+1` times among the 4 chosen elements, and (3) if `c == count_a` (i.e., some other value ties), it's not unique.

We'll count by complement: total ways to pick 2 from left and 2 from right, minus subsequences where middle is NOT the unique mode.

For position `i`, total = C(L,2) * C(R,2).

To subtract "bad" subsequences, consider for each other value `v != a`:
- Count pairs (left, right) where `v` appears `k` times among the 4 chosen (`k >= 1`), and `v`'s count among the 4 chosen `k` is such that `v` ties or beats `a` (i.e., `k >= count_a + 1` where `count_a` in the 4 chosen equals 1 + (# of a in chosen left/right)).

This is a standard problem (LeetCode 3395). Approach: for each `i`, compute for each value `v`:
- `cl[i]`, `cr[i]` = number of `v` left/right of `i`.
- `aL = cl[i]`, `aR = cr[i]` (counts of middle value left/right).

Then the number of bad subsequences is computed by considering cases based on the count of `v` among the 4 chosen elements:
- `v` appears once: pick 1 from left+right of `v` (excluding those used for `a`), and remaining 3 from non-`a`, non-`v` positions, but only if `1 >= count_a_in_4 + 1`.
- `v` appears twice: pick 2 from left+right of `v`, remaining 2 from non-`a`, non-`v`.
- `v` appears 3 times: pick 3 from left+right of `v`, remaining 1 from non-`a`, non-`v`.
- `v` appears 4 times: pick 4 from `v`.

But we must handle when `v == a` separately (subcases where other `a`s appear).

This is complex. The known solution (LeetCode 3395) uses O(n^2) by precomputing left/right counts and using combinatorial formulas with inclusion-exclusion, or O(n^2) by iterating over pairs.

Given n ≤ 1000, O(n^2) with O(n) per pair is fine. Let me think of a cleaner approach.

**Cleaner approach**: For each middle index `i`, let `a = nums[i]`, `L = i`, `R = n-1-i`. We want to count pairs `(S_left, S_right)` where `|S_left|=2`, `|S_right|=2`, and `a` is unique mode.

Let `x` = # of `a`'s in the 4 other chosen elements. Let `y` = max count of any non-`a` value in the 4 chosen. We need: `x+1 > y`, i.e., `x+1 > y`, equivalently `y < x+1`, so `y <= x`.

Wait, middle has count `x+1` (1 + x from sides). Other value `v` has count `y_v` in the 4 chosen. We need `x+1 > y_v` for all `v != a`. So `y < x+1` where `y = max y_v`.

So valid iff `max_v y_v <= x`. And `x` can be 0,1,2,3,4 (but limited by available a's on left and right).

For each value `v != a`, let `cv = cl[i] + cr[i]` = total count of `v` excluding position `i`. The count of `v` in the 4 chosen elements follows hypergeometric: choose `y_v` from `cv` total of `v`, and `4 - y_v` from `L+R - cv` non-`v` elements.

So the count where `a` is unique mode = sum over `x` of [ways to pick x `a`'s from sides] * [ways to pick remaining 4-x from non-`a` such that max count of any value <= x].

Hmm, still complex. Let me recall the editorial approach for this exact problem (LeetCode 3395).

**Editorial approach**:
For each index `i` (middle), `L = i`, `R = n-1-i`. Let `tot = C(L,2)*C(R,2)`.

Let `aL` = count of `nums[i]` in left part (indices < i), `aR` = count in right part (indices > i). So `aL + aR` = number of `a`'s available on sides.

Let `fL2 = C(aL,2)`, `fR2 = C(aR,2)`, `fLR = aL*aR` (ways to pick 2 a's, both on left; both on right; one on each side).

For a non-`a` value `v` with `cl` count on left, `cr` count on right, `c = cl+cr`:
- Number of ways where `v` appears exactly `k` times in the 4 chosen (`k=1,2,3,4`): this is a hypergeometric distribution.

The "bad" event for `v` is: `v` appears at least as many times as `a` in the 4 chosen, AND the actual count of `a` in the 4 chosen is some value. Specifically, we need to subtract cases where the unique mode is NOT `a`. This happens when:
- Some `v != a` has count `k_v` in the 4 chosen with `k_v >= count_a_in_4 + 1`.

Using inclusion-exclusion is messy. Let me think of the known O(n^2) solution.

**Known O(n^2) solution** (LeetCode 3395 editorial):
For each middle `i`, iterate over the smaller side (say left if L <= R, else right) to fix how many `a`'s are picked from that side, and count ways.

Actually, the known efficient approach:

For each `i`, let's count "good" directly.

`good_i = total_i - bad_i`

`bad_i` = # of (left pair, right pair) such that the middle `a` is NOT the unique mode, i.e., either (i) some other value appears >= 2 times and the middle `a` appears 0 times in the 4 chosen, or (ii) middle `a` appears exactly 1 time and some other value appears 2 times, or (iii) middle `a` appears 2 times and some other appears 3 times, etc.

This decomposes based on `x` = # of `a`'s in the 4 chosen (0, 1, 2, 3, 4) and for each `x`, the # of ways to distribute these `x` `a`'s between left and right, and then from remaining positions, pick `4-x` elements such that no non-`a` value appears more than `x` times.

Hmm, I think the cleanest is: for each `i`, for each non-`a` value `v`, compute contributions and use inclusion-exclusion. Let me just code the O(n^2) solution from editorial.

Let me look up the formula mentally. The LeetCode 3395 solution:

```python
class Solution:
    def subsequencesWithMiddleMode(self, nums):
        MOD = 10**9 + 7
        n = len(nums)
        ans = 0
        for i in range(n):
            L, R = i, n-1-i
            aL, aR = 0, 0
            left_counts = {}
            right_counts = {}
            for j in range(i):
                left_counts[nums[j]] = left_counts.get(nums[j],0)+1
            for j in range(i+1,n):
                right_counts[nums[j]] = right_counts.get(nums[j],0)+1
            aL = left_counts.get(nums[i],0)
            aR = right_counts.get(nums[i],0)
            total = comb(L,2)*comb(R,2) % MOD
            
            bad = 0
            # Case analysis
            ...
```

Let me think more carefully. I'll derive it from scratch.

For middle `i`, value `a`. We pick 2 from left, 2 from right.

Let `x_l, x_r` = # of `a`'s picked from left/right, with `x_l + x_r = x` (total `a`'s in 4 chosen), `0 <= x_l <= aL`, `0 <= x_r <= aR`.

The remaining `4-x` positions: `2-x_l` from left (non-`a`) and `2-x_r` from right (non-`a`).

For the subsequence to have `a` as unique mode, we need: among the non-`a` chosen elements, every value appears at most `x` times. (Since `a` has total count `x+1`, and we need `x+1 > y_v` for all `v`, so `y_v <= x`.)

So: for each `x in {0,1,2,3,4}`:
```
good_i += sum_{x_l+x_r=x} C(aL, x_l) * C(aR, x_r) * [ways to pick (2-x_l) from L-aL non-a on left and (2-x_r) from R-aR non-a on right, with each value appearing <= x times]
```

The bracketed term is the tricky part. But we can use inclusion-exclusion or compute "bad" (where some value appears >= x+1 times) and subtract from total.

For a fixed `x` and `x_l, x_r`: let `L' = L - aL` (non-`a` on left), `R' = R - aR`. We pick `k_l = 2-x_l` from `L'`, `k_r = 2-x_r` from `R'`, total `k = 4-x` from `L'+R'`. We need no value appears more than `x` times.

This is still complex. Let me think of a different angle.

**Alternative: iterate over non-a values and subtract bad cases**.

Define "bad" = exists non-`a` value `v` with count in 4 chosen >= count of `a` in 4 chosen + 1.

Hmm, inclusion-exclusion over values is hard because many values.

**Let me try a different decomposition**: 
- Count subsequences where `a` is a mode (ties allowed).
- Subtract those where `a` ties for mode.

Subsequences where `a` is a mode (possibly tied): count of `a` in 4 chosen + 1 >= count of any other value in 4 chosen.

This is still hard.

OK here's another approach. Let's enumerate by `x_l, x_r`:

For each `x_l in [0, min(2, aL)]` and `x_r in [0, min(2, aR)]` with `x_l + x_r <= 4`:

We pick `x_l` `a`'s from left, `x_r` `a`'s from right. Then pick `2-x_l` non-`a` from left, `2-x_r` non-`a` from right.

For each non-`a` value `v` on left, count `cl[v]`, on right `cr[v]`. In the chosen, `v` appears with some count `y`. We need `y <= x_l + x_r` for uniqueness, or `y < x_l + x_r + 1`, i.e., `y <= x_l + x_r`.

For a given `x = x_l + x_r`, the "bad" ways are where some `v` has `y >= x+1`.

Let's define `f(x_l, x_r)` = # ways to pick `(2-x_l)` non-`a` from left, `(2-x_r)` non-`a` from right, such that max count of any single value <= `x = x_l+x_r`.

Using inclusion-exclusion on which value exceeds `x`:

`f(x_l, x_r) = sum_{S subset of values} (-1)^|S| * [ways where each v in S has count >= x+1]`

But enumerating subsets is infeasible.

**Alternative: for each non-a value v, compute its "bad" contribution assuming it's the worst, then use union bound / inclusion-exclusion with pairwise... no this is getting complex.

Let me look for a smarter O(n^2) approach.

**Approach: Fix pairs on the smaller side, iterate**

For each middle `i`, WLOG assume `L <= R` (left is smaller side). Iterate over the C(L, 2) left pairs. For each left pair, count # of right pairs (2 from right) such that the resulting 5-element subseq has `a` as unique mode.

For a fixed left pair (2 elements from left), let's say they contribute counts. Let `c_v` = count of value `v` in the left pair (0, 1, or 2). Then we need to pick 2 from right such that overall:
- `a`'s count in (left pair + right pair) + 1 (the middle) > any other value's count in (left pair + right pair).

Let `c_a` = count of `a` in left pair. Let `c_v` for `v != a`. We need for all `v != a`: `c_a + d_v + 1 > c_v + e_v` where `d_v, e_v` are counts in right pair (only one of them is nonzero, the value of the right pair, or if both same, `e_v=2` etc).

Actually, the right pair has 2 elements. Let the right pair be values `(r1, r2)`. They contribute to counts: value `r1` gets +1, value `r2` gets +1 (or +2 if `r1=r2`).

We need: `c_a + [1 if a in right pair else 0] + 1 > c_v + [1 if v in right pair once] + [2 if v in right pair twice]` for all `v != a`.

Equivalently, for all `v != a`: `c_a + 1 + I(a in right) > c_v + I(v in right once) + 2*I(v in right twice)`.

This is still complex per right pair. But for a fixed left pair, the constraint involves only whether `a` is in right pair and which value is in right pair.

Hmm. Let me think of yet another approach.

**Direct count via cases on x_l, x_r**:

For each `i` and each `(x_l, x_r)` with `x_l + x_r = x`:

Good = `C(aL, x_l) * C(aR, x_r) * g(x_l, x_r)`

where `g(x_l, x_r)` = ways to pick `2-x_l` non-`a` from left and `2-x_r` non-`a` from right, with each non-`a` value appearing at most `x = x_l+x_r` times.

For `g`, let's compute total minus bad. Total = `C(L-aL, 2-x_l) * C(R-aR, 2-x_r)`.

Bad = # ways where some non-`a` value `v` has count in the chosen `>= x+1`.

Since we're picking only `4-x` non-`a` elements total (some from left, some from right), and `x+1 > 4-x` when `x >= 2`, when `x >= 2`, it's impossible for any value to have count `>= x+1` (since total non-`a` chosen is `4-x <= x`). So bad = 0 for `x >= 2`. Wait, `x+1 > 4-x` iff `2x > 3` iff `x >= 2`. Yes! So for `x >= 2`, all choices are good.

So we only need to handle `x = 0` and `x = 1` carefully (for `x >= 2`, `g = C(L-aL, 2-x_l) * C(R-aR, 2-x_r)`).

**Case x >= 2**: 
For each `(x_l, x_r)` with `x_l + x_r = x >= 2`:
contribution = `C(aL, x_l) * C(aR, x_r) * C(L-aL, 2-x_l) * C(R-aR, 2-x_r)`

Sum over all such `(x_l, x_r)`.

**Case x = 0**: 
`x_l = x_r = 0`. We pick 2 non-`a` from left, 2 non-`a` from right, and NO `a` in the 4 chosen. We need max count of any value <= 0, i.e., no value can appear at all! But we're picking 4 elements, contradiction. So `x=0` contributes 0.

Wait, max count <= 0 means all counts are 0, but we pick 4 non-`a` elements, so they have positive counts. So 0 ways. Yes, `x=0` gives 0.

**Case x = 1**:
`x_l + x_r = 1`. Either `(1,0)` or `(0,1)`.

We pick 1 `a` from one side, 0 from other. Then `2-x_l` non-`a` from one side, `2-x_r` from other.

Sub-case `(x_l, x_r) = (1, 0)`: 1 `a` from left, 0 from right. Then pick 1 non-`a` from left, 2 non-`a` from right.

Constraint: each non-`a` value appears at most 1 time in the 3 chosen non-`a` elements. So all 3 non-`a` elements must be distinct.

# ways = `C(aL, 1) * C(R-aR, 2) * [ways to pick 1 non-a from L-aL distinct, and 2 non-a from R-aR all distinct and distinct from the left pick]`.

Hmm. The 3 non-`a` chosen must all be distinct. So we pick 3 distinct values from the union, with specific left/right split.

# ways = `aL * C(R-aR, 2) * [ways to pick 1 from L-aL such that it's a value not appearing in the 2 right picks]`.

For each choice of 2 distinct non-`a` values from right (with no repetition within right pair), we need the left non-`a` to be a value different from those 2.

This is getting complicated because of the "distinctness" constraint coupling left and right.

Let me reconsider. The 3 non-`a` elements (1 from left, 2 from right) must be all different values.

Let me denote left non-`a` value as `u`, right non-`a` values as `(v1, v2)` (could be same or different). We need `u != v1`, `u != v2`, and if `v1 = v2`, that's the same value twice on right.

So constraint: `u != v1`, `u != v2`. (And `v1, v2` can be anything, including equal.)

Hmm wait, if `v1 = v2 = v`, then the value `v` appears 2 times. We need max count <= 1 (since `x=1`, `a` count = `1+1=2`, other values need count < 2, i.e., <= 1). So `v` can't appear 2 times. So we also need `v1 != v2`.

OK so all 3 must be distinct values. This is complex.

**Let me re-examine my earlier claim**. For `x = 1`, `a` appears 1+1=2 times. For uniqueness, other values can appear at most 1 time. So the non-`a` elements (3 of them) must all be distinct values.

For `x = 0`, `a` appears 1 time, others must appear 0 times, impossible.

For `x = 1`, the 3 non-`a` chosen are all distinct.

For `x = 2`, `a` appears 3 times, others can appear up to 2 times. The non-`a` chosen are 2, they can be same or different.

For `x = 3`, `a` appears 4 times, others up to 3 times. Non-`a` chosen is 1, trivially fine.

For `x = 4`, `a` appears 5 times, all 4 sides are `a`, trivially fine.

**For x >= 2, easy** (no constraint beyond pick any).

**For x = 1, constraint**: the 3 non-`a` chosen are all distinct.

**Compute # ways for x=1**:

Sub-case `(1, 0)`: 
- Ways to pick 1 `a` from left: `aL`.
- Ways to pick 0 `a` from right: 1.
- Ways to pick 1 non-`a` from left + 2 non-`a` from right, all 3 distinct.

Sub-case `(0, 1)`: symmetric.

Let me compute the "3 distinct" count. Let's define:
- `L' = L - aL` non-`a` on left, `R' = R - aR` non-`a` on right.
- For each value `v`, `cl[v]` count on left (non-`a`), `cr[v]` count on right.
- We pick 1 from left, 2 from right, all distinct values.

# ways = sum over distinct value `u` chosen from left: `cl[u] * (ways to pick 2 from right, both != u, and they can be same or different)`.

`ways to pick 2 from right, both != u` = `C(R' - cr[u], 2)`.

So # ways = `sum_u cl[u] * C(R' - cr[u], 2)`.

Wait, but we also need the 2 right ones to be... no, for `x=1`, we need all 3 distinct, so the 2 right ones can be same or different as long as both != `u`.

So: `ways_3_distinct_(1_left, 2_right) = sum_v cl[v] * C(R' - cr[v], 2)`.

Similarly for `(2_left, 1_right)`: `sum_v cr[v] * C(L' - cl[v], 2)`.

So `good for x=1 at position i` = `aL * sum_v cl[v] * C(R'-cr[v], 2) + aR * sum_v cr[v] * C(L'-cl[v], 2)`.

Wait let me re-derive. For `(x_l, x_r) = (1, 0)`:
- 1 `a` from left: `aL` ways.
- 1 non-`a` from left: `cl[v]` for some `v` -> pick a specific value `v`, `cl[v]` ways.
- 2 non-`a` from right, both != `v`: `C(R' - cr[v], 2)` ways.

Total for `(1,0)`: `sum_v aL * cl[v] * C(R' - cr[v], 2)`... wait no, `aL` is just one factor.

`= aL * sum_v cl[v] * C(R' - cr[v], 2)`.

Similarly `(0,1)`: `aR * sum_v cr[v] * C(L' - cl[v], 2)`.

Great, this is computable.

**For x >= 2**:

For each `(x_l, x_r)` with `x_l + x_r = x`, `x in {2,3,4}`, `0 <= x_l <= min(2, aL)`, `0 <= x_r <= min(2, aR)`:

`C(aL, x_l) * C(aR, x_r) * C(L-aL, 2-x_l) * C(R-aR, 2-x_r)`.

Sum these.

**Total for position i**:
`good_i = (sum for x=1) + (sum for x>=2)`.

Let me code this. But wait, I should double-check `x=1` case.

`x=1`, `x_l + x_r = 1`. The middle contributes 1, plus 1 from sides = 2 `a`'s total. Other values appear at most 1 time in the 4 chosen. So the 3 non-`a` (since we pick 4 total, 1 is `a`, 3 non-`a`) must all be distinct. Yes.

Actually wait, I should double check. We pick 4 elements from the sides (2 left + 2 right). If `x_l + x_r = 1`, then 1 is `a` and 3 are non-`a`. These 3 non-`a` must have no value repeated (each appears at most 1 time). And the 1 `a` doesn't conflict with non-`a` (they're different). So yes, the 3 non-`a` are 3 distinct values.

Now the way I pick them: 1 non-`a` from left + 2 non-`a` from right (sub-case `(1,0)`), or 2 from left + 1 from right (sub-case `(0,1)`).

For `(1,0)`: left has 1 non-`a`, right has 2 non-`a`, all 3 distinct.

`= sum_v (cl[v] * C(R' - cr[v], 2))` where the sum is over all non-`a` values `v` with `cl[v] > 0` and `R' - cr[v] >= 2`.

Yes, that looks right.

Now let me also verify `x >= 2`:
- `x=2`: `a` appears 3 times. Others at most 2 times. The 2 non-`a` chosen can be same value (count 2) or different. No constraint beyond picking. So total ways = `C(L-aL, 2-x_l) * C(R-aR, 2-x_r)`. ✓
- `x=3`: 1 non-`a` chosen, trivially any. ✓
- `x=4`: 0 non-`a` chosen, 1 way. ✓

Now let's also verify the count `cl[v]` for non-`a` values:
- `L' = L - aL` non-`a` on left.
- For value `v != a`, `cl[v]` = count of `v` in `nums[0..i-1]`.
- `cr[v]` = count of `v` in `nums[i+1..n-1]`.

`C(R' - cr[v], 2)` where `R' = R - aR`. This is correct: total non-`a` on right minus those equal to `v`, choose 2.

OK this approach works.

**Compute the sum for x=1 efficiently**:

We need `sum_v cl[v] * C(R' - cr[v], 2)` summed over non-`a` values `v`.

We can precompute `cl[v]` and `cr[v]` for all `v`. For each `i`, iterating over all distinct values in the array is O(n) per `i`, giving O(n^2) total. Since n <= 1000, this is fine.

Similarly for x >= 2 case, we just need combinatorial values which are O(1) per `(x_l, x_r)`.