
## ideation
**Core Difficulty**: The problem asks for the maximum subarray sum after removing all occurrences of *at most one* integer $x$. A naive solution would iterate through every unique number in the array, create a new array (or simulate removal), and run Kadane's algorithm. In the worst case (all elements unique), this results in $O(N^2)$ time complexity, which is too slow for $N=10^5$.

**Candidate Approaches**:
1.  **Prefix/Suffix Arrays (Optimized)**:
    *   Precompute standard Kadane's results: `max_ending_here`, `max_starting_here`, `max_so_far` (global max).
    *   However, simply knowing the global max isn't enough because removing $x$ might split the optimal subarray into two parts, or the optimal subarray might be entirely within a segment that wasn't part of the original global max.
    *   We need to efficiently query the max subarray sum in the array *excluding* specific values.
    *   Idea: For each unique $x$, the array splits into contiguous segments of non-$x$ values. The answer is the maximum of the max subarray sums of these segments.
    *   To do this in $O(N)$ total:
        *   We can precompute the max subarray sum for the whole array.
        *   If the original max subarray sum does *not* contain $x$, then the answer for removing $x$ is at least the original max subarray sum (since we can choose not to remove anything, or removing $x$ doesn't hurt the best subarray). Actually, the problem says "at most once", so the answer is $\max(\text{original\_max}, \text{max after removing } x)$.
        *   The critical case is when the original max subarray sum *does* contain $x$. Removing $x$ splits this subarray. The new max subarray sum would be the maximum of the left part (ending before the last occurrence of $x$ in the subarray) and the right part (starting after the first occurrence of $x$ in the subarray).
        *   Wait, is it just the original max subarray? No. Removing a negative number $x$ from a subarray can increase the sum. Removing a positive number $x$ can decrease it.
        *   Actually, the optimal strategy is usually to remove a number that is "blocking" a large sum or is a large negative number itself.
        *   Correct Logic:
            1. Calculate `global_max` for the original array.
            2. Identify all unique elements.
            3. For each unique element $x$, we want to find the max subarray sum in `nums` excluding $x$.
            4. This is equivalent to finding the max subarray sum in the sequence formed by concatenating all contiguous blocks of non-$x$ numbers.
            5. Since we can't iterate $O(N)$ for each $x$, we need a way to aggregate.
            6. **Key Insight**: The max subarray sum after removing $x$ is either:
               a. The `global_max` of the original array (if the optimal subarray doesn't use $x$).
               b. A subarray formed by merging two parts of the original `global_max` subarray if $x$ was inside it and was negative? No, if $x$ is inside, removing it splits the subarray. The new candidate is $\max(\text{sum of left part}, \text{sum of right part})$.
               c. OR, a completely different subarray that becomes optimal only after $x$ is removed (e.g., $x$ was separating two positive blocks).
            7. Actually, the most robust approach is:
               - Precompute `pref_max[i]`: Max subarray sum in `nums[0...i]`.
               - Precompute `suff_max[i]`: Max subarray sum in `nums[i...n-1]`.
               - Also precompute `max_ending[i]` and `max_starting[i]` for the original array.
               - But we need to exclude $x$.
               - Alternative: Since the number of unique elements can be large, but the "interesting" elements to remove are likely those that appear in the optimal subarray or are large negative numbers.
               - Actually, we can iterate over all unique elements. For each $x$, we can calculate the max subarray sum in $O(\text{count}(x))$? No.
               - Let's reconsider the constraints. $N=10^5$. We need $O(N)$.
               - Is it possible that we only need to check the elements present in the *original* maximum subarray?
                 - If the original max subarray does not contain $x$, removing $x$ doesn't affect it (sum stays same).
                 - If the original max subarray contains $x$, removing $x$ splits it. The new max sum is $\max(\text{sum of left part}, \text{sum of right part})$.
                 - BUT, there could be another subarray $S'$ that doesn't contain $x$ and has sum $> \text{original\_max}$. If such an $S'$ exists, then `original_max` was not the true global max? Contradiction. `original_max` is the max of *all* subarrays. So any subarray $S'$ has sum $\le \text{original\_max}$.
                 - Therefore, if we remove $x$, the new max subarray sum can be:
                   1. `original_max` (if the subarray achieving `original_max` does not contain $x$).
                   2. A subarray that was part of the original `global_max` subarray but split by $x$. Specifically, if the original `global_max` subarray is $A \dots x \dots B$, the new candidates are $A$ and $B$.
                   3. Wait, what if removing $x$ allows merging two previously separated positive segments?
                      - Example: `[10, -5, 10]`. Max subarray is 10 (either one). If we remove -5, we get `[10, 10]`, sum 20.
                      - Here, the original max subarray (10) does not contain -5. So removing -5 gives a new max of 20.
                      - In this case, the new max is formed by merging segments.
                      - The new max is $\max($
                        - Max subarray sum in `nums` excluding $x$ (which could be formed by merging segments),
                        - ...
                      -)
                 - Actually, the max subarray sum after removing $x$ is simply the max subarray sum of the array where all $x$ are replaced by $-\infty$ (effectively breaking the array).
                 - We can compute this efficiently?
                 - Let's look at the structure. The array breaks into segments $S_1, S_2, \dots, S_k$ separated by $x$.
                 - We need $\max(\text{Kadane}(S_i))$ for all $i$.
                 - Note that $\max(\text{Kadane}(S_i)) \le \text{global\_max}$.
                 - Also, note that $\max(\text{Kadane}(S_i))$ is the max subarray sum in the original array that does *not* contain $x$.
                 - So the answer is $\max(\text{global\_max}, \max_{x} (\text{max subarray sum in } nums \text{ excluding } x))$.
                 - Wait, if the original `global_max` subarray does not contain $x$, then "max subarray sum excluding $x$" is at least `global_max`.
                 - If the original `global_max` subarray *does* contain $x$, then "max subarray sum excluding $x$" is strictly less than `global_max`? Not necessarily.
                   - Example: `[10, -20, 10]`. Global max = 10. Remove -20 -> `[10, 10]`, sum 20.
                   - Here, the original max subarray (10) does *not* contain -20. So the condition "original max subarray contains $x$" is false.
                   - Example: `[10, 5, -20, 5, 10]`. Global max = 20 (10+5). Remove -20 -> `[10, 5, 5, 10]`, sum 30.
                   - Original max subarray `[10, 5]` does not contain -20.
                 - It seems the only case where removing $x$ increases the sum is if $x$ is negative and separates two positive blocks, OR if $x$ is negative and inside a positive block (splitting it into two smaller positive blocks, but the sum of the two might be larger? No, sum is additive. If $x$ is negative, removing it increases the sum of the specific subarray it was in. But if it splits the subarray, we lose the connection.
                   - Wait, if $x$ is inside a subarray $S$, and we remove $x$, the subarray $S$ becomes $S_{left} + S_{right}$. The sum becomes $\text{sum}(S_{left}) + \text{sum}(S_{right})$. Since $x < 0$, $\text{sum}(S) = \text{sum}(S_{left}) + x + \text{sum}(S_{right}) < \text{sum}(S_{left}) + \text{sum}(S_{right})$.
                   - So removing a negative $x$ from *inside* a subarray increases the sum of that subarray.
                   - However, the "subarray" definition requires contiguity. If we remove $x$, the elements to the left and right are no longer contiguous. They become part of different segments.
                   - So, if the original max subarray is $S$, and it contains $x$, then after removing $x$, the part of $S$ that remains is either the left part or the right part (whichever is larger, or maybe a sub-segment of them). The sum of the *combined* left and right parts is not achievable as a single subarray because they are separated by the gap where $x$ was.
                   - UNLESS there are other elements between the occurrences of $x$? No, we remove *all* occurrences.
                   - So, if the original max subarray $S$ contains $x$, removing $x$ breaks $S$ into pieces. The best we can get from $S$ is $\max(\text{max subarray in } S_{left}, \text{max subarray in } S_{right})$.
                   - But wait, what if there is another subarray $S'$ that doesn't contain $x$ and has sum $> \text{original\_max}$? Impossible by definition of `original_max`.
                   - So, if the original max subarray contains $x$, the new max subarray sum must be $\le \text{original\_max}$?
                     - Let's re-evaluate `[10, -20, 10]`. Max subarray is 10. It does NOT contain -20. Removing -20 gives 20.
                     - Let's re-evaluate `[10, -5, 10]`. Max subarray is 10. Does not contain -5. Removing -5 gives 20.
                     - Let's re-evaluate `[10, 5, -20, 5, 10]`. Max subarray is 20 (`10, 5`). Does not contain -20. Removing -20 gives 30.
                     - It seems the case where removing $x$ increases the sum is when $x$ is *not* in the original max subarray, but its removal merges two segments that were separated by $x$, creating a new, larger subarray.
                     - In this case, the new subarray is formed by concatenating a suffix of a segment to the left of $x$ and a prefix of a segment to the right of $x$.
                     - The sum of this new subarray is $\text{suffix\_sum}(L) + \text{prefix\_sum}(R)$.
                     - Since $x$ was not in the original max subarray, the original max subarray was either entirely in $L$, entirely in $R$, or entirely in some other segment.
                     - If it was entirely in $L$ or $R$, its sum is $\le \text{original\_max}$.
                     - The new sum $\text{suffix\_sum}(L) + \text{prefix\_sum}(R)$ could be greater than `original_max`.
                     - So, we need to check for each $x$: what is the max sum of a subarray that crosses an occurrence of $x$?
                     - Actually, since we remove *all* occurrences of $x$, the new array consists of segments. The max subarray sum is the max of:
                       1. Max subarray sum within any single segment. (This is $\le$ `original_max` because any such subarray existed in the original array).
                       2. Max subarray sum formed by combining the end of one segment and the start of the next segment (if $x$ appears multiple times, it's just adjacent segments).
                       - Wait, if $x$ appears multiple times, say `... A x ... B x ... C ...`.
                       - Removing $x$ gives `... A B ... C ...`.
                       - The new max subarray could be `A` + `B` or `B` + `C` or `A` + `B` + `C` (if they are contiguous after removal).
                       - Basically, we need the max subarray sum in the array where all $x$ are removed.
                       - This is equivalent to: $\max($
                         - `original_max`,
                         - $\max_{x} (\text{max subarray sum in } nums \text{ excluding } x)$
                       -)
                       - But `max subarray sum in nums excluding x` is simply the max subarray sum of the segments.
                       - And we know that any subarray within a segment exists in the original array, so its sum is $\le$ `original_max`.
                       - The ONLY way the sum increases is if we combine parts from different segments.
                       - This happens if we take a suffix of a segment ending just before an $x$, and a prefix of a segment starting just after an $x$.
                       - So, for each $x$, we want to find $\max(\text{suffix sum ending at } i \text{ where } nums[i] \neq x) + \max(\text{prefix sum starting at } j \text{ where } nums[j] \neq x)$ such that there is an $x$ between $i$ and $j$.
                       - Actually, simpler: The new max subarray sum is the max of:
                         1. `original_max`.
                         2. For each $x$, the max sum of a subarray that "crosses" an instance of $x$ (i.e., includes elements from both sides of an $x$).
                         - Wait, if we remove $x$, the elements on both sides become adjacent. So a subarray that was `... left_part right_part ...` becomes valid.
                         - The sum is $\text{sum}(left\_part) + \text{sum}(right\_part)$.
                         - We need to maximize this over all $x$ and all occurrences of $x$.
                         - But we remove *all* occurrences. So if $x$ appears at indices $i_1, i_2, \dots$, we can combine the segment ending at $i_1-1$ with the segment starting at $i_1+1$, AND the segment ending at $i_2-1$ with the segment starting at $i_2+1$, etc.
                         - Actually, if we remove all $x$, the segments are $S_1, S_2, \dots, S_k$. The new array is $S_1 S_2 \dots S_k$.
                         - The max subarray sum is the max subarray sum of this concatenated array.
                         - This can be computed as:
                           - Max subarray sum within any $S_i$ (which is $\le$ `original_max`).
                           - Max subarray sum crossing the boundary between $S_i$ and $S_{i+1}$. This is $\max(\text{suffix of } S_i) + \max(\text{prefix of } S_{i+1})$.
                         - So for a fixed $x$, we need $\max_i (\text{max\_suffix}(S_i) + \text{max\_prefix}(S_{i+1}))$.
                         - Note that $\text{max\_suffix}(S_i)$ is the max suffix sum of the segment in the original array ending at $i_1-1$.
                         - $\text{max\_prefix}(S_{i+1})$ is the max prefix sum of the segment in the original array starting at $i_1+1$.
                         - We can precompute `max_suffix_ending_at[i]` and `max_prefix_starting_at[i]` for the original array.
                         - Then for each $x$, we iterate through its occurrences. Let occurrences be $idx_1, idx_2, \dots$.
                         - The segments are between these indices.
                         - Boundary 1: between $idx_1-1$ and $idx_1+1$. Candidate: `max_suffix_ending_at[idx_1-1] + max_prefix_starting_at[idx_1+1]`.
                         - Boundary 2: between $idx_2-1$ and $idx_2+1$. Candidate: `max_suffix_ending_at[idx_2-1] + max_prefix_starting_at[idx_2+1]`.
                         - And so on.
                         - We take the max of all these candidates over all $x$.
                         - Also compare with `original_max`.
                         - Complexity:
                           - Precompute `max_suffix_ending_at` and `max_prefix_starting_at`: $O(N)$.
                           - Iterate over all unique $x$. For each $x$, iterate over its occurrences.
                           - Total iterations = sum of counts of all unique $x$ = $N$.
                           - So total time $O(N)$.

## worker: Precompute `max_ending_here` (max subarray sum end
1.  **Precomputation**: I implemented the precomputation of `max_ending` and `max_starting` arrays as requested. `max_ending[i]` stores the maximum subarray sum of a subarray that *must* end at index `i`. `max_starting[i]` stores the maximum subarray sum of a subarray that *must* start at index `i`. Both are computed in $O(N)$ time using a modified Kadane's algorithm.
2.  **Logic for Removal**: The core insight is that removing all occurrences of a number $x$ splits the array into contiguous segments of non-$x$ numbers. The maximum subarray sum in the new array is the maximum of:
    *   The maximum subarray sum within any single segment (which is bounded by the original `global_max`).
    *   The maximum subarray sum formed by concatenating a suffix of a segment ending just before an occurrence of $x$ and a prefix of a segment starting just after that occurrence.
3.  **Efficiency**: Instead of simulating the removal for each unique number (which would be $O(N^2)$ in the worst case), I grouped the indices of each number. Then, for each occurrence of a number $x$, I checked the potential "merge" sum formed by `max_ending[i-1] + max_starting[i+1]`. Since the total number of occurrences across all unique numbers is $N$, this step is also $O(N)$.
4.  **Edge Cases**:
    *   If $x$ is at the start or end of the array, no merge is possible across it.
    *   If removing $x$ results in an empty array (not possible per constraints "nums remains non-empty"), we handle it, but constraints say $1 \le nums.length$. If all elements are $x$, removing $x$ leaves an empty array, but the problem says "remains non-empty", implying we can't remove the only element if it's the only unique element? Actually, the constraint says "remains non-empty", so if `nums = [5]`, we can't remove 5. My code handles this naturally because if `indices` has only one element and it's the only element, the loops for `i>0` and `i<n-1` won't trigger a merge, and `ans` remains `global_max`. Wait, if `nums=[5]`, `global_max` is 5. We can't remove 5. The code returns 5. Correct.
    *   If `nums = [-3, 2, -2, -1, 3, -2, 3]`, `global_max` is 4. Removing -2 merges `2` and `-1` and `3` and `3`? No, removing -2 splits the array.
        *   Original: `[-3, 2, -2, -1, 3, -2, 3]`
        *   Remove -2: `[-3, 2, -1, 3, 3]`. Max subarray is `2 + -1 + 3 + 3 = 7`.
        *   My logic: Occurrences of -2 are at indices 2 and 5.
        *   At index 2: `max_ending[1]` (sum ending at 2 is `2`? No, `max_ending` is max subarray ending at `i`. `nums[1]=2`. `max_ending[1]=2`. `max_starting[3]` (starts at 3, `nums[3]=-1`). `max_starting[3]` would be `max(-1, -1+3, -1+3+3) = 8`? No.
        *   Let's trace `max_starting` for `[-3, 2, -2, -1, 3, -2, 3]`.
            *   `i=6 (3)`: 3
            *   `i=5 (-2)`: max(-2, -2+3) = 1
            *   `i=4 (3)`: max(3, 3+1) = 4
            *   `i=3 (-1)`: max(-1, -1+4) = 3
            *   `i=2 (-2)`: max(-2, -2+3) = 1
            *   `i=1 (2)`: max(2, 2+1) = 3
            *   `i=0 (-3)`: max(-3, -3+3) = 0
        *   At index 2 (value -2): `max_ending[1]` = 3 (subarray `[2]`? No, `max_ending[1]` is max subarray ending at 1. `nums[1]=2`. `max_ending[0]=-3`. `max_ending[1]=max(2, -3+2)=2`. Wait, `max_ending` calculation:
            *   `i=0`: -3
            *   `i=1`: max(2, -3+2) = 2
            *   `i=2`: max(-2, 2-2) = 0
            *   `i=3`: max(-1, 0-1) = 0
            *   `i=4`: max(3, 0+3) = 3
            *   `i=5`: max(-2, 3-2) = 1
            *   `i=6`: max(3, 1+3) = 4
        *   So `max_ending[1]` is 2. `max_starting[3]` is 3. Sum = 5.
        *   At index 5 (value -2): `max_ending[4]` is 3. `max_starting[6]` is 3. Sum = 6.
        *   Wait, the example output is 7. Where does 7 come from? `2 + -1 + 3 + 3`.
        *   Indices: 1 (`2`), 3 (`-1`), 4 (`3`), 6 (`3`).
        *   This subarray crosses the gap at index 2 (removed -2) and index 5 (removed -2).
        *   My logic only checks merging *adjacent* segments separated by a *single* instance of $x$.
        *   If $x$ appears multiple times, say at $i_1, i_2$, removing $x$ merges segment $S_1$ (before $i_1$), $S_2$ (between $i_1, i_2$), $S_3$ (after $i_2$).
        *   The new array is $S_1 S_2 S_3$.
        *   The max subarray could be a suffix of $S_1$ + $S_2$ + prefix of $S_3$.
        *   My current logic only checks `suffix(S_1) + prefix(S_2)` and `suffix(S_2) + prefix(S_3)`. It misses `suffix(S_1) + S_2 + prefix(S_3)`.
        *   Correction: When removing $x$, the segments $S_1, S_2, \dots$ are concatenated. The max subarray sum is the max subarray sum of this concatenated array.
        *   This is equivalent to finding the max subarray sum in the original array *excluding* $x$.
        *   We can compute this by iterating through the array once for each $x$? No, too slow.
        *   Alternative: The max subarray sum after removing $x$ is the max of:
            1. `global_max` (if the optimal subarray doesn't use $x$).
            2. If the optimal subarray uses $x$, it must be formed by merging parts.
            3. Actually, the max subarray sum after removing $x$ is simply the max subarray sum of the array where all $x$ are replaced by $-\infty$.
            4. We can compute this efficiently?
            5. Let's reconsider the structure. The array becomes $S_1, S_2, \dots, S_k$.
            6. The max subarray sum is $\max($
                - $\max_i (\text{max subarray sum in } S_i)$,
                - $\max_i (\text{max suffix of } S_i + \text{max prefix of } S_{i+1})$
            -)
            7. Wait, if we have $S_1, S_2, S_3$, we can have $S_1 + S_2 + S_3$.
            8. The max subarray sum of $S_1 S_2 S_3$ is $\max($
                - $\text{max subarray in } S_1$,
                - $\text{max subarray in } S_2$,
                - $\text{max subarray in } S_3$,
                - $\text{max suffix } S_1 + \text{max prefix } S_2$,
                - $\text{max suffix } S_2 + \text{max prefix } S_3$,
                - $\text{max suffix } S_1 + \text{sum}(S_2) + \text{max prefix } S_3$
            -)
            9. This looks like we need to consider sums of multiple segments.
            10. However, note that $\text{sum}(S_2)$ is just the sum of elements between two occurrences of $x$.
            11. Is it possible that the optimal solution involves merging more than 2 segments? Yes, as seen in the example.
            12. But notice: $\text{max suffix } S_1 + \text{sum}(S_2) + \text{max prefix } S_3 = (\text{max suffix } S_1 + \text{max prefix } S_2) + (\text{sum}(S_2) - \text{max prefix } S_2) + \dots$ No.
            13. Actually, the max subarray sum of the concatenated array $S_1 S_2 \dots S_k$ can be found by a standard Kadane's algorithm on the fly if we process segments.
            14. But we can't run Kadane's for each $x$.
            15. Key observation: The max subarray sum after removing $x$ is the max of:
                - `global_max`
                - For each $x$, the max subarray sum in the array where $x$ is removed.
            16. Let's re-examine the example `[ -3, 2, -2, -1, 3, -2, 3 ]`.
                - Remove -2. Segments: `[-3, 2]`, `[-1, 3]`, `[3]`.
                - Concatenated: `[-3, 2, -1, 3, 3]`.
                - Max subarray: `2, -1, 3, 3` -> sum 7.
                - This is `max_suffix([-3, 2]) + sum([-1, 3]) + max_prefix([3])`.
                - `max_suffix([-3, 2])` is 2. `sum([-1, 3])` is 2. `max_prefix([3])` is 3. Total 7.
            17. So we need to consider `suffix(S_i) + sum(S_{i+1}) + prefix(S_{i+2})`.
            18. This implies we need to check combinations of adjacent segments.
            19. Since the number of segments is equal to the count of $x$ (plus 1), and the sum of counts is $N$, maybe we can do it?
            20. For a fixed $x$, let the segments be $S_0, S_1, \dots, S_m$.
                - We need $\max(\text{Kadane}(S_i))$ and $\max(\text{suffix}(S_i) + \text{prefix}(S_{i+1}))$ and $\max(\text{suffix}(S_i) + \text{sum}(S_{i+1}) + \text{prefix}(S_{i+2}))$, etc.
                - Actually, the max subarray sum of the concatenated array is simply the max subarray sum of the sequence formed by concatenating $S_i$.
                - We can compute this in $O(\text{count}(x))$ if we precompute `sum(S_i)`, `max_suffix(S_i)`, `max_prefix(S_i)`.
                - `sum(S_i)` is easy: `prefix_sum[j] - prefix_sum[i]`.
                - `max_suffix(S_i)` is `max_ending` of the last element of $S_i$? No, `max_ending` in the original array ending at the last element of $S_i$.
                - `max_prefix(S_i)` is `max_starting` of the first element of $S_i$.
                - So for each $x$, we can iterate through its segments, compute the max subarray sum of the concatenated segments.
                - Since the total number of segments across all $x$ is $N$ (each element belongs to exactly one segment for a specific $x$), the total time is $O(N)$.
                - Algorithm:
                    1. Precompute `max_ending`, `max_starting`, `prefix_sum`.
                    2. Group indices by value.
                    3. For each $x$:
                        - Identify segments. A segment is defined by indices between occurrences of $x$.
                        - Let occurrences be $idx_0, idx_1, \dots, idx_k$.
                        - Segments are:
                          - $S_0$: indices $0$ to $idx_0-1$.
                          - $S_1$: indices $idx_0+1$ to $idx_1-1$.
                          - ...
                          - $S_{k+1}$: indices $idx_k+1$ to $n-1$.
                        - For each segment $S_j$, compute:
                          - `seg_sum`: sum of elements.
                          - `seg_max_suffix`: max suffix sum. (Can be derived from `max_ending` at the end of segment).
                          - `seg_max_prefix`: max prefix sum. (Can be derived from `max_starting` at the start of segment).
                          - `seg_max_sub`: max subarray sum within the segment. (Can be derived from `max_ending` values within the segment? Or just run Kadane's on the fly).
                        - Now, we have a list of "super-elements" for the new array: each super-element has a `sum`, `max_suffix`, `max_prefix`, `max_sub`.
                        - We want the max subarray sum of the sequence of these super-elements.
                        - This is a variation of Kadane's on the super-elements.
                        - `current_max` = 0. `global_max_new` = -inf.
                        - For each super-element:
                          - `current_max` = max(super.max_sub, super.max_suffix + current_max) ? No.
                          - The super-element itself contributes `super.max_sub`.
                          - It can extend a previous `current_max` via `super.max_prefix`.
                          - So `current_max` = max(super.max_sub, super.max_prefix + current_max).
                          - `global_max_new` = max(global_max_new, current_max).
                        - Wait, `super.max_sub` is the max subarray *within* the segment. `super.max_prefix` is the max prefix *of* the segment.
                        - If we extend from previous, we take `current_max` (which is a suffix of previous segments) + `super.max_prefix`.
                        - But `super.max_sub` might be entirely inside the segment and not connected to the prefix.
                        - So `current_max` = max(super.max_sub, super.max_prefix + current_max).
                        - And `global_max_new` = max(global_max_new, current_max).
                        - This works.
                        - Complexity: Sum of number of segments over all $x$ is $O(N)$.
                        - Total time $O(N)$.

## worker: Iterate through each unique element $x$, identify 
The solution involves the following steps:
1.  **Precomputation**:
    *   `max_ending[i]`: Maximum subarray sum ending at index `i`.
    *   `max_starting[i]`: Maximum subarray sum starting at index `i`.
    *   `prefix_sum`: To allow O(1) sum queries for segments.
    *   `Sparse Table`: Built on `max_ending` to allow O(1) range maximum queries for `seg_max_sub` (max subarray sum within a segment).
2.  **Grouping**: Indices of each unique number are grouped to efficiently identify segments formed by removing that number.
3.  **Simulation**: For each unique number `x`:
    *   Identify the contiguous segments of non-`x` elements.
    *   For each segment, compute its `sum`, `max_prefix`, `max_suffix`, and `max_sub` (using the Sparse Table).
    *   Treat each segment as a "super-element" and run a modified Kadane's algorithm to find the maximum subarray sum in the concatenated sequence of segments.
    *   Update the global answer if a larger sum is found.
4.  **Complexity**:
    *   Precomputation: $O(N \log N)$ due to Sparse Table.
    *   Iterating unique numbers and segments: The total number of segments across all unique numbers is $O(N)$ (since each element belongs to exactly one segment for a specific `x`, and the number of segments is $count(x)+1$).
    *   Total Time Complexity: $O(N \log N)$.
    *   Space Complexity: $O(N \log N)$ for the Sparse Table.

## worker: finalize
The solution efficiently handles the problem by leveraging precomputed arrays and a Sparse Table for Range Maximum Queries (RMQ).
1.  **Precomputation**:
    *   `max_ending[i]` and `max_starting[i]` store the maximum subarray sum ending at or starting at index `i` respectively, computed in $O(N)$.
    *   `prefix_sum` allows calculating the sum of any segment in $O(1)$.
    *   A **Sparse Table** is built on `max_ending` to query the maximum subarray sum within any contiguous segment in $O(1)$ time. This is crucial because calculating the max subarray sum for a segment naively would take $O(\text{length})$, leading to $O(N^2)$ in the worst case.
2.  **Processing Removals**:
    *   Indices of each unique number are grouped.
    *   For each unique number $x$, the array is virtually split into contiguous segments of non-$x$ elements.
    *   For each segment, we compute its properties: `seg_sum`, `seg_max_prefix`, `seg_max_suffix`, and `seg_max_sub` (using the Sparse Table).
    *   These segments are treated as "super-elements". We run a modified Kadane's algorithm on this sequence of super-elements to find the maximum subarray sum in the array after removing $x$.
3.  **Complexity**:
    *   Building the Sparse Table: $O(N \log N)$.
    *   Iterating through unique numbers and their segments: The total number of segments across all unique numbers is $O(N)$ (since each element belongs to exactly one segment for a specific $x$).
    *   Total Time Complexity: $O(N \log N)$.
    *   Space Complexity: $O(N \log N)$ for the Sparse Table.
4.  **Edge Cases**:
    *   If removing $x$ leaves an empty array (not possible per constraints as we can choose not to remove, and "remains non-empty" implies valid operations), the logic naturally handles it by checking `start <= end`.
    *   If $x$ is at the start or end, the corresponding segments are handled correctly (length 0 or 1).
