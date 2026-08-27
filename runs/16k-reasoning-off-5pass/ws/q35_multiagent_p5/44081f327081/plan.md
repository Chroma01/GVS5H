1. For each possible GCD value `g` (from 1 to max(A)), we want to know if there are at least `K` elements in `A` that are multiples of `g`.
2. We can count the frequency of each number in `A`, then for each `g`, iterate through its multiples and sum up the frequencies to get the count of numbers in `A` divisible by `g`.
3. For each index `i`, we need to find the maximum `g` such that:
   - `A_i` is divisible by `g` (since `A_i` must be included in the chosen set, all chosen elements including `A_i` must be divisible by `g`)
   - There are at least `K` elements in `A` that are divisible by `g`
4. To efficiently find the answer for each `i`, we can precompute for each `g` whether it's feasible (count >= K). Then for each `A_i`, we iterate through all divisors of `A_i` and pick the largest feasible one.
5. Since `A_i <= 10^6`, we can precompute divisors for all numbers up to `10^6` or compute divisors on the fly using trial division up to sqrt(A_i).