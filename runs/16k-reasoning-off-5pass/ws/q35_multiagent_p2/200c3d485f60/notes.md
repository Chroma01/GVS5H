
## ideation
The core difficulty lies in correctly modeling the combinatorial structure of the problem and implementing efficient modular arithmetic for large numbers.

1.  **Combinatorial Structure**:
    - An array of size `n` has `n-1` adjacent pairs.
    - We need exactly `k` of these pairs to be equal (`arr[i-1] == arr[i]`).
    - The remaining `n-1-k` pairs must be unequal (`arr[i-1] != arr[i]`).
    - First, choose which `k` positions out of the `n-1` possible adjacent positions are "equal". This is given by the binomial coefficient $C(n-1, k)$.
    - Once the positions are chosen, the values are determined as follows:
        - The first element `arr[0]` can be any of the `m` values.
        - For each "equal" position, the next element is forced to be the same as the previous one (1 choice).
        - For each "unequal" position, the next element can be any value except the previous one (`m-1` choices).
    - Therefore, the total number of ways is: $C(n-1, k) \times m \times (m-1)^{n-1-k}$.

2.  **Modular Arithmetic**:
    - Since the result can be very large, all calculations must be done modulo $10^9 + 7$.
    - We need a function to compute combinations $C(n, k) \pmod P$. This can be done using factorials and modular inverse (using Fermat's Little Theorem since $P$ is prime).
    - We need a function for modular exponentiation to compute $(m-1)^{n-1-k} \pmod P$.

3.  **Edge Cases**:
    - If `m == 1` and `k < n-1`, it's impossible to have unequal pairs, so the answer should be 0 (unless `k == n-1`, then only 1 array exists: all 1s). The formula handles this naturally because if `m-1 == 0` and the exponent `n-1-k > 0`, then $(m-1)^{n-1-k} = 0$. If `n-1-k == 0`, then $(m-1)^0 = 1$.
    - If `k == n-1`, then all adjacent pairs are equal, so the array is constant. There are `m` such arrays. The formula gives $C(n-1, n-1) \times m \times (m-1)^0 = 1 \times m \times 1 = m$. Correct.
    - If `k == 0`, then no adjacent pairs are equal. The formula gives $C(n-1, 0) \times m \times (m-1)^{n-1} = 1 \times m \times (m-1)^{n-1}$. Correct.

4.  **Implementation Details**:
    - Precompute factorials and inverse factorials up to `n` (or `n-1`) to compute combinations in $O(1)$ or $O(\log MOD)$ time. Given $n \le 10^5$, precomputing factorials is efficient.
    - Use Python's `pow(base, exp, mod)` for modular exponentiation.

## worker: (None)
The solution uses a combinatorial approach:
1. There are `n-1` adjacent positions in an array of size `n`.
2. We need exactly `k` of these positions to have equal adjacent elements. The number of ways to choose these positions is $C(n-1, k)$.
3. For the chosen "equal" positions, the value is forced (1 choice). For the remaining `n-1-k` "unequal" positions, there are `m-1` choices for each (any value except the previous one).
4. The first element has `m` choices.
5. Therefore, the total count is $C(n-1, k) \times m \times (m-1)^{n-1-k}$.
6. All calculations are performed modulo $10^9 + 7$.
7. Edge case `m == 1` is handled separately: if `k == n-1`, the answer is 1 (all elements are 1), otherwise 0 (impossible to have unequal pairs).
8. Factorials and inverse factorials are precomputed to efficiently calculate combinations using Fermat's Little Theorem for modular inverse.
