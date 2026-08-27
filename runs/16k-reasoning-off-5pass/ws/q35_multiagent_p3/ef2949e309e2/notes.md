
## ideation
The core difficulty lies in efficiently counting subsequences where the middle element is the unique mode. A naive $O(N^3)$ approach checking all combinations of 4 other elements is too slow for $N=1000$. The key insight is to iterate through each element as the potential middle element `nums[i]` and calculate the number of valid pairs from the left (`nums[0...i-1]`) and right (`nums[i+1...n-1]`) sides.

For a fixed middle element `v = nums[i]`, we choose 2 elements from the left and 2 from the right. Let `k` be the total number of `v`s chosen from these 4 slots. The total frequency of `v` in the subsequence is `1 + k`. For `v` to be the unique mode, the frequency of any other value `u` in the subsequence must be strictly less than `1 + k`.

Since we only choose 4 elements total, the maximum frequency of any other value is at most 4. We can categorize the choices based on `k` (0 to 4):
1.  **k=4**: Total `v` count is 5. No other values are present. Condition always holds.
2.  **k=3**: Total `v` count is 4. One other value `u` is present with frequency 1. Since $1 < 4$, condition always holds.
3.  **k=2**: Total `v` count is 3. Two other values are present. Their max frequency is at most 2. Since $2 < 3$, condition always holds.
4.  **k=1**: Total `v` count is 2. Three other values are present. For `v` to be unique mode, no other value can appear $\ge 2$ times. Thus, the three other values must be **distinct**.
5.  **k=0**: Total `v` count is 1. Four other values are present. For `v` to be unique mode, no other value can appear $\ge 1$ time. This is impossible if there are other values. So this case yields 0.

Therefore, we only need to handle the general case (k=2,3,4) where any combination of non-`v` elements is valid, and the specific case (k=1) where the 3 non-`v` elements must be distinct.

For each index `i`:
1.  Identify `v = nums[i]`.
2.  Count occurrences of `v` in left (`cntL_v`) and right (`cntR_v`).
3.  Calculate total non-`v` counts in left (`nonL`) and right (`nonR`).
4.  Iterate over possible splits of `v`'s: `k_vL` (0..2) from left and `k_vR` (0..2) from right.
    *   Let `k = k_vL + k_vR`.
    *   If `k < 1`, skip (0 ways).
    *   Calculate ways to choose `v`s: `ways_v = C(cntL_v, k_vL) * C(cntR_v, k_vR)`.
    *   Determine non-`v` counts needed: `needL = 2 - k_vL`, `needR = 2 - k_vR`.
    *   If `k >= 2`:
        *   `ways_non_v = C(nonL, needL) * C(nonR, needR)`.
    *   If `k == 1`:
        *   We need to choose `needL` non-`v` from left and `needR` non-`v` from right such that all `needL + needR = 3` elements are distinct.
        *   Cases: `(needL=1, needR=2)` or `(needL=2, needR=1)`.
        *   For `(1,2)`: Sum over each unique value `u` in left: `freqL[u] * (C(nonR, 2) - sum_{w in right, w!=u} C(freqR[w], 2) - ...)`? Actually, simpler: Total pairs from right minus pairs that include the specific left element? No, the left element is a single value.
        *   Better: Total ways to pick 1 from left and 2 from right is `nonL * C(nonR, 2)`. Subtract invalid ones where the 2 from right are equal OR one of the 2 from right equals the 1 from left.
        *   Invalid if:
            1.  The 2 from right are equal: Sum over `w` in right: `C(freqR[w], 2)`.
            2.  The 2 from right are distinct but one equals the left element `u`: For a fixed left element `u`, the number of pairs from right that include `u` is `freqR[u] * (nonR - freqR[u])`. Wait, if we pick `u` from left, we cannot pick `u` from right. So we must pick 2 from right from `nonR - freqR[u]` elements, but ensuring they are distinct? No, the condition is all 3 distinct. So if left picks `u`, right must pick 2 distinct values neither of which is `u`.
            *   So for a fixed left value `u`, valid right pairs = `C(nonR - freqR[u], 2)`.
            *   Sum over all `u` in left: `freqL[u] * C(nonR - freqR[u], 2)`.
        *   Similarly for `(2,1)`: Sum over `w` in right: `freqR[w] * C(nonL - freqL[w], 2)`.
5.  Sum up all valid ways modulo $10^9+7$.

Complexity: $O(N^2)$ because for each `i`, we iterate through distinct values in left/right or use precomputed sums. With $N=1000$, $N^2 = 10^6$, which is acceptable.

Pitfalls:
-   Combinatorics modulo arithmetic.
-   Handling distinctness correctly for k=1.
-   Edge cases where `nonL` or `nonR` are small.

## worker: Implement the solution based on the derived logic.
The solution iterates through each element in `nums` considering it as the middle element of the subsequence. For each middle element `v`, it calculates the number of ways to choose 2 elements from the left and 2 from the right such that `v` is the unique mode.

The key insight is categorizing by `k`, the number of `v`s chosen from the 4 slots:
- **k=4**: All 4 are `v`. Valid.
- **k=3**: 3 `v`s, 1 other. The other appears once, which is less than 4. Valid.
- **k=2**: 2 `v`s, 2 others. Max frequency of others is 2, which is less than 3. Valid.
- **k=1**: 1 `v`, 3 others. For `v` (count 2) to be unique mode, no other value can appear $\ge 2$ times. Thus, the 3 others must be distinct.
- **k=0**: 0 `v`s, 4 others. For `v` (count 1) to be unique mode, no other value can appear $\ge 1$ time. Impossible.

For `k=1`, we handle the distinctness constraint by iterating over the unique values in the left or right part and using combinatorics to count valid pairs/triples that exclude the chosen value. The complexity is $O(N^2)$ due to iterating over each middle element and then iterating over distinct values in the left/right maps, which is efficient enough for $N=1000$.
