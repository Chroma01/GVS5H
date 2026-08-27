
## ideation
The problem asks us to count numbers in a range $[l, r]$ where the product of digits is divisible by the sum of digits. Given the constraint $r < 10^9$, a Digit DP approach is optimal. We can compute a helper function `count(n)` that returns the number of beautiful numbers in $[1, n]$, then return `count(r) - count(l-1)`.

Key insights for the DP state:
1. **State Variables**: `idx` (current digit position), `current_sum` (sum of digits so far), `current_prod` (product of digits so far), `tight` (whether we are restricted by the digits of `n`), and `started` (whether we have placed a non-zero digit yet).
2. **Product Tracking**: The product of digits only contains prime factors 2, 3, 5, and 7. For numbers up to $10^9$, the number of distinct reachable products is surprisingly small (~1800 values). This keeps the memoization table sparse and efficient.
3. **Zero Handling**: If any digit is `0`, the product becomes `0`. Since the sum of digits of a positive integer is always positive, `0 % sum == 0` is always true. The DP naturally handles this as `current_prod` becomes `0` and the base case returns `1`.
4. **Leading Zeros**: The `started` flag ensures leading zeros don't contribute to the sum or product. Once a non-zero digit is placed, `started` becomes `True` and tracking begins.
5. **Base Case**: When `idx == len(s)`, we check if `started` is `True` (to exclude the number `0`) and if `current_prod % current_sum == 0`.

The state space size is roughly $10 \times 82 \times 2000 \times 2 \times 2$, but reachable states are far fewer due to the structure of digit products. Python's `@lru_cache` handles the sparse dictionary efficiently.

## worker: Implement a helper function `count(X)` that comput
The solution uses Digit DP to count beautiful numbers up to `X`. The helper function `count(X)` computes the number of beautiful integers in `[1, X]`. The final answer is `count(r) - count(l-1)`.
- **State**: `(idx, current_sum, current_prod, tight, started)` tracks the current digit position, sum of digits placed so far, product of digits placed so far, whether we are restricted by the digits of `X`, and whether we have started placing non-zero digits.
- **Product Tracking**: The product of digits only contains prime factors 2, 3, 5, and 7. For numbers up to $10^9$, the number of distinct reachable products is surprisingly small (~1800 values), keeping the memoization table sparse and efficient.
- **Zero Handling**: If any digit is `0`, the product becomes `0`. Since the sum of digits of a positive integer is always positive, `0 % sum == 0` is always true. The DP naturally handles this as `current_prod` becomes `0` and the base case returns `1`.
- **Leading Zeros**: The `started` flag ensures leading zeros don't contribute to the sum or product. Once a non-zero digit is placed, `started` becomes `True` and tracking begins.
- **Base Case**: When `idx == len(s)`, we check if `started` is `True` (to exclude the number `0`) and if `current_prod % current_sum == 0`.
- **Complexity**: The state space is roughly $10 \times 82 \times 2000 \times 2 \times 2$, but reachable states are far fewer due to the structure of digit products. Python's `@lru_cache` handles the sparse dictionary efficiently, making this approach well within time limits for $r < 10^9$.
