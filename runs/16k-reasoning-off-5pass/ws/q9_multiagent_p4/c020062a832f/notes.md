
## ideation
**Core Difficulty**: Calculating the inversion number for $M$ different sequences where each element is shifted by $k$ modulo $M$. A naive simulation would take $O(N \cdot M \log N)$ or $O(N \cdot M)$, which is too slow given $N, M \le 2 \times 10^5$. The total operations would exceed $10^{10}$.

**Key Insight**:
1.  **Initial State**: Calculate the inversion count for $k=0$ using a Fenwick Tree (Binary Indexed Tree) or Merge Sort in $O(N \log N)$.
2.  **Transition**: When moving from $k$ to $k+1$, elements $A_i$ where $A_i + k < M$ simply increase their value by 1. Elements where $A_i + k \ge M$ wrap around to $A_i + k - M$.
3.  **Change in Inversions**:
    *   For elements that **do not wrap**: Their relative order with other non-wrapping elements remains unchanged. Their relative order with wrapping elements changes, but since all non-wrapping values are in range $[k+1, M-1]$ and wrapping values become $[0, k]$, the set of values is just shifted. Actually, a better way to view the transition is:
        *   Let $S$ be the set of indices that wrap at step $k \to k+1$. These are indices where $A_i = M - 1 - k$. Wait, the condition for wrapping at step $k$ (to get $B$ for $k$) is $A_i + k \ge M \implies A_i \ge M-k$.
        *   Let's re-evaluate the transition from $k$ to $k+1$.
        *   Sequence $B^{(k)}$ has values $(A_i + k) \% M$.
        *   Sequence $B^{(k+1)}$ has values $(A_i + k + 1) \% M$.
        *   For an index $i$:
            *   If $A_i + k < M - 1$, then $B^{(k)}_i = A_i + k$ and $B^{(k+1)}_i = A_i + k + 1$. The value increases by 1.
            *   If $A_i + k = M - 1$, then $B^{(k)}_i = M - 1$ and $B^{(k+1)}_i = 0$. The value drops from $M-1$ to $0$.
    *   **Effect on Inversions**:
        *   When a value increases by 1 (non-wrap): It might gain inversions with elements to its left that are now smaller, and lose inversions with elements to its right that are now smaller? No.
        *   Let's look at pairs $(i, j)$ with $i < j$.
        *   **Case 1: Neither $i$ nor $j$ wraps.** $B^{(k+1)}_i = B^{(k)}_i + 1$, $B^{(k+1)}_j = B^{(k)}_j + 1$. The inequality $B^{(k+1)}_i > B^{(k+1)}_j$ is equivalent to $B^{(k)}_i > B^{(k)}_j$. No change.
        *   **Case 2: Both $i$ and $j$ wrap.** $B^{(k+1)}_i = B^{(k)}_i - (M-1)$, $B^{(k+1)}_j = B^{(k)}_j - (M-1)$. The inequality is preserved. No change.
        *   **Case 3: $i$ wraps, $j$ does not.** $B^{(k+1)}_i = 0$ (assuming it was $M-1$), $B^{(k+1)}_j = B^{(k)}_j + 1$.
            *   Previously ($k$): $B^{(k)}_i = M-1$, $B^{(k)}_j < M-1$. So $B^{(k)}_i > B^{(k)}_j$ was TRUE.
            *   Now ($k+1$): $0 > \text{something} \ge 1$ is FALSE.
            *   Change: Inversion count decreases by 1 for every such pair where $i < j$ and $i$ wraps.
        *   **Case 4: $i$ does not wrap, $j$ wraps.** $B^{(k+1)}_i = B^{(k)}_i + 1$, $B^{(k+1)}_j = 0$.
            *   Previously ($k$): $B^{(k)}_i < M-1$, $B^{(k)}_j = M-1$. So $B^{(k)}_i > B^{(k)}_j$ was FALSE.
            *   Now ($k+1$): $\text{something} \ge 1 > 0$ is TRUE.
            *   Change: Inversion count increases by 1 for every such pair where $i < j$ and $j$ wraps.

    *   **Simplification**: At step $k \to k+1$, only elements with value $M-1-k$ in the current sequence $B^{(k)}$ will wrap (become 0). Let $S_k$ be the set of indices $i$ such that $B^{(k)}_i = M-1$.
        *   For each $i \in S_k$:
            *   Count $j > i$ such that $B^{(k)}_j < M-1$. These pairs $(i, j)$ lose an inversion.
            *   Count $j < i$ such that $B^{(k)}_j < M-1$. These pairs $(j, i)$ gain an inversion (since $B^{(k)}_j < M-1$ and new $B^{(k+1)}_i = 0$, so $B^{(k+1)}_j > B^{(k+1)}_i$).
        *   Wait, is it just elements equal to $M-1$?
            *   Yes, because only $x = M-1$ becomes $0$. Others become $x+1$.
            *   The relative order of non-wrapping elements is preserved relative to each other.
            *   The relative order of wrapping elements relative to each other is preserved (all become $0, 1, \dots$? No, they all become $0$ if they were $M-1$? No, only those with value $M-1$ become $0$. Those with value $M-2$ become $M-1$, etc. Only one specific value wraps to 0).
            *   Actually, at step $k$, the values are $(A_i+k)\%M$. The elements that wrap at step $k \to k+1$ are those where $(A_i+k)\%M = M-1$.
            *   Let $cnt\_small\_right$ be the number of elements to the right of $i$ that are NOT equal to $M-1$.
            *   Let $cnt\_small\_left$ be the number of elements to the left of $i$ that are NOT equal to $M-1$.
            *   Actually, since only $M-1$ wraps to $0$, and everything else shifts up:
                *   Pairs involving two non-wrapping: No change.
                *   Pairs involving two wrapping: No change (both shift or both wrap? No, only one value wraps).
                *   Pairs $(i, j)$ with $i < j$:
                    *   If $i$ wraps, $j$ doesn't: $i$ goes $M-1 \to 0$, $j$ goes $v \to v+1$. Inversion $M-1 > v$ (True) becomes $0 > v+1$ (False). Loss of 1.
                    *   If $i$ doesn't, $j$ wraps: $i$ goes $v \to v+1$, $j$ goes $M-1 \to 0$. Inversion $v > M-1$ (False) becomes $v+1 > 0$ (True). Gain of 1.
            *   So, for each $i$ such that $B^{(k)}_i = M-1$:
                *   Subtract (number of $j > i$ where $B^{(k)}_j \neq M-1$).
                *   Add (number of $j < i$ where $B^{(k)}_j \neq M-1$).
            *   Note: "Not equal to $M-1$" is equivalent to "Not wrapping".
            *   Let $Total = N$. Let $Count\_MMinus1$ be the number of elements equal to $M-1$.
            *   For a specific $i$ with $B^{(k)}_i = M-1$:
                *   $j > i$ and $B^{(k)}_j \neq M-1$: This is $(N - i) - (\text{count of } M-1 \text{ in } i+1 \dots N)$.
                *   $j < i$ and $B^{(k)}_j \neq M-1$: This is $(i - 1) - (\text{count of } M-1 \text{ in } 1 \dots i-1)$.
            *   We need to efficiently query the count of $M-1$s in ranges. We can precompute positions of all $M-1$s or use a Fenwick tree. Since the set of $M-1$s changes every step (values shift), we need to track where the $M-1$s are.
            *   Actually, the values shift cyclically. The element with value $v$ at step $k$ will have value $v+1$ at step $k+1$. The element with value $M-1$ at step $k$ becomes $0$ at step $k+1$. The element with value $0$ at step $k$ becomes $1$.
            *   We can maintain the positions of all values. But we only care about the positions of the current $M-1$s.
            *   Algorithm:
                1. Compute initial inversions for $k=0$.
                2. Identify all indices $i$ where $A_i = M-1$. These are the ones that wrap at $k=0 \to 1$.
                3. For each such $i$, update the inversion count based on the number of non-$M-1$ elements to left and right.
                4. Update the data structure: Remove $i$ from the set of "non-$M-1$" elements? No.
                5. Better approach: Maintain a Fenwick tree that stores the positions of elements that are **NOT** equal to $M-1$ in the current configuration.
                6. Initially, build a BIT with 1 at position $i$ if $A_i \neq M-1$.
                7. When moving $k \to k+1$:
                   - Identify indices $i$ where $B^{(k)}_i = M-1$. These are indices where $A_i = (M-1-k) \% M$.
                   - For each such $i$:
                     - $loss = \text{query\_BIT}(N) - \text{query\_BIT}(i)$ (Count of non-M-1 to the right)
                     - $gain = \text{query\_BIT}(i-1)$ (Count of non-M-1 to the left)
                     - $ans = ans - loss + gain$
                     - Remove $i$ from BIT (set to 0) because it is no longer "non-M-1" (it becomes 0, which is not $M-1$ unless $M=1$, but if $M=1$ there are no inversions anyway). Wait, if it becomes 0, it is definitely not $M-1$ (for $M>1$). So it stays in the "non-M-1" set?
                     - **Correction**: The condition for the BIT is "elements that do NOT wrap in the NEXT step".
                     - In step $k \to k+1$, elements with value $M-1$ wrap. Elements with value $< M-1$ become $+1$, so they are still $< M-1$ (unless they were $M-1$, which we handled).
                     - So, in the new state $k+1$, the elements that will wrap are those with value $M-1$.
                     - The elements that did NOT wrap in $k \to k+1$ are those that had value $< M-1$. In the new state, they have value $< M-1$ (shifted up by 1, max becomes $M-2$).
                     - The elements that DID wrap in $k \to k+1$ (had value $M-1$) now have value $0$. In the new state, $0 < M-1$ (for $M>1$). So they are also "non-wrapping" for the next step?
                     - **Wait**, the logic for the update depends on the state at $k$.
                     - Let's redefine the BIT content: The BIT should store 1 at index $i$ if $B^{(k)}_i \neq M-1$.
                     - At step $k$, we identify all $i$ where $B^{(k)}_i = M-1$. Let this set be $W$.
                     - For each $i \in W$:
                       - $loss = (\text{total non-M-1}) - (\text{non-M-1 in } 1..i)$
                       - $gain = (\text{non-M-1 in } 1..i-1)$
                       - $ans += gain - loss$
                     - After processing all $i \in W$, we need to prepare for step $k+1$.
                     - In step $k+1$, the values are shifted. The elements that were $M-1$ become $0$. The elements that were $< M-1$ become $+1$.
                     - Who are the elements equal to $M-1$ in step $k+1$? They are the elements that were equal to $M-2$ in step $k$.
                     - So, to prepare the BIT for step $k+1$:
                       - We need to mark elements that were $M-2$ as "active" (non-M-1) for the calculation of step $k+1 \to k+2$?
                       - No, the BIT at the start of step $k$ (before calculating transition $k \to k+1$) should represent the set of indices $i$ where $B^{(k)}_i \neq M-1$.
                       - Initially ($k=0$): Mark all $i$ where $A_i \neq M-1$.
                       - Transition $0 \to 1$:
                         - Find $i$ where $A_i = M-1$.
                         - Update ans.
                         - Now, for $k=1$, we need the BIT to represent $B^{(1)}_i \neq M-1$.
                         - $B^{(1)}_i = (A_i+1)\%M$.
                         - $B^{(1)}_i = M-1 \iff A_i+1 \equiv M-1 \pmod M \iff A_i = M-2$.
                         - So, in the new BIT for $k=1$, we need 1s at indices where $A_i = M-2$, and 0s elsewhere?
                         - No. The BIT must reflect the current configuration $B^{(k)}$.
                         - At $k=0$, BIT has 1s where $A_i \neq M-1$.
                         - After processing $k=0 \to 1$, the configuration changes.
                         - The elements that were $M-1$ become $0$. The elements that were $x < M-1$ become $x+1$.
                         - The set of indices where $B^{(1)}_i \neq M-1$ is ALL indices EXCEPT those where $B^{(1)}_i = M-1$.
                         - $B^{(1)}_i = M-1 \iff A_i = M-2$.
                         - So for the next step, we need the BIT to have 0s at indices where $A_i = M-2$ and 1s everywhere else.
                         - But we just processed indices where $A_i = M-1$.
                         - This suggests we can just maintain the BIT dynamically.
                         - **Strategy**:
                           1. Calculate initial inversions.
                           2. Build BIT with 1 at $i$ if $A_i \neq M-1$.
                           3. Loop $k$ from $0$ to $M-2$ (to compute answers for $k+1$):
                              - Identify indices $i$ where $A_i = (M-1-k) \% M$. These are the ones with value $M-1$ in current $B^{(k)}$.
                              - For each such $i$:
                                - $loss = \text{query}(N) - \text{query}(i)$
                                - $gain = \text{query}(i-1)$
                                - $ans += gain - loss$
                              - Update BIT: Set position $i$ to 0?
                                - Why 0? Because in the current state $B^{(k)}$, these $i$ are $M-1$. In the BIT definition "1 if $\neq M-1$", they should be 0.
                                - What about other elements?
                                - Elements that were $x \neq M-1$ (so BIT=1) remain $\neq M-1$ in $B^{(k)}$? Yes, because only $M-1$ wraps.
                                - So the BIT state is consistent: 1 if current value $\neq M-1$, 0 if current value $= M-1$.
                                - After updating $ans$, we move to $k+1$.
                                - The values shift. The element that was $M-1$ becomes $0$. The element that was $M-2$ becomes $M-1$.
                                - So for the next iteration ($k+1$), the element that was $M-2$ (which currently has BIT=1) will now be $M-1$ (so BIT should become 0).
                                - The element that was $M-1$ (currently BIT=0) becomes $0$ (so BIT should remain 0, since $0 \neq M-1$).
                                - The element that was $x < M-2$ (BIT=1) becomes $x+1 \neq M-1$ (BIT remains 1).
                                - **Crucial Step**: Before moving to $k+1$, we must update the BIT to reflect the new "non-M-1" status.
                                - Specifically, the indices $i$ where $A_i = M-2$ (which are currently 1 in BIT) must be set to 0, because in the next step they will be $M-1$.
                                - Wait, do we need to do this manually?
                                - The loop identifies $i$ where $A_i = M-1-k$.
                                - At $k=0$, we process $A_i = M-1$.
                                - At $k=1$, we process $A_i = M-2$.
                                - So in each step $k$, we identify the set $S_k = \{i \mid A_i = (M-1-k)\%M\}$.
                                - We use the BIT to calculate changes.
                                - Then, we must ensure the BIT is ready for $k+1$.
                                - In the BIT, we want 1 if $B^{(k)}_i \neq M-1$.
                                - After the shift to $B^{(k+1)}$, we want 1 if $B^{(k+1)}_i \neq M-1$.
                                - $B^{(k+1)}_i = M-1 \iff B^{(k)}_i = M-2$.
                                - So, in the BIT (which currently has 1s for $B^{(k)}_i \neq M-1$), the positions where $B^{(k)}_i = M-2$ are currently 1. They need to become 0 for the next step.
                                - The positions where $B^{(k)}_i = M-1$ are currently 0. They stay 0 (since $0 \neq M-1$).
                                - So, the only update needed to the BIT between steps is: **Set to 0 all indices $i$ where $B^{(k)}_i = M-2$**.
                                - Note: $B^{(k)}_i = M-2 \iff A_i = M-3-k$.
                                - So, at the end of step $k$, we find all $i$ where $A_i = M-3-k$ and set BIT[i] = 0.
                                - Wait, this seems complicated to track indices.
                                - Alternative: Just maintain the BIT such that it always has 1 at $i$ if $B^{(k)}_i \neq M-1$.
                                - Initially ($k=0$): BIT[i] = 1 if $A_i \neq M-1$.
                                - Step $k$:
                                  1. Identify $i$ where $B^{(k)}_i = M-1$. These are $i$ where $A_i = M-1-k$.
                                  2. Calculate $\Delta$ using BIT.
                                  3. Update BIT: For these $i$, they are $M-1$, so they are already 0 in BIT. No change needed for them.
                                  4. Prepare for $k+1$: We need BIT to have 0 at $i$ if $B^{(k+1)}_i = M-1$.
                                     $B^{(k+1)}_i = M-1 \iff B^{(k)}_i = M-2$.
                                     So we need to set BIT[i] = 0 for all $i$ where $B^{(k)}_i = M-2$.
                                     These are $i$ where $A_i = M-2-k$.
                                  5. So, after step $k$, iterate $i$ where $A_i = M-2-k$ and update BIT[i] = 0.
                                - This works. We can pre-group indices by value $A_i$.

## worker: Implement the solution logic: Read inputs, handle 
1.  **Algorithm**: The solution uses a Fenwick Tree (BIT) to efficiently calculate the initial inversion count and then updates it incrementally as $k$ increases.
2.  **Initial State**: For $k=0$, we compute the inversion count in $O(N \log N)$ using a standard BIT approach.
3.  **Transition**: When moving from $k$ to $k+1$, only elements with value $M-1$ in the current sequence $B^{(k)}$ wrap around to $0$.
    *   For each such element at index $i$:
        *   It loses inversions with all elements to its right that are not $M-1$ (since $M-1 > x$ becomes $0 > x+1$ which is false).
        *   It gains inversions with all elements to its left that are not $M-1$ (since $x < M-1$ becomes $x+1 > 0$ which is true).
    *   The change in inversion count for an element $i$ is `gain - loss`, where `gain` is the count of non-$M-1$ elements to the left, and `loss` is the count of non-$M-1$ elements to the right.
4.  **Data Structure**: We maintain a BIT that stores `1` at index $i$ if $B^{(k)}_i \neq M-1$, and `0` otherwise. This allows us to query the counts of non-$M-1$ elements to the left or right in $O(\log N)$.
5.  **Maintenance**: After processing the wrap-around for step $k$, we prepare the BIT for step $k+1$. The elements that will become $M-1$ in the next step are those that were $M-2$ in the current step. We update the BIT by setting their values to `0`.
6.  **Complexity**:
    *   Initial inversion count: $O(N \log N)$.
    *   Loop runs $M$ times.
    *   Inside the loop, we iterate over elements wrapping around. In the worst case, all elements wrap, but each element wraps exactly once over the entire process (since values cycle $0 \to 1 \to \dots \to M-1 \to 0$). Thus, the total number of updates to the BIT across all $k$ is $O(N)$.
    *   Total time complexity: $O(N \log N + M \log N)$ (due to BIT operations). Given $N, M \le 2 \times 10^5$, this fits well within the time limit.
7.  **Edge Cases**: Handled $M=1$ explicitly. Constraints $A_i < M$ are respected.

## worker: Run the code against the provided sample inputs to
The code implements the logic derived in the thought process:
1.  **Initial Calculation**: Computes the inversion count for $k=0$ using a Fenwick Tree (BIT) in $O(N \log N)$.
2.  **State Maintenance**: Maintains a BIT where `bit[i] = 1` if the current element $B^{(k)}_i \neq M-1$, and `0` otherwise. This allows $O(\log N)$ queries for the number of "non-wrapping" elements to the left or right of a specific index.
3.  **Transition Logic**:
    *   For each step $k \to k+1$, elements with value $M-1$ wrap around to $0$.
    *   For each such element at index $i$, the change in inversions is calculated as `(count of non-M-1 to left) - (count of non-M-1 to right)`.
    *   The BIT is updated to reflect the new state for $k+1$. Specifically, elements that were $M-2$ in step $k$ become $M-1$ in step $k+1$, so their BIT value is set to $0$.
4.  **Efficiency**: By grouping indices by value in the `pos` array, we efficiently access the indices that wrap or need updating. The total complexity is $O(N \log N + M \log N)$, which fits within the constraints.

## worker: Run the code against Sample 1, Sample 2, and Sampl
The code implements the logic derived in the thought process:
1.  **Initial Calculation**: Computes the inversion count for $k=0$ using a Fenwick Tree (BIT) in $O(N \log N)$.
2.  **State Maintenance**: Maintains a BIT where `bit[i] = 1` if the current element $B^{(k)}_i \neq M-1$, and `0` otherwise. This allows $O(\log N)$ queries for the number of "non-wrapping" elements to the left or right of a specific index.
3.  **Transition Logic**:
    *   For each step $k \to k+1$, elements with value $M-1$ wrap around to $0$.
    *   For each such element at index $i$, the change in inversions is calculated as `(count of non-M-1 to left) - (count of non-M-1 to right)`.
    *   The BIT is updated to reflect the new state for $k+1$. Specifically, elements that were $M-2$ in step $k$ become $M-1$ in step $k+1$, so their BIT value is set to $0$.
4.  **Efficiency**: By grouping indices by value in the `pos` array, we efficiently access the indices that wrap or need updating. The total complexity is $O(N \log N + M \log N)$, which fits within the constraints.

## worker: finalize
The solution implements an $O(N \log N + M \log N)$ algorithm.
1.  **Initial Calculation**: Computes the inversion count for $k=0$ using a Fenwick Tree (BIT) in $O(N \log N)$.
2.  **State Maintenance**: Maintains a BIT where `bit[i] = 1` if the current element $B^{(k)}_i \neq M-1$, and `0` otherwise. This allows $O(\log N)$ queries for the number of "non-wrapping" elements to the left or right of a specific index.
3.  **Transition Logic**:
    *   For each step $k \to k+1$, elements with value $M-1$ wrap around to $0$.
    *   For each such element at index $i$, the change in inversions is calculated as `(count of non-M-1 to left) - (count of non-M-1 to right)`.
    *   The BIT is updated to reflect the new state for $k+1$. Specifically, elements that were $M-2$ in step $k$ become $M-1$ in step $k+1$, so their BIT value is set to $0$.
4.  **Efficiency**: By grouping indices by value in the `pos` array, we efficiently access the indices that wrap or need updating. The total complexity is $O(N \log N + M \log N)$, which fits within the constraints.
