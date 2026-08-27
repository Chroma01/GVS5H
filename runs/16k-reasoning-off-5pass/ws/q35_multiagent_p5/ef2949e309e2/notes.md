
## ideation
The core difficulty lies in efficiently counting valid subsequences for each potential middle element while satisfying the "unique middle mode" constraint. A naive $O(N^4)$ approach is too slow given $N \le 1000$.

Key insights:
1.  **Middle Element Role**: For an element at index `i` to be the unique middle mode of a subsequence of size 5, it must appear at least twice in that subsequence (since if it appears once, the other 4 elements must have max frequency < 1, which is impossible).
2.  **Case Splitting**:
    *   **Case 1: Middle element appears 3 times in the subsequence.** This means we pick 2 more instances of `nums[i]` from the left and right parts. The remaining 2 elements can be anything (even identical to each other) because their max frequency will be at most 2, which is strictly less than 3.
    *   **Case 2: Middle element appears 2 times in the subsequence.** This means we pick exactly 1 more instance of `nums[i]` from the left and right parts. The remaining 2 elements must be distinct from each other AND distinct from `nums[i]`. If they are identical, they form a mode with frequency 2, tying with the middle element, violating the "unique" condition.
3.  **Efficient Calculation**:
    *   Precompute global frequencies.
    *   Iterate through each index `i` considering it as the middle.
    *   Maintain `left_freq` and `right_freq` maps (or update them dynamically). Initially, `left_freq` is empty and `right_freq` contains all elements except `nums[i]`.
    *   For each `i`:
        *   Let `m = nums[i]`.
        *   Let `L = i` (number of elements to the left), `R = n - 1 - i` (number of elements to the right).
        *   Let `l_m` be count of `m` in left, `r_m` be count of `m` in right.
        *   **Case 1 (3 m's)**:
            *   Pick 2 m's from left: `C(l_m, 2) * C(R - r_m, 2)`
            *   Pick 2 m's from right: `C(r_m, 2) * C(L - l_m, 2)`
            *   Pick 1 m from left, 1 m from right: `l_m * r_m * (L - l_m) * (R - r_m)`
        *   **Case 2 (2 m's)**:
            *   We need to pick exactly 1 `m` from the combined left/right pool, and 2 non-`m` elements that are distinct.
            *   Subcase 2a: Pick 1 `m` from left. Then pick 2 distinct non-`m` from right.
                *   Ways to pick 2 distinct non-`m` from right = `C(R - r_m, 2) - sum(C(freq_right[x], 2) for x != m)`.
                *   Note: `sum(C(freq_right[x], 2) for x != m)` is equal to `(Total pairs from right) - (pairs of m from right)`.
                *   So, `ValidDistinctRight = C(R, 2) - C(r_m, 2)`.
                *   Contribution: `l_m * ValidDistinctRight`.
            *   Subcase 2b: Pick 1 `m` from right. Then pick 2 distinct non-`m` from left.
                *   Similarly, `ValidDistinctLeft = C(L, 2) - C(l_m, 2)`.
                *   Contribution: `r_m * ValidDistinctLeft`.
    *   Sum contributions for all `i`.
    *   Use modular arithmetic for the final answer.

Pitfalls:
-   Forgetting that in Case 2, the two non-middle elements must be distinct.
-   Incorrectly calculating combinations when counts are less than 2 (use 0).
-   Not handling the modulo operation correctly at each addition.
-   The definition of "subsequence" implies order doesn't matter for the set of values, but indices matter for selection. The problem asks for number of subsequences, which corresponds to choosing indices. The logic above counts index combinations correctly.

## worker: Implement helper function for combinations `nCr` m
The solution iterates through each element considering it as the middle of the subsequence. For each middle element `m` at index `i`:
1.  **Case 1 (m appears 3 times)**: We pick 2 more `m`'s from the left and right parts. The remaining 2 elements can be any non-m elements (even identical) because their max frequency (2) is strictly less than 3. We calculate the number of ways to pick 2 m's from left+right and 2 non-m's from the opposite side.
2.  **Case 2 (m appears 2 times)**: We pick exactly 1 more `m` from left or right. The remaining 2 elements must be distinct non-m elements. We calculate the number of ways to pick 2 distinct non-m elements from the opposite side by taking all pairs of non-m elements and subtracting pairs that have the same value.
3.  **Efficiency**: For each `i`, we iterate over the frequency maps to compute the sum of combinations for same-value pairs. Since the number of distinct elements is at most `N`, this is $O(N)$ per `i`, leading to an overall $O(N^2)$ complexity, which is acceptable for $N \le 1000$.
4.  **Modulo Arithmetic**: All additions and multiplications are performed modulo $10^9 + 7$. Combinations are computed using modular inverse for division.
