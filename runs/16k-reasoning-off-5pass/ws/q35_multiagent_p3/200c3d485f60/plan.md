1. We need to count arrays of length `n` with elements in `[1, m]` such that exactly `k` adjacent pairs are equal.
2. Think of the array as being composed of `k+1` contiguous blocks of identical values. The boundaries between blocks are where `arr[i-1] != arr[i]`. There are `n-1` adjacent pairs, and `k` of them are equal, so `n-1-k` are unequal.
3. The number of ways to choose which `k` of the `n-1` positions are equal is C(n-1, k).
4. For the first element, we have `m` choices. For each subsequent block start (i.e., each position where a new block begins, which corresponds to an unequal pair), we have `m-1` choices (since it must differ from the previous element).
5. There are `n-1-k` unequal pairs, meaning there are `n-1-k` positions where the value changes. Including the first element, we have `1 + (n-1-k) = n-k` "independent" choices: the first element and each new block's starting value.
6. So the total count is: C(n-1, k) * m * (m-1)^(n-1-k) modulo 10^9+7.