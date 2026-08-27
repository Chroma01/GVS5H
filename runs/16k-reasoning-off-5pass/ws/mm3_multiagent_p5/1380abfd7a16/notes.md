
## ideation
The problem asks for the final state of an initially empty list after N insertions. At step i we insert the number i so that it becomes the P_i‑th element (1‑indexed).  
Direct simulation with a Python list costs O(N) per insertion → O(N²), too slow for N up to 5·10⁵.  
Processing backwards (i = N … 1) and using a list still costs O(N²).  
We need O(N log N) or O(N).

Standard solution: treat the final array as N slots, all initially empty. Process i from N down to 1. At step i the list has (N‑i+1) elements; we need to place i so that exactly P_i‑1 empty slots remain before it.  
Using a Fenwick tree (BIT) over the N positions storing 1 for an empty slot, we can binary‑search (BIT “find kth”) to locate the index where the prefix sum first becomes ≥ P_i. That index is the position to occupy. Mark it 0, store i there. Repeating for all i gives the final array. Complexity O(N log N), memory O(N).

Edge cases: P_i is always between 1 and i, so the binary search is always valid. Indices are 1‑based internally for the BIT.

## worker: Implement the solution in Python: read N and P, bu
- We read all input at once for speed.
- Fenwick tree stores 1 for each free slot. The find_kth operation runs in O(log N) by binary lifting on the tree.
- Processing i from N down to 1 ensures that at step i exactly (N-i+1) slots are still free, matching the P_i constraint (1 ≤ P_i ≤ i).
- After locating position pos we store i there and mark the slot as occupied (add -1).
- Final answer is printed in order.
