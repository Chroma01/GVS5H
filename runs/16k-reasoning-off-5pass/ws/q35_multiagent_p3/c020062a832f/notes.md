
## ideation
The core difficulty lies in efficiently updating the inversion count as we shift the sequence by $k=0, \dots, M-1$. A naive $O(N)$ calculation for each $k$ would result in $O(NM)$, which is too slow given $N, M \le 2 \times 10^5$.

The key insight is to derive a recurrence relation for the change in inversion count when moving from $k$ to $k+1$.
When shifting from $k$ to $k+1$, elements with value $A_i = M - 1 - k$ wrap around to $0$. All other elements increase by $1$.
Let $X = M - 1 - k$. The elements with value $X$ are the "wrapping" elements.
- **Loss of Inversions**: Pairs $(i, j)$ with $i < j$ such that $A_i = X$ and $A_j < X$. Originally, $A_i > A_j$ (inversion). After shift, $A_i$ becomes $0$ and $A_j$ becomes $A_j+1 \ge 1$, so $A_i < A_j$ (no inversion).
- **Gain of Inversions**: Pairs $(i, j)$ with $i < j$ such that $A_i < X$ and $A_j = X$. Originally, $A_i < A_j$ (no inversion). After shift, $A_i$ becomes $A_i+1 \ge 1$ and $A_j$ becomes $0$, so $A_i > A_j$ (inversion).

Thus, $\Delta Inv = \text{Gain} - \text{Loss}$.
To compute Gain and Loss efficiently for each $k$:
1. We need to count, for each occurrence of value $X$ at index $idx$, how many elements to its left are $< X$ (for Gain) and how many to its right are $< X$ (for Loss).
2. We can maintain a Fenwick Tree (BIT) over the indices $1 \dots N$. The BIT will store $1$ at index $i$ if $A_i < X$, and $0$ otherwise.
3. We start with $X = M-1$. The BIT initially marks all $A_i < M-1$.
4. For each $k$ from $0$ to $M-1$:
   - Let $X = M - 1 - k$.
   - Calculate Loss: Sum of BIT queries for ranges $[idx+1, N]$ for all indices $idx$ where $A_{idx} = X$.
   - Calculate Gain: Sum of BIT queries for ranges $[1, idx-1]$ for all indices $idx$ where $A_{idx} = X$.
   - Update current inversion count: $Inv_{k+1} = Inv_k + \text{Gain} - \text{Loss}$.
   - Prepare for next step ($X-1$): Remove indices where $A_i = X$ from the BIT (set to 0), because for the next step, the threshold is $X-1$, and these elements are no longer $< X-1$.

This approach requires $O(N \log N)$ to build the initial BIT and $O(M \log N)$ to process all shifts, fitting well within the time limits.

Pitfalls:
- Off-by-one errors in BIT queries (1-based vs 0-based indexing).
- Correctly handling the case where $X=0$ (no elements are $<0$, so BIT becomes all zeros).
- Ensuring the initial inversion count for $k=0$ is computed correctly.

## worker: (None)
The solution efficiently computes the inversion number for each shift $k$ by leveraging a recurrence relation.
1. **Initial Inversion Count**: Calculated using a Fenwick Tree (BIT) over values in $O(N \log M)$.
2. **Transition Logic**: When shifting from $k$ to $k+1$, elements with value $X = M-1-k$ wrap around to 0.
   - **Loss**: Inversions $(i, j)$ with $i < j$, $A_i = X$, $A_j < X$ are lost because $A_i$ becomes 0 and $A_j$ becomes $\ge 1$.
   - **Gain**: Inversions $(i, j)$ with $i < j$, $A_i < X$, $A_j = X$ are gained because $A_i$ becomes $\ge 1$ and $A_j$ becomes 0.
3. **Efficient Querying**: A second Fenwick Tree is maintained over the *indices* of the array. This BIT marks position $i$ with 1 if $A_i < \text{current threshold}$.
   - Initially, the threshold is $M-1$, so all $A_i < M-1$ are marked.
   - For each $k$, we query this BIT to count how many elements to the left/right of wrapping elements are smaller than the wrapping value.
   - After processing $k$, we update the BIT by unmarking indices where $A_i = X-1$ to prepare for the next threshold $X-1$.
4. **Complexity**:
   - Initial inversion count: $O(N \log M)$.
   - Loop runs $M$ times. Inside the loop, we iterate over occurrences of value $X$. Each index is processed exactly once when its value is the wrapping value, and once when it's removed from the BIT. Total BIT operations are $O(N \log N)$.
   - Overall complexity: $O(N \log N + M \log N + N \log M)$, which fits within the constraints.
