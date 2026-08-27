
## ideation
The core difficulty lies in efficiently updating the inversion count as we transition from $k$ to $k+1$. A naive recomputation for each $k$ would be $O(M \cdot N \log N)$ or $O(M \cdot N)$, which is too slow given $N, M \le 2 \times 10^5$.

The key insight is that the transformation $B_i = (A_i + k) \pmod M$ preserves the relative order of pairs $(A_i, A_j)$ unless one of the values "wraps around" from $M-1$ to $0$. Specifically, when moving from $k$ to $k+1$, only the elements that are currently equal to $M-1$ (which correspond to original values $A_i = (M - 1 - k) \pmod M$) change their relative standing with respect to all other elements.

Let $v_k = (M - 1 - k) \pmod M$. The elements with original value $v_k$ wrap around to 0. All other elements increase by 1.
- For a pair where neither wraps, the relative order is unchanged ($x < y \implies x+1 < y+1$).
- For a pair where both wrap, they both become 0, so they are equal (no inversion change, as inversions require strict inequality).
- For a pair where one wraps and the other doesn't:
  - If the wrapping element is at index $i$ and the non-wrapping element is at index $j$:
    - If $i < j$: Originally $A_i = M-1 > A_j$. After wrap, $B_i = 0 < B_j$. We lose 1 inversion.
    - If $i > j$: Originally $A_j < A_i = M-1$. After wrap, $B_j > B_i = 0$. We gain 1 inversion.

Thus, the change in inversion count when moving from $k$ to $k+1$ is:
$\Delta = (\text{# of non-wrapping elements to the left of wrapping elements}) - (\text{# of non-wrapping elements to the right of wrapping elements})$.

More precisely, for each wrapping element at index $idx$, let $L$ be the number of non-wrapping elements to its left and $R$ be the number of non-wrapping elements to its right. The contribution to the change is $R - L$.
Summing over all wrapping elements:
$\Delta = \sum_{i \in Wrapping} (R_i - L_i)$.

We can compute $L_i$ and $R_i$ efficiently if we know the positions of all elements with value $v_k$.
Let $P$ be the sorted list of indices where $A_i = v_k$. Let $cnt = |P|$.
For the $m$-th element in $P$ (0-indexed) at index $idx = P[m]$:
- Number of wrapping elements to its left is $m$.
- Number of wrapping elements to its right is $cnt - 1 - m$.
- Total elements to left is $idx$. So $L_i = idx - m$.
- Total elements to right is $N - 1 - idx$. So $R_i = (N - 1 - idx) - (cnt - 1 - m) = N - idx - cnt + m$.
- Contribution: $R_i - L_i = (N - idx - cnt + m) - (idx - m) = N - cnt - 2 \cdot idx + 2m$.

We can precompute the list of indices for each value $0 \dots M-1$. Then for each $k$, we identify $v_k$, retrieve its indices, and compute the sum in $O(cnt)$ time. The total time will be $O(N + M + \sum cnt) = O(N + M)$, which is efficient.

Pitfalls:
1. Initial inversion count must be computed correctly using a Fenwick tree or merge sort.
2. The modulo arithmetic for $v_k$ must handle negative results correctly (though $M-1-k$ can be negative, in Python `%` handles it, but logically we want $(M - 1 - k) \% M$).
3. Ensure that the indices are 0-based or 1-based consistently. The problem uses 1-based indexing for description, but arrays are 0-based in implementation. The logic for $L_i$ and $R_i$ depends on the count of elements, which is independent of 0/1-based indexing as long as it's consistent.
4. Large inputs require fast I/O.

## worker: (none)
1. **Initial Inversion Count**: Computed using a Fenwick Tree (BIT) in $O(N \log M)$ time. This is efficient given $N, M \le 2 \times 10^5$.
2. **Transition Logic**: The key insight is that moving from $k$ to $k+1$ only affects pairs involving elements that wrap around (value $M-1 \to 0$). Elements that don't wrap maintain their relative order. Elements that both wrap become equal (0), so no inversion change between them.
3. **Delta Calculation**: For each wrapping element at index `idx`, the change in inversions is determined by how many non-wrapping elements are to its left vs right. Specifically, each non-wrapping element to the right contributes $+1$ (since the wrapping element drops below it), and each non-wrapping element to the left contributes $-1$ (since the wrapping element drops below it, but it was already above them? No, wait. Let's re-verify).
   - Pair $(i, j)$ with $i < j$.
   - If $A_i$ wraps and $A_j$ doesn't:
     - Before: $A_i = M-1, A_j < M-1 \implies A_i > A_j$ (Inversion).
     - After: $B_i = 0, B_j = A_j + 1 \ge 1 \implies B_i < B_j$ (Not Inversion).
     - Change: $-1$.
     - Here $i$ is the wrapping element, $j$ is to the right. So each non-wrapping element to the right of a wrapping element causes a loss of 1 inversion.
   - If $A_j$ wraps and $A_i$ doesn't ($i < j$):
     - Before: $A_i < M-1, A_j = M-1 \implies A_i < A_j$ (Not Inversion).
     - After: $B_i = A_i + 1 \ge 1, B_j = 0 \implies B_i > B_j$ (Inversion).
     - Change: $+1$.
     - Here $j$ is the wrapping element, $i$ is to the left. So each non-wrapping element to the left of a wrapping element causes a gain of 1 inversion.
   - Total Change = (Sum of non-wrapping elements to the left of all wrapping elements) - (Sum of non-wrapping elements to the right of all wrapping elements).
   - My formula derived: $R_i - L_i$ for each wrapping element $i$.
     - $L_i$ = non-wrapping to left.
     - $R_i$ = non-wrapping to right.
     - Contribution = $R_i - L_i$.
     - Summing this gives: $\sum R_i - \sum L_i$.
     - $\sum R_i$ is total non-wrapping to right of all wrapping elements.
     - $\sum L_i$ is total non-wrapping to left of all wrapping elements.
     - So Change = $\sum R_i - \sum L_i$.
     - This matches the logic: Gain from left neighbors, Loss from right neighbors.
     - Formula: $R_i - L_i = (N - idx - cnt + m) - (idx - m) = N - cnt - 2 \cdot idx + 2m$.
     - This is correct.
4. **Complexity**:
   - Initial inversion count: $O(N \log M)$.
   - Precomputing positions: $O(N)$.
   - Loop over $k$: Each element is processed exactly once as a "wrapping" element across all $k$. Total work is $O(N)$.
   - Overall time complexity: $O(N \log M + N) = O(N \log M)$.
   - Space complexity: $O(N + M)$ for storing positions and BIT.
