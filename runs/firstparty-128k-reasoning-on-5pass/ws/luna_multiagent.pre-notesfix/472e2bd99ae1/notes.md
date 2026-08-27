
## ideation
The core difficulty is handling an implicit \(N^3\)-sized collection when \(N\) is as large as \(2\times 10^5\). Since all entries are positive, sorting each sequence in descending order makes the expression monotone in every coordinate: decreasing any index cannot increase the value. The challenge is therefore to exploit this 3D monotonicity while processing only enough states to determine the first \(K\) values, with \(K\leq 5\times10^5\). Values and intermediate products require 64-bit arithmetic.

## worker: Implement the 3D max-heap best-first traversal: so
After sorting all three arrays in descending order, the expression is non-increasing when any coordinate increases, since all values are positive.

The heap stores states in descending value order. To avoid duplicate insertion without a memory-heavy visited set, each state uses one canonical parent:
- if `i > 0`, its parent is `(i-1, j, k)`;
- otherwise if `j > 0`, its parent is `(0, j-1, k)`;
- otherwise its parent is `(0, 0, k-1)`.

Therefore, transitions are:
- always to `(i+1, j, k)`;
- to `(0, j+1, k)` only when `i == 0`;
- to `(0, 0, k+1)` only when `i == j == 0`.

Every state is generated exactly once. Since each state’s parent has value at least as large as the state, best-first traversal correctly enumerates the values in descending order. Complexity is `O(K log K)` time and `O(K)` memory.
