For each i we need the maximum possible GCD of a size‑K subset that must contain A_i.  
Observe that the GCD of a subset is always a divisor of every element in the subset, in particular it divides A_i.  
Therefore the answer for i is the largest divisor d of A_i such that we can pick (K‑1) other elements from the whole array whose values are all multiples of d.

Let freq[d] be how many numbers in the whole array are divisible by d.  
We compute freq for all d up to MAX = 10^6 using a sieve‑like frequency array: count how many times each value appears, then for each d add its count to its multiples.

Then for each i we iterate over the divisors d of A_i (there are at most ~240).  
The first divisor d (in decreasing order) with freq[d] ≥ K is the answer, because we can then pick the K largest multiples of d (which include A_i) and their GCD is exactly d.

Complexities:  
- Building freq: O(MAX log MAX) with harmonic sum ≈ 1.2·10^7 operations.  
- Answering each i: number of divisors × log steps per divisor → about 2·10^6 operations total.  
Both fit easily in the limits. Memory: two integer arrays of size MAX+1.