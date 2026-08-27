
## ideation
**Core Difficulty**: The problem requires maximizing the subarray sum after removing all instances of a specific number $x$. A naive simulation (removing $x$ and running Kadane's) for every unique $x$ results in $O(N^2)$ time complexity, which is too slow given $N \le 10^5$. The challenge is to efficiently calculate the new maximum subarray sum for each candidate $x$ without re-scanning the entire array.

**Candidate Approaches**:
1.  **Prefix/Suffix Arrays (Optimal)**:
    *   Precompute `max_prefix[i]`: The maximum subarray sum in `nums[0...i]`.
    *   Precompute `max_suffix[i]`: The maximum subarray sum in `nums[i...n-1]`.
    *   Precompute `max_cross[i]`: The maximum subarray sum that ends at or before index `i` and starts after `i` (or simply track the max subarray sum in the prefix ending at `i` and suffix starting at `i+1`). Actually, a simpler structure is needed:
        *   `left_max[i]`: Max subarray sum in `nums[0...i]`.
        *   `right_max[i]`: Max subarray sum in `nums[i...n-1]`.
        *   `left_sum[i]`: Sum of `nums[0...i]`.
        *   `right_sum[i]`: Sum of `nums[i...n-1]`.
    *   For a specific $x$, identify the range of indices where $x$ appears. Let the first occurrence be `first` and the last be `last`.
    *   If we remove $x$, the array splits into `nums[0...first-1]` and `nums[last+1...n-1]`. Note: If $x$ appears multiple times, removing *all* occurrences means the gap is from the *first* occurrence to the *last* occurrence inclusive.
    *   The new max subarray sum is `max(left_max[first-1], right_max[last+1])`. Wait, this is incorrect. The subarray could span across the gap if the gap was just a single element? No, if we remove *all* occurrences of $x$, the array is contiguous in terms of indices *except* the indices occupied by $x$ are gone. The resulting array is formed by concatenating `nums[0...first-1]` and `nums[last+1...n-1]`. These two parts are now adjacent.
    *   So the candidates are:
        1. Max subarray in the left part (`nums[0...first-1]`).
        2. Max subarray in the right part (`nums[last+1...n-1]`).
        3. A subarray formed by the suffix of the left part + the prefix of the right part.
    *   To handle case 3 efficiently, we need:
        *   `max_suffix_left[i]`: Max subarray sum starting at index `i` within `nums[0...i]` (or ending at `i`? No, starting at `i` going left? No, we need the max sum of a suffix of the left segment). Let's define `max_suffix_end[i]` as the max subarray sum in `nums[0...i]` that ends at `i`. Or better: `max_ending_at[i]` (standard Kadane state) and `max_ending_at_suffix[i]` (max sum of a subarray ending at `i` but extending as far left as possible? No).
        *   Let's refine: We need the max sum of a suffix of `nums[0...first-1]` and the max sum of a prefix of `nums[last+1...n-1]`.
        *   Precompute `max_suffix[i]`: Max subarray sum in `nums[0...i]` that ends at `i`? No, we need the max sum of *any* suffix of the prefix `0..first-1`. That is `max(nums[i...first-1])` for some `i`. This is equivalent to `max_ending_at[first-1]` if we compute Kadane backwards?
        *   Actually, simpler:
            *   `pref_max[i]`: Max subarray sum in `nums[0...i]`.
            *   `suff_max[i]`: Max subarray sum in `nums[i...n-1]`.
            *   `pref_suffix_max[i]`: Max subarray sum in `nums[0...i]` that ends at `i`. (This helps combine with the right part).
            *   `suff_prefix_max[i]`: Max subarray sum in `nums[i...n-1]` that starts at `i`.
    *   Algorithm:
        1. Calculate `pref_max`, `suff_max`, `pref_suffix_max` (max subarray ending at `i`), `suff_prefix_max` (max subarray starting at `i`).
        2. Store positions of each number.
        3. For each unique number $x$:
           - Find `first` and `last` index of $x$.
           - If no $x$ exists, skip (or treat as no op).
           - Left part: `0` to `first-1`. Right part: `last+1` to `n-1`.
           - Candidate 1: `pref_max[first-1]` (if `first > 0`).
           - Candidate 2: `suff_max[last+1]` (if `last < n-1`).
           - Candidate 3: If both parts exist, `pref_suffix_max[first-1] + suff_prefix_max[last+1]`.
           - Update global max.
        4. Also consider the case of doing nothing (original max subarray sum).

2.  **Pitfalls**:
    *   **Empty Arrays**: After removal, one side might be empty. Handle indices carefully (e.g., if `first == 0`, left part is empty).
    *   **Single Element Removal**: If $x$ appears only once, `first == last`. The split is `0..first-1` and `first+1..n-1`. The logic holds.
    *   **All Elements Same**: Removing the only element leaves an empty array. The problem states "nums remains non-empty". So if removing $x$ makes the array empty, we cannot choose that $x$. We must check if the resulting array is non-empty.
    *   **Negative Numbers**: Kadane's algorithm needs to handle all-negative arrays correctly (return the max single element, not 0).
    *   **Time Complexity**: Must be $O(N)$. Iterating unique elements is fine since sum of counts is $N$.
    *   **Space Complexity**: $O(N)$ for storing prefix/suffix arrays and position maps.

**Refined Plan**:
1.  Compute `total_max` (Kadane on original).
2.  Build `count` map and `positions` list for each unique number.
3.  Precompute arrays:
    *   `max_ending_here[i]`: Max subarray sum ending at `i`.
    *   `max_starting_here[i]`: Max subarray sum starting at `i`.
    *   `max_prefix[i]`: Max subarray sum in `0..i`.
    *   `max_suffix[i]`: Max subarray sum in `i..n-1`.
    *   `max_suffix_ending_at[i]`: Max subarray sum in `0..i` that ends at `i`. (Same as `max_ending_here`).
    *   `max_prefix_starting_at[i]`: Max subarray sum in `i..n-1` that starts at `i`. (Same as `max_starting_here`).
    *   Wait, to combine left and right parts, we need:
        *   Max sum of a suffix of `0..first-1`. This is `max(max_ending_here[k])` for `k` in `0..first-1`? No, that's just `max_prefix[first-1]`. We need the sum of the suffix of the segment `0..first-1`. That corresponds to `max_ending_here[first-1]`? No.
        *   Let's re-evaluate "Suffix of the left part". The left part is `nums[0...L]`. We want the max sum of a subarray `nums[i...L]`. This is exactly `max_ending_here[L]` if we define `max_ending_here[i]` as the max subarray sum ending at `i`. Yes.
        *   Similarly, "Prefix of the right part". The right part is `nums[R...n-1]`. We want max sum of `nums[R...j]`. This is `max_starting_here[R]`.
    *   So we need:
        *   `max_ending[i]`: Max subarray sum ending at `i`.
        *   `max_starting[i]`: Max subarray sum starting at `i`.
        *   `global_max_prefix[i]`: Max subarray sum in `0..i`.
        *   `global_max_suffix[i]`: Max subarray sum in `i..n-1`.
4.  Iterate unique $x$:
    *   Get `first`, `last`.
    *   If removing $x$ leaves array empty (i.e., `first == 0` and `last == n-1` and all elements are $x$), skip.
    *   Calculate candidates:
        *   If `first > 0`: `global_max_prefix[first-1]`
        *   If `last < n-1`: `global_max_suffix[last+1]`
        *   If `first > 0` and `last < n-1`: `max_ending[first-1] + max_starting[last+1]`
    *   Take max of valid candidates.
5.  Return max of all results (including original array).

## worker: Implement the helper functions for Kadane's variat
1.  **Precomputation**:
    *   `max_ending[i]`: Stores the maximum subarray sum ending exactly at index `i`. This is computed using a forward pass similar to Kadane's algorithm.
    *   `max_starting[i]`: Stores the maximum subarray sum starting exactly at index `i`. This is computed using a backward pass.
    *   `global_max_prefix[i]`: Stores the maximum subarray sum found within the range `nums[0...i]`. This is the standard result of Kadane's algorithm up to index `i`.
    *   `global_max_suffix[i]`: Stores the maximum subarray sum found within the range `nums[i...n-1]`. This is computed using a backward pass.

2.  **Logic for Removal**:
    *   For a chosen number `x`, we identify its first occurrence (`first`) and last occurrence (`last`).
    *   Removing all occurrences of `x` splits the array into two parts: `nums[0...first-1]` and `nums[last+1...n-1]`.
    *   The new maximum subarray sum can be:
        1.  The max subarray entirely in the left part (`global_max_prefix[first-1]`).
        2.  The max subarray entirely in the right part (`global_max_suffix[last+1]`).
        3.  A subarray formed by concatenating the suffix of the left part (ending at `first-1`) and the prefix of the right part (starting at `last+1`). The sum is `max_ending[first-1] + max_starting[last+1]`.
    *   We take the maximum of these valid candidates.

3.  **Edge Cases**:
    *   **Empty Result**: If removing `x` results in an empty array (i.e., `x` is the only element in the array), we skip this `x`.
    *   **Single Side Empty**: If `first == 0`, the left part is empty, so we only consider the right part and the combination (which effectively ignores the left part). The code handles this by checking `if first > 0`.
    *   **All Negatives**: The logic holds because `max_ending`, `max_starting`, and `global_max` arrays store the maximum single element if all subarrays are negative, ensuring correctness.

4.  **Complexity**:
    *   Time: $O(N)$ for precomputing arrays and $O(N)$ for iterating unique elements (sum of lengths of `indices` lists is $N$). Total $O(N)$.
    *   Space: $O(N)$ for storing the arrays and the position map.

## worker: Implement the helper functions for Kadane's variat
The implementation follows the plan exactly:
1.  **Precomputation**:
    *   `max_ending` and `max_starting` arrays are computed using forward and backward passes respectively, tracking the maximum subarray sum ending/starting at each index.
    *   `global_max_prefix` and `global_max_suffix` arrays track the maximum subarray sum found within the prefix/suffix ranges up to or from each index.
2.  **Logic**:
    *   The positions of each unique number are stored to quickly identify the range `[first, last]` that needs to be removed.
    *   For each unique number `x`, the algorithm checks three potential candidates for the new maximum subarray sum:
        1.  The best subarray entirely in the left segment (`0` to `first-1`).
        2.  The best subarray entirely in the right segment (`last+1` to `n-1`).
        3.  The sum of the best suffix of the left segment (ending at `first-1`) and the best prefix of the right segment (starting at `last+1`).
    *   Edge cases where removing `x` results in an empty array are handled by checking if `first == 0` and `last == n-1`.
3.  **Complexity**:
    *   Time Complexity: $O(N)$ due to four linear passes for precomputation and one pass over unique elements (where the sum of indices lengths is $N$).
    *   Space Complexity: $O(N)$ for storing the four auxiliary arrays and the position map.

## worker: Implement prefix/suffix global max arrays.
The implementation correctly precomputes four arrays:
1.  `max_ending[i]`: The maximum subarray sum ending exactly at index `i`. This is calculated by deciding whether to extend the subarray ending at `i-1` or start a new one at `i`.
2.  `max_starting[i]`: The maximum subarray sum starting exactly at index `i`. This is the symmetric backward pass of `max_ending`.
3.  `global_max_prefix[i]`: The maximum subarray sum found anywhere within the range `0` to `i`. This is the standard cumulative maximum of the `max_ending` values.
4.  `global_max_suffix[i]`: The maximum subarray sum found anywhere within the range `i` to `n-1`. This is the symmetric cumulative maximum of the `max_starting` values.

These arrays allow us to efficiently query the maximum subarray sum for any split of the array caused by removing a specific number `x`. If `x` is removed, the array splits into a left part (before the first occurrence of `x`) and a right part (after the last occurrence of `x`). The new maximum subarray sum is the maximum of:
- The best subarray entirely in the left part (`global_max_prefix[first-1]`).
- The best subarray entirely in the right part (`global_max_suffix[last+1]`).
- The sum of the best suffix of the left part (`max_ending[first-1]`) and the best prefix of the right part (`max_starting[last+1]`).

Edge cases where removing `x` results in an empty array are handled by checking if `first == 0` and `last == n-1`.

## worker: Implement the position map, iterate through unique
The solution implements an $O(N)$ approach by precomputing four auxiliary arrays:
1.  `max_ending[i]`: Maximum subarray sum ending exactly at index `i`.
2.  `max_starting[i]`: Maximum subarray sum starting exactly at index `i`.
3.  `global_max_prefix[i]`: Maximum subarray sum found within the range `0` to `i`.
4.  `global_max_suffix[i]`: Maximum subarray sum found within the range `i` to `n-1`.

These arrays allow us to efficiently determine the maximum subarray sum after removing all occurrences of any integer $x$. For a specific $x$ with first occurrence at `first` and last at `last`, the array splits into a left part (`0` to `first-1`) and a right part (`last+1` to `n-1`). The new maximum subarray sum is the maximum of:
- The best subarray entirely in the left part (`global_max_prefix[first-1]`).
- The best subarray entirely in the right part (`global_max_suffix[last+1]`).
- The sum of the best suffix of the left part (`max_ending[first-1]`) and the best prefix of the right part (`max_starting[last+1]`).

Edge cases are handled:
- If removing $x$ results in an empty array (i.e., $x$ is the only element), we skip it.
- If one side of the split is empty, we only consider the valid side or the combination if both exist.
- The original array's maximum subarray sum is considered as a baseline (case where no operation is performed).

## worker: finalize
The solution implements an $O(N)$ approach by precomputing four auxiliary arrays:
1.  `max_ending[i]`: Maximum subarray sum ending exactly at index `i`.
2.  `max_starting[i]`: Maximum subarray sum starting exactly at index `i`.
3.  `global_max_prefix[i]`: Maximum subarray sum found within the range `0` to `i`.
4.  `global_max_suffix[i]`: Maximum subarray sum found within the range `i` to `n-1`.

These arrays allow us to efficiently determine the maximum subarray sum after removing all occurrences of any integer $x$. For a specific $x$ with first occurrence at `first` and last at `last`, the array splits into a left part (`0` to `first-1`) and a right part (`last+1` to `n-1`). The new maximum subarray sum is the maximum of:
- The best subarray entirely in the left part (`global_max_prefix[first-1]`).
- The best subarray entirely in the right part (`global_max_suffix[last+1]`).
- The sum of the best suffix of the left part (`max_ending[first-1]`) and the best prefix of the right part (`max_starting[last+1]`).

Edge cases are handled:
- If removing $x$ results in an empty array (i.e., $x$ is the only element), we skip it.
- If one side of the split is empty, we only consider the valid side or the combination if both exist.
- The original array's maximum subarray sum is considered as a baseline (case where no operation is performed).
