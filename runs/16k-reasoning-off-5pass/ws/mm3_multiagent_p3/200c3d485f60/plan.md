We need to count arrays of length n with values in [1, m] such that exactly k adjacent equal pairs exist.  
An adjacent equal pair occurs when two consecutive elements are same; this happens at the boundary between two identical "runs".  
If we have r runs (segments of equal values), then the number of equal adjacent pairs is r-1. So we need r = k+1 runs.  

For r runs:
- Choose values for each run: m choices for the first run, and m-1 choices for each subsequent run (must differ from previous). So m * (m-1)^(r-1).
- Choose positions of the r-1 "breaks" among the n-1 gaps: C(n-1, r-1).

Total: answer = C(n-1, k) * m * (m-1)^k mod (1e9+7), where k = r-1.

We precompute factorials and inverse factorials up to n to compute binomial coefficients in O(1) per query. Use fast exponentiation for the power term.