1. We need to count arrays of length `n` with values in `[1, m]` such that exactly `k` adjacent pairs are equal.
2. This means there are `n - 1 - k` adjacent pairs that are unequal.
3. We can think of building the array by choosing the first element (m choices), then for each subsequent position, if we want equality with the previous, we have 1 choice; if we want inequality, we have `m - 1` choices.
4. The problem reduces to: choose which `k` of the `n-1` adjacent positions are equal (the rest are unequal). The number of ways to choose these positions is C(n-1, k).
5. For each such choice, the number of arrays is: m * (1)^k * (m-1)^(n-1-k) = m * (m-1)^(n-1-k).
6. So the answer is C(n-1, k) * m * (m-1)^(n-1-k) mod 10^9+7. We need to compute combinations and powers modulo 10^9+7.