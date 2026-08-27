The problem asks to maximize the sum of `max(X_i+X_j, Y_i+Y_j, Z_i+Z_i)` over K disjoint pairs.  
For each item we define its maximum value `M_i = max(X_i, Y_i, Z_i)` and the set of coordinates where it attains this maximum, `G_i ⊆ {X,Y,Z}`.  
A pair of items `(i,j)` achieves the full value `M_i + M_j` if and only if they share a coordinate in their `G`‑sets; otherwise the value is reduced by a penalty equal to the smaller of the two “slacks” (the amount each item is below its maximum in the other’s coordinate).  
The optimal total price is therefore `sum M_i` over the selected 2K items minus the minimum unavoidable penalty.  
Because only six specific type pairs incur a penalty (pure‑X with pure‑Y, pure‑X with pure‑Z, pure‑Y with pure‑Z, pure‑X with type {Y,Z}, pure‑Y with type {X,Z}, pure‑Z with type {X,Y}), we can solve the problem greedily:  

1. Sort all items by `M_i` descending.  
2. Take the top `2K` items as a candidate set.  
3. Try to assign them to the three colors with even counts (a necessary and sufficient condition for zero penalty). If possible, the answer is the sum of their `M_i`.  
4. If the parity condition fails, we need exactly one cross‑color pair. We choose the cross pair with the smallest possible penalty, possibly swapping a few items with slightly smaller `M_i` to improve the parity.  

The algorithm runs in `O(N log N)` per test case due to sorting and linear scans.