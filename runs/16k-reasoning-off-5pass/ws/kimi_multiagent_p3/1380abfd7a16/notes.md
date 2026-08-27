
## ideation
Core difficulty: N ≤ 5×10⁵, so naive list insertion (O(N) per insert, O(N²) total) is too slow. We need an O(N log N) approach.

Key insight: process insertions in reverse (i = N down to 1). When inserting value i, all values j > i are already placed in their final positions. Value i must land at the P_i-th *empty* slot from the left (since the P_i-1 elements before it at insertion time are exactly values < i that will later occupy the first P_i-1 empty slots... wait, more carefully: at insertion time, the array contains only values 1..i-1, and inserting i at position P_i means P_i-1 elements precede it. In reverse, values > i are fixed; i's final position is the P_i-th empty slot counting from the left, because the elements that will precede i are exactly the P_i-1 smaller values that will fill the empty slots before it).

Data structure: Fenwick tree (BIT) over positions 1..N, initially all empty (value 1 = empty). For each i from N down to 1: find the index of the P_i-th empty slot via BIT find-by-order (binary lifting on prefix sums), record answer[pos] = i, then mark slot occupied (add -1). Each step O(log N).

Pitfalls:
- 1-indexed BIT; find_kth must return the smallest index with prefix sum ≥ k.
- Binary lifting: start from highest power of two ≥ N.
- Input parsing speed: use sys.stdin.buffer.read().
- P_i can equal i, and empty slots count at step i is exactly i, so the k-th empty slot always exists.
- Output: join with spaces, values in slot order.

Alternative approaches: balanced BST / sorted list with order statistics (e.g., treap with subtree sizes), or a segment tree with find-by-order. BIT is simplest and fastest in Python.

Complexity: O(N log N) time, O(N) memory — fine for 5×10⁵.

## worker: Write the complete Python solution: fast input par
- **Correctness sketch:** At the moment value `i` is inserted (forward direction), the array contains exactly values `1..i-1`, and `i` is placed so that exactly `P_i - 1` of them precede it; later insertions of values `> i` never change the relative order of `i` versus smaller values. Processing in reverse (`i = N … 1`), the slots occupied by values `> i` are fixed, so `i` must occupy the `P_i`-th remaining empty slot from the left. The Fenwick tree stores per-slot emptiness (1 = empty) and supports both "find index of k-th empty slot" (binary lifting, O(log N)) and "occupy a slot" (point update, O(log N)). Total O(N log N), O(N) memory.
- **Sample 1 check:** N=4, P=[1,1,2,1]. Reverse: i=4 → 1st empty slot = 1 → ans[1]=4; i=3 → 2nd empty = 3 → ans[3]=3; i=2 → 1st empty = 2 → ans[2]=2; i=1 → 1st empty = 4 → ans[4]=1. Output `4 2 3 1` ✓.
- **Sample 2 check:** P=[1,2,3,4,5]. i=5 → slot 5; i=4 → slot 4; … i=1 → slot 1. Output `1 2 3 4 5` ✓.
- Edge cases: N=1 works (log=1, single slot). P_i = i always valid since exactly i empty slots remain at step i. Fast I/O via `sys.stdin.buffer.read`.
