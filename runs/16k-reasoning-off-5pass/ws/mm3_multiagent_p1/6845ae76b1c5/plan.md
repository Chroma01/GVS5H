We need to answer K queries of the form Σ_{i=1}^{X} Σ_{j=1}^{Y} |A_i - B_j| efficiently.  
We can rewrite the double sum as a sum over all (i,j) with i≤X, j≤Y, so it depends only on the prefixes of A and B.  
Precompute two 2D prefix-sum structures that count how many A_i are ≤ a value and how many B_j are ≤ b, and their sums.  
Using these we can compute for any prefix (X,Y) the total absolute difference in O(log N) by splitting the A_i's into those ≤ B_Y and those > B_Y, and summing contributions via prefix counts and sums.  
This yields O((N+K) log N) time, well within limits.