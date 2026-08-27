1. For each possible GCD value `g` (from 1 to max(A)), count how many elements in A are divisible by `g`.
2. For each element A_i, we want the largest `g` such that:
   - A_i is divisible by `g` (so A_i can be part of the group with GCD `g`)
   - There are at least K elements in A divisible by `g` (so we can form a group of size K including A_i)
3. We can precompute for each `g`, the count of multiples of `g` in A using a sieve-like approach.
4. Then for each A_i, iterate over all divisors of A_i and find the largest divisor `d` such that count[d] >= K.
5. To optimize, we can precompute the answer for each possible value `v` (1 to max_A) by checking if there exists a divisor `d` of `v` with count[d] >= K, and taking the maximum such `d`. But since we need per-element answers, we can instead for each A_i, check its divisors.
6. Since A_i <= 10^6, we can precompute divisors for all numbers up to 10^6, or compute divisors on the fly efficiently.