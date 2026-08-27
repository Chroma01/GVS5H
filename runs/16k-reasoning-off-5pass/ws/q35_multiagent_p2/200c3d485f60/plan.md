1. Recognize that the problem involves counting arrays with exactly `k` adjacent equal pairs. This is equivalent to choosing which `k` of the `n-1` possible adjacent positions are "equal" and the remaining `n-1-k` positions are "different".
2. The number of ways to choose which positions are equal is given by the binomial coefficient C(n-1, k).
3. For the first element, there are `m` choices. For each subsequent position where the value must be different from the previous one, there are `m-1` choices. For positions where the value must be equal, there is only 1 choice (must match the previous).
4. Therefore, the total count is: C(n-1, k) * m * (m-1)^(n-1-k), all modulo 10^9 + 7.
5. Implement modular arithmetic for combinations and exponentiation to handle large numbers efficiently.