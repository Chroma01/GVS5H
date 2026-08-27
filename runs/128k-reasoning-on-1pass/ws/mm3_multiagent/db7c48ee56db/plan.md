The constraint \(\binom{N}{K}\le10^{6}\) guarantees that the total number of \(K\)-element subsets is at most one million, which is small enough to enumerate directly.  
To keep the recursion depth modest we enumerate the *smaller* side of each subset: let  
\(k = \min(K, N-K)\).  
If we enumerate subsets of size \(k\) we need the XOR of the whole array (`total_xor`) only when the original \(K\) is larger than \(N-K\); in that case the answer for a complement subset of size \(k\) is `total_xor ^ xor_of_subset`.  
We perform a depth‑first search that builds subsets one element at a time, carrying the current XOR, and updates the global maximum when a complete subset is formed.  
Because the total number of recursive calls is bounded by \(\binom{N}{k}\le10^{6}\) and the depth never exceeds \(k\le20\) (for the allowed values of \(N\)), the solution easily fits into time and memory limits.