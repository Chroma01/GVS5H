
## ideation
The core difficulty is that the cost of each operation depends on the **current total sum** of A (i.e., the number of 1s weighted by C_k), and that sum changes after every flip.  
A naive simulation or DP over the order of flips is exponential.  

**Key observation:**  
When we flip a position `i`:
- If `A_i` was 1 (a 1→0 flip), the new sum is `S − C_i`. The cost of this flip is `S`.
- If `A_i` was 0 (a 0→1 flip), the new sum is `S + C_i`. The cost of this flip is `S + C_i`.

Since `C_i > 0`, flipping a 1 to 0 **reduces** the future cost base `S`, while flipping a 0 to 1 **increases** it. Therefore, to minimise total cost, we should:
1. Do all necessary 1→0 flips first.
2. Then do all necessary 0→1 flips.

Let:
- `S` = initial weighted sum of A (sum of C_i where A_i = 1).
- `x` = number of 1→0 flips needed (positions where A_i = 1 and B_i = 0).
- `y` = number of 0→1 flips needed (positions where A_i = 0 and B_i = 1).

After the `x` 1→0 flips, the sum becomes `S - sum_{i in 1→0} C_i`.  
Each of those `x` flips costs the current `S` at the time of the flip. However, because we only care about the *minimum* total cost, and flipping a 1→0 first is always beneficial (it lowers the base for later 0→1 flips), the total cost formula is:

```
total = x * S + Σ_{i in 0→1} (S - sum_{j in 1→0, j before i} C_j + C_i)
```

But since all 1→0 flips are done before any 0→1 flips, the sum used for each 0→1 flip is `S - sum_{1→0} C`. So:

```
total = x * S + y * (S - sum_{1→0} C) + sum_{0→1} C
```

This can be computed in a single pass:
- Compute `S`.
- Compute `sum_10 = sum of C_i where A_i=1 and B_i=0`.
- Compute `sum_01 = sum of C_i where A_i=0 and B_i=1`.
- `x = count of 1→0`, `y = count of 0→1`.
- `answer = x * S + y * (S - sum_10) + sum_01`.

**Pitfalls:**
- Must distinguish between 1→0 and 0→1 positions.
- `C_i` can be up to 10^6, `N` up to 2e5, so use 64-bit integers.
- No need to simulate; the closed-form works because order is forced.
- Edge case: A already equals B → `x = y = 0` → answer 0.

## worker: Implement the solution: parse input, compute S, su
The solution follows the derived closed-form:

- Compute initial weighted sum `S = Σ C_i` where `A_i = 1`.
- `sum_10` and `sum_01` are the weighted sums of positions that need a 1→0 flip and a 0→1 flip respectively.
- `x` and `y` are the counts of such positions.

The minimum total cost is:
`ans = x * S + y * (S - sum_10) + sum_01`

Reasoning: doing all 1→0 flips first (each costing the current `S`) reduces the base sum to `S - sum_10` for the subsequent 0→1 flips. Each 0→1 flip then costs `S - sum_10 + C_i`, and summing over those positions yields the formula above.

All operations are O(N) and use 64-bit integers (Python handles big ints natively), easily within the limits for N up to 2·10⁵ and C_i up to 10⁶.
