
## ideation
The problem requires computing the sum of absolute differences between all pairs $(A_i, B_j)$ for prefixes $A[1..X_k]$ and $B[1..Y_k]$. A naive $O(N^2)$ per query approach is too slow. 
The core difficulty lies in efficiently aggregating contributions across two dynamic prefixes while handling absolute differences. This is a classic application of **Persistent Segment Trees** combined with **Coordinate Compression**.
1. **Coordinate Compression**: Values up to $2 \times 10^8$ are mapped to ranks $[0, M-1]$ where $M \le 2N$. This allows the segment tree to operate over indices rather than raw values.
2. **Persistent Segment Trees**: We build two persistent segment trees, one for $A$ and one for $B$. The $x$-th version stores the multiset $\{A_1, \dots, A_x\}$ (and similarly for $B$). Each node maintains `cnt` (number of elements) and `sum` (sum of elements) in its range.
3. **Query Processing**: For each query $(X_k, Y_k)$, we traverse the $X_k$-th tree of $A$ and $Y_k$-th tree of $B$ simultaneously. At each node covering $[L, R]$, we split contributions into four parts:
   - Both in left child: recursive call.
   - Both in right child: recursive call.
   - $A$ in left, $B$ in right: all $a \le mid < b$, so $|a-b| = b-a$. Contribution: $sum_B^{right} \cdot cnt_A^{left} - sum_A^{left} \cdot cnt_B^{right}$.
   - $A$ in right, $B$ in left: all $b \le mid < a$, so $|a-b| = a-b$. Contribution: $sum_A^{right} \cdot cnt_B^{left} - sum_B^{left} \cdot cnt_A^{right}$.
4. **Complexity**: Building takes $O(N \log N)$. Each query takes $O(\log N)$. Total time $O((N+K)\log N)$, well within limits. Memory is $O(N \log N)$.

Pitfalls to avoid:
- Recursion depth: $\log N \approx 18$, but `sys.setrecursionlimit` is added for safety.
- Null node handling: Index 0 represents an empty node with `cnt=0`, `sum=0`. Cross-term formulas naturally yield 0 when multiplied by 0, so explicit checks for null children only optimize performance.
- Integer overflow: Python handles arbitrarily large integers automatically, so no special modulo or overflow handling is needed.

## worker: <none>

```python
import sys

# Increase recursion
- **Coordinate Compression**: Maps values up to $2 \times 10^8$ to ranks $[0, M-1]$ where $M \le 2N$. This allows the segment tree to operate over indices rather than raw values, keeping the tree depth logarithmic.
- **Persistent Segment Trees**: Two persistent segment trees are built, one for prefix sums of $A$ and one for $B$. The $x$-th version stores the multiset $\{A_1, \dots, A_x\}$ (and similarly for $B$). Each node maintains `cnt` (number of elements) and `sum` (sum of elements) in its range.
- **Query Processing**: For each query $(X_k, Y_k)$, we traverse the $X_k$-th tree of $A$ and $Y_k$-th tree of $B$ simultaneously. At each node covering $[L, R]$, we split contributions into:
  1. Pairs where both values fall in the left child.
  2. Pairs where both values fall in the right child.
  3. Cross pairs where $A_i$ is in the left child and $B_j$ is in the right child. Since all values in the left child are $\le$ all values in the right child, $|A_i - B_j| = B_j - A_i$. Contribution: $\text{sum}(\text{right}_B) \cdot \text{cnt}(\text{left}_A) - \text{sum}(\text{left}_A) \cdot \text{cnt}(\text{right}_B)$.
  4. Cross pairs where $A_i$ is in the right child and $B_j$ is in the left child. Similarly, $|A_i - B_j| = A_i - B_j$. Contribution: $\text{sum}(\text{right}_A) \cdot \text{cnt}(\text{left}_B) - \text{sum}(\text{left}_B) \cdot \text{cnt}(\text{right}_A)$.
- **Complexity**: Building takes $O(N \log N)$. Each query takes $O(\log N)$. Total time $O((N+K)\log N)$, well within limits. Memory is $O(N \log N)$, acceptable for Python.
- Python handles arbitrarily large integers automatically, so no overflow handling is needed. Recursion limit is increased to safely handle tree traversals.
