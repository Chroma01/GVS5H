For each index i, we need the maximum possible GCD of a K-element subset that includes A_i.  
Observation: If we select any K elements, their GCD must be a divisor of A_i (since A_i is included). So the answer for i is a divisor d of A_i such that we can find at least K-1 other elements in the whole array that are multiples of d.  
Equivalently, for each divisor d of A_i, we can achieve GCD d if the total count of elements in the whole array divisible by d is at least K. Among all such divisors, we want the largest d.

Thus, precompute for every value x in [1, 10^6] the count of array elements divisible by x using a sieve-like frequency array and divisor counting. Then for each A_i, iterate over its divisors, find the largest divisor with count[x] >= K, and output it.

We need an O(N sqrt(maxA) + maxA log maxA) approach, which is fine for 1.2e6 and 1e6.