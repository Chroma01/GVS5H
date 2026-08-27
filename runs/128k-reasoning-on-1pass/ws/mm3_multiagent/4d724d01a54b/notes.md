
## ideation
The problem asks for the minimum total cost to sort a permutation by repeatedly swapping adjacent elements, where swapping positions `i` and `i+1` costs `i` (the index of the left element before the swap).  
Key observations:

* A swap always involves a **larger** element on the left and a **smaller** element on the right (the only way to reduce inversions).  
* Moving an element **right** costs, moving **left** is free.  
* For each value `v`, let `r(v)` be the number of **smaller** elements originally to its right.  
  - By Lemma 1, `v` must move right exactly `r(v)` times in any sorting process.  
  - In an optimal schedule we first move `v` left across all larger elements on its left (free) and then right across the `r(v)` smaller elements.  
  - After the left moves the position of `v` becomes `v - r(v)`; the `k`‑th right move costs `v - r(v) + k`.  
  - Summing over `k = 0 … r(v)-1` gives the contribution  
    `cost(v) = r(v)·v - r(v)·(r(v)+1)/2`.  

Thus the answer is `Σ_{v=1..N} ( r(v)·v - r(v)·(r(v)+1)/2 )`.  
The only remaining task is to compute `r(v)` efficiently.

`r(v)` can be obtained by scanning values in increasing order and maintaining a Fenwick tree (Binary Indexed Tree) that stores, for each position, whether a smaller value has already appeared.

* `leftSmaller = BIT.sum(pos[v] - 1)` → number of already processed (smaller) values to the left of `v`.  
* Since among the `v-1` smaller values exactly `leftSmaller` are on the left, the rest are on the right:  
  `r(v) = (v-1) - leftSmaller`.  

All operations are `O(log N)`, giving an overall `O(N log N)` algorithm and `O(N)` memory.

Correctness relies on the lower bound from Lemma 3 (any process must pay at least the derived term for each `v`) and the upper bound from the explicit construction described in Lemma 4‑5, which matches the sum. Hence the computed value is optimal.

Potential pitfalls:
* Cost depends on the index **before** the swap, not after.  
* Use 1‑based indexing for the BIT to avoid off‑by‑one errors.  
* The answer can be as large as `~N³` (≈ 8·10¹⁵ for N=2·10⁵), so Python’s arbitrary‑precision integers are required.  
* Ensure the BIT query for `pos[v] - 1` handles the case `pos[v] = 1` (returns 0).

## worker: finalize
- The algorithm computes the minimum total cost as  
  `Σ_{v=1..N} ( r(v)·v – r(v)·(r(v)+1)/2 )`,  
  where `r(v)` is the number of smaller elements originally to the right of `v`.  
- `r(v)` is obtained by scanning values in increasing order and using a Fenwick tree to count how many already seen (smaller) values lie left of the current position.  
- Each value `v` is forced to move right exactly `r(v)` times; moving left is free. The cheapest possible positions for those right moves are `v‑r(v), v‑r(v)+1, …, v‑1`, whose sum yields the term above.  
- The total time complexity is `O(N log N)` and memory usage is `O(N)`, well within the limits (`N ≤ 2·10⁵`).
