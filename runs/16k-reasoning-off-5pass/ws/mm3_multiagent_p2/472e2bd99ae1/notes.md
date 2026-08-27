
## ideation
The core problem is to find the K-th largest value among N^3 combinations of the form `A_i*B_j + B_j*C_k + C_k*A_i`, with N up to 2×10^5 and K up to 5×10^5.

Key observations:
1. The expression is symmetric and can be rewritten as `(A_i + C_k)*B_j + A_i*C_k`.
2. The expression is strictly increasing in each of A_i, B_j, and C_k individually (since all values are positive).
3. If we sort A, B, C in descending order, then increasing the index in any array decreases the value.
4. This monotonicity allows us to use a best-first search (max-heap) starting from the maximum triple (0,0,0) and expanding by incrementing one index at a time.
5. Since K ≤ 5×10^5, generating the top K values via heap expansion is efficient: O(K log K) time and O(K) memory.
6. To avoid pushing duplicate triples, we maintain a visited set using integer encoding (e.g., `i * N * N + j * N + k`).

Pitfalls:
- Memory: visited set must be memory-efficient. Using integer keys instead of 3-tuples saves space.
- Overflow: Python handles big integers natively, so no overflow issues.
- Tie handling: Values may repeat, but we only need the K-th largest value, not a specific triple.
- Edge cases: N=1 works trivially; K=1 returns the single maximum.

## worker: Implement the solution in Python: read input, sort
The solution exploits the monotonicity of the expression `A_i*B_j + B_j*C_k + C_k*A_i` in each of the three variables. After sorting A, B, C in descending order, larger indices correspond to smaller values. This allows a best-first search using a max-heap to enumerate the top K triples in non-increasing order, starting from the maximum (0,0,0) and expanding by incrementing one index at a time. A visited set (using integer encoding to reduce memory overhead) prevents duplicate entries. The complexity is O(K log K) time and O(K) memory, which fits easily within the given constraints (K ≤ 5×10^5).
