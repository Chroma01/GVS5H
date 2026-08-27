The problem asks for the number of subsequences of length 5 where the middle element (index 2) is the unique mode. A brute-force O(n^5) approach is infeasible for n up to 1000. We need an O(n^2) or O(n^2 log n) solution.

The standard approach is to iterate over the middle element `nums[m]`. For each `m`, we want to choose 2 elements to the left of `m` (in increasing order of index) and 2 elements to the right of `m` (in increasing order of index). Let `L` be the set of indices `i < m` and `R` be the set of indices `j > m`.

We can split the calculation into:
1. **Valid pairs**: Total pairs (left, right) such that no element other than `nums[m]` appears more than once.
2. **Subtract conflicts**: Pairs where some other element `x` appears twice, making `nums[m]` not the unique mode.

To do this efficiently, for each `m`, we can iterate over potential "bad" elements `x != nums[m]`. We need to count the number of ways to pick 2 left indices and 2 right indices such that `x` appears at least twice among the 4 chosen elements.

For a fixed middle index `m` and a fixed conflicting value `x`:
- Let `cL` = number of `x`'s in the left part.
- Let `cR` = number of `x`'s in the right part.
- Let `L0` = number of non-`x` elements in the left part = `(m) - cL`.
- Let `R0` = number of non-`x` elements in the right part = `(n - 1 - m) - cR`.

We choose 2 left elements. They can contain 0, 1, or 2 occurrences of `x`. Similarly for the right side. To make `x` appear at least twice in total, we sum over the distributions of occurrences of `x` in the left pair and right pair such that their sum is at least 2.

The number of ways to choose 2 left elements is `C(m, 2)`. We can compute the number of "valid" choices (where `x` appears at most 1 time in left pair AND at most 1 time in right pair) and subtract it from the total `C(m, 2) * C(n - 1 - m, 2)`. This valid count gives subsequences where `x` does NOT tie or beat the middle. We then use inclusion-exclusion? No, the standard trick for this specific problem (LeetCode 3395) is:

For each middle index `m`:
- Total pairs = `C(left, 2) * C(right, 2)`.
- For each value `v != nums[m]`, calculate the number of ways `v` appears at least twice in the chosen 4 elements. Let's call this `bad(v)`.
- If a subsequence has `v` appearing >= 2 times, it's bad. But multiple `v`'s could appear >= 2 times? Actually, in a sequence of length 5, if the middle is `nums[m]`, the other 4 elements are distributed as 2 left, 2 right. The only way `nums[m]` is NOT the unique mode is if some other value appears at least twice. Since the total other elements is 4, at most one other value can appear twice (or one three times, etc). Wait, if one value appears 3 times, it beats the middle (which appears at least 1 time, but if middle is distinct, the other appears 3 times -> bad). If two different values each appear twice, that's impossible because 2+2=4, so the middle must be one of them? No, the middle is fixed as `nums[m]`. If two other values each appear twice, the middle appears 1 time, so the other values tie with 2. Then the mode is not unique. But in 4 elements, the only way two different values appear twice is impossible because 2+2=4, leaving 0 for the middle. But the middle is fixed. So exactly one other value can appear >= 2 times, or no other value appears >= 2 times.

Wait, if the middle is `A`, and the left 2 are `B, B` and right 2 are `C, C`, then the frequencies are A:1, B:2, C:2. The modes are B and C, not A. So this is bad. So we can have multiple bad values. However, we need to subtract the number of subsequences where `nums[m]` is NOT the unique mode. This is the union of events "value v appears at least twice".

Actually, the standard solution for LeetCode 3395 is:
- Iterate `m` from 0 to n-1.
- For each `m`, maintain a frequency map for the left side as we expand `m` outwards? No, that's for online.
- Standard O(n^2) approach: fix `m`. We want to count pairs `(l1, l2)` from left and `(r1, r2)` from right.
- Total pairs = `C(m, 2) * C(n-1-m, 2)`.
- Subtract pairs where some other value appears twice. We can process this by iterating over the other values present in the left and right.
- For each value `v != nums[m]`, let `cL` be its count in left, `cR` in right.
- The number of ways `v` appears at least twice in the chosen 4 elements is:
  - Choose 2 left containing `v`: `C(cL, 2) * C(R0, 2)` (where `R0` is right non-v) -> but wait, this counts cases where right has 0 of v, so total v is 2.
  - Choose 2 right containing `v`: `C(L0, 2) * C(cR, 2)`.
  - Choose 1 left and 1 right containing `v`: `cL * cR * L0 * R0`? No, we need to choose 1 left (which can be v or non-v? No, the 2 left elements must contain exactly 1 v, so we choose 1 v from left and 1 non-v from left? That's not right. We choose 2 left elements. To have exactly 1 v in left pair, we choose 1 v and 1 non-v: `cL * L0`. Similarly for right: `cR * R0`. So 1 left v and 1 right v gives 2 v's total.
  - Wait, what if left has 2 v's? Then we need 0 v's in right. That's `C(cL, 2) * C(R0, 2) + C(cL, 2) * cR * 2`? No, if left has 2 v's, we can have right with 0 v's (so 2 non-v's) or right with 1 v (1 non-v).
  - Actually, it's simpler: Number of ways `v` appears >= 2 times in the 4 chosen elements = Total ways - Ways `v` appears 0 times - Ways `v` appears 1 time.
    - Ways 0 times: `C(L0, 2) * C(R0, 2)`.
    - Ways 1 time: left has 1 v, right has 0 v + left has 0 v, right has 1 v = `cL * L0 * C(R0, 2) + C(L0, 2) * cR * R0`.
  - So `bad(v) = Total - good(0) - good(1)`.

However, we must be careful: a subsequence might have TWO different values `v1` and `v2` each appearing twice. In that case, `nums[m]` is not the unique mode, and it is counted in both `bad(v1)` and `bad(v2)`. So we need to add back the intersection (using inclusion-exclusion). But in a sequence of 4 elements (2 left, 2 right), can we have two different values each appearing exactly twice? That would require the 4 elements to be `v1, v1, v2, v2`. The middle is `nums[m]`. This is possible! Example: left is `v1, v2`, right is `v1, v2` (order doesn't matter, just multiset). So `v1` appears twice, `v2` appears twice. Then `nums[m]` is not the unique mode.

So we need to subtract `bad(v)` for all `v`, but add back `bad(v1, v2)` for pairs. This makes it complicated.

Is there a simpler O(n^2) approach? Yes, the standard editorial for this problem uses a different method:
- Iterate `m` from 0 to n-1.
- We will pick 2 left and 2 right.
- Total ways to pick 2 left and 2 right = `C(m, 2) * C(n-1-m, 2)`.
- For the middle `nums[m]` to be the unique mode, no other value can appear more than once in the 4 chosen elements, AND no other value can appear exactly twice while `nums[m]` appears once (so `nums[m]` beats them). Wait, if `nums[m]` appears once, and another value appears twice, that other value is the mode. So we need NO other value to appear twice or more. So each other value can appear at most once in the 4 chosen elements.
- So we need: in the chosen 2 left elements, all values are distinct. In the chosen 2 right elements, all values are distinct. AND no value appears in both left and right (because then that value appears twice). AND no value equals `nums[m]` in the left or right? Wait, if `nums[m]` appears in left or right, its count becomes 2 or 3. That's fine! The middle is `nums[m]`. If `nums[m]` appears in left, the frequency of `nums[m]` in the subsequence is 2. That's strictly greater than 1 (from the middle), so it's still the unique mode (unless another value appears twice, but we already forbid other values appearing twice).
- So the conditions are:
  1. Left 2 elements are distinct.
  2. Right 2 elements are distinct.
  3. The 4 elements (left + right) are all distinct EXCEPT possibly `nums[m]`. That is, no value other than `nums[m]` can appear in both left and right.
- So we can calculate:
  - Total pairs - (pairs where left has duplicate) - (pairs where right has duplicate) - (pairs where some non-`nums[m]` value appears in both left and right).
- Wait, this is a direct counting! Let's check.
  - Total pairs = `C(m, 2) * C(n-1-m, 2)`.
  - Subtract pairs where left has duplicate (both elements same value `v`):
    - For each `v` in left, number of ways to pick 2 identical `v` in left is `C(count_L(v), 2)`. For each such choice, we can pick any 2 from right: `C(right_size, 2)`.
    - But we must be careful: if `v == nums[m]`, is that bad? If left has two `nums[m]`, then the subsequence has three `nums[m]`. That's still unique mode! So duplicates of `nums[m]` are GOOD. So we only subtract for `v != nums[m]`.
  - Subtract pairs where right has duplicate of `v != nums[m]`.
  - Add back pairs where left has duplicate of `v != nums[m]` AND right has duplicate of `w != nums[m]`. This could be `v == w` or `v != w`.
    - If `v == w`, we chose 2 `v` in left and 2 `v` in right. This means `v` appears 4 times. `nums[m]` is not the mode. This is correctly subtracted twice and added once.
    - If `v != w`, we chose 2 `v` in left and 2 `w` in right. `v` appears twice, `w` appears twice. `nums[m]` appears once. Not a unique mode. Correctly subtracted twice and added once.
  - Subtract pairs where some value `v != nums[m]` appears in both left and right (i.e., one in left, one in right).
    - For each `v != nums[m]`, we choose 1 `v` from left and 1 `v` from right. The other left element can be anything (distinct from this chosen one? No, we are just counting the number of pairs where at least one such cross-pair exists). Wait, we are using inclusion-exclusion on the conditions.
    - Let's define events:
      - A_v: `v` appears twice in left (both left elements are `v`).
      - B_v: `v` appears twice in right.
      - C_v: `v` appears once in left and once in right.
    - We want to count pairs that avoid A_v, B_v, C_v for all `v != nums[m]`.
    - Total = `T`.
    - We can compute: Valid = `T - sum_{v != m} (ways A_v + ways B_v + ways C_v) + sum_{v != m, w != m} (ways A_v \cap B_w + ways A_v \cap C_w + ways B_v \cap C_w) - ...`
    - This seems complicated because of intersections.

Wait, is there a simpler formula?
Let's rethink: The 4 chosen elements must not contain any value (other than `nums[m]`) more than once. This is equivalent to saying: the 4 elements form a set of size 4 if we ignore `nums[m]`, or size 3 if one of them is `nums[m]`. In other words, the number of distinct values among the 4 elements, counting `nums[m]` as a special value, must be at least 3 if `nums[m]` is not in the 4, or at least 2 if `nums[m]` is in the 4.
Actually, the condition "no other value appears more than once" means:
- If we look at the multiset of the 4 elements, every value `v != nums[m]` has multiplicity <= 1.
- So the 4 elements are a collection where duplicates are only allowed for `nums[m]`.
- So the 4 elements are formed by picking some number of `nums[m]` (0, 1, or 2) and the rest are all distinct values different from `nums[m]`.

So we can count directly:
- Case 0: 0 `nums[m]` in the 4 elements. The 4 elements are 4 distinct values != `nums[m]`. The number of ways to choose such a 4-tuple is: choose 2 from left (distinct, != `nums[m]`) and 2 from right (distinct, != `nums[m]`) and no overlap.
- Case 1: 1 `nums[m]` in the 4 elements. It can be in left or right.
  - Subcase 1a: 1 in left. Then left has 1 `nums[m]` and 1 other (distinct from `nums[m]`). Right has 2 distinct, != `nums[m]`, and distinct from the left other.
  - Subcase 1b: 1 in right. Symmetric.
- Case 2: 2 `nums[m]` in the 4 elements. They can be both in left, both in right, or one in each.
  - Subcase 2a: 2 in left. Left has 2 `nums[m]`. Right has 2 distinct, != `nums[m]`.
  - Subcase 2b: 2 in right. Right has 2 `nums[m]`. Left has 2 distinct, != `nums[m]`.
  - Subcase 2c: 1 in left, 1 in right. Left has 1 `nums[m]` and 1 other (distinct). Right has 1 `nums[m]` and 1 other (distinct). And the two "other" elements must be distinct from each other.

This direct counting is O(n^2) if we can precompute for each index `m`:
- The number of distinct pairs in left, right, etc.
But we need to be careful with overlaps. For example, in Case 0, we need to pick 2 from left (distinct, != m), 2 from right (distinct, != m), and no value appears in both. This is like picking a set of 2 from left and 2 from right with no intersection of values.
This is similar to counting independent sets in a bipartite graph where left nodes are indices, right nodes are indices, and edges connect same values. But n=1000, n^2 is 10^6, which is fine.

Actually, the standard O(n^2) solution for this problem (LeetCode 3395) is:
- Iterate `m` from 0 to n-1.
- Maintain a frequency array `freq` for the right side initially empty, or we can just use prefix/suffix.
- For each `m`, we can process the left and right sets.
- But there's a known O(n^2) solution that fixes `m` and iterates over the left elements, and for each left element, we know the number of valid right elements.

Let's recall the exact algorithm for "Subsequences With a Unique Middle Mode II" or similar. Wait, this is LeetCode 3395. I remember the solution:
- For each `m`, we want to count the number of pairs (L, R) where L is a 2-element subset of indices < m, R is a 2-element subset of indices > m, such that no value other than `nums[m]` appears more than once in L union R.
- This is equivalent to: the 4 values in L union R are all distinct, except possibly `nums[m]`.
- We can iterate `i` from 0 to `m-1`. For each `i`, we consider the pair (i, something in right).
- Wait, the known solution uses a different approach:
  - Total ways = `C(m, 2) * C(n-1-m, 2)`.
  - We subtract the ways where some value `v` appears at least twice.
  - For each `v != nums[m]`, let `cL` be count in left, `cR` in right.
  - Ways `v` appears >= 2 times = `C(cL, 2)*C(n-1-m, 2) + C(m, 2)*C(cR, 2) + C(cL, 2)*C(cR, 2) - ...` wait, no.
  - The number of ways to choose 2 left and 2 right such that `v` appears at least twice is:
    - Choose 2 left containing `v` (can be `C(cL, 2)` or `cL * (m - cL)`) and any 2 right.
    - But we must ensure that the total number of `v`'s is at least 2.
    - It's easier to compute the number of ways `v` appears 0 or 1 time, and subtract from total.
    - Ways 0 times: `C(m - cL, 2) * C(n-1-m - cR, 2)`.
    - Ways 1 time: left has 1, right has 0 + left has 0, right has 1 = `cL * (m - cL) * C(n-1-m - cR, 2) + C(m - cL, 2) * cR * (n-1-m - cR)`.
    - So `bad(v) = Total - ways(0) - ways(1)`.
  - But as noted, there can be overlaps (two different `v`'s each appearing twice). We need inclusion-exclusion.
  - However, the problem can be solved without inclusion-exclusion by using the fact that we only care about the middle being the UNIQUE mode. If we count the number of ways where `nums[m]` is NOT the unique mode, this is the number of ways some other value appears >= 2 times.
  - Since the other 4 elements can have at most one value appearing >= 2 times, OR two values each appearing exactly twice? Wait, if two values each appear twice, the middle appears once, so the modes are the two values, not the middle. But is it possible to have two values each appearing twice? Yes, e.g., `v1, v2, m, v1, v2`. Here `v1` and `v2` both appear twice. So `m` is not the unique mode.
  - So we need to subtract the number of ways where ANY value `v != m` appears >= 2 times. This is the union of events `E_v` = "v appears >= 2 times".
  - The intersection of two such events `E_v` and `E_w` (v != w) is the event "v appears >= 2 times AND w appears >= 2 times". Since the total number of non-middle elements is 4, this requires v to appear at least 2 times and w to appear at least 2 times, so v appears exactly 2 and w appears exactly 2 (or v=2, w=2; v=3, w=1; but w can't be 1 if w>=2). So v appears exactly 2, w appears exactly 2. This is a valid intersection.
  - So we would need inclusion-exclusion over all pairs, which is O(k^2) where k is the number of distinct values, too slow.

Wait, is there a way to compute the number of valid pairs directly without inclusion-exclusion?
Yes, by considering the 4 elements as a sequence and ensuring all values except `nums[m]` are distinct.
Let's define:
- `L` = set of indices < m.
- `R` = set of indices > m.
- We need to choose 2 indices from L and 2 from R.
- The 4 values must satisfy: for any value `v != nums[m]`, its frequency in the 4 chosen indices is at most 1.
- This means the 4 chosen indices, if we remove `nums[m]`, must have all distinct values.
- So the 4 indices correspond to a set of values where `nums[m]` can appear 0, 1, or 2 times, and all other values appear exactly once (if present).
- So the 4 indices are formed by:
  - 0 `nums[m]`: 4 distinct values != `nums[m]`. 2 from L, 2 from R.
  - 1 `nums[m]`: either in L or R. The other 3 indices must have distinct values != `nums[m]`, and no overlap.
  - 2 `nums[m]`: could be (2 in L, 0 in R), (0 in L, 2 in R), (1 in L, 1 in R). The non-`nums[m]` indices must be distinct.

This seems like we can compute it by iterating over the combinations of left and right elements.
But n=1000, n^2 is 1e6. If we do something O(n) per middle, it's O(n^2). If we do O(n) per middle per distinct value, it might be O(n^2) with a small constant if we only iterate over the actual values present.

Actually, the known solution for this exact problem (LeetCode 3395) is O(n^2) and goes like this:
- For each `m` from 0 to n-1:
  - Let `L` be the list of values to the left of `m`, `R` to the right.
  - We can iterate `i` from 0 to `m-1`. For each `i`, we can compute the number of valid right pairs for each left pair (i, j) or something.
  - Alternatively, we can precompute for each index the number of distinct values to its left/right, etc.

Let's search my memory for the standard solution.
I recall a solution that uses the "contribution" technique:
- For each `m`, we count the number of pairs (l, r) of subsets.
- We can use a frequency map for the right side.
- For each `m`, we initialize a frequency map for the right side with all elements > m.
- Then we iterate `i` from 0 to `m-1` (left elements).
- We remove `nums[i]` from the right frequency? No, we can just maintain a map of right frequencies.
- For each `i`, we want to pair it with another left element `j` (i < j < m) and two right elements.
- This is getting complicated.

Another approach: The total number of subsequences of size 5 is `C(n, 5)`. But we need unique middle mode.
Let's think about the constraints: n <= 1000. O(n^2) is 1e6, which is very fast in Python. O(n^2 * log n) or O(n^2) with hash maps is also fine.
Can we do O(n^2) with the following:
For each `m`:
  - Count `C(m, 2) * C(n-1-m, 2)`.
  - Subtract bad pairs.
  - To subtract bad pairs, we can iterate over all `v != nums[m]`. How many such `v`? At most n.
  - For each `v`, we need to know `cL` and `cR`.
  - The number of bad pairs due to `v` is:
    - `bad(v) = C(cL, 2)*C(n-1-m, 2) + C(m, 2)*C(cR, 2) + C(cL, 2)*C(cR, 2) + cL*(m-cL)*C(cR, 2) + C(cL, 2)*cR*(n-1-m-cR) + cL*(m-cL)*cR*(n-1-m-cR)` ... wait, this counts all pairs where `v` appears at least twice.
    - Let's simplify: Number of ways to choose 2 left and 2 right such that `v` appears at least twice.
    - We can choose 2 left and 2 right. Let `x` be the number of `v`'s in left pair, `y` in right pair. We need `x + y >= 2`.
    - `x` can be 0, 1, 2. `y` can be 0, 1, 2.
    - Total ways = `C(m, 2) * C(n-1-m, 2)`.
    - Ways with `x+y <= 1`:
      - x=0, y=0: `C(m - cL, 2) * C(n-1-m - cR, 2)`
      - x=1, y=0: `cL * (m - cL) * C(n-1-m - cR, 2)`
      - x=0, y=1: `C(m - cL, 2) * cR * (n-1-m - cR)`
    - So `bad(v) = Total - above`.
  - This is easy to compute for each `v` if we have `cL` and `cR`.
  - But we have the double-counting issue (two different `v`'s each appearing twice).
  - However, note that in a bad pair, if two different values `v` and `w` each appear twice, then the four elements are `v, v, w, w`. This is counted in `bad(v)` and in `bad(w)`. So we need to add it back once.
  - How many such pairs? We need to choose 2 `v`'s and 2 `w`'s. This is `C(cL_v, 2)*C(cR_w, 2) + C(cL_w, 2)*C(cR_v, 2) + cL_v * cL_w * C(cR_v, 2)`? No, the four elements are partitioned into left pair and right pair. The left pair can be (v,v) and right pair (w,w) -> `C(cL_v, 2) * C(cR_w, 2)`. Or left (w,w) and right (v,v) -> `C(cL_w, 2) * C(cR_v, 2)`. Or left (v,w) and right (v,w) -> `cL_v * cL_w * cR_v * cR_w`. So there are 3 configurations.
  - So the number of pairs where BOTH `v` and `w` appear >= 2 times is:
    - For each configuration, the number of ways:
      - Config 1: left has 2 v, right has 2 w. Ways: `C(cL_v, 2) * C(cR_w, 2)`.
      - Config 2: left has 2 w, right has 2 v. Ways: `C(cL_w, 2) * C(cR_v, 2)`.
      - Config 3: left has 1 v, 1 w; right has 1 v, 1 w. Ways: `cL_v * cL_w * cR_v * cR_w`.
    - Total for pair (v, w) is sum of these three.
  - So we would need to sum this over all pairs (v, w). This is O(n^2) per middle, which is O(n^3) total. Too slow.

So inclusion-exclusion over pairs of values is too slow. We need a direct way to count valid pairs.

Let's go back to the direct condition: The 4 chosen elements (2 left, 2 right) must have the property that every value except `nums[m]` appears at most once.
This is equivalent to: The 4 elements are either:
- 4 distinct values != `nums[m]`.
- 1 `nums[m]` and 3 distinct values != `nums[m]`.
- 2 `nums[m]` and 2 distinct values != `nums[m]`.
In all cases, the non-`nums[m]` elements are all distinct.
So the number of valid pairs is the number of ways to choose 2 left and 2 right such that the non-`nums[m]` elements are all distinct.
This is exactly: Total ways to choose 2 left and 2 right, MINUS the ways where there is some duplication among the non-`nums[m]` elements.
Duplication among non-`nums[m]` elements can happen in two ways:
1. Both left elements are the same value `v != nums[m]`.
2. Both right elements are the same value `v != nums[m]`.
3. One left element and one right element are the same value `v != nums[m]`.
Note that if left has (v, v) and right has (v, v), this is covered by 1 and 2 and 3. But wait, 3 counts pairs where one left is v and one right is v. If left is (v, v) and right is (v, v), then there are two v's in left and two in right. Does 3 count this? No, 3 requires exactly one v in left and one v in right. So the union of 1, 2, 3 covers all cases where there is a duplicate of a non-`nums[m]` value.
Let's check if 1, 2, 3 are mutually exclusive? No.
- 1 and 2: left has (v, v) and right has (w, w). Here v and w are != nums[m]. This is covered by 1 (for v) and 2 (for w). It is NOT covered by 3 because 3 requires one in left and one in right, i.e., same value in both.
- 1 and 3: left has (v, v) and right has (v, x). This is covered by 1 (v in left) and 3 (v in right). Is it possible? Yes.
- 2 and 3: left has (v, x) and right has (v, v). Covered by 2 and 3.
- 1 and 2 and 3: left has (v, v) and right has (v, v). Covered by 1, 2, and 3? Wait, 3 is "one left and one right are the same value v". But here both left are v and both right are v. So there ARE a left v and a right v. So 3 applies. But does 3 overcount? We need to be careful with inclusion-exclusion.

However, we can count the number of pairs that DO NOT satisfy 1, 2, or 3.
Valid = Total - |1 \cup 2 \cup 3|.
By inclusion-exclusion:
|1 \cup 2 \cup 3| = sum |1_v| + sum |2_v| + sum |3_v| - sum |1_v \cap 1_w| - sum |2_v \cap 2_w| - sum |3_v \cap 3_w| - sum |1_v \cap 2_w| - sum |1_v \cap 3_w| - sum |2_v \cap 3_w| + sum |1_v \cap 2_w \cap 3_x| + ...
This seems to lead back to the same complexity.

Is there a way to compute the number of valid pairs in O(k) per middle, where k is the number of distinct values on the left or right?
Let's analyze the conditions again.
We want to choose 2 left indices and 2 right indices.
Let the left indices be `i1 < i2`. The values are `a = nums[i1], b = nums[i2]`.
Let the right indices be `j1 < j2`. The values are `c = nums[j1], d = nums[j2]`.
Conditions for valid:
- a, b, c, d are not all distinct? No, they can have duplicates only if the duplicate is `nums[m]`.
So the multiset {a, b, c, d} can contain `nums[m]` at most twice, and any other value at most once.
This means:
- If a == b, then a must be nums[m].
- If c == d, then c must be nums[m].
- If a == c, then a must be nums[m].
- If a == d, then a must be nums[m].
- If b == c, then b must be nums[m].
- If b == d, then b must be nums[m].
- If a == nums[m] and c == nums[m], that's fine.
- If a != nums[m], then a must be different from b, c, d.

So basically, the 4 elements can be seen as:
- We have 4 slots: L1, L2, R1, R2.
- We want to assign values to them such that the only allowed duplicates are with `M = nums[m]`.
- This is equivalent to: The 4 values are either:
  - All 4 distinct and != M.
  - One is M, the other 3 are distinct and != M.
  - Two are M, the other 2 are distinct and != M.

So we can count:
1. Pairs with 0 M's: 4 distinct values != M.
   - Number of ways = (number of ways to choose 2 left with distinct values != M) * (number of ways to choose 2 right with distinct values != M) - (number of ways where a left value equals a right value).
   - This is still complex because of the cross condition.

Wait, we can precompute for each middle `m`:
- The number of ways to choose 2 left with distinct values != M.
- The number of ways to choose 2 right with distinct values != M.
- The number of ways to choose 2 left and 2 right with all 4 values distinct and != M.
But the cross condition (no shared value between left and right) is the hard part.

Let's think differently. The problem is from LeetCode 3395. I am almost certain the intended solution is O(n^2) and works as follows:
- For each `m` from 0 to n-1:
  - Total pairs = `C(m, 2) * C(n - 1 - m, 2)`.
  - We subtract the number of pairs that are "bad".
  - A pair is bad if there exists a value `v != nums[m]` that appears at least twice in the 4 chosen elements.
  - We can count the number of bad pairs by iterating over all possible "bad" values `v`.
  - For a fixed `v`, the number of pairs where `v` appears at least twice is:
    - `C(cL, 2) * C(R_total, 2) + C(L_total, 2) * C(cR, 2) - C(cL, 2) * C(cR, 2)`?
    - Let's be precise. We choose 2 left and 2 right. Let `x` be the number of `v`'s in left, `y` in right. We want `x + y >= 2`.
    - Total = `C(m, 2) * C(R_size, 2)`.
    - Ways with `x + y <= 1`:
      - x=0, y=0: `C(m - cL, 2) * C(R_size - cR, 2)`
      - x=1, y=0: `cL * (m - cL) * C(R_size - cR, 2)`
      - x=0, y=1: `C(m - cL, 2) * cR * (R_size - cR)`
    - So `bad(v) = Total - these`.
  - Now, to handle the overcounting (when two different `v` and `w` both appear twice), we can use the fact that the problem only has 4 elements. If we know the exact number of ways to have NO duplicates of non-M values, we can compute it directly by:
    - Valid = Total - (pairs with duplicate in left) - (pairs with duplicate in right) - (pairs with duplicate across left and right) + (pairs with duplicate in left AND duplicate in right) + (pairs with duplicate in left AND duplicate across) + (pairs with duplicate in right AND duplicate across) - (pairs with all three).
  - Let's define:
    - `DL` = number of pairs with duplicate in left (both left elements equal, value != M).
      - `DL = sum_{v != M} C(cL_v, 2) * C(R_size, 2)`.
    - `DR` = number of pairs with duplicate in right.
      - `DR = sum_{v != M} C(L_size, 2) * C(cR_v, 2)`.
    - `DC` = number of pairs with duplicate across (one in left, one in right, same value v != M).
      - `DC = sum_{v != M} cL_v * cR_v * (L_size - 1) * (R_size - 1)`? No.
      - We need to choose 2 left and 2 right such that one left and one right are `v`. The other left can be anything (but not v? No, we are counting the number of pairs that have AT LEAST one such cross duplicate). If we just want to count pairs with AT LEAST one cross duplicate of v, we can count pairs with EXACTLY one cross duplicate of v.
      - Actually, to use inclusion-exclusion correctly, we should define the events precisely.
      - Event A_v: left has two v's.
      - Event B_v: right has two v's.
      - Event C_v: left has one v and right has one v.
      - We want to count pairs that avoid all A_v, B_v, C_v for v != M.
      - Note that C_v is a specific condition: exactly one v in left and exactly one v in right.
      - But wait, if left has two v's and right has one v, then C_v is true (there is at least one v in left and one in right). So A_v and C_v can overlap.
      - To use inclusion-exclusion, we can define the events based on the actual configuration of the 4 elements. There are C(4,2) = 6 ways to partition 4 elements into left and right. But we have indices, so order matters.
      - Alternatively, we can use the principle of counting valid configurations directly by iterating over the values.
      - Since n <= 1000, the number of distinct values in the whole array is at most 1000. For a fixed m, the number of distinct values in left and right is at most 1000.
      - We can iterate over all values v != M. For each v, we have cL_v and cR_v.
      - The number of ways to choose 2 left and 2 right such that the non-M values are all distinct is:
        - Total ways to choose 2 left and 2 right: `C(m,2) * C(R,2)`.
        - Subtract ways where at least one non-M value is duplicated.
        - This is equivalent to: the 4 chosen elements, after removing M's, have no duplicates.
        - So the chosen elements (ignoring M) must be a set of size 4, 3, or 2.
        - If we iterate over the number of M's in the 4 elements (0, 1, 2):
          - 0 M's: choose 4 distinct non-M values, 2 from left, 2 from right.
          - 1 M: choose 1 M (in left or right) and 3 distinct non-M values, with 2 in the same side as M and 1 in the other, or 1 in same and 2 in other? Wait, the M takes one slot. The other 3 slots are 2 on one side, 1 on the other. So either (2 left, 1 right) or (1 left, 2 right). The 3 non-M values must be distinct.
          - 2 M's: could be (2 left, 0 right), (0 left, 2 right), (1 left, 1 right). The non-M values are 0, 0, or 2 distinct.
        - This still seems to require knowing the intersection of values between left and right.

Let's reconsider the approach of subtracting bad events.
We want to compute:
Valid = Total - |A \cup B \cup C|, where:
A = union of A_v (v != M)
B = union of B_v (v != M)
C = union of C_v (v != M)
But we can compute |A|, |B|, |C| easily.
|A| = sum_{v != M} C(cL_v, 2) * C(R, 2)
|B| = sum_{v != M} C(L, 2) * C(cR_v, 2)
|C| = sum_{v != M} cL_v * cR_v * (L - 1) * (R - 1)? No, C_v is "there is at least one v in left and at least one v in right". The number of ways to choose 2 left and 2 right such that left contains at least one v and right contains at least one v.
- We can choose 1 v and 1 non-v in left, and 1 v and 1 non-v in right: `cL_v * (L - cL_v) * cR_v * (R - cR_v)`.
- We can choose 2 v in left and 1 v in right: `C(cL_v, 2) * cR_v * (R - cR_v)`.
- We can choose 1 v in left and 2 v in right: `cL_v * (L - cL_v) * C(cR_v, 2)`.
- We can choose 2 v in left and 2 v in right: `C(cL_v, 2) * C(cR_v, 2)`.
- So |C_v| = the sum of these 4 terms. This is exactly the number of ways v appears at least once in left and at least once in right.
But note that if v appears 3 or 4 times, it's also in C_v.
Actually, the union of A_v, B_v, C_v covers all cases where v appears at least twice? No, C_v includes cases where v appears exactly once in left and once in right. That's a duplicate! Because the value v appears in both left and right, so in the 4 elements, v appears twice. And it's not M. So it IS bad.
So the bad condition is: there exists v != M such that v appears at least twice in the 4 elements.
This is equivalent to: v appears 2 in left, OR 2 in right, OR 1 in left and 1 in right, OR 3 in left, etc.
So the bad events for v are exactly A_v, B_v, C_v as defined above! Because if v appears at least twice, either it has 2 in left (A_v), or 2 in right (B_v), or 1 in left and 1 in right (C_v). (If it has 3 in left, A_v is true. If 2 in left and 1 in right, A_v and C_v are true.)
So the set of bad pairs is exactly A \cup B \cup C.
We can compute |A|, |B|, |C| using the formulas above.
Now, we need the intersections:
|A \cap B|, |A \cap C|, |B \cap C|, and |A \cap B \cap C|.
Let's compute |A \cap B|:
A = union of A_v, B = union of B_w.
Intersection means there exists v with A_v and w with B_w.
Case 1: v == w. Then we have 2 v in left and 2 v in right. This is `C(cL_v, 2) * C(cR_v, 2)`.
Case 2: v != w. Then we have 2 v in left and 2 w in right. This is `C(cL_v, 2) * C(cR_w, 2)`.
So |A \cap B| = sum_v C(cL_v, 2) * C(cR_v, 2) + sum_{v != w} C(cL_v, 2) * C(cR_w, 2).
Note that sum_{v != w} = sum_v C(cL_v, 2) * sum_w C(cR_w, 2) - sum_v C(cL_v, 2) * C(cR_v, 2).
So |A \cap B| = sum_v C(cL_v, 2) * C(cR_v, 2) + (sum_v C(cL_v, 2)) * (sum_w C(cR_w, 2)) - sum_v C(cL_v, 2) * C(cR_v, 2)
= (sum_v C(cL_v, 2)) * (sum_w C(cR_w, 2)).
Wait! This is beautiful!
Because A_v is about left, B_w is about right. They are independent! The only thing is we sum over all v and w. There is no restriction that v != w for the intersection to be non-empty? Actually, if v=w, the pair has 2 v in left and 2 v in right, which is counted in A_v and B_v. So it is in the intersection. The formula (sum A_v) * (sum B_w) exactly counts all pairs of (A_v, B_w) events, including v=w.
But wait, we are counting pairs of events. The intersection A \cap B is the set of pairs that are in A and in B. A pair is in A if there is SOME v with A_v. A pair is in B if there is SOME w with B_w. So the pair is in A \cap B if there exists v and w (possibly different) such that the pair satisfies A_v and B_w.
The number of such pairs is indeed the number of pairs that satisfy A_v for some v AND B_w for some w.
If we define `A_total` = number of pairs satisfying A_v for some v = sum_v C(cL_v, 2) * C(R, 2).
And `B_total` = sum_w C(L, 2) * C(cR_w, 2).
Then is |A \cap B| = A_total * B_total / Total? No! That would be if they were independent, but they are not. A pair is counted in A_total if it has a duplicate in left. It is counted in B_total if it has a duplicate in right. These are independent! The left duplicate and right duplicate are independent choices. So the number of pairs that have BOTH a left duplicate (of some value) and a right duplicate (of some value) is exactly the product of the number of ways to have a left duplicate and the number of ways to have a right duplicate?
Wait. If a pair has left duplicate of v and right duplicate of w, it is counted once in A_total (under v) and once in B_total (under w).
So the number of pairs that have at least one left duplicate AND at least one right duplicate is NOT A_total * B_total. A_total * B_total would count pairs with left duplicate of v and right duplicate of w multiple times if there are multiple ways.
But we want the NUMBER of pairs, not the sum over events.
For a specific pair, it can have left duplicate of v and right duplicate of w. How many such (v, w) pairs exist for this configuration? If the left pair is (v, v) and right pair is (w, w), there is exactly one v and one w. So it contributes 1 to A_v and 1 to B_w. So it is counted once in A_total and once in B_total.
What if the left pair is (v, v) and the right pair also contains v? Say left is (v, v), right is (v, w). Then this pair has a left duplicate (v) and a right duplicate (w). It also has a right duplicate? No, right is (v, w), so the right duplicate is w. It does NOT have a right duplicate of v. So it is in A_v and B_w. It is counted once in A_total and once in B_total.
What if left is (v, v) and right is (v, v)? Then it has left duplicate v and right duplicate v. It is counted in A_v and B_v. So once in A_total and once in B_total.
So for ANY pair that has a left duplicate and a right duplicate, it is counted EXACTLY ONCE in A_total (for the specific value duplicated in left) and EXACTLY ONCE in B_total (for the specific value duplicated in right).
Therefore, the number of such pairs is exactly the number of pairs of (left duplicate choice, right duplicate choice) that result in a valid pair.
But the left duplicate choice and right duplicate choice are made independently! We just pick a left duplicate (which is a choice of value v and 2 indices in left), and a right duplicate (value w and 2 indices in right). Any such independent choices give a valid pair that has a left duplicate and a right duplicate.
Wait, is that true? If we pick a left duplicate of v and a right duplicate of w, the resulting pair definitely has a left duplicate and a right duplicate. And every pair with a left duplicate and a right duplicate is formed by exactly one such choice of (v, w) and indices? Yes, because the left duplicate uniquely determines v and the 2 indices, and the right duplicate uniquely determines w and the 2 indices.
So the number of pairs in A \cap B is EXACTLY (sum_v C(cL_v, 2)) * (sum_w C(cR_w, 2)) * C(R_remaining)? No!
Let's be careful. A pair is defined by the choice of 2 left indices and 2 right indices.
The number of ways to choose 2 left indices that form a duplicate of some value v is: for each v, C(cL_v, 2). So the number of "left duplicate" 2-subsets is `S_L = sum_v C(cL_v, 2)`.
Similarly, the number of "right duplicate" 2-subsets is `S_R = sum_w C(cR_w, 2)`.
To form a pair in A \cap B, we must pick a left duplicate 2-subset AND a right duplicate 2-subset. Are these choices independent? YES! The left subset and right subset are disjoint, so we can pick any left duplicate and any right duplicate independently.
So the number of pairs in A \cap B is `S_L * S_R`.
This is amazing! So `|A \cap B| = S_L * S_R`.

Now, what about |A \cap C|?
A is the set of pairs with a left duplicate. C is the set of pairs with a cross duplicate (at least one v in left and at least one v in right, for some v).
Intersection: pairs that have a left duplicate AND a cross duplicate.
If a pair has a left duplicate, say left is (v, v). Then it has a cross duplicate if right contains v. So the right subset must contain at least one v.
The number of such pairs: For each v, we choose 2 v's in left (C(cL_v, 2)), and we choose a right subset of size 2 that contains at least one v.
The number of right subsets containing at least one v is `C(R, 2) - C(R - cR_v, 2)`.
So `|A \cap C| = sum_v C(cL_v, 2) * (C(R, 2) - C(R - cR_v, 2))`.
This is NOT a simple product. It depends on the specific v.

Similarly, |B \cap C| = sum_w C(cR_w, 2) * (C(L, 2) - C(L - cL_w, 2)).

And |A \cap B \cap C|?
Pairs with left duplicate, right duplicate, and cross duplicate.
This means there is a left duplicate of some v, a right duplicate of some w, AND a cross duplicate of some x.
If we have left duplicate of v and right duplicate of w, the left pair is (v, v) and right pair is (w, w). The cross duplicate condition means there is some x that appears in both left and right. Since left only has v, the cross duplicate must be x = v. So v must appear in right. But right only has w. So w must equal v.
So A \cap B \cap C requires v = w. So we need a value v that has a duplicate in left, a duplicate in right, AND appears in both (which is automatic if it has duplicates in both? No, if it has duplicate in left, left is (v, v). For it to appear in right, right must contain v. But right is (w, w). So right must be (v, v). Thus v = w.
So A \cap B \cap C is exactly the set of pairs where left is (v, v) and right is (v, v) for some v.
The number of such pairs is `sum_v C(cL_v, 2) * C(cR_v, 2)`.

This is still computable! We just need to iterate over v.
So the inclusion-exclusion is:
|A \cup B \cup C| = |A| + |B| + |C| - |A \cap B| - |A \cap C| - |B \cap C| + |A \cap B \cap C|.
All terms can be computed in O(k) where k is the number of distinct values in left and right (at most 1000).
For each m, we can precompute cL_v and cR_v for all v. This can be done by maintaining two frequency maps as we sweep m.
But wait, we need to do this for each m. If we rebuild the maps for each m, it's O(n^2) to build and O(n) to compute, total O(n^2). n=1000, so 1e6 operations, very fast.

Let's verify this logic.
Total pairs = T.
A = pairs with left duplicate (v != M). Note: A only includes v != M. What if the left duplicate is M? That's GOOD! We don't want to subtract it. So A_v is only for v != M.
Similarly for B_v and C_v, only v != M.
Let's re-evaluate:
Valid = T - |A \cup B \cup C|, where A, B, C are unions over v != M.
We have:
T = C(m, 2) * C(R, 2).
|A| = sum_{v != M} C(cL_v, 2) * C(R, 2).
|B| = sum_{v != M} C(L, 2) * C(cR_v, 2).
|C| = sum_{v != M} [cL_v * cR_v * ...] wait, we need the exact formula for |C|.

Let's derive |C| again.
C_v: the pair has at least one v in left and at least one v in right.
Number of ways to choose 2 left and 2 right such that left has at least one v and right has at least one v.
= Total ways to choose left and right - (left has 0 v) - (right has 0 v) + (left has 0 v AND right has 0 v)
= C(L, 2)*C(R, 2) - C(L - cL_v, 2)*C(R, 2) - C(L, 2)*C(R - cR_v, 2) + C(L - cL_v, 2)*C(R - cR_v, 2).
So |C| = sum_{v != M} [ T - C(L - cL_v, 2)*C(R, 2) - C(L, 2)*C(R - cR_v, 2) + C(L - cL_v, 2)*C(R - cR_v, 2) ].
This is O(k) to compute.

Now |A \cap B|:
A_v: left has two v's. B_w: right has two w's.
We want the number of pairs that have a left duplicate of some v != M and a right duplicate of some w != M.
As argued, this is exactly the number of ways to pick a left duplicate of v and a right duplicate of w independently.
Number of left duplicates = S_L = sum_{v != M} C(cL_v, 2).
Number of right duplicates = S_R = sum_{w != M} C(cR_w, 2).
So |A \cap B| = S_L * S_R.
This is correct because any left duplicate and any right duplicate can be combined to form a unique pair, and all such pairs are in A \cap B.

Now |A \cap C|:
A_v: left has two v's. C_w: right has at least one w, left has at least one w.
But wait! C_w is defined for a specific w. The union C is over w != M.
So A \cap C is the set of pairs that have a left duplicate of some v != M AND have a cross duplicate of some w != M.
If a pair has a left duplicate of v, then left is (v, v). For it to have a cross duplicate of w, we need w to be in left and in right. Since left only has v, we must have w = v, and v must be in right.
So A \cap C is exactly the set of pairs where left is (v, v) and right contains v (and v != M).
The number of such pairs is: for each v != M, C(cL_v, 2) * (number of right subsets containing at least one v).
Number of right subsets containing at least one v is C(R, 2) - C(R - cR_v, 2).
So |A \cap C| = sum_{v != M} C(cL_v, 2) * (C(R, 2) - C(R - cR_v, 2)).
This is O(k).

Similarly, |B \cap C| = sum_{v != M} C(cR_v, 2) * (C(L, 2) - C(L - cL_v, 2)).

Now |A \cap B \cap C|:
A_v, B_w, C_x.
Left is (v, v), right is (w, w). Cross duplicate of x means x is in left and right. So x = v and x = w, hence v = w.
So we need v = w, and v != M.
The number of such pairs is sum_{v != M} C(cL_v, 2) * C(cR_v, 2).

So the bad count is:
Bad = |A| + |B| + |C| - |A \cap B| - |A \cap C| - |B \cap C| + |A \cap B \cap C|.
Valid = T - Bad.

Let's double check this with a small example.
n=6, nums = [1, 2, 2, 3, 3, 4]
m=1 (nums[1]=2). L = [1], R = [2, 2, 3, 3, 4]. L_size=1, R_size=4.
M=2.
T = C(1,2)*C(4,2) = 0 * 6 = 0. Valid=0.
m=2 (nums[2]=2). L=[1,2], R=[3,3,4]. L_size=2, R_size=3.
M=2.
T = C(2,2)*C(3,2) = 1 * 3 = 3.
cL: 1->1, 2->1. cR: 3->2, 4->1. (M=2 is not in R).
v != M: 1, 3, 4.
|A|: C(cL_1,2)*C(3,2) = 0. C(cL_3,2)=0. C(cL_4,2)=0. So |A|=0.
|B|: C(2,2)*C(cR_3,2) = 1*1 = 1. C(cR_4,2)=0. So |B|=1.
|C|: T - C(2-cL_v,2)*C(3,2) - C(2,2)*C(3-cR_v,2) + C(2-cL_v,2)*C(3-cR_v,2).
For v=1: cL=1, cR=0. T=3. C(1,2)*3=0. C(2,2)*C(3,2)=3. C(1,2)*C(3,2)=0. Term = 3 - 0 - 3 + 0 = 0.
For v=3: cL=0, cR=2. T=3. C(2,2)*3=3. C(2,2)*C(1,2)=0. C(2,2)*C(1,2)=0. Term = 3 - 3 - 0 + 0 = 0.
For v=4: cL=0, cR=1. Term = 3 - 3 - 0 + 0 = 0.
So |C|=0.
|A \cap B| = S_L * S_R. S_L = C(1,2)+C(1,2)=0. S_R = C(2,2)+C(1,2)=1. So |A \cap B|=0.
|A \cap C|: sum C(cL_v,2)*(C(3,2) - C(3-cR_v,2)). All C(cL_v,2)=0. So 0.
|B \cap C|: sum C(cR_v,2)*(C(2,2) - C(2-cL_v,2)).
v=3: C(2,2)=1. C(2,2)-C(2,2)=0. Term=0.
v=4: C(1,2)=0. Term=0.
|A \cap B \cap C| = sum C(cL_v,2)*C(cR_v,2) = 0.
Bad = 0 + 1 + 0 - 0 - 0 - 0 + 0 = 1.
Valid = T - Bad = 3 - 1 = 2.
The valid subsequences of size 5 with middle 2 at index 2:
Indices: 0,1,2,3,4 or 0,1,2,3,5 or 0,1,2,4,5.
Let's check them:
0,1,2,3,4: 1,2,2,3,3. Modes: 2 and 3 (both twice). Middle is 2. Not unique mode. Bad.
0,1,2,3,5: 1,2,2,3,4. Frequencies: 1:1, 2:2, 3:1, 4:1. Mode is 2, unique. Valid.
0,1,2,4,5: 1,2,2,4,3. Same as above. Valid.
So 2 valid. Matches!

Let's test m=3 (nums[3]=3). L=[1,2,2], R=[3,4]. L_size=3, R_size=2.
M=3.
T = C(3,2)*C(2,2) = 3 * 1 = 3.
cL: 1->1, 2->2. cR: 4->1, 3->1.
v != M: 1, 2, 4.
|A|: C(cL_1,2)=0, C(cL_2,2)=1. C(R,2)=1. |A|=1.
|B|: C(L,2)=3. C(cR_4,2)=0, C(cR_1? no 1 is in left), 3 is M. |B|=0.
|C|: T - C(3-cL_v,2)*C(2,2) - C(3,2)*C(2-cR_v,2) + C(3-cL_v,2)*C(2-cR_v,2).
v=1: cL=1, cR=0. T=3. C(2,2)*1=1. C(3,2)*C(2,2)=0. C(2,2)*C(2,2)=0. Term = 3-1-0+0=2.
v=2: cL=2, cR=0. T=3. C(1,2)*1=0. C(3,2)*C(2,2)=3. C(1,2)*C(2,2)=0. Term = 3-0-3+0=0.
v=4: cL=0, cR=1. T=3. C(3,2)*1=3. C(3,2)*C(1,2)=0. C(3,2)*C(1,2)=0. Term = 3-3-0+0=0.
|C| = 2.
|A \cap B| = S_L * S_R. S_L = C(1,2)+C(2,2)=1. S_R = 0. So 0.
|A \cap C|: sum C(cL_v,2)*(C(2,2)-C(2-cR_v,2)).
v=1: 0.
v=2: C(2,2)=1. C(2,2)-C(2,2)=0. Term=0.
v=4: 0.
|A \cap C| = 0.
|B \cap C|: sum C(cR_v,2)*(C(3,2)-C(3-cL_v,2)). All C(cR_v,2)=0. So 0.
|A \cap B \cap C| = 0.
Bad = 1 + 0 + 2 - 0 - 0 - 0 + 0 = 3.
Valid = 3 - 3 = 0.
Check subsequences with middle at index 3 (value 3):
Indices: 0,1,2,3,4 -> 1,2,2,3,4. Valid (we found it earlier).
Wait! The subsequence 0,1,2,3,4 is a subsequence of size 5. It has middle at index 2! Because the size is 5, the middle is the 3rd element (index 2). So for a fixed middle m, we are choosing 2 from left and 2 from right. The subsequence's middle is m. So the middle is always m. So the subsequence 0,1,2,3,4 has middle index 2, not 3. The subsequence 0,1,3,4,5? We need 2 left and 2 right for m=3. Left indices < 3: {0,1,2}. Right indices > 3: {4,5}.
So the possible pairs of right indices are {4,5}. Left pairs: {0,1}, {0,2}, {1,2}.
Pairs:
(0,1) left = 1,2. Right = 3,4. Subsequence: 1,2,3,3,4. Modes: 1:1, 2:1, 3:2, 4:1. Unique mode is 3. Valid.
(0,2) left = 1,2. Right = 3,4. Subsequence: 1,2,2,3,4. Modes: 1:1, 2:2, 3:1, 4:1. Mode is 2, not 3. Bad.
(1,2) left = 2,2. Right = 3,4. Subsequence: 2,2,2,3,4? No, left is {1,2} which is nums[1]=2, nums[2]=2. So left values are 2,2. Right values are nums[4]=3, nums[5]=4. Subsequence: 2,2,3,3,4. Modes: 2:2, 3:2. Not unique. Bad.
So only 1 valid for m=3. But my formula gave 0?
Let's recalculate for m=3.
T = 3.
|A| = C(cL_2,2)*C(R,2) = 1 * 1 = 1. (This counts pair (1,2) left).
|C|: v=1 term was 2. What does this count?
v=1: cL_1=1, cR_1=0. Term = T - C(3-1,2)*1 - C(3,2)*C(2,2) + C(2,2)*C(2,2) = 3 - 1 - 0 + 0 = 2.
Wait, the formula for |C| was: pairs with cross duplicate of v.
v=1: cL_1=1 (index 0), cR_1=0. Cross duplicate of 1 means 1 is in left and 1 is in right. But cR_1=0! So it should be 0!
Why did the formula give 2?
Ah! The formula: T - C(L - cL_v, 2)*C(R, 2) - C(L, 2)*C(R - cR_v, 2) + C(L - cL_v, 2)*C(R - cR_v, 2).
For v=1: L=3, cL_1=1, so L-cL=2. R=2, cR_1=0, so R-cR=2.
T = 3.
C(2,2)*C(2,2) = 1*1 = 1.
C(3,2)*C(2,2) = 3*1 = 3.
C(2,2)*C(2,2) = 1.
Term = 3 - 1 - 3 + 1 = 0.
Wait