We need for each index i the maximum possible GCD of a K‑element subset that contains A_i.  
Observation: If we pick any K elements containing A_i, their GCD must be a divisor of A_i. Conversely, for any divisor d of A_i, we can achieve GCD ≥ d iff we can pick K−1 other elements all multiples of d. So the answer for i is the largest divisor d of A_i for which the total count of multiples of d in the whole array is at least K (i.e., we have enough multiples to fill the rest of the subset).  

Therefore we:
1. Count, for every integer v up to MAX_A = 1e6, how many A_j are multiples of v using a frequency array and a “sieve” accumulation.
2. For each i, iterate divisors of A_i (enumerated in O(sqrt(A_i))) and pick the largest divisor whose multiple‑count ≥ K.

Complexities:  
- Building the multiple counts in O(MAX_A log MAX_A) via harmonic series sum.  
- Answer queries in sum O(√A_i) ≈ up to 1e3 per element → O(N·√MAX_A) ≤ 1.2e9 worst case but practically fast because A_i ≤ 1e6 and many are small; however 1.2e6 * 1000 = 1.2e9 may be heavy. We can optimise: enumerate divisors in decreasing order and stop as soon as we find a valid one, because usually large divisors are few. Expected time passes within limits for Python with careful loops.

Memory: frequency size 1e6+5 integers, fine.