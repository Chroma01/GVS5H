The value `A_i*B_j + B_j*C_k + C_k*A_i` can be rewritten as `(A_i + C_k) * B_j + A_i * C_k`. For a fixed pair `(i,k)`, this is linear in `B_j`, so we can efficiently obtain the top N values for each `(i,k)` by sorting B descending and taking the largest N (or all N). Then we need the K-th largest among all `(i,k)` combos using the top values from each.

However N can be 2e5, so O(N^2) is too large. Key observation: we can binary search the answer X and count how many triples give value ≥ X. Count = number of `(i,k)` pairs such that `(A_i + C_k) * B_j + A_i * C_k ≥ X`. For each j, we need to count pairs (i,k) with `A_i*C_k + (A_i + C_k)*B_j ≥ X`.

We can rewrite as `(A_i + C_k) * B_j + A_i*C_k = A_i*B_j + C_k*(A_i + B_j)`. For fixed j, define `t = B_j`. We need to count pairs (i,k) with `A_i*t + C_k*(A_i + t) ≥ X`, i.e., `C_k*(A_i + t) ≥ X - A_i*t`. Sort C descending, and for each A_i, find how many C_k satisfy. Since both A and C are sorted, we can two-pointer: for each A_i, we need `C_k ≥ (X - A_i*t) / (A_i + t)`. Walking A_i in descending order and C pointer works.

Then do binary search on answer over the feasible range (0 to 3*1e18).