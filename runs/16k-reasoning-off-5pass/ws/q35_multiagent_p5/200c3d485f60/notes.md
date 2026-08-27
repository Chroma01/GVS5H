
## ideation
The core difficulty lies in correctly modeling the combinatorial structure of the problem. The key insight is that the condition "exactly k adjacent pairs are equal" is independent of the specific values chosen, as long as we account for the degrees of freedom at each step.

1.  **Structure**: An array of size `n` has `n-1` adjacent pairs. We need exactly `k` of these pairs to be equal (`arr[i-1] == arr[i]`) and `n-1-k` pairs to be unequal (`arr[i-1] != arr[i]`).
2.  **Choices**:
    *   The first element `arr[0]` can be any of the `m` values.
    *   For each subsequent element `arr[i]` (where `i > 0`):
        *   If the pair `(arr[i-1], arr[i])` is required to be equal, there is only **1** choice for `arr[i]` (it must equal `arr[i-1]`).
        *   If the pair `(arr[i-1], arr[i])` is required to be unequal, there are **m-1** choices for `arr[i]` (any value except `arr[i-1]`).
3.  **Combinatorics**:
    *   We need to choose which `k` positions out of the `n-1` possible adjacent positions are "equal". The number of ways to choose these positions is given by the binomial coefficient `C(n-1, k)`.
    *   Once the positions are chosen, the number of ways to fill the array is `m * (1)^k * (m-1)^(n-1-k)`.
4.  **Formula**: The total count is `C(n-1, k) * m * (m-1)^(n-1-k)`.
5.  **Modulo Arithmetic**: Since the result can be large, all calculations (combinations, powers, multiplication) must be done modulo `10^9 + 7`.
6.  **Edge Cases**:
    *   If `m == 1` and `k < n-1`, it's impossible to have unequal pairs, so the answer is 0 (unless `n=1`, where `k=0` is valid). The formula handles this because `m-1 = 0`, so if `n-1-k > 0`, the term `(m-1)^(n-1-k)` becomes 0.
    *   If `n=1`, then `k` must be 0. The formula gives `C(0,0) * m * (m-1)^0 = 1 * m * 1 = m`, which is correct.

Pitfalls to avoid:
*   Incorrectly calculating combinations modulo a prime. Need to use Fermat's Little Theorem for modular inverse since `10^9+7` is prime.
*   Forgetting to handle the case where `m=1` correctly (though the formula naturally handles it if implemented carefully).
*   Integer overflow before modulo operations in languages like C++/Java, but in Python, large integers are handled automatically, so we just need to apply modulo at appropriate steps to keep numbers manageable.

## worker: (none)
The solution uses a combinatorial approach:
1. An array of size `n` has `n-1` adjacent pairs.
2. We need exactly `k` of these pairs to be equal and `n-1-k` to be unequal.
3. The number of ways to choose which `k` positions are equal is `C(n-1, k)`.
4. For each such configuration:
   - The first element has `m` choices.
   - Each "equal" pair contributes a factor of 1 (only one choice for the next element).
   - Each "unequal" pair contributes a factor of `m-1` (any value except the previous one).
5. Thus, the total count is `C(n-1, k) * m * (m-1)^(n-1-k)`.
6. All calculations are done modulo `10^9 + 7`. The binomial coefficient is computed using factorials and modular inverses (via Fermat's Little Theorem, since `10^9+7` is prime).
7. Edge cases like `m=1` are handled naturally: if `m=1` and `n-1-k > 0`, then `(m-1)^(n-1-k) = 0`, giving the correct answer of 0. If `n=1`, `k=0`, the formula gives `C(0,0)*m*(m-1)^0 = m`, which is correct.
