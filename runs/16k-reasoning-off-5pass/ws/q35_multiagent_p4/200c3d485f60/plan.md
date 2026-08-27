1. We need to count arrays of length `n` with values in `[1, m]` such that exactly `k` adjacent pairs are equal.
2. This means exactly `n - 1 - k` adjacent pairs are unequal.
3. We can think of this as choosing which `k` positions (out of `n-1` possible adjacent positions) have equal values. The number of ways to choose these positions is C(n-1, k).
4. For the positions where values are equal, the value is determined by the previous element in the group. For positions where values are unequal, the current element must differ from the previous one, giving `m-1` choices.
5. The first element has `m` choices. Then, for each of the `n-1` transitions: if it's an "equal" transition, there's 1 choice (same as previous); if it's an "unequal" transition, there are `m-1` choices.
6. So the total count is: m * C(n-1, k) * (m-1)^(n-1-k), all modulo 10^9 + 7.