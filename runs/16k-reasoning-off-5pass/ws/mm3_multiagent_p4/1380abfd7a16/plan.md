We need to simulate the process of inserting numbers `1..N` into a list at given positions `P_i` (1-indexed). The naive `list.insert` is O(N) per operation, leading to O(N^2) which is too slow for N up to 5·10^5. We can process the insertions in reverse order, using a Fenwick tree (Binary Indexed Tree) to keep track of free positions. When we insert i-th number (going backward from N to 1), its final position among the N slots is determined by the P_i-th free slot currently available. We can find the k-th zero (free slot) using BIT in O(log N) time. The result is the array placed in these slots.

Steps:
1. Read N and the array P[1..N].
2. Initialize a BIT of size N where each position holds 1 (free).
3. Process i from N down to 1:
   - `pos = find_kth(P[i])` – the index of the P_i-th free slot.
   - Mark this slot as occupied: update BIT at `pos` by adding -1.
   - Set `result[pos] = i`.
4. Output `result`.

All operations are O(log N) per element, total O(N log N), which fits the constraints.