
## ideation
The core difficulty is that $N$ is up to $2 \times 10^5$, making an $O(N^3)$ or even $O(N^2)$ approach infeasible. However, $K$ is relatively small ($\le 5 \times 10^5$). This suggests we can use a priority queue (max-heap) to generate the largest values one by one, similar to finding the K-th largest sum from multiple sorted arrays.

The expression is $V_{i,j,k} = A_i B_j + B_j C_k + C_k A_i$.
If we sort arrays $A, B, C$ in descending order, the largest value is likely at indices $(1,1,1)$ (1-based).
We can use a max-heap to explore the state space $(i, j, k)$.
Start by pushing the largest candidate $(A_1 B_1 + B_1 C_1 + C_1 A_1, 1, 1, 1)$ into the heap.
In each step, extract the maximum value from the heap. If this is the $K$-th extraction, we return the value.
Otherwise, push the "neighbors" of the current state into the heap. To avoid duplicates and ensure we cover the space efficiently, we can use a standard technique for K-th largest element in a product/sum space:
From state $(i, j, k)$, we can transition to:
1. $(i+1, j, k)$
2. $(i, j+1, k)$
3. $(i, j, k+1)$

However, simply pushing all three neighbors can lead to duplicates (e.g., $(2,1,1)$ can be reached from $(1,1,1)$ via $i$-increment or from $(1,1,1)$ via... wait, no, $(1,1,1)$ only goes to $(2,1,1), (1,2,1), (1,1,2)$).
Actually, the standard way to avoid duplicates in a 3D grid when moving only in positive index directions is to enforce an ordering on the transitions. A common strategy is:
- From $(i, j, k)$, push $(i+1, j, k)$.
- If $i=1$, also push $(i, j+1, k)$.
- If $i=1$ and $j=1$, also push $(i, j, k+1)$.
This ensures each state is generated exactly once from its "parent" in a specific tree structure.
Alternatively, just use a `visited` set to track which $(i,j,k)$ tuples have been added to the heap. Given $K$ is small, the number of visited states will be proportional to $K$, so a hash set is efficient enough.

Steps:
1. Read input.
2. Sort $A, B, C$ in descending order.
3. Use a max-heap (negate values for Python's min-heap) to store tuples `(value, i, j, k)`.
4. Use a set `visited` to store `(i, j, k)` tuples that have been pushed to the heap.
5. Push the initial state `(A[0]*B[0] + B[0]*C[0] + C[0]*A[0], 0, 0, 0)` into the heap and add `(0,0,0)` to visited.
6. Loop $K$ times:
   a. Pop the largest value from the heap.
   b. If it's the $K$-th pop, return the value.
   c. Generate neighbors: $(i+1, j, k), (i, j+1, k), (i, j, k+1)$.
   d. For each neighbor, if indices are within bounds $[0, N-1]$ and not in `visited`, push to heap and add to `visited`.

Complexity: $O(K \log K)$ due to heap operations. With $K=5 \times 10^5$, this is well within time limits.

Pitfalls:
- Integer overflow: The values can be up to $3 \times 10^{18}$, which fits in a 64-bit integer. Python handles large integers automatically.
- Duplicate states: Must use a visited set to avoid processing the same $(i,j,k)$ multiple times.
- Indexing: Ensure 0-based indexing is handled correctly.

## worker: none
The problem asks for the K-th largest value among $N^3$ possible values of $A_i B_j + B_j C_k + C_k A_i$. Given $N$ up to $2 \times 10^5$, we cannot generate all $N^3$ values. However, $K$ is small ($\le 5 \times 10^5$).

We use a max-heap (simulated with a min-heap by negating values) to generate the largest values in descending order.
1. Sort $A, B, C$ in descending order. The largest value is at indices $(0,0,0)$.
2. Push the initial state $(0,0,0)$ into the heap.
3. Use a `visited` set to keep track of states $(i,j,k)$ that have been pushed to the heap to avoid duplicates.
4. In each of the $K$ iterations, pop the largest value from the heap. This is the current largest unprocessed value.
5. Push the "neighbors" of the current state into the heap: $(i+1, j, k), (i, j+1, k), (i, j, k+1)$, provided the indices are within bounds and not already visited.
6. The value popped in the $K$-th iteration is the answer.

This approach has a time complexity of $O(K \log K)$ because we perform at most $K$ pops and each pop pushes at most 3 new elements, leading to $O(K)$ heap operations. The space complexity is $O(K)$ for the heap and visited set. This fits well within the constraints.
