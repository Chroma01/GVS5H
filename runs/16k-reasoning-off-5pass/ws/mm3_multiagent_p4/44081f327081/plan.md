The GCD of a set that includes A_i equals the largest d such that there are at least K-1 other elements in A whose value is divisible by d. So for each i, we need the largest d where (count of multiples of d in A, excluding possibly A_i) is at least K-1.

We precompute, for every d ≤ 10^6, the count of A_j divisible by d: `cnt[d]`. For each i, we enumerate all divisors d of A_i. For each divisor d, the number of other elements (j ≠ i) divisible by d is `cnt[d]` minus (1 if d equals A_i's divisor contribution). Since A_i itself is counted in cnt[d] for each divisor d, the count of other elements divisible by d is `cnt[d] - 1`. We need this to be ≥ K-1.

We also need to consider d that are not divisors of A_i but still divide A_i? No — if d divides A_i, then gcd of the chosen set can be at most d, but for the gcd to equal d, every chosen element must be a multiple of d. Since A_i must be a multiple of d, d must divide A_i. Therefore only divisors of A_i are candidates.

So for each i: enumerate all divisors of A_i (O(√A_i)), check if cnt[d] ≥ K (since we need at least K elements including A_i). Take the maximum d.

Divisor enumeration for each i is fast enough: total O(N √maxA) worst case ~ 1.2e6 * 1000 = 1.2e9, too slow. But max A is 1e6, √A is 1000, and N is up to 1.2e6, so worst case is huge. We need optimization.

We can precompute divisors of all numbers up to 1e6 using a sieve-like approach: for d from 1 to 1e6, for multiples m of d, add d to divisors[m]. This takes O(maxA log maxA) ≈ 1e6 * (1e6/d) sum = 1e6 * (H_1e6) ≈ 1.4e7, which is fine. Memory: storing all divisors lists — total number of divisor entries is also about 1e6 * H_1e6 ≈ 1.4e7, acceptable if stored as a single list with offsets or vector of vectors (vector<int> per index). 1.4e7 ints ≈ 56 MB, okay.

Then for each i, iterate over its precomputed divisor list and find max d with cnt[d] ≥ K.