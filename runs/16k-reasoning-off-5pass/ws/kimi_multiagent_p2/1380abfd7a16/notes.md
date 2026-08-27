
## ideation
The core difficulty is that N can be 5×10^5, so a naive list insertion (O(N) per operation, O(N²) total) is too slow. The key insight is to process insertions in reverse order: when inserting value i at position P_i, all values j > i are already placed in their final slots. So value i must go into the P_i-th empty slot among the N final positions. This works because inserting i at position P_i (1-indexed) means exactly P_i - 1 elements come before it, and those elements are precisely the ones already placed in the first P_i - 1 empty slots.

A Fenwick tree (BIT) over positions 1..N, initialized with all 1s (all slots empty), supports:
- Finding the k-th empty slot via binary lifting (order-statistics query) in O(log N).
- Marking a slot as occupied (add -1) in O(log N).

Total complexity: O(N log N), well within limits.

Pitfalls:
- 1-indexed BIT implementation details (find_kth must return the smallest index with prefix sum >= k).
- Input parsing must be fast (use sys.stdin.buffer.read).
- P_i ≤ i guarantees validity: when processing i in reverse, there are exactly i empty slots remaining, and P_i ≤ i ensures the k-th query is valid.
- Output should be space-separated values in slot order 1..N.

## worker: Implement the complete solution: Fenwick tree with
- **Algorithm**: Process insertions in reverse. When placing value `i`, all values `j > i` already occupy their final slots. Inserting `i` at position `P_i` means exactly `P_i - 1` elements precede it, so `i` goes into the `P_i`-th currently-empty slot.
- **Fenwick tree**: initialized with all 1s via the O(N) trick `tree[i] = i & -i`. `find_kth` uses binary lifting from the highest power of two ≤ N, returning the smallest index with prefix sum ≥ k. After placement, `add(pos, -1)` marks the slot occupied.
- **Validity**: when processing `i`, exactly `i` slots remain empty, and the constraint `P_i ≤ i` guarantees the order-statistics query is always valid.
- **Sample 1 trace** (N=4, P=[1,1,2,1]): i=4 → 1st empty slot = 1; i=3 → 2nd empty slot among {2,3,4} = 3; i=2 → 1st empty among {2,4} = 2; i=1 → 1st empty among {4} = 4. Slots 1..4 = [4,2,3,1] ✓.
- **Sample 2 trace** (P=[1,2,3,4,5]): i=5 → slot 5; i=4 → slot 4; ... i=1 → slot 1. Output [1,2,3,4,5] ✓.
- **Complexity**: O(N log N) time, O(N) memory. Fast I/O via `sys.stdin.buffer.read`.
