We solve the problem by processing the insertions in reverse order.  
Start with an empty array of size N and treat each position as an “empty slot.”  
Maintain a Fenwick tree (Binary Indexed Tree) where each slot stores 1 if it is still empty.  
Iterate i from N down to 1; at step i the P₁‑th empty slot is exactly the position where i must finally reside, because among the numbers 1…i the element i must be the P₁‑th from the left.  
We query the Fenwick tree for the P₁‑th empty slot (order‑statistics via binary lifting), place i there, and mark the slot as filled (update the tree with ‑1).  
After all numbers are placed we output the resulting array. The whole algorithm runs in O(N log N) time and O(N) memory, easily handling N ≤ 5·10⁵.