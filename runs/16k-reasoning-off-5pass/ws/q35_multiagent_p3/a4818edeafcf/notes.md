
## ideation
The problem requires splitting an array $A$ of length $N$ into three non-empty contiguous subarrays to maximize the sum of the counts of distinct integers in each subarray.
Constraints are $N \le 3 \times 10^5$, requiring an $O(N)$ or $O(N \log N)$ solution.

Key observations:
1. Let the split points be after index $i$ and after index $j$ (1-indexed), where $1 \le i < j \le N-1$.
   - Subarray 1: $A[1 \dots i]$
   - Subarray 2: $A[i+1 \dots j]$
   - Subarray 3: $A[j+1 \dots N]$
   - Objective: Maximize $D(1, i) + D(i+1, j) + D(j+1, N)$, where $D(l, r)$ is the number of distinct elements in $A[l \dots r]$.

2. We can precompute:
   - `pre[k]`: Number of distinct elements in $A[1 \dots k]$.
   - `suf[k]`: Number of distinct elements in $A[k \dots N]$.

3. The term $D(j+1, N)$ is simply `suf[j+1]`.
4. The term $D(1, i)$ is simply `pre[i]`.
5. The middle term $D(i+1, j)$ is the tricky part.
   For a fixed right cut $j$, we want to maximize $pre[i] + D(i+1, j)$ for $1 \le i \le j-1$.
   Let $Val_j(i) = pre[i] + D(i+1, j)$.
   As we increment $j$ to $j+1$, the middle segment expands to include $A[j+1]$.
   $D(i+1, j+1) = D(i+1, j) + 1$ if $A[j+1]$ does not appear in $A[i+1 \dots j]$.
   $D(i+1, j+1) = D(i+1, j)$ if $A[j+1]$ appears in $A[i+1 \dots j]$.
   
   Let $last\_pos[x]$ be the last index where value $x$ appeared before the current position.
   When we move from $j$ to $j+1$, let $x = A[j+1]$.
   If $x$ has appeared before at index $p = last\_pos[x]$, then for any $i$ such that the middle segment $A[i+1 \dots j]$ includes $p$ (i.e., $i+1 \le p \implies i \le p$), the element $x$ is already present in the middle segment, so the distinct count doesn't increase.
   For $i$ such that the middle segment does *not* include $p$ (i.e., $i < p$), the element $x$ is new to the middle segment, so the distinct count increases by 1.
   Note: The middle segment is $A[i+1 \dots j]$. It contains index $p$ if $i+1 \le p \le j$. Since we are adding $A[j+1]$, we care if $x$ was in $A[i+1 \dots j]$. The last occurrence of $x$ in $A[1 \dots j]$ is at $p$. So $x$ is in $A[i+1 \dots j]$ if and only if $i+1 \le p$, i.e., $i \le p-1$.
   Wait, if $i = p-1$, the segment is $A[p \dots j]$, which includes $p$. So $x$ is present.
   If $i = p$, the segment is $A[p+1 \dots j]$, which does not include $p$. So $x$ is NOT present (assuming $p$ was the last occurrence).
   So, for $i < p$, the distinct count increases by 1. For $i \ge p$, it stays the same.
   
   Therefore, when moving from $j$ to $j+1$:
   - Update $last\_pos[A[j+1]]$ to $j+1$ (after processing).
   - Let $p$ be the previous $last\_pos[A[j+1]]$.
   - For all $i$ in range $[1, p-1]$, $Val_{j+1}(i) = Val_j(i) + 1$.
   - For $i$ in range $[p, j]$, $Val_{j+1}(i) = Val_j(i)$.
   
   We need a data structure that supports:
   - Range Add: Add 1 to $Val[i]$ for $i \in [1, p-1]$.
   - Range Max Query: Find $\max_{i \in [1, j-1]} Val[i]$.
   
   A Segment Tree is suitable for this.
   - Initialize the segment tree with $Val_1(i) = pre[i] + D(i+1, 1)$. But the middle segment must be non-empty, so $j$ starts from 2.
   - For $j=2$, middle is $A[i+1 \dots 2]$. $i$ can only be 1.
     $Val_2(1) = pre[1] + D(2, 2)$.
   - We iterate $j$ from 2 to $N-1$.
   - At each step $j$, we query the max in range $[1, j-1]$.
   - Then we prepare for $j+1$ by updating the segment tree based on $A[j+1]$.
   
   Wait, the update happens when we extend the middle segment from ending at $j$ to ending at $j+1$.
   So, after computing the answer for cut $j$ (where middle ends at $j$), we update the structure to reflect the middle ending at $j+1$.
   
   Algorithm:
   1. Precompute `pre` and `suf`.
   2. Initialize Segment Tree of size $N$.
      The value at index $i$ in the segment tree will store $pre[i] + D(i+1, \text{current\_end})$.
      Initially, let current\_end = 1? No, middle segment must have at least one element.
      Let's start with $j=2$. Middle segment ends at 2.
      Possible $i$: 1.
      $Val(1) = pre[1] + D(2, 2)$.
      Set $ST[1] = pre[1] + 1$ (since $A[2]$ is distinct in itself).
   3. Iterate $j$ from 2 to $N-1$:
      a. Query max in $ST[1 \dots j-1]$. Let this be $max\_mid$.
      b. Current total = $max\_mid + suf[j+1]$.
      c. Update global answer.
      d. Prepare for next $j$ (which will be $j+1$).
         We need to update $ST$ to reflect middle segment ending at $j+1$.
         Let $x = A[j+1]$.
         Let $p = last\_pos[x]$.
         If $p$ exists:
             Range Add 1 to $ST[1 \dots p-1]$.
         Update $last\_pos[x] = j+1$.
         Also, we need to initialize $ST[j]$ for the new potential cut $i=j$?
         When middle ends at $j+1$, $i$ can go up to $j$.
         The new term for $i=j$ is $pre[j] + D(j+1, j+1) = pre[j] + 1$.
         So we set $ST[j] = pre[j] + 1$.
         Note: The range update $[1, p-1]$ applies to existing $i$. The new $i=j$ is a new leaf.
         
   4. Edge cases: $N=3$. Loop $j$ from 2 to 2.
      $j=2$: Query $ST[1 \dots 1]$. Update ans. Update for $j=3$ (but loop ends).

   Complexity: $O(N \log N)$ due to Segment Tree operations.

## worker: Implement the Segment Tree with Range Add and Rang
The solution uses a Segment Tree with lazy propagation to efficiently handle range updates and range maximum queries.
1. **Precomputation**: We compute `pre[i]` (distinct count in $A[0 \dots i-1]$) and `suf[i]` (distinct count in $A[i \dots N-1]$) in $O(N)$.
2. **Segment Tree**: The tree maintains values $V_i = \text{pre}[i+1] + \text{distinct}(A[i+1 \dots \text{current\_end}])$ for each possible left cut position $i$.
3. **Iteration**: We iterate through the right cut position $j$ (end of the middle segment). For each $j$, we query the maximum $V_i$ for $i < j$ and add `suf[j+1]` to get the total distinct count for that split.
4. **Update**: When moving from $j$ to $j+1$, the middle segment extends to include $A[j+1]$. If $A[j+1]$ was previously seen at index $p$, then for all $i < p$, the element $A[j+1]$ is new to the middle segment, so $V_i$ increases by 1. For $i \ge p$, it's already present, so $V_i$ doesn't change. This is a range add operation on the segment tree. We also add a new leaf for the new possible cut $i=j$.
5. **Complexity**: Precomputation is $O(N)$. The loop runs $N$ times, with each iteration involving $O(\log N)$ segment tree operations. Total time complexity is $O(N \log N)$, which fits within the constraints.
