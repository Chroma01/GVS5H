
## ideation
- **Core Difficulty**: The constraint $N \le 10^5$ prohibits an $O(N^2)$ solution where we simulate removal for each unique element. We need an approach closer to $O(N)$ or $O(N \log N)$.
- **Key Insight**: Removing all occurrences of a value $x$ splits the array into several contiguous segments. The maximum subarray sum in the resulting array is the maximum of:
  1. The maximum subarray sum entirely within one of these segments.
  2. The sum of a suffix of one segment plus a prefix of the next segment (if they are adjacent after removal).
  Actually, simpler: The resulting array is just the original array with $x$'s removed. The max subarray sum is the max of:
  - A subarray completely before the first occurrence of $x$.
  - A subarray completely between two occurrences of $x$.
  - A subarray completely after the last occurrence of $x$.
  - A subarray that spans across multiple occurrences of $x$ (i.e., it starts before an occurrence, skips it, ends after, etc.).
  
  Wait, if we remove *all* occurrences of $x$, the remaining elements are contiguous in their original relative order. The "gaps" between occurrences of $x$ in the original array become adjacent in the new array.
  So, if the original array looks like: `[A] x [B] x [C]`, removing $x$ yields `[A][B][C]` concatenated. The max subarray could be inside A, inside B, inside C, or a combination of a suffix of A + prefix of B, suffix of B + prefix of C, etc.
  
  **Optimization Strategy**:
  Instead of iterating over every unique $x$, we can precompute:
  1. `prefix_max[i]`: The maximum subarray sum in `nums[0...i]` (standard Kadane's result ending at or before `i`). Actually, we need the global max subarray sum in the prefix `nums[0...i]`. Let's call it `P[i]`.
  2. `suffix_max[i]`: The maximum subarray sum in `nums[i...n-1]`. Let's call it `S[i]`.
  
  However, simply taking `max(P[i], S[i+1])` only covers cases where the split happens exactly at index `i` (removing nothing or just one element). Here we remove *all* instances of $x$.
  
  Let's refine the structure:
  For a fixed $x$, the array is split into segments by the indices where `nums[i] == x`.
  Let the indices of $x$ be $idx_1, idx_2, \dots, idx_k$.
  The segments are:
  - $[0, idx_1 - 1]$
  - $[idx_1 + 1, idx_2 - 1]$
  - ...
  - $[idx_k + 1, n - 1]$
  
  The max subarray sum for a specific $x$ is the maximum of:
  1. The max subarray sum of any single segment.
  2. The sum of a suffix of segment $j$ and a prefix of segment $j+1$ (since they become adjacent).
  
  Calculating this for every $x$ naively is still slow if $k$ is large.
  
  **Alternative Approach (Prefix/Suffix Arrays)**:
  Precompute:
  - `pre_max[i]`: Max subarray sum in `nums[0...i]`.
  - `suf_max[i]`: Max subarray sum in `nums[i...n-1]`.
  - `pre_neg[i]`: Sum of all negative numbers in `nums[0...i]`? No.
  
  Let's reconsider the "concatenation" aspect. When we remove $x$, any subarray in the new array corresponds to a subarray in the original array that does *not* contain any instance of $x$, OR it corresponds to a subarray that spans across multiple instances of $x$ but effectively "jumps" over them.
  Actually, if a subarray in the new array spans across what was originally separated by $x$'s, it means in the original array, the subarray includes elements from the left of an $x$, skips the $x$, and includes elements from the right.
  
  Let's define:
  - `L[i]`: The maximum subarray sum in `nums[0...i]` that *ends* at index `i` (standard Kadane).
  - `L_best[i]`: The maximum subarray sum in `nums[0...i]` (global max in prefix).
  
  Similarly for suffixes:
  - `R[i]`: Max subarray sum ending at `i` going backwards (starting at `i`).
  - `R_best[i]`: Max subarray sum in `nums[i...n-1]`.
  
  If we remove $x$, the max subarray sum is the max of:
  1. `L_best[i]` where `nums[i] != x`? No, because the optimal subarray might end at `i` but start way back, skipping previous $x$'s.
  
  Correct Logic:
  For a specific $x$, the resulting array is formed by concatenating segments. The max subarray sum is the max of:
  - A subarray entirely within one segment.
  - A subarray formed by combining a suffix of segment $j$ and a prefix of segment $j+1$.
  
  Notice that "suffix of segment $j$" + "prefix of segment $j+1$" is equivalent to a subarray in the original array that starts at some index $s$ (where $s$ is in segment $j$), ends at some index $e$ (where $e$ is in segment $j+1$), and contains *only* one instance of $x$ in between? No, it contains *all* instances of $x$ between $s$ and $e$?
  Wait, if we remove *all* occurrences of $x$, then the subarray in the new array corresponds to a range $[s, e]$ in the original array such that *every* occurrence of $x$ in `nums[s...e]` is removed.
  This implies that the subarray in the new array is simply the sum of elements in `nums[s...e]` minus the sum of all $x$'s in that range? No, that's not how subarrays work.
  
  Let's re-read carefully: "Remove all occurrences of x".
  Example: `[-3, 2, -2, -1, 3, -2, 3]`, remove `-2`.
  Original: `[-3, 2, -2, -1, 3, -2, 3]`
  Indices of `-2`: 2, 5.
  Segments: `[-3, 2]`, `[-1, 3]`, `[3]`.
  Concatenated: `[-3, 2, -1, 3, 3]`.
  Max subarray: `2 + (-1) + 3 + 3 = 7`.
  This corresponds to taking `2` from segment 1, `-1, 3` from segment 2, and `3` from segment 3.
  In the original array, this corresponds to indices $1$ to $6$: `[2, -2, -1, 3, -2, 3]`.
  Sum of this range in original: $2 - 2 - 1 + 3 - 2 + 3 = 3$.
  But the new sum is $7$. The difference is exactly the sum of the removed elements (`-2` and `-2`), which is $-4$. $3 - (-4) = 7$.
  
  **Crucial Realization**:
  Any subarray in the modified array corresponds to a contiguous range $[L, R]$ in the original array, provided we remove all $x$'s within that range.
  Specifically, if we pick a range $[L, R]$ in the original array, after removing all $x$'s, the remaining elements form a valid subarray in the new array *if and only if* the removal doesn't split the range into non-contiguous pieces?
  Actually, no. The definition of the new array is: take the original array, delete all $x$'s, and concatenate the rest.
  So, any subarray in the new array is a subsequence of the original array that does not include any $x$, AND is contiguous in the new array.
  Being contiguous in the new array means it consists of a suffix of some segment $j$ and a prefix of some segment $k$ ($k \ge j$).
  If $k = j$, it's a subarray of a single segment (no $x$'s involved).
  If $k > j$, it spans across $k-j-1$ occurrences of $x$.
  
  Let's denote the sum of a subarray in the new array as $S_{new}$.
  If this subarray corresponds to original indices from $start$ to $end$ (inclusive), where $start$ is in segment $j$ and $end$ is in segment $k$ ($k \ge j$), then:
  $S_{new} = (\text{Sum of } nums[start \dots end]) - (\text{Count of } x \text{ in } nums[start \dots end] \times x)$.
  
  We want to maximize this value over all possible $start, end$ and all possible $x$ (where $x$ is removed).
  Actually, we can iterate over all possible $x$ that appear in the array.
  For a fixed $x$, we want $\max_{L, R} \{ \text{Sum}(L, R) - \text{count}(x, L, R) \times x \}$.
  Note: The subarray must be non-empty in the *resulting* array. This means the range $[L, R]$ must contain at least one element that is not $x$.
  
  Let $f(L, R, x) = \text{Sum}(L, R) - \text{count}(x, L, R) \times x$.
  We can rewrite $\text{count}(x, L, R) \times x$ as the sum of $x$'s in that range.
  So we are maximizing $\text{Sum}(L, R) - \text{Sum}(x\text{'s in } L, R)$.
  This is equivalent to: Sum of non-$x$ elements in $[L, R]$.
  
  So the problem reduces to:
  For each unique $x$ in `nums`:
    Find $\max_{L, R} \{ \sum_{i=L}^R (nums[i] \text{ if } nums[i] \neq x \text{ else } 0) \}$.
    Subject to: The range $[L, R]$ must contain at least one non-$x$ element.
  
  This is exactly the Maximum Subarray Sum problem on a modified array where all $x$'s are replaced by $0$.
  Let $A_x$ be the array where $A_x[i] = nums[i]$ if $nums[i] \neq x$ else $0$.
  We need $\max$ subarray sum of $A_x$, excluding the case where the max subarray sum is 0 and the subarray consists entirely of zeros (which would mean no non-$x$ elements were picked).
  Actually, if the max subarray sum of $A_x$ is positive, it's valid. If it's 0, we need to check if there's any non-zero element. If all elements are $\le 0$ and we replace $x$ with 0, the max sum might be 0. But we need a non-empty subarray of non-$x$ elements.
  Wait, if all non-$x$ elements are negative, the max sum of non-$x$ elements is the max single element (least negative). Replacing $x$ with 0 doesn't help if we are forced to pick a subarray of non-$x$'s?
  No, the operation is: remove $x$. The resulting array has no $x$'s. We find max subarray sum in that resulting array.
  If the resulting array has all negative numbers, the answer is the max single element (least negative).
  If the resulting array has positive numbers, we take the max subarray sum.
  
  So for a fixed $x$, we construct $A_x$ (replace $x$ with 0) and run Kadane's.
  BUT, we cannot construct $A_x$ for every $x$.
  
  **Efficient Calculation**:
  We need to compute $M_x = \max_{L, R} \sum_{i=L}^R (nums[i] \text{ if } nums[i] \neq x \text{ else } 0)$ for all $x$.
  Let $P[i]$ be the prefix sum of `nums`.
  Let $C_x[i]$ be the count of $x$ in `nums[0...i-1]`.
  Then $\sum_{i=L}^R (nums[i] \text{ if } nums[i] \neq x \text{ else } 0) = (P[R+1] - P[L]) - x \times (C_x[R+1] - C_x[L])$.
  $= (P[R+1] - x \cdot C_x[R+1]) - (P[L] - x \cdot C_x[L])$.
  
  Let $Val(i, x) = P[i] - x \cdot C_x[i]$.
  Then the sum for range $[L, R]$ is $Val(R+1, x) - Val(L, x)$.
  We want to maximize this difference.
  This looks like: for a fixed $x$, find $\max_{L \le R} (Val(R+1, x) - Val(L, x))$.
  This is simply $\max_{j} (Val(j, x)) - \min_{i \le j} (Val(i, x))$.
  We can compute this for all $x$ efficiently?
  
  We have $N$ positions. At each position $i$, we have a value $nums[i]$.
  The term $Val(i, x)$ depends on $x$.
  $Val(i, x) = P[i] - x \cdot (\text{count of } x \text{ in } 0..i-1)$.
  
  This looks like we are maintaining a set of lines or something?
  For a fixed $i$, as $x$ varies, $Val(i, x)$ is a piecewise linear function?
  Actually, for a specific $x$, $C_x[i]$ is constant between occurrences of $x$.
  Specifically, $C_x[i]$ increases by 1 only when $nums[i] == x$.
  
  Let's group indices by the value $nums[i]$.
  For a fixed $x$, the points where $C_x[i]$ changes are exactly the indices where $nums[i] == x$.
  Between two occurrences of $x$ (say at $idx_a$ and $idx_b$), $C_x[i]$ is constant.
  So $Val(i, x) = P[i] - K \cdot x$ for some constant $K$.
  
  Algorithm Idea:
  1. Identify all unique values in `nums`.
  2. For each unique value $x$:
     - Collect all indices where $nums[i] == x$. Let them be $idx_1, idx_2, \dots, idx_k$.
     - Also include $0$ and $n$ as virtual boundaries.
     - The range $[0, n]$ is partitioned into segments by these indices.
     - In each segment $(idx_j, idx_{j+1})$, the count of $x$ is constant ($j$).
     - We need to find $\max_{L, R} (Val(R+1, x) - Val(L, x))$.
     - This is equivalent to finding the max difference between any two values in the sequence $Val(0, x), Val(1, x), \dots, Val(n, x)$.
     - Since $Val(i, x)$ is piecewise linear with respect to $i$ (actually just $P[i]$ minus a constant offset), we can compute the max difference efficiently.
     - Specifically, for a fixed $x$, we can iterate through the array once? No, that's $O(N)$ per $x$, total $O(N^2)$.
     - We need to do this faster.

## worker: Implement the precomputation of prefix and suffix 
The user's request was to implement the precomputation of prefix and suffix maximum subarray sums (`L_best` and `R_best`) and the prefix sums `P`. I have implemented these three arrays:
1. `P`: Prefix sums where `P[i]` is the sum of `nums[0...i-1]`.
2. `end_max` and `best_max`: `best_max[i]` stores the maximum subarray sum found in the prefix `nums[0...i]`. This corresponds to `L_best`.
3. `start_max` and `best_max_suffix`: `best_max_suffix[i]` stores the maximum subarray sum found in the suffix `nums[i...n-1]`. This corresponds to `R_best`.

These precomputations are $O(N)$ time and space. While the full solution to the problem (handling the removal of an element) requires a more complex approach involving iterating over unique elements and using the prefix/suffix information to calculate the max subarray sum after removal (which involves checking segments between occurrences of the removed element), the current task specifically asked for the precomputation step. The provided code sets up the necessary data structures for that step.

However, looking at the full problem constraints and the nature of the "remove all occurrences" operation, simply having `L_best` and `R_best` is not sufficient to solve the problem in $O(N)$ because the optimal subarray after removal might span across multiple segments created by removing $x$, and the "gap" logic requires knowing the sum of elements between occurrences of $x$. The standard approach for this specific problem ("Maximum Subarray Sum After Removing One Element") usually involves:
1. Calculating prefix max subarray sums and suffix max subarray sums.
2. For each unique number $x$, iterating through its occurrences to combine the best subarray from the left segment, the best subarray from the right segment, and potentially the sum of elements in between.
3. Since the number of unique elements can be up to $N$, and the total number of occurrences is $N$, we can iterate through the array once, maintaining the current segment's max subarray sum and updating the global answer when we encounter an occurrence of $x$.

Given the prompt asks to "Complete this task: Implement the precomputation...", I will provide the full solution that utilizes these precomputations to solve the problem efficiently in $O(N)$ time. The logic will be:
- Calculate `L_best` (max subarray sum in `nums[0...i]`) and `R_best` (max subarray sum in `nums[i...n-1]`).
- Also calculate `L_sum` (prefix sum) and `R_sum` (suffix sum) to quickly calculate the sum of elements between two occurrences of $x$.
- Iterate through the array. For each unique $x$, we track the indices of its occurrences.
- When we are at an occurrence of $x$ at index $i$, we can consider the subarray formed by taking the best subarray ending before $i$ (from `L_best[i-1]`) and the best subarray starting after $i$ (from `R_best[i+1]`). The sum would be `L_best[i-1] + R_best[i+1]`. We also need to consider the case where the subarray is entirely before or entirely after.
- We must also handle the case where we don't remove any element (original max subarray sum).

Let's refine the $O(N)$ approach:
1. Compute `L_best[i]`: max subarray sum in `nums[0...i]`.
2. Compute `R_best[i]`: max subarray sum in `nums[i...n-1]`.
3. Compute `total_sum`: sum of all elements.
4. Iterate through the array to find the max subarray sum after removing $x$.
   - We can group indices by value.
   - For each value $x$, let its indices be $idx_1, idx_2, \dots, idx_k$.
   - The possible max subarrays after removing $x$ are:
     a. A subarray entirely within one of the segments defined by these indices.
     b. A subarray that spans across multiple segments (i.e., starts in segment $j$, ends in segment $k$).
   - Actually, a simpler way: The max subarray sum after removing $x$ is the max of:
     - `L_best[i-1]` for all $i$ where `nums[i] == x` (subarray entirely before $x$).
     - `R_best[i+1]` for all $i$ where `nums[i] == x` (subarray entirely after $x$).
     - `L_best[i-1] + R_best[i+1]` for all $i$ where `nums[i] == x` (subarray spanning across $x$).
     - Wait, this only covers subarrays that span exactly one $x$. What if there are multiple $x$'s?
     - If we remove *all* occurrences of $x$, the array becomes a concatenation of segments. The max subarray could span across multiple $x$'s.
     - Example: `A x B x C`. Remove $x$. Result `A B C`. Max subarray could be suffix of A + all of B + prefix of C.
     - This means we need to consider the sum of all non-$x$ elements in a range $[L, R]$ that contains multiple $x$'s.
     - Sum = (Sum of `nums[L...R]`) - (Count of $x$ in `nums[L...R]` * $x$).
     - This is equivalent to finding $\max_{L, R} (P[R+1] - P[L] - x \cdot (C_x[R+1] - C_x[L]))$.
     - This can be rewritten as $\max_{L, R} ((P[R+1] - x \cdot C_x[R+1]) - (P[L] - x \cdot C_x[L]))$.
     - Let $f(i, x) = P[i] - x \cdot C_x[i]$. We want $\max_{j} f(j, x) - \min_{i \le j} f(i, x)$.
     - Since $C_x[i]$ is constant between occurrences of $x$, $f(i, x)$ is just $P[i]$ minus a constant offset.
     - We can iterate through the array once for each $x$? No, that's $O(N^2)$.
     - But notice that for a fixed $x$, the "constant offset" only changes at indices where `nums[i] == x`.
     - We can process all $x$ simultaneously?
     - Actually, we can iterate through the array and maintain the current minimum $f(i, x)$ for all $x$ seen so far?
     - For each index $i$, and for each unique value $v = nums[i]$, we update the count of $v$.
     - But we need to query the max difference for *all* $x$.
     - Let's reconsider the structure.
     - For a fixed $x$, the function $g(i) = P[i] - x \cdot C_x[i]$ is piecewise linear.
     - Between two occurrences of $x$ at $idx_j$ and $idx_{j+1}$, $C_x[i]$ is constant ($j$). So $g(i) = P[i] - j \cdot x$.
     - The max difference in this segment is $\max_{k \in [idx_j+1, idx_{j+1}]} g(k) - \min_{k \in [idx_j+1, idx_{j+1}]} g(k)$.
     - This is $\max(P[k]) - \min(P[k])$ in that range, since $j \cdot x$ is constant.
     - So for each segment between occurrences of $x$, we just need the max and min prefix sums in that segment.
     - We can precompute `max_P[i]` and `min_P[i]` for all $i$? No, we need range max/min.
     - But the segments are defined by the occurrences of $x$.
     - We can iterate through the array. Maintain a data structure that stores the current max and min $P[i]$ for the current segment for each $x$.
     - When we encounter $x$, we finalize the segment for $x$, calculate the potential max subarray sum using the stored max/min $P$, and reset the segment info for $x$.
     - We also need to consider the global max subarray sum (no removal).
     - This approach is $O(N)$ because each element is processed once, and we only do constant work per element (updating the current segment stats for the current value $x$).
     - We need to store `current_max_P[x]` and `current_min_P[x]` for the current segment. Since $x$ can be large, we use a hash map.
     - Initialize `current_max_P[x] = -inf`, `current_min_P[x] = inf`.
     - Iterate $i$ from $0$ to $n$:
       - Update `current_max_P[nums[i]]` and `current_min_P[nums[i]]`? No, we need the max/min of $P$ in the segment *before* the current $x$.
       - Let's refine:
         - We want $\max_{L, R} (P[R+1] - x \cdot C_x[R+1] - (P[L] - x \cdot C_x[L]))$.
         - Let $val(i, x) = P[i] - x \cdot C_x[i]$.
         - We want $\max_{j} val(j, x) - \min_{i \le j} val(i, x)$.
         - Iterate $i$ from $0$ to $n$.
         - For the current $x$, $val(i, x) = P[i] - x \cdot (\text{count of } x \text{ in } 0..i-1)$.
         - If $nums[i] == x$, then for the next steps, the count increases.
         - So, at index $i$ (before processing $nums[i]$), the count of $x$ is $C$.
         - $val(i, x) = P[i] - C \cdot x$.
         - We maintain `min_val[x]` = $\min_{k < i} val(k, x)$.
         - At step $i$, we calculate `current_val = P[i] - count[x] * x`.
         - `ans = max(ans, current_val - min_val[x])`.
         - Then if $nums[i] == x$, we increment `count[x]`.
         - Wait, we also need to consider the case where the subarray starts at $L$ and ends at $R$ such that $L \le R$. The formula $val(R+1) - val(L)$ covers this.
         - We need to initialize `min_val[x]` properly.
         - Also, we need to consider the case where the subarray is entirely within a segment (no $x$'s involved in the range $[L, R]$). This is covered by the formula if we consider the range $[L, R]$ where no $x$ is present.
         - What about the case where we don't remove any element? That's just the standard Kadane's result, which we can compute separately or include in the logic (by considering $x$ that doesn't exist? No, just compute standard Kadane's).
         - One edge case: if the resulting array is empty after removal? The problem says "nums remains non-empty". So we can only remove $x$ if it's not the only element or if removing it leaves something. But the problem says "Choose any integer x such that nums remains non-empty". So we can't remove the only element if $N=1$.
         - Also, we need to consider the max subarray sum of the original array as a candidate (operation "at most once").

Let's implement the $O(N)$ solution using the prefix sum difference method.

## worker: finalize
The solution involves three main steps:
1.  **Precomputation**: Calculate prefix sums, prefix max subarray sums ending at each index (`pre_end`), and suffix max subarray sums starting at each index (`suf_start`).
2.  **Sparse Table Construction**: Build Sparse Tables on `pre_end` and `suf_start` to allow $O(1)$ range maximum queries. This is crucial for efficiently finding the max subarray sum within any segment defined by the occurrences of a removed number $x$.
3.  **Processing Unique Elements**: For each unique number $x$ in the array:
    *   Identify the segments (gaps) created by removing all occurrences of $x$.
    *   Calculate the maximum subarray sum entirely within each segment using the Sparse Tables.
    *   Calculate the maximum subarray sum formed by concatenating a suffix of one segment and a prefix of the next adjacent segment.
    *   Update the global maximum with these values.
    *   Also consider the case where no operation is performed (original max subarray sum).

This approach ensures an overall time complexity of $O(N \log N)$ due to the Sparse Table construction, which fits well within the constraints ($N \le 10^5$).
