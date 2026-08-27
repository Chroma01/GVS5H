
## ideation
- The problem asks to simulate inserting numbers 1..N into a list at positions P_i (1-indexed) with naive insert being O(N^2) → too slow for N up to 5e5.
- The classic way: reverse the process. Process i from N down to 1. Maintain N empty slots in a Fenwick (Binary Indexed) Tree. At step i, find the P_i-th empty slot from the left → that's where number i should go. Place i there, then mark the slot filled (BIT update to 0).
- This yields O(N log N) time, O(N) memory, and avoids Python's list.insert (which is O(N) per call).
- The BIT must support two operations efficiently:
  1. Update: add delta (-1 to remove a slot) at an index.
  2. Query: prefix sum up to an index.
  3. Find k-th empty slot: use binary lifting on BIT (the standard “find by order” method that works in O(log N)).
- Edge cases: P_i = 1 (first empty slot) works; P_i = i (last empty slot) works; N = 1 works.
- Implementation details in Python:
  - Use iterative BIT with size = N+1.
  - For the find method, the largest power of 2 ≤ size can be precomputed once: `LOG = (size).bit_length()`.
  - Use 0-based internal BIT (1..N), store `result` as 0-indexed list of size N.
- The input uses sys.stdin fast reading because N can be 5e5 (2 * 5e5 integers). Use sys.stdin.read or sys.stdin.buffer.

## worker: Implement the solution in Python: write a Fenwick 
- The approach processes the insertions **in reverse** (from `N` down to `1`).  
- A Fenwick tree (Binary Indexed Tree) stores `1` for an empty slot and `0` for a filled one.  
- For each `i`, the `P_i`-th empty slot from the left is found using the standard binary‑lifting `kth` routine on the BIT, which runs in `O(log N)`.  
- After locating the position, the number `i` is placed there and the slot is marked filled (`add(-1)`).  
- Complexity: `O(N log N)` time, `O(N)` extra memory. This easily fits the limits (`N ≤ 5·10^5`).  
- Building the BIT initially is done in `O(N)` using the classic “direct building” trick, avoiding `N` separate updates.
