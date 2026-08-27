The constraints `A_x XOR A_y = Z` are linear equations over GF(2) for each bit of the numbers.  
We can treat every bit independently: for bit `k` we have variables `x_i ∈ {0,1}` with equations  
`x_{X_i} XOR x_{Y_i} = (Z_i>>k)&1`.  

All equations of one bit are handled with a **Disjoint Set Union with parity** (also called “union‑find with xor distance”).  
* Each set stores a representative `r` and for every node `i` the xor `d[i] = x_i XOR x_r`.  
* Union of `X,Y` with required xor `w` either merges two sets (setting the xor between the two roots) or, if they are already in the same set, checks the consistency `(d[X] XOR d[Y]) == w`. Any inconsistency means the whole instance has no solution.

When the DSU finishes without conflict, each connected component can be assigned a value for its root (0 or 1).  
If the root value is `t`, a node’s bit is `t XOR d[i]`.  
Let `cnt1` be the number of nodes with `d[i]=1` in a component; then the number of 1‑bits in the component is `cnt1` when `t=0` and `size‑cnt1` when `t=1`.  
To minimise the total sum we choose `t = 0` if `cnt1 ≤ size‑cnt1`, otherwise `t = 1`. This decision is optimal because the contribution of a bit to the sum is `2^k * (#ones)`, and bits are independent.

We repeat the whole procedure for the 30 possible bit positions (0 … 30, safe for `Z_i ≤ 10^9`).  
During the processing of a bit we add `2^k` to `A_i` whenever the computed bit of node `i` equals 1.  
If any bit reports a conflict we output `-1`.  
Otherwise the final `A` is a feasible sequence with the smallest possible sum.