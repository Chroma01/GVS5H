
## ideation
The core difficulty is counting arrays by the exact number of equal adjacent pairs while handling large values of n and m efficiently under modular arithmetic. A useful observation is that each adjacent relation is independently classified as either equal or different once its pattern is fixed; equal relations force the next value, while different relations provide a choice among all values except the previous one. The main implementation concerns are computing the required combinatorial quantity efficiently, handling edge cases such as m = 1 or k = 0, and avoiding invalid modular division.

## worker: Implement `countGoodArrays` using the direct formu
For each array, choose the `k` positions among the `n - 1` adjacent pairs that are equal. The remaining `n - 1 - k` positions must differ.

- The first element has `m` choices.
- Each equal adjacent pair has exactly one choice.
- Each differing adjacent pair has `m - 1` choices.
- The equal-pair positions can be selected in `C(n - 1, k)` ways.

Therefore, the result is:

`m * C(n - 1, k) * (m - 1)^(n - 1 - k) mod (10^9 + 7)`.

Factorials and inverse factorials compute the binomial coefficient in `O(n)` time and space. The formula also correctly handles `m = 1`, including the case where all adjacent pairs must be equal.
