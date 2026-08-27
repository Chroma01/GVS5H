
## ideation
The core difficulty lies in efficiently counting the number of valid subsequences where the middle element is the unique mode. A brute-force approach checking all combinations is O(n^5), which is too slow for n=1000.

Key observations:
1. The subsequence has fixed size 5, with the middle element at index 2 of the subsequence.
2. We iterate through each element in `nums` as the potential middle element `m` at index `i`.
3. We need to choose 2 elements from `nums[0:i]` (left) and 2 elements from `nums[i+1:n]` (right).
4. Let `k` be the total frequency of `m` in the subsequence (1 + count from left + count from right). `k` can be 1, 2, or 3 (since we pick at most 2 more from left/right).
5. For `m` to be the unique mode, all other elements in the subsequence must have frequency strictly less than `k`.
   - If k=1: All other 4 elements must be distinct and not equal to `m`. Also, no other element can appear twice (because if another element appears twice, its frequency is 2 which is > 1, violating unique mode condition for m). Actually, if k=1, then m appears once. The other 4 elements must all have frequency < 1, i.e., 0? That's impossible. Wait: frequency in the subsequence. If another element appears twice, its frequency is 2, which is > 1, so m is not the mode. If another element appears once, its frequency is 1, which is equal to m's frequency, so the mode is not unique. Therefore, for k=1, it's impossible for m to be the unique mode because there will always be other elements with frequency >= 1. Actually, if all 4 other elements are distinct and different from m, then each has frequency 1, same as m, so mode is not unique. So k=1 yields 0 valid subsequences.
   - If k=2: m appears twice. The other 3 elements must have frequency < 2, i.e., 1. So the other 3 elements must be distinct from each other and from m.
   - If k=3: m appears three times. The other 2 elements must have frequency < 3, which is always true since there are only 2 other elements. They can be same or different. But we need to ensure that no other element has frequency >= 3, which is impossible with only 2 slots. So any pair works as long as we account for the counts of m.

So we only need to consider k=2 and k=3.

For each index `i` as middle:
- Precompute frequency maps for left (`left_freq`) and right (`right_freq`) parts.
- For k=2: We need exactly 1 more `m` from left or right (so total 2 for m). 
  - Case 1: 1 from left, 0 from right. Choose 1 `m` from left, and 1 other from left (not m), and 2 others from right (not m, and distinct from each other and from the left-other).
  - Case 2: 0 from left, 1 from right. Symmetric.
  - Actually, simpler: Total ways to choose 2 from left and 2 from right such that exactly 1 is `m` (from either side) and the other 3 are distinct and not `m`.
  
This is getting complex. A better approach:
For each middle index `i`:
1. Maintain `left_freq` and `right_freq` as we iterate `i` from 1 to n-2 (since we need at least 2 on each side).
2. For each `i`, let `m = nums[i]`.
3. Calculate `l_m = left_freq.get(m, 0)`, `r_m = right_freq.get(m, 0)`.
4. For k=2 (m appears twice in subsequence):
   - We need to pick exactly 1 `m` from left or right, and the other 3 elements must be non-m and distinct.
   - Subcase 1: Pick 1 `m` from left, 1 non-m from left, 2 non-m from right (distinct from each other and from left non-m).
     Ways = `l_m * ( (i) - l_m ) * C(r_m, 0) * ...` wait, we need to choose 2 from right that are not m and distinct.
     Actually, the number of ways to choose 2 distinct non-m elements from right is: 
     Let `R = right_freq` (excluding m). The number of pairs of distinct elements from right is: 
     Total pairs from right (non-m) minus pairs where both are same.
     Total non-m elements in right: `right_total = (n-1-i) - r_m`.
     Total ways to choose 2 from right non-m: `C(right_total, 2)`.
     But this includes pairs where both are same element? No, `C(n,2)` chooses 2 distinct indices, but if the values are same, it's still one pair of indices. The condition is that the values are distinct? No, the condition is that the frequency of any other element is < 2, i.e., 1. So if we pick two elements from right that have the same value, that value will have frequency 2 in the subsequence, which is not < 2, so it violates the condition.
     Therefore, we need to choose 2 elements from right that have different values (and not m).
     Similarly for left.
     
This suggests we need to count pairs of indices from left/right with distinct values.

Given the complexity, an O(n^2) approach per middle element is acceptable if n=1000? 1000*1000=1e6, which is fine.

Alternative plan:
For each middle index `i`:
1. Get left part `L = nums[0:i]`, right part `R = nums[i+1:n]`.
2. For k=2:
   - Count ways to choose 2 from L and 2 from R such that:
     - Exactly one of the 4 is `m` (nums[i]).
     - The other 3 are not `m` and all have distinct values.
   - This can be broken into:
     a) 1 `m` from L, 1 non-m from L, 2 non-m from R (distinct values).
     b) 0 `m` from L, 2 non-m from L (distinct values), 1 `m` from R, 1 non-m from R.
   - For a, we need:
     - Choose 1 `m` from L: `l_m` ways.
     - Choose 1 non-m from L: `i - l_m` ways.
     - Choose 2 non-m from R with distinct values: 
       Let `freq_R` be frequency map of R (excluding m). 
       Total ways to choose 2 indices from R non-m: `C(right_total, 2)`.
       Minus ways where both have same value: sum over x in R non-m of `C(freq_R[x], 2)`.
     - But we also need the non-m from L to have a value different from both chosen from R? Yes, because if the non-m from L equals one of the non-m from R, then that value appears twice, which is not < 2.
     So we need: 
       Let `val_L` be the value of the non-m chosen from L.
       Then the two chosen from R must not include `val_L` and must be distinct from each other.
     This requires iterating over possible values for the non-m from L, which is O(n) per middle, leading to O(n^2) per middle, total O(n^3) which is 1e9, too slow.

Given the constraints and complexity, perhaps a different strategy is needed. 

Reconsider: Since the subsequence size is small (5), and we fix the middle, we can iterate over all possible pairs from left and right? That's O(n^2) per middle, total O(n^3). With n=1000, 1e9 operations might be borderline in Python.

However, note that we only care about frequencies. We can precompute for each middle index, the frequency maps for left and right. Then for k=2 and k=3, use combinatorics with inclusion-exclusion or direct counting.

For k=3:
- m appears 3 times. So we pick 2 more m's from left and right.
- The other 2 elements can be anything (since their max frequency is 2, which is < 3).
- So for k=3:
  - Choose 2 m's from left: `C(l_m, 2)`
  - Choose 0 m's from right: `C(r_m, 0)=1`
  - Choose 2 from left non-m: `C(i - l_m, 2)`
  - Choose 2 from right non-m: `C(right_total, 2)`
  - But wait, we need to choose 2 from left total and 2 from right total. And exactly 2 of the 4 are m's? No, for k=3, total m's is 3, so we pick 2 from left and 1 from right? Or 1 from left and 2 from right? Or 2 from left and 0 from right? No, we pick 2 from left and 2 from right. The total m's is 1 (middle) + l_pick + r_pick = 3, so l_pick + r_pick = 2.
  - Cases for k=3:
    - l_pick=2, r_pick=0: `C(l_m,2) * C(right_total, 2)`
    - l_pick=1, r_pick=1: `l_m * r_m * (i - l_m) * (right_total)`  [choose 1 m and 1 non-m from left, 1 m and 1 non-m from right]
    - l_pick=0, r_pick=2: `C(r_m,2) * C(i - l_m, 2)`
  - And since the other 2 elements (non-m) can be anything (their frequency will be at most 2, which is < 3), we don't need to worry about them being same or different.

For k=2:
- l_pick + r_pick = 1.
- Cases:
  - l_pick=1, r_pick=0: 
    - Choose 1 m from left: `l_m`
    - Choose 1 non-m from left: `i - l_m`
    - Choose 2 non-m from right: but they must be distinct from each other and from the left non-m.
    - This is the tricky part.
  - l_pick=0, r_pick=1: symmetric.

To handle the distinctness for k=2, we can do:
For l_pick=1, r_pick=0:
  Let `A` be the set of values in left non-m, `B` be the set of values in right non-m.
  We need to choose one value `a` from A and two values `b1, b2` from B such that `a != b1`, `a != b2`, and `b1 != b2`.
  This can be computed as:
  Total ways to choose 1 non-m from left and 2 non-m from right: `(i - l_m) * C(right_total, 2)`
  Minus cases where the left non-m equals one of the right non-m's.
  For each value `v` in right non-m, if it also appears in left non-m, then we subtract the cases where the left non-m is `v` and one of the right non-m's is `v`.
  Specifically, for a value `v` that appears `freq_L[v]` times in left non-m and `freq_R[v]` times in right non-m:
  The number of bad pairs where left non-m is `v` and at least one right non-m is `v` is:
    `freq_L[v] * [ C(freq_R[v], 1) * C(right_total - freq_R[v], 1) + C(freq_R[v], 2) ]`
  Actually, it's easier to compute:
  Good ways = sum over all pairs of (left non-m index, right non-m indices) such that the values are distinct.
  = sum_{v in left non-m values} freq_L[v] * [ number of ways to choose 2 distinct non-m from right that are not v ]
  For a fixed `v`, the number of ways to choose 2 distinct non-m from right that are not `v` is:
    Let `R_v = right_total - freq_R[v]` (non-m, non-v in right)
    Then `C(R_v, 2) + freq_R[v] * R_v`? No, we need two distinct indices from right non-m, and neither can have value `v`.
    Actually, the number of ways to choose 2 indices from right non-m that do not have value `v` is `C(right_total - freq_R[v], 2)`.
  So for l_pick=1, r_pick=0:
    ways = sum_{v in left non-m values} freq_L[v] * C(right_total - freq_R.get(v,0), 2)
  Similarly for l_pick=0, r_pick=1:
    ways = sum_{v in right non-m values} freq_R[v] * C(i - l_m - freq_L.get(v,0), 2)

This is O(n) per middle element for the sum, and we have n middle elements, so total O(n^2), which is acceptable.

Let's implement this plan.

Steps:
1. Initialize `ans = 0`.
2. Precompute a frequency map for the entire array to help with right part? Or update left and right frequency maps as we iterate.
3. For `i` from 1 to n-2 (0-indexed, so that there are at least 2 elements on each side):
   a. Update `left_freq` by adding `nums[i-1]` (actually, we can maintain `left_freq` and `right_freq` incrementally).
   b. Initially, `left_freq` is empty, `right_freq` is frequency of `nums[2:]` (for i=1, left is nums[0:1], right is nums[2:]).
   c. Actually, better: 
      - Start with `left_freq = {}`, `right_freq = Counter(nums[2:])`.
      - For `i` from 1 to n-2:
        - `m = nums[i]`
        - `l_m = left_freq.get(m, 0)`
        - `r_m = right_freq.get(m, 0)`
        - `left_total = i`  (number of elements in left)
        - `right_total = n - 1 - i`  (number of elements in right)
        - `left_non_m_total = left_total - l_m`
        - `right_non_m_total = right_total - r_m`
        
        - Calculate for k=3:
          case1 = C(l_m, 2) * C(right_non_m_total, 2)
          case2 = l_m * r_m * left_non_m_total * right_non_m_total
          case3 = C(r_m, 2) * C(left_non_m_total, 2)
          ans += case1 + case2 + case3
        
        - Calculate for k=2:
          # l_pick=1, r_pick=0
          # ways = sum_{v in left non-m} freq_L[v] * C(right_non_m_total - freq_R.get(v,0), 2)
          ways1 = 0
          for v, count in left_freq.items():
              if v == m: continue
              r_v = right_freq.get(v, 0)
              rem = right_non_m_total - r_v
              if rem >= 2:
                  ways1 += count * (rem * (rem-1) // 2)
          
          # l_pick=0, r_pick=1
          ways2 = 0
          for v, count in right_freq.items():
              if v == m: continue
              l_v = left_freq.get(v, 0)
              rem = left_non_m_total - l_v
              if rem >= 2:
                  ways2 += count * (rem * (rem-1) // 2)
          
          ans += ways1 + ways2
        
        - Update `left_freq` by adding `nums[i]`? No, after processing i, we move to i+1, so we add `nums[i]` to left_freq and remove `nums[i+1]` from right_freq? 
          Actually, for next iteration i+1:
          - left part becomes nums[0:i+1], so we add nums[i] to left_freq.
          - right part becomes nums[i+2:n], so we remove nums[i+1] from right_freq.
        - So after processing i:
          `left_freq[m] = left_freq.get(m,0) + 1`
          `right_freq[nums[i+1]] -= 1`
          `if right_freq[nums[i+1]] == 0: del right_freq[nums[i+1]]`

4. Return ans % (10^9+7)

Edge cases: when rem < 2, skip.

Let's implement accordingly.

## worker: Implement the solution with incremental left and r
The solution iterates through each element as the potential middle element of a 5-element subsequence. For each middle element at index `i`, it maintains frequency maps for the left (`nums[0:i]`) and right (`nums[i+1:n]`) parts. 

For each middle element `m`, we consider two cases where `m` can be the unique mode:
1. **k=3**: `m` appears 3 times in the subsequence. The other 2 elements can be anything since their maximum frequency (2) is less than 3. We calculate three subcases based on how many `m`'s are chosen from left and right.
2. **k=2**: `m` appears 2 times in the subsequence. The other 3 elements must all have frequency 1 (distinct values and different from `m`). We calculate two subcases:
   - 1 `m` from left, 1 non-`m` from left, 2 distinct non-`m` from right (distinct from each other and from the left non-`m`).
   - 1 `m` from right, 1 non-`m` from right, 2 distinct non-`m` from left (distinct from each other and from the right non-`m`).

The key insight for k=2 is using inclusion-exclusion: for each value `v` in the left (or right) non-`m` elements, we count the number of ways to choose 2 distinct non-`m` elements from the right (or left) that are not equal to `v`.

The algorithm runs in O(n²) time because for each of the O(n) middle elements, we iterate over the frequency maps which have at most O(n) entries. This is efficient enough for n ≤ 1000.
