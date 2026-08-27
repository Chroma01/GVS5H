
## ideation
The core difficulty is efficiently simulating N sequential insertions where each new element i is placed at position P_i. A direct simulation using a Python list and `insert()` is O(N) per operation due to element shifting, resulting in O(N²) total time, which is too slow for N=5×10⁵.

The key insight is to process operations in reverse. When inserting element i at position P_i, it occupies the P_i-th "empty" slot among the positions not yet taken by elements i+1 through N. By working backwards from i=N down to 1, we can determine each element's final position using an order-statistic structure.

A Fenwick tree (Binary Indexed Tree) can maintain counts of available slots and support finding the k-th available slot in O(log N) time via binary lifting. Initially all N slots are available (count=1). For each i from N down to 1, we find the P_i-th available slot, assign it to element i, and mark it as used (update count to 0). This yields O(N log N) total time.

Pitfalls to avoid:
- Off-by-one errors when converting between 1-indexed positions and 0-indexed array indices
- Fenwick tree implementation must correctly handle the "find k-th" operation with binary lifting
- Input parsing must be fast (use sys.stdin.buffer)
- The reverse logic must correctly map insertion order to final positions

## worker: Implement the complete Python solution: Fenwick tr
Implemented the reverse-simulation approach with a Fenwick tree. The tree tracks available slots (1 = available, 0 = used). Processing from i=N down to 1, we find the P_i-th available slot using binary lifting on the Fenwick tree, assign element i to that position, and mark it used. This achieves O(N log N) time complexity. Fast I/O via sys.stdin.buffer ensures we handle N=5×10⁵ efficiently.
