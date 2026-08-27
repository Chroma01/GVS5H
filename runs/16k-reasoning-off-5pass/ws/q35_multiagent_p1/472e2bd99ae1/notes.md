
## ideation
The problem asks for the K-th largest value of $A_i B_j + B_j C_k + C_k A_i$ over all $1 \le i,j,k \le N$.
Constraints: $N \le 2 \times 10^5$, $K \le 5 \times 10^5$.
The total number of triples is $N^3$, which is too large to generate explicitly.
However, K is relatively small ($5 \times 10^5$). This suggests we can use a max-heap (priority queue) to extract the top K values.

The expression is $V_{i,j,k} = A_i B_j + B_j C_k + C_k A_i$.
To use a heap to find the K-th largest, we can start with the maximum possible value, which corresponds to the indices of the maximum elements in A, B, and C.
Let's sort A, B, and C in descending order. Let the sorted arrays be $A', B', C'$.
The maximum value is $V_{0,0,0} = A'_0 B'_0 + B'_0 C'_0 + C'_0 A'_0$.

We can use a max-heap to store tuples `(value, i, j, k)`.
Initially, push `(V_{0,0,0}, 0, 0, 0)` into the heap.
We also need a set to keep track of visited indices `(i, j, k)` to avoid duplicates.

In each step, we pop the largest element from the heap. This is the current largest unprocessed value.
If we have popped K times, the K-th popped value is our answer.
Otherwise, we generate neighbors. For a state `(i, j, k)`, the "next" states in lexicographical order of indices (since arrays are sorted descending) would be:
1. `(i+1, j, k)`
2. `(i, j+1, k)`
3. `(i, j, k+1)`

However, simply adding all three neighbors can lead to duplicates (e.g., `(1,0,0)` can be reached from `(0,0,0)` via i+1 or from `(0,0,0)` via j+1? No, `(0,0,0)` -> `(1,0,0)` and `(0,0,0)` -> `(0,1,0)`. But `(1,1,0)` can be reached from `(1,0,0)` via j+1 or from `(0,1,0)` via i+1).
To avoid duplicates and ensure we cover the space correctly, a standard technique for "K-th largest sum from sorted arrays" is to only allow transitions that increase the index in a specific way to prevent cycles and duplicates.
A common strategy for 3D is:
From `(i, j, k)`, we can push:
- `(i+1, j, k)` if `i+1 < N`
- `(i, j+1, k)` if `j+1 < N` AND `i == 0` (This restricts j-increments to only happen when i is at its minimum for that j-level? No, this is for 2D. For 3D, it's trickier.)

Actually, a simpler and robust way for K-th largest with small K is:
Push `(i+1, j, k)` always.
Push `(i, j+1, k)` only if `i == 0`.
Push `(i, j, k+1)` only if `i == 0` and `j == 0`.
This ensures each state is generated exactly once from a unique parent.
Let's verify:
- `(0,0,0)` generates `(1,0,0)`, `(0,1,0)`, `(0,0,1)`.
- `(1,0,0)` generates `(2,0,0)`. It does NOT generate `(1,1,0)` because `i != 0`.
- `(0,1,0)` generates `(0,2,0)`. It does NOT generate `(1,1,0)` because `i != 0`.
- `(0,0,1)` generates `(0,1,1)`? No, `j != 0` so it doesn't generate `(0,1,1)` via j+1? Wait.
The rule "Push `(i, j+1, k)` only if `i == 0`" means `(0,0,1)` will generate `(0,1,1)`.
Does `(1,1,0)` get generated?
Parent of `(1,1,0)` could be `(0,1,0)` via i+1? Yes, `(0,1,0)` is generated from `(0,0,0)` via j+1. So `(0,1,0)` generates `(1,1,0)`.
Does `(0,1,1)` get generated?
Parent could be `(0,0,1)` via j+1? Yes. `(0,0,1)` is generated from `(0,0,0)` via k+1. So `(0,0,1)` generates `(0,1,1)`.
Does `(1,0,1)` get generated?
Parent could be `(0,0,1)` via i+1? Yes. `(0,0,1)` generates `(1,0,1)`.
Does `(1,1,1)` get generated?
Parent could be `(0,1,1)` via i+1? Yes. `(0,1,1)` generates `(1,1,1)`.
This logic seems to cover all states uniquely.
The condition is:
From `(i, j, k)`:
1. If `i + 1 < N`, push `(i+1, j, k)`.
2. If `i == 0` and `j + 1 < N`, push `(i, j+1, k)`.
3. If `i == 0` and `j == 0` and `k + 1 < N`, push `(i, j, k+1)`.

This is a standard way to traverse the grid of indices for K-th largest sum.

Complexity:
Sorting: $O(N \log N)$.
Heap operations: We pop K times. Each pop pushes up to 3 items. Heap size is at most $3K$.
Each heap operation is $O(\log K)$.
Total time: $O(N \log N + K \log K)$.
With $N=2 \cdot 10^5$ and $K=5 \cdot 10^5$, this is well within time limits.

Pitfalls:
- Integer overflow: Values can be up to $10^9 \cdot 10^9 + \dots \approx 3 \cdot 10^{18}$, which fits in a 64-bit integer (Python handles large ints automatically).
- Visited set: We don't need a visited set if we use the strict generation rules above, as each state is generated exactly once.
- 1-based vs 0-based indexing: Input is 1-based, but we can use 0-based internally.

Next steps:
1. Read input.
2. Sort A, B, C in descending order.
3. Implement the max-heap logic with the specific neighbor generation rules.
4. Extract the K-th largest value.

## worker: Implement the solution based on the ideation.
The problem asks for the K-th largest value of $A_i B_j + B_j C_k + C_k A_i$. Given $N$ up to $2 \cdot 10^5$, we cannot iterate over all $N^3$ triples. However, $K$ is small ($5 \cdot 10^5$).

The solution uses a max-heap (simulated with a min-heap by negating values) to extract the largest values one by one.
1. **Sorting**: Arrays A, B, and C are sorted in descending order. This ensures that the largest possible value is at indices $(0,0,0)$.
2. **Heap Initialization**: The initial state $(0,0,0)$ is pushed into the heap.
3. **Extraction and Expansion**: We pop the largest value K times. For each popped state $(i,j,k)$, we generate "next" states to explore. To avoid duplicates and ensure we cover the search space systematically without a visited set (which would be memory heavy), we use specific transition rules:
   - From $(i,j,k)$, we can always go to $(i+1, j, k)$.
   - We can go to $(i, j+1, k)$ only if $i=0$.
   - We can go to $(i, j, k+1)$ only if $i=0$ and $j=0$.
   
   This logic ensures that every triple $(i,j,k)$ is generated exactly once from a unique parent. For example, $(1,1,0)$ is generated from $(0,1,0)$ via $i+1$, not from $(1,0,0)$ via $j+1$ (since $i \neq 0$ for $(1,0,0)$).

4. **Complexity**: Sorting takes $O(N \log N)$. The heap operations involve K extractions and up to 3 pushes per extraction. The heap size is bounded by $O(K)$. Each heap operation is $O(\log K)$. Total time complexity is $O(N \log N + K \log K)$, which fits well within the limits for $N=2 \cdot 10^5$ and $K=5 \cdot 10^5$.
