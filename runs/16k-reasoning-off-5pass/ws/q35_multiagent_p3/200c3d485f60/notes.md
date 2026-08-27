
## ideation
The problem asks for the number of arrays of length `n` with elements in `[1, m]` such that exactly `k` adjacent pairs are equal.

Key insight:
1. The condition "exactly k adjacent pairs are equal" means that there are `k` indices `i` where `arr[i-1] == arr[i]`. Consequently, there are `(n-1) - k` indices where `arr[i-1] != arr[i]`.
2. We can think of the array as being partitioned into contiguous blocks of identical values. The number of blocks is equal to the number of unequal transitions plus one, i.e., `(n-1-k) + 1 = n - k`.
3. To form such an array:
   a. Choose which `k` of the `n-1` adjacent positions are equal. This can be done in `C(n-1, k)` ways.
   b. Assign values to the blocks. The first block can have any of `m` values. Each subsequent block must have a value different from the previous block's value, so there are `m-1` choices for each of the remaining `n-k-1` blocks.
   c. Therefore, the number of ways to assign values is `m * (m-1)^(n-k-1)`.
4. The total number of good arrays is `C(n-1, k) * m * (m-1)^(n-k-1)`.
5. We need to compute this modulo `10^9 + 7`.
6. We'll need helper functions for combinations (using modular inverse for division) and modular exponentiation.

Pitfalls:
- When `k = n-1`, then `n-k-1 = 0`, so `(m-1)^0 = 1`, which is correct.
- When `k = 0`, then `n-k-1 = n-1`, so we have `m * (m-1)^(n-1)`, which is also correct.
- Need to handle large numbers with modulo arithmetic at each step.
- The combination formula `C(n-1, k) = (n-1)! / (k! * (n-1-k)!)` requires modular inverse for division.

## worker: Implement the combination function C(n-1, k) mod 1
The solution uses the combinatorial insight that:
1. We need to choose exactly `k` positions out of `n-1` adjacent pairs to be equal. This is `C(n-1, k)`.
2. The array is partitioned into `n-k` contiguous blocks of identical values.
3. The first block can have any of `m` values.
4. Each subsequent block must differ from the previous block, giving `m-1` choices per block.
5. There are `n-k-1` such subsequent blocks, so the value assignment count is `m * (m-1)^(n-k-1)`.
6. The final answer is the product of these two counts, modulo `10^9 + 7`.

We use modular exponentiation for efficient computation of powers and Fermat's little theorem for modular inverse (since `10^9 + 7` is prime). The combination is computed using the multiplicative formula with modular inverses for each term in the denominator.
