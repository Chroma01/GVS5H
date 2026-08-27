
## ideation
The core difficulty: each forced flip (indices where A differs from B) has a direction fixed (0→1 adds c_i, 1→0 subtracts c_i). The only choice is the **order** of these flips, which determines the cumulative sum S at each step (and thus the cost of each operation).

Key insight: The cost equals the sum of S values after each operation. Expressing this in terms of the sequence of changes δ ∈ {+a, -d} with weights w_j = remaining_ops+1, the optimal assignment pairs:
- Largest c among "subtract" (M) ops with the largest weights (earliest positions) → all M before all P, M in decreasing c.
- Smallest c among "add" (P) ops with the smallest weights among the P block (earliest P positions) → P in increasing c.

Formula derived; verified with sample 1 (total 16). Pitfall: must use 64-bit ints (Python handles arbitrary precision). O(N log N).

## worker: Implement the algorithm in Python: read inputs, co
The algorithm works by separating forced flips into two groups: "M" (1→0, subtracts c_i from S) and "P" (0→1, adds c_i to S). Since each flip's cost equals the current S after the flip, and the final S is fixed, the problem reduces to ordering these changes to minimize the sum of intermediate S values. By writing the total cost as a weighted sum of the changes with weights equal to the number of remaining operations, we can show that:
- All M operations should come before all P operations (interleaving only increases cost).
- Within M, execute in decreasing c (largest reduction earliest).
- Within P, execute in increasing c (smallest increase earliest).

The formula `K*S0 - p*sum(M) - sum(prefix_M) + sum(prefix_P)` gives the minimum total cost. Verified with Sample 1 (16) and logic checks out for the structure.
