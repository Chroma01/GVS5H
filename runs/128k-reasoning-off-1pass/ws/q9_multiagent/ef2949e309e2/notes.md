
## ideation
The core difficulty lies in correctly interpreting the definition of "unique middle mode" and ensuring that the counting method does not overcount or undercount based on the specific constraints of subsequences (order matters, indices matter).

Key insights derived from the problem statement:
1.  **Subsequence Definition**: A subsequence maintains the relative order of elements. If we select indices $i_1 < i_2 < i_3 < i_4 < i_5$, the element at index 2 of the subsequence is `nums[i_3]`.
2.  **Unique Middle Mode Condition**: The element at `seq[2]` (which is `nums[i_3]`) must be the *unique* mode.
    *   In a sequence of length 5, the maximum frequency of any element is 5.
    *   If the middle element appears $k$ times, for it to be the unique mode, no other element can appear $k$ or more times.
    *   Since the total length is 5:
        *   If the middle element appears 3 times, the remaining 2 elements can be anything. The max frequency of any other element is 2. Thus, 3 > 2, so the mode is unique.
        *   If the middle element appears 4 times, the remaining 1 element has frequency 1. 4 > 1, unique.
        *   If the middle element appears 5 times, unique.
        *   If the middle element appears 2 times, another element could also appear 2 times (e.g., [1, 2, 1, 2, 3]), making the mode not unique. Or the middle element isn't even the mode if another appears 3 times.
    *   **Conclusion**: The condition "unique middle mode" is satisfied if and only if the middle element appears **at least 3 times** in the subsequence.

3.  **Counting Strategy**:
    *   We iterate through every index `i` in `nums` and assume `nums[i]` is the middle element (the 3rd element of the subsequence).
    *   To form a valid subsequence where `nums[i]` is at position 2, we must choose exactly 2 indices from the range `[0, i-1]` and exactly 2 indices from the range `[i+1, n-1]`.
    *   We need to calculate combinations: $C(\text{count}(nums[i] \text{ in left}), 2) \times C(\text{count}(nums[i] \text{ in right}), 2)$.
    *   Wait, do we need to restrict the *values* chosen from left/right?
        *   The problem asks for the number of *subsequences*. Each set of 5 indices defines a unique subsequence.
        *   If we pick 2 indices from the left and 2 from the right, the resulting subsequence has `nums[i]` at the middle.
        *   Does the value of the other elements matter for the "unique mode" check?
            *   As established, if `nums[i]` appears at least 3 times (which it does by construction: 1 at `i` + 2 from left + 2 from right? No, wait).
            *   **Correction**: We are fixing `nums[i]` as the middle element. We need to pick 2 *other* instances of `nums[i]`? No.
            *   Let's re-read carefully: "A sequence of numbers seq of size 5 contains a unique middle mode if the middle element (seq[2]) is a unique mode."
            *   If I fix `nums[i]` as the middle element, I need to ensure that in the final subsequence, `nums[i]` appears $\ge 3$ times.
            *   My previous logic assumed I pick 2 *occurrences* of `nums[i]` from left and right. Is that required?
            *   Scenario A: I pick 2 indices from left and 2 from right, but those indices contain values *different* from `nums[i]`.
                *   Resulting subsequence: `[x, y, nums[i], z, w]`.
                *   Frequency of `nums[i]` is 1.
                *   Can `nums[i]` be the unique mode? Only if no other number appears $\ge 1$ times? Impossible, `x, y, z, w` exist. If all are distinct, frequencies are 1. Then there are 5 modes (all unique). Not a unique mode.
                *   So `nums[i]` MUST appear $\ge 3$ times.
            *   Therefore, the 2 elements chosen from the left MUST be `nums[i]`, and the 2 elements chosen from the right MUST be `nums[i]`.
            *   Wait, if I pick 2 from left and 2 from right, that's 4 elements + `nums[i]` = 5 elements. Total count of `nums[i]` is 5.
            *   Is it possible to have count 3 or 4?
                *   To have count 3: Pick 1 from left, 1 from right? No, we need 2 from left and 2 from right to maintain the "middle" position relative to the sorted indices?
                *   Definition of subsequence: indices $idx_1 < idx_2 < idx_3 < idx_4 < idx_5$. The middle element is at $idx_3$.
                *   If we fix $idx_3 = i$, then we MUST pick 2 indices from $0..i-1$ and 2 indices from $i+1..n-1$.
                *   This forces the subsequence to have exactly 5 elements.
                *   For `nums[i]` to be the mode with frequency $\ge 3$, we need at least 2 other occurrences of `nums[i]` in the chosen set.
                *   Since we pick 2 from left and 2 from right, we have 4 slots to fill.
                *   If we pick non-`nums[i]` values, the frequency of `nums[i]` is 1. Not a mode.
                *   If we pick 1 `nums[i]` from left and 1 from right, frequency is 3. This works.
                *   If we pick 2 `nums[i]` from left and 0 from right? Impossible, we must pick 2 from right.
                *   So, we need to choose 2 indices from left and 2 from right such that the total count of `nums[i]` in the set $\{idx_1, idx_2, i, idx_4, idx_5\}$ is $\ge 3$.
                *   Let $L_{val}$ be the count of `nums[i]` in $0..i-1$.
                *   Let $R_{val}$ be the count of `nums[i]` in $i+1..n-1$.
                *   We need to choose $l$ indices from left and $r$ indices from right such that $l+r \ge 2$ (to get total count $1+l+r \ge 3$).
                *   Wait, the constraint is simply: The subsequence is formed by picking ANY 2 from left and ANY 2 from right.
                *   Among all such combinations, which ones satisfy the condition?
                *   Condition: Count of `nums[i]` $\ge 3$.
                *   Let $k_L$ be the number of times `nums[i]` is picked from the left (0, 1, or 2).
                *   Let $k_R$ be the number of times `nums[i]` is picked from the right (0, 1, or 2).
                *   We need $1 + k_L + k_R \ge 3 \implies k_L + k_R \ge 2$.
                *   Total ways = (Ways to pick 2 from left) * (Ways to pick 2 from right) MINUS (Ways where $k_L + k_R < 2$).
                *   Cases where $k_L + k_R < 2$:
                    1.  $k_L = 0, k_R = 0$: Pick 2 non-`nums[i]` from left, 2 non-`nums[i]` from right.
                    2.  $k_L = 1, k_R = 0$: Pick 1 `nums[i]` and 1 non-`nums[i]` from left, 2 non-`nums[i]` from right.
                    3.  $k_L = 0, k_R = 1$: Pick 2 non-`nums[i]` from left, 1 `nums[i]` and 1 non-`nums[i]` from right.
                *   This seems complicated. Is there a simpler interpretation?
                *   Re-read Example 2: `[1,2,2,3,3,4]`. Output 4.
                    *   Valid subsequences:
                        *   `[1, 2, 2, 3, 4]`: Middle is 2. Counts: 1:1, 2:2, 3:1, 4:1. Mode is 2? No, max freq is 2. Is it unique? Yes. Wait, earlier I said mode must be $\ge 3$.
                        *   Let's re-evaluate "Unique Mode".
                        *   Sequence: `[1, 2, 2, 3, 4]`. Frequencies: 1->1, 2->2, 3->1, 4->1. Max freq is 2. Only '2' has freq 2. So '2' is the unique mode.
                        *   Middle element is '2'. It is the unique mode. Valid.
                        *   Sequence: `[1, 2, 3, 3, 4]`. Middle is 3. Counts: 1->1, 2->1, 3->2, 4->1. Unique mode 3. Valid.
                        *   Sequence: `[1, 2, 2, 3, 3]`. Middle is 2. Counts: 1->1, 2->2, 3->2. Modes are 2 and 3. Not unique. Invalid.
                *   **Correction to Logic**: The middle element must be the unique mode. It does NOT need to appear 3 times. It just needs to appear more times than any other element.
                *   In a sequence of length 5:
                    *   If middle element appears 3 times: Max freq of others is 2. Unique. (Valid)
                    *   If middle element appears 2 times:
                        *   Others must appear $\le 1$ time.
                        *   Since there are 3 other elements, they must be distinct and different from the middle element.
                        *   So pattern: `[x, y, M, z, w]` where $x,y,z,w \neq M$ and $x,y,z,w$ are all distinct.
                    *   If middle element appears 1 time:
                        *   Max freq of others must be 0? Impossible. Others exist.
                        *   So middle element cannot appear 1 time.
                    *   If middle element appears 0 times: Impossible (it is the middle element).
                *   So valid cases for middle element $M$:
                    1.  Count($M$) = 3. (Others can be anything, max freq 2).
                    2.  Count($M$) = 2. (Others must be distinct and $\neq M$).
                    3.  Count($M$) = 4. (Others distinct, $\neq M$).
                    4.  Count($M$) = 5. (All $M$).

    *   **Refined Algorithm**:
        Iterate `i` from 0 to `n-1`. Let `val = nums[i]`.
        We need to choose 2 indices from `0..i-1` and 2 from `i+1..n-1`.
        Let $L$ be the count of `val` in `0..i-1`.
        Let $R$ be the count of `val` in `i+1..n-1`.
        Let $TotalLeft = i$ (size of left part).
        Let $TotalRight = n - 1 - i$ (size of right part).
        
        We need to sum over all valid combinations of picking 2 from left and 2 from right.
        Let $k_L$ be count of `val` picked from left ($0 \le k_L \le 2$, also $k_L \le L$).
        Let $k_R$ be count of `val` picked from right ($0 \le k_R \le 2$, also $k_R \le R$).
        Total count of `val` = $1 + k_L + k_R$.
        
        Condition for Unique Mode:
        1.  If $1 + k_L + k_R \ge 3$: Always valid (since max freq of others is 2).
        2.  If $1 + k_L + k_R = 2$: Valid ONLY if no other number appears 2 times.
            *   This means the 3 non-`val` elements (2 from left/right non-`val` slots) must be distinct and not equal to `val`.
            *   Actually, if count(`val`) = 2, we have 3 other slots. If any other number appears 2 times, then we have two modes.
            *   So we need the 3 other elements to be distinct from each other and from `val`.
            *   Wait, if we have `[A, B, val, C, D]` where `val` appears twice. The other 3 are `A, B, C, D`? No, total 5. `val` appears twice. 3 others.
            *   If the 3 others are distinct, max freq is 1. `val` (2) > 1. Unique.
            *   If any of the 3 others are the same, say `A=A`, then that number appears 2 times. Then `val` and `A` are both modes. Not unique.
            *   So condition for count=2: The 3 non-`val` elements must be pairwise distinct and not equal to `val`.
        
        This looks like we need to count combinations based on values.
        However, notice the constraints: $N \le 1000$. $O(N^2)$ is acceptable.
        We can precompute prefix counts for all numbers? No, values are large. Map is needed.
        But iterating all pairs of left/right indices is $O(N^2)$, which is $10^6$, feasible.
        
        **Optimized Approach ($O(N^2)$)**:
        Iterate `i` (middle index).
        Identify the set of values in `nums[0...i-1]` and `nums[i+1...n-1]`.
        Actually, we can just iterate `i`, then iterate all pairs `(j, k)` from left and `(p, q)` from right? That's $O(N^4)$. Too slow.
        
        We need to count efficiently.
        For a fixed `i` and `val = nums[i]`:
        We need to choose 2 from left, 2 from right.
        Total ways to choose 2 from left: $C(i, 2)$.
        Total ways to choose 2 from right: $C(n-1-i, 2)$.
        Total combinations = $C(i, 2) \times C(n-1-i, 2)$.
        Subtract invalid combinations.
        Invalid cases:
        1.  Count(`val`) < 2 (i.e., 0 or 1).
            *   If count(`val`) = 0 or 1, `val` cannot be the unique mode (needs $\ge 2$).
            *   Wait, if count=1, max freq of others is 2? Possible. e.g. `[A, A, B, C, D]`. Mode A. Middle B. Not unique mode B.
            *   So if count(`val`) < 2, it's invalid.
            *   How many ways to get count < 2?
                *   Count = 0: Pick 0 `val` from left, 0 `val` from right.
                *   Count = 1: Pick 1 `val` from left, 0 from right OR 0 from left, 1 from right.
        2.  Count(`val`) = 2, but there is another element with count 2.
            *   This happens if among the 3 non-`val` elements, two are the same.
            *   Let the chosen indices be $L_1, L_2$ from left and $R_1, R_2$ from right.
            *   Suppose we picked $k_L$ copies of `val` from left and $k_R$ from right. Total $1+k_L+k_R = 2 \implies k_L+k_R=1$.
            *   Case A: $k_L=1, k_R=0$. Left picked: 1 `val`, 1 non-`val` ($x$). Right picked: 2 non-`val` ($y, z$).
                *   Invalid if $x=y$, $x=z$, or $y=z$.
            *   Case B: $k_L=0, k_R=1$. Left picked: 2 non-`val` ($x, y$). Right picked: 1 `val`, 1 non-`val` ($z$).
                *   Invalid if $x=y$, $x=z$, or $y=z$.
        
        This inclusion-exclusion seems messy to implement cleanly without careful case tracking.
        Alternative: Direct counting of valid configurations.
        For a fixed `i`:
        Valid configurations are those where:
        - Count(`val`) $\ge 3$.
        - OR Count(`val`) $= 2$ AND all other 3 elements are distinct and $\neq val$.
        
        Let's break down the count:
        1.  **Count(`val`) $\ge 3$**:
            *   Possible splits of remaining 2 slots (from left/right) into `val`s:
                *   2 from left, 0 from right (Total 3).
                *   1 from left, 1 from right (Total 3).
                *   0 from left, 2 from right (Total 3).
                *   2 from left, 1 from right (Total 4).
                *   1 from left, 2 from right (Total 4).
                *   2 from left, 2 from right (Total 5).
            *   For each split, we choose specific indices.
            *   Ways = $\sum_{k_L, k_R} (\text{ways to pick } k_L \text{ `val`s from left} \times \text{ways to pick } 2-k_L \text{ non-`val`s from left}) \times (\dots \text{right})$.
            *   This is getting complex.
        
        Simpler view:
        Total ways to pick 2 from left and 2 from right is $W_{total} = C(i, 2) \times C(n-1-i, 2)$.
        Invalid ways:
        A. Count(`val`) $\le 1$.
           - Count 0: Pick 0 `val` from left, 0 `val` from right.
             Ways: $C(i - L, 2) \times C((n-1-i) - R, 2)$.
           - Count 1:
             - 1 from left, 0 from right: $C(L, 1) \times C(i-L, 1) \times C((n-1-i)-R, 2)$.
             - 0 from left, 1 from right: $C(i-L, 2) \times C(R, 1) \times C((n-1-i)-R, 1)$.
        B. Count(`val`) $= 2$ AND collision among others.
           - This requires Count(`val`) = 2.
           - Splits: (1 from left, 0 from right) or (0 from left, 1 from right).
           - Let's analyze "1 from left, 0 from right":
             - Left: 1 `val`, 1 non-`val` ($x$). Ways: $L \times (i-L)$.
             - Right: 2 non-`val` ($y, z$). Ways: $C((n-1-i)-R, 2)$.
             - Invalid if $x=y$, $x=z$, or $y=z$.
             - Instead of subtracting invalid, maybe calculate valid directly?
             - Valid if $x, y, z$ are distinct and $\neq val$.
             - This seems hard because checking distinctness of arbitrary values requires knowing the specific values chosen.
        
        **Wait, is there a property I'm missing?**
        If Count(`val`) = 2, we need the other 3 to be distinct.
        If the array has many duplicates, this is hard.
        But $N=1000$. Can we iterate?
        For a fixed `i`, we have a specific `val`.
        We need to count pairs $(L_{set}, R_{set})$ of size 2 each.
        Maybe iterate over the "other" elements?
        No, $O(N^2)$ per `i` is $O(N^3) \approx 10^9$, too slow.
        
        Let's reconsider the "Count $\ge 3$" case.
        If Count $\ge 3$, it's always valid.
        If Count $= 2$, valid iff others distinct.
        
        Is it possible that the number of "others distinct" cases is small or calculable?
        Actually, if Count(`val`) = 2, the other 3 elements come from the pool of $N-1$ elements excluding `val`.
        If we pick 3 elements from the pool, they are distinct with probability... hard to count exactly without knowing frequencies.
        
        **Alternative Idea**:
        Iterate `i`.
        Count `L` (total left), `R` (total right), `cntL` (left count of `val`), `cntR` (right count of `val`).
        Non-`val` left: $NL = L - cntL$.
        Non-`val` right: $NR = R - cntR$.
        
        Valid scenarios:
        1.  **Count $\ge 3$**:
            *   (2, 0): $C(cntL, 2) \times C(NR, 2)$? No, we need 2 from left, 0 `val` from right? No, 0 `val` from right means 2 non-`val` from right.
                *   Left: 2 `val`. Right: 2 non-`val`.
                *   Ways: $C(cntL, 2) \times C(NR, 2)$.
            *   (1, 1): 1 `val` left, 1 non-`val` left. 1 `val` right, 1 non-`val` right.
                *   Ways: $(cntL \times NL) \times (cntR \times NR)$.
            *   (0, 2): 0 `val` left, 2 non-`val` left. 2 `val` right.
                *   Ways: $C(NL, 2) \times C(cntR, 2)$.
            *   (2, 1): 2 `val` left, 1 non-`val` left. 1 `val` right, 1 non-`val` right.
                *   Ways: $(C(cntL, 2) \times NL) \times (cntR \times NR)$.
            *   (1, 2): 1 `val` left, 1 non-`val` left. 2 `val` right, 1 non-`val` right.
                *   Ways: $(cntL \times NL) \times (C(cntR, 2) \times NR)$.
            *   (2, 2): 2 `val` left, 2 `val` right.
                *   Ways: $C(cntL, 2) \times C(cntR, 2)$.
            *   Sum these up. These cover all cases where total `val` count $\ge 3$.
        
        2.  **Count $= 2$**:
            *   Requires exactly 1 `val` from left and 0 from right (Total 2) OR 0 from left and 1 from right.
            *   **Case 2a**: 1 `val` left, 1 non-`val` left. 0 `val` right, 2 non-`val` right.
                *   Base ways: $(cntL \times NL) \times C(NR, 2)$.
                *   Constraint: The 3 non-`val` elements (1 from left, 2 from right) must be distinct.
                *   Let the non-`val` from left be $x$. Non-`val` from right be $y, z$.
                *   Invalid if $x=y, x=z, y=z$.
                *   This looks like we need to subtract collisions.
                *   Collisions involving $x$:
                    *   $x = y$: Choose $x$ ($NL$ ways), choose $y$ from right such that $y=x$ ($cntR$ ways? No, $y$ is non-`val`. Count of $x$ in right is needed).
                    *   This requires knowing the frequency of every number in the right part.
                *   Collisions between $y, z$:
                    *   $y=z$: Choose pair of identical non-`val` from right.
            *   **Case 2b**: 0 `val` left, 2 non-`val` left. 1 `val` right, 1 non-`val` right.
                *   Symmetric to 2a.
        
        This approach requires knowing the frequency of every number in the left and right partitions.
        We can precompute a frequency map for the whole array, then as we iterate `i`, update the map (remove `nums[i]` from right, add to left).
        With the map, we can calculate:
        - $NL, NR$: Easy.
        - Number of pairs $(y, z)$ in right that are equal: $\sum_{v \neq val} C(freq_R(v), 2)$.
        - Number of pairs $(y, z)$ in right where one is $x$ (specific value): $freq_R(x) \times (freq_R(x) - 1)$? No, we pick 2. If $y=z=x$, ways = $C(freq_R(x), 2)$.
        
        So for Case 2a:
        Total ways = $(cntL \times NL) \times C(NR, 2)$.
        Subtract invalid:
        - $x=y$ (where $y$ is one of the 2 from right):
          Sum over all possible values $v$ (that exist in left non-`val`):
          Ways to pick $x=v$ from left: $1$ (since we pick 1 specific instance? No, we pick 1 index. If there are multiple instances of $v$ in left, we have $NL$ choices? No, $NL$ is count of indices. If we pick index $j$ with value $v$, then we need to pick $y=v$ from right.
          Actually, simpler:
          We pick 1 index from left non-`val` ($NL$ choices). Let its value be $v$.
          We pick 2 indices from right non-`val`.
          Invalid if the set of 2 right indices contains $v$.
          Number of ways to pick 2 from right non-`val` containing at least one $v$:
          Total ways to pick 2 from right non-`val` = $C(NR, 2)$.
          Ways with NO $v$ = $C(NR - freq_R(v), 2)$.
          Ways with $\ge 1$ $v$ = $C(NR, 2) - C(NR - freq_R(v), 2)$.
          Sum this over all $v$ present in left non-`val`.
          Wait, if left has multiple $v$'s, we sum over indices?
          Yes. Sum over each index $j$ in left non-`val`: $(C(NR, 2) - C(NR - freq_R(nums[j]), 2))$.
          This is $O(N)$ per `i` if we iterate left indices. Total $O(N^2)$. Acceptable.
        - $y=z$ (collision in right):
          Sum over all $v$ in right non-`val`: $C(freq_R(v), 2)$.
          Multiply by $(cntL \times NL)$? No, the choice of $x$ doesn't affect $y=z$.
          So subtract: $(cntL \times NL) \times (\sum_{v \neq val} C(freq_R(v), 2))$.
        
        This seems doable in $O(N^2)$ with $O(1)$ or $O(\text{distinct})$ updates.
        Given $N=1000$, even $O(N^2)$ with inner loop over distinct elements (max 1000) is $10^6$ ops, perfectly fine.

## worker: Define a helper for combinations $C(n, 2)$.
The solution involves iterating through each element of the array, treating it as the middle element of a subsequence of size 5. For each middle element `nums[i]`, we calculate the number of valid ways to choose 2 elements from the left part (`0` to `i-1`) and 2 elements from the right part (`i+1` to `n-1`) such that `nums[i]` is the unique mode.

The condition for `nums[i]` to be the unique mode is:
1. It appears at least 3 times in the subsequence.
2. OR it appears exactly 2 times, and all other 3 elements are distinct and different from `nums[i]`.

We categorize the choices based on how many times `nums[i]` is picked from the left (`kL`) and right (`kR`).
- If `kL + kR >= 2`, the count of `nums[i]` is $\ge 3$, which guarantees it is the unique mode. We sum the combinations for all valid `(kL, kR)` pairs.
- If `kL + kR == 1`, the count is 2. We must ensure no other element appears twice. This involves subtracting invalid cases where the non-`nums[i]` elements collide (either two are the same, or one from left matches one from right).

We maintain frequency maps for the left and right partitions to efficiently calculate counts and combinations. The complexity is $O(N^2)$ due to iterating over the array and then over distinct elements (bounded by $N$) for collision checks.

## worker: Implement the `subsequencesWithMiddleMode` functio
The solution iterates through each element of the array, treating it as the potential middle element of a subsequence of size 5. For a fixed middle element `nums[i]`, we need to choose 2 indices from the left part (`0` to `i-1`) and 2 indices from the right part (`i+1` to `n-1`).

The condition for `nums[i]` to be the unique mode is:
1.  It appears at least 3 times in the subsequence.
2.  OR it appears exactly 2 times, and all other 3 elements are distinct and different from `nums[i]`.

The algorithm calculates the number of valid combinations for Case 1 directly by summing over all splits of picking `kL` instances of `nums[i]` from the left and `kR` from the right such that `kL + kR >= 2`.

For Case 2 (exactly 2 instances of `nums[i]`), we calculate the total ways to pick the required elements and then subtract the invalid configurations where another number appears twice. This involves checking for collisions within the left pool, within the right pool, and between the left and right pools. The complexity is $O(N^2)$ because for each of the $N$ elements, we iterate over the distinct elements in the frequency maps (at most $N$).

## worker: Implement the full solution code inside the class,
The solution implements the logic derived in the thought process:
1.  **Iterate through each element** `nums[i]` treating it as the middle element (3rd position) of a subsequence of size 5.
2.  **Maintain Frequency Maps**: `left_counts` tracks elements before `i`, and `right_counts` tracks elements after `i`.
3.  **Case 1 (Count $\ge 3$)**: Calculate combinations where `nums[i]` appears 3, 4, or 5 times. This is done by summing valid splits of picking `kL` instances from the left and `kR` from the right such that `kL + kR >= 2`. The remaining slots are filled with non-`nums[i]` elements. Since the count of `nums[i]` is $\ge 3$, it is guaranteed to be the unique mode.
4.  **Case 2 (Count $= 2$)**: Calculate combinations where `nums[i]` appears exactly 2 times (splits 1+0 or 0+1). Here, we must ensure no other element appears twice. We calculate the total ways and subtract invalid configurations:
    *   Collisions within the right pool (two non-`nums[i]` elements are the same).
    *   Collisions within the left pool (two non-`nums[i]` elements are the same).
    *   Collisions between left and right pools (one non-`nums[i]` from left matches one from right).
5.  **Complexity**: The outer loop runs $N$ times. The inner loops iterate over distinct elements (at most $N$). Thus, the time complexity is $O(N^2)$, which fits within the constraints ($N \le 1000$).
6.  **Modulo Arithmetic**: All additions and subtractions are handled modulo $10^9 + 7$.

## worker: Implement the `subsequencesWithMiddleMode` method 
The solution implements the derived logic:
1.  **Iteration**: Iterates through each element `nums[i]` treating it as the middle element (3rd position) of a subsequence of size 5.
2.  **Frequency Tracking**: Maintains `left_counts` and `right_counts` to efficiently query the number of occurrences of `val` and other numbers in the respective partitions.
3.  **Case 1 (Count $\ge 3$)**: Directly calculates the number of valid subsequences where `val` appears 3, 4, or 5 times. Since `val` appears $\ge 3$ times in a sequence of length 5, it is guaranteed to be the unique mode (max frequency of any other element is 2). This covers splits of picking `kL` instances from the left and `kR` from the right such that `kL + kR >= 2`.
4.  **Case 2 (Count $= 2$)**: Calculates the number of subsequences where `val` appears exactly 2 times. For this to be a unique mode, all other 3 elements must be distinct and different from `val`. The code calculates the total ways to form such subsequences and subtracts invalid configurations:
    *   Collisions within the right pool (two non-`val` elements are the same).
    *   Collisions within the left pool (two non-`val` elements are the same).
    *   Collisions between left and right pools (one non-`val` from left matches one from right).
5.  **Complexity**: The outer loop runs $N$ times. The inner loops iterate over distinct elements in the frequency maps (at most $N$). Thus, the time complexity is $O(N^2)$, which fits within the constraints ($N \le 1000$).
6.  **Modulo Arithmetic**: All additions and subtractions are handled modulo $10^9 + 7$.

## worker: finalize
The solution iterates through each element of the array, treating it as the potential middle element (3rd position) of a subsequence of size 5. For a fixed middle element `nums[i]`, we need to choose 2 indices from the left part (`0` to `i-1`) and 2 indices from the right part (`i+1` to `n-1`).

The condition for `nums[i]` to be the unique mode is:
1.  It appears at least 3 times in the subsequence.
2.  OR it appears exactly 2 times, and all other 3 elements are distinct and different from `nums[i]`.

The algorithm calculates the number of valid combinations for Case 1 directly by summing over all splits of picking `kL` instances of `nums[i]` from the left and `kR` from the right such that `kL + kR >= 2`. The remaining slots are filled with non-`nums[i]` elements. Since the count of `nums[i]` is $\ge 3$, it is guaranteed to be the unique mode (max frequency of any other element is 2).

For Case 2 (exactly 2 instances of `nums[i]`), we calculate the total ways to pick the required elements and then subtract the invalid configurations where another number appears twice. This involves checking for collisions within the left pool, within the right pool, and between the left and right pools. The complexity is $O(N^2)$ because for each of the $N$ elements, we iterate over the distinct elements in the frequency maps (at most $N$).
