
## ideation
The problem asks for the number of arrays of length n with values in [1,m] that have exactly k adjacent equal pairs (i.e., positions i where arr[i-1]==arr[i]). This is equivalent to having exactly n-1-k positions where the adjacent elements differ. The array can be viewed as n-k "runs" (maximal blocks of equal elements). The first run can be any of m values, and each subsequent run must differ from the previous one, giving (m-1) choices. We need to choose which k of the n-1 adjacent positions are the "equal" ones (the boundaries within runs). Number of ways: C(n-1, k) * m * (m-1)^(n-k-1). The difficulty lies in efficient computation under modulo 1e9+7, handling large n up to 1e5, and edge cases where m=1 (then m-1=0, need to be careful with the power term and only valid if k=n-1). We'll use modular exponentiation and precompute factorials + inverse factorials for binomial coefficient. Complexity O(n) precomputation, O(log MOD) per query.

## worker: Implement the `countGoodArrays` method in the `Sol
- The solution follows the standard combinatorial derivation: the array consists of `n - k` "runs" (maximal blocks of equal elements). The first run can be any of `m` values, and each subsequent run must differ from the previous one, giving `m - 1` choices.
- The positions of the `k` equal adjacent pairs are chosen from the `n - 1` adjacent positions, giving `C(n-1, k)` ways.
- Overall formula: `C(n-1, k) * m * (m-1)^(n-k-1) mod (10^9+7)`.
- Factorials and inverse factorials are precomputed up to `n` to compute binomial coefficients in O(1) time after O(n) preprocessing.
- Edge cases handled: `n == 1` (only `m` arrays if `k == 0`), `m == 1` (only the all-ones array, valid only when `k == n-1`), and `k > n-1` (impossible, return 0).
- Fast modular exponentiation is used for the power term.
