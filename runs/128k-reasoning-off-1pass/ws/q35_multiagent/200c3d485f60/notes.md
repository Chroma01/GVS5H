
## ideation
The core difficulty lies in correctly modeling the combinatorial structure of the problem. The key insight is that the positions where `arr[i-1] == arr[i]` (equal pairs) and `arr[i-1] != arr[i]` (different pairs) are independent in terms of counting, once we fix which positions are equal.

1.  **Choosing Positions**: There are `n-1` adjacent pairs in an array of size `n`. We need exactly `k` of these to be equal. The number of ways to choose which `k` positions are equal is given by the binomial coefficient `C(n-1, k)`.
2.  **Filling Values**:
    *   The first element `arr[0]` can be any of the `m` values.
    *   For each of the `k` "equal" positions, the value is forced to be the same as the previous element (1 choice).
    *   For each of the `n - 1 - k` "different" positions, the value must be different from the previous element. Since there are `m` total choices and 1 is forbidden (the previous value), there are `m - 1` choices for each such position.
3.  **Formula**: The total number of good arrays is `C(n-1, k) * m * (m-1)^(n-1-k)`.
4.  **Modulo Arithmetic**: All calculations must be done modulo `10^9 + 7`. We need efficient functions for:
    *   Modular exponentiation: `pow(base, exp, mod)`
    *   Binomial coefficient modulo `p`: `C(n, k) = n! / (k! * (n-k)!) mod p`. This requires computing factorials and their modular inverses. Since `p = 10^9 + 7` is prime, we can use Fermat's Little Theorem for modular inverse: `a^(p-2) mod p`.

## worker: <none>
The solution is based on a combinatorial approach:
1. There are `n-1` adjacent positions in an array of size `n`.
2. We choose `k` of these positions to be "equal" (i.e., `arr[i-1] == arr[i]`). The number of ways to do this is `C(n-1, k)`.
3. The first element can be chosen in `m` ways.
4. For each of the `k` equal positions, the value is forced (1 choice).
5. For each of the `n-1-k` different positions, the value must be different from the previous one, giving `m-1` choices per position.
6. The total count is `C(n-1, k) * m * (m-1)^(n-1-k)`.
7. All calculations are performed modulo `10^9 + 7`.
8. Edge case: if `m == 1`, then all elements are 1, so all `n-1` pairs are equal. Thus, the answer is 1 if `k == n-1`, else 0. This is handled separately for correctness and efficiency.
9. The binomial coefficient is computed using factorials and modular inverses via Fermat's Little Theorem, which is valid since `10^9 + 7` is prime.
