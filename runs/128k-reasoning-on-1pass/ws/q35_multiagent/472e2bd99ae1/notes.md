
## ideation
The problem requires finding the $K$-th largest value of $A_i B_j + B_j C_k + C_k A_i$ over all triples $(i, j, k)$. Given $N \le 2 \times 10^5$ and $K \le 5 \times 10^5$, an exhaustive search is infeasible. However, since $K$ is relatively small, we can use a max-heap (simulated with a min-heap storing negative values) to generate the largest values in descending order.

Key observations:
1. Sorting $A, B, C$ in descending order ensures that $f(i, j, k) = A_i B_j + B_j C_k + C_k A_i$ is monotonically non-increasing with respect to each index.
2. We can use a priority queue to explore states $(i, j, k)$ starting from $(0, 0, 0)$.
3. To avoid duplicates and ensure each state is visited exactly once, we use a specific generation rule:
   - From $(i, j, k)$, always push $(i+1, j, k)$.
   - If $i = 0$, also push $(0, j+1, k)$.
   - If $i = 0$ and $j = 0$, also push $(0, 0, k+1)$.
   This rule creates a tree structure where every state has a unique parent, guaranteeing no duplicates and full coverage.
4. The time complexity will be $O(N \log N + K \log K)$, which fits well within the limits. Python's arbitrary-precision integers handle the large values naturally.

## worker: Implement the Python solution: read input, sort ar
The problem requires finding the $K$-th largest value of $A_i B_j + B_j C_k + C_k A_i$. Given $N \le 2 \times 10^5$ and $K \le 5 \times 10^5$, an exhaustive search is infeasible. However, since $K$ is relatively small, we can use a max-heap to generate values in descending order.

Key steps:
1. Sort arrays $A, B, C$ in descending order. This ensures the function $f(i, j, k) = A_i B_j + B_j C_k + C_k A_i$ is monotonically non-increasing with respect to each index.
2. Use a max-heap (simulated with negative values in Python's min-heap) to explore states $(i, j, k)$ starting from $(0, 0, 0)$.
3. To avoid duplicates and ensure each state is visited exactly once, we use a specific generation rule that forms a tree structure:
   - From $(i, j, k)$, always push $(i+1, j, k)$.
   - If $i = 0$, also push $(0, j+1, k)$.
   - If $i = 0$ and $j = 0$, also push $(0, 0, k+1)$.
   This rule guarantees each state has a unique parent, preventing duplicates without needing a visited set.
4. Pop the heap $K$ times. The $K$-th popped value is the answer.
Time complexity: $O(N \log N + K \log K)$, which fits well within the limits. Python's arbitrary-precision integers handle large values naturally.
