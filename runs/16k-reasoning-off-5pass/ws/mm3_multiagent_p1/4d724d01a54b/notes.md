
## ideation
**Core difficulty:**  
We have a permutation and we can swap adjacent elements at cost equal to the left index of the pair. We need the minimum total cost to sort the permutation in ascending order.

**Observation:**  
Any sequence of adjacent swaps that sorts the permutation is equivalent to moving each element from its original position to its final position. The cost of a swap between positions `i` and `i+1` is `i`.  
If two elements `a` and `b` are inverted (i.e., `a` is left of `b` in the original array but `a > b`), they must cross each other at some point during the sorting process. The cost paid for that crossing is the minimum of the two positions involved, because the crossing happens at the earlier (leftmost) of the two indices (the swap at that index will eventually be performed).  
Therefore, the total minimum cost is the sum over all inversions `(a,b)` of `min(pos(a), pos(b))`.

**Candidate approaches:**  
1. **O(N^2) simulation** – bubble sort from left to right: for each position `i`, keep swapping the element that belongs there rightward until it arrives. The number of swaps at cost `i` equals the number of smaller elements originally to the right of the final element at position `i`. This is O(N^2) worst-case (e.g., reverse sorted array).  
2. **O(N log N) using Fenwick tree (BIT):**  
   - Iterate the array from right to left, maintaining a BIT over positions or values.  
   - For each element `x` at position `p` (1-indexed), count how many already-seen elements have value `< x` and position `> p`. Their contribution to the answer is `p` each.  
   - This works because the earlier of the two positions is `p` (since the other is to the right).  
   - Add `x` to the BIT and continue.  
3. **Alternative BIT formulation:**  
   - Iterate left to right, using a BIT on values. For each element `x`, count how many elements already placed (to the left) have `> x`. Their contribution is `current_index`.  
   - But the left-to-right method requires knowing the cost of swaps at the *current* index, which is the position of the left element. This also works with a BIT on values to count how many larger elements are to the left.

Both BIT approaches are valid; the left-to-right version is perhaps more intuitive: while processing position `i` (1-indexed), we pay cost `i` for every inversion where the left element is at position `i` and the right element is smaller and still to the right. The number of such inversions equals the number of elements to the left of `i` that are greater than the current element. So we need a data structure that can query, among elements already processed, how many are greater than `P[i]`. This is a classic BIT/segment tree query.

**Pitfalls:**  
- Answer can be up to ~O(N^3) in theory but for N=2e5 the maximum is bounded (worst case reverse permutation, sum = N(N-1)(N-2)/6? Actually sum of min(i,j) over all inversions in reverse permutation equals N choose 3 * 2? Need to check bound – for N=2e5 it's well within 64-bit, ~ (2/3)*10^15 < 9.22e18).  
- Off-by-one errors with 1-indexed BIT.  
- Using Python's int is fine, but careful with performance (use fast I/O).  
- Ensure we don't confuse the two BIT approaches.

**Complexities:** O(N log N) time, O(N) memory.

---

## worker: Implement the left-to-right Fenwick tree approach 
The algorithm iterates left to right. For each position `i` (0-indexed), the cost of swaps at index `i+1` (1-indexed) is incurred for every inversion where the left element is at position `i` and the right element is smaller and still to the right. The number of such inversions equals the count of elements to the left that are greater than `P[i]`. A Fenwick tree over values tracks how many processed elements are ≤ `x`; `i - sum(x)` gives the count of greater elements. Each such inversion contributes `i+1` to the total cost. The BIT is 1-indexed and supports `add`/`sum` in O(log N). The answer fits in Python's arbitrary-precision integer (max ≈ 1.3e16 for N=2e5). Fast I/O via `sys.stdin.buffer.read` ensures performance within limits.
