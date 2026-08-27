1. We need to construct an array of size `n` with elements in `[1, m]` such that exactly `k` adjacent pairs are equal.
2. This means there are `n - 1` adjacent positions, and we choose `k` of them to be "equal" (i.e., `arr[i-1] == arr[i]`) and the remaining `n - 1 - k` positions to be "different" (i.e., `arr[i-1] != arr[i]`).
3. The number of ways to choose which `k` positions are equal is given by the binomial coefficient C(n-1, k).
4. For the first element, we have `m` choices.
5. For each position where the value must be different from the previous one, we have `m - 1` choices (any value except the previous one).
6. For each position where the value must be equal to the previous one, we have only `1` choice (must be the same as previous).
7. Therefore, the total count is: C(n-1, k) * m * (m-1)^(n-1-k) modulo 10^9+7.
8. We need to compute combinations modulo 10^9+7 and power modulo 10^9+7 efficiently.