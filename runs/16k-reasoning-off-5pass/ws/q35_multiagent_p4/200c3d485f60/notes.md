
## ideation
The problem asks for the number of arrays of length `n` with elements in `[1, m]` such that exactly `k` adjacent pairs are equal.

Key insights:
1. There are `n-1` adjacent pairs in an array of size `n`.
2. We need exactly `k` of these pairs to be equal, which means `n-1-k` pairs must be unequal.
3. We can choose which `k` positions (out of `n-1`) have equal values in C(n-1, k) ways.
4. For the first element, there are `m` choices.
5. For each "equal" transition, the value is forced (1 choice).
6. For each "unequal" transition, there are `m-1` choices (any value except the previous one).
7. Therefore, the total count is: `m * C(n-1, k) * (m-1)^(n-1-k)` modulo 10^9 + 7.

Pitfalls to avoid:
- Computing combinations modulo a prime requires modular inverse for division. We can use Fermat's little theorem since 10^9+7 is prime.
- Need to handle large exponents efficiently using modular exponentiation.
- Edge cases: when k = n-1, then (m-1)^0 = 1; when k = 0, we have (m-1)^(n-1).

The approach is straightforward combinatorics with modular arithmetic.

## worker: <none>
## Proof/Reasoning
1. **Problem Analysis**: We need to count arrays of length `n` with values in `[1, m]` such that exactly `k` adjacent pairs `(arr[i-1], arr[i])` are equal.

2. **Key Insight**: 
   - There are `n-1` adjacent positions in an array of size `n`.
   - We need exactly `k` of these to be "equal" transitions and `n-1-k` to be "unequal" transitions.
   - First, choose which `k` positions out of `n-1` are equal: `C(n-1, k)` ways.
   - The first element has `m` choices.
   - For each "equal" transition, the next element is forced to be the same as the previous: 1 choice.
   - For each "unequal" transition, the next element can be any value except the previous one: `m-1` choices.
   - Total: `m * C(n-1, k) * (m-1)^(n-1-k)`.

3. **Modular Arithmetic**: Since the answer can be very large, we compute everything modulo `10^9 + 7`. For the combination `C(n-1, k)`, we use factorials and modular inverses (via Fermat's little theorem since `10^9 + 7` is prime).

4. **Edge Cases**:
   - `k = n-1`: All adjacent pairs are equal, so `(m-1)^0 = 1`. Result: `m * C(n-1, n-1) * 1 = m`.
   - `k = 0`: No adjacent pairs are equal, so `(m-1)^(n-1)`. Result: `m * C(n-1, 0) * (m-1)^(n-1) = m * (m-1)^(n-1)`.
   - `k > n-1`: Impossible, return 0.

5. **Complexity**: O(n) for precomputing factorials, O(log MOD) for modular inverse and exponentiation. Overall O(n) time and O(n) space.
