The answer for index i is the largest divisor d of A_i that appears as a divisor of at least K elements in the whole array.  
We first count how many times each value occurs (frequency).  
Then, for every possible d (1 … max A) we sum the frequencies of all multiples of d (a sieve‑like loop) to know how many array elements are divisible by d; we mark d as “good” if this sum is at least K.  
Finally we compute, for each value v, the largest good divisor that divides v. This can be done by iterating d from max A down to 1 and, whenever d is good, assigning the current answer for every multiple m of d that has not yet received an answer. Because we scan d in decreasing order, the first assignment is the maximal good divisor.  
The answer for each position i is simply the pre‑computed value for A_i.  

The whole procedure runs in O(M log M + N) time (M = max A ≤ 10⁶) and uses O(M + N) memory, well within the limits.