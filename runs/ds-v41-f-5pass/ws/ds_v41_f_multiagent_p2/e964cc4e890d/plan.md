1. Reduce the problem to counting perfect matchings between W and B vertices such that every prefix cut has at least one backward edge (B before W).  
2. Show that this is equivalent to counting permutations σ of [N] satisfying prefix-maximum lower bounds M_p ≥ c_p, where c_p is derived from the positions of B and W.  
3. Convert the bounds into a DP over the minimum position of suffix values, processing values from N down to 1.  
4. Optimize the DP using the fact that the thresholds p_v are non-increasing and maintain the DP array with prefix sums and range updates.  
5. Implement the O(N) DP and output the final value modulo 998244353.