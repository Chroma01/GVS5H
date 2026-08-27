
## ideation
The core difficulty lies in correctly modeling the structure of the array based on the constraint of exactly `k` adjacent equal pairs.

1.  **Combinatorial Structure**:
    *   An array of size `n` has `n-1` adjacent pairs.
    *   We need exactly `k` of these pairs to be equal (`arr[i-1] == arr[i]`).
    *   The remaining `(n-1) - k` pairs must be different (`arr[i-1] != arr[i]`).
    *   This effectively partitions the array into `n - k` "blocks" of consecutive identical elements. For example, if `n=4, k=2`, we might have blocks like `[1, 1], [2, 2]` (2 blocks) or `[1, 1, 1], [2]` (2 blocks). The number of blocks is always `n - k`.

2.  **Counting Ways**:
    *   **Step 1: Choose positions for equality**. We need to choose which `k` of the `n-1` gaps between elements are "equal". The number of ways to do this is the binomial coefficient `C(n-1, k)`.
    *   **Step 2: Assign values to blocks**.
        *   The first block can take any of the `m` values.
        *   Each subsequent block must start with a value *different* from the previous block's value to ensure the gap between blocks is "different". There are `m-1` choices for each subsequent block.
        *   Since there are `n - k` blocks, the first block has `m` choices, and the remaining `n - k - 1` blocks have `m-1` choices each.
        *   Total ways to assign values = `m * (m-1)^(n-k-1)`.

3.  **Edge Cases**:
    *   If `m == 1`:
        *   If `k == n - 1`, the only possible array is all 1s. Answer is 1.
        *   If `k != n - 1`, it's impossible to have any "different" pairs, so answer is 0.
    *   If `n == 1`:
        *   `k` must be 0. The answer is `m`. The formula `C(0,0) * m * (m-1)^(-1)` is problematic due to negative exponent. We should handle `n=1` separately or ensure the exponent logic holds. Note: `n-k-1` becomes `0-0-1 = -1`. So special handling for `n=1` or `n-k-1 < 0` is needed. Actually, if `n=1`, `k=0`, blocks = 1. Formula: `C(0,0)*m*(m-1)^0 = m`. It works if we define `(m-1)^0 = 1`. But if `n-k-1` is negative, it's invalid. `n-k-1 < 0` implies `n-k < 1` => `k > n-1`, which is impossible by constraints. The minimum `n-k-1` is when `k=n-1`, then exponent is 0. So exponent is always >= 0.
    *   Modulo arithmetic must be applied at each step.

4.  **Implementation Details**:
    *   Need a function for combinations `C(n, k) % MOD`. Since `n` up to 10^5, we can precompute factorials or compute on the fly with modular inverse. Given constraints, precomputing factorials up to 10^5 is efficient.
    *   Need modular exponentiation for `(m-1)^(n-k-1)`.

Pitfalls:
- Forgetting to handle `m=1` correctly.
- Incorrectly calculating combinations modulo prime.
- Off-by-one errors in the exponent or combination arguments.

## worker: (none)
The solution uses a combinatorial approach:
1. **Choosing Equal Gaps**: An array of size `n` has `n-1` adjacent pairs. We need exactly `k` of these to be equal. The number of ways to choose which `k` positions are equal is given by the binomial coefficient `C(n-1, k)`.
2. **Assigning Values**: The constraint of exactly `k` equal adjacent pairs means the array is partitioned into `n - k` contiguous blocks of identical values. Adjacent blocks must have different values.
   - The first block can take any of the `m` values.
   - Each of the remaining `n - k - 1` blocks must take a value different from the previous block, giving `m - 1` choices each.
   - Total value assignments: `m * (m-1)^(n-k-1)`.
3. **Edge Cases**:
   - If `m == 1`, the only possible array is all 1s. This requires `k == n-1`. Otherwise, it's impossible.
   - If `n == 1`, `k` must be 0, and there are `m` possible arrays.
4. **Modulo Arithmetic**: All calculations are performed modulo `10^9 + 7`. Factorials and their modular inverses are precomputed to efficiently calculate combinations.
